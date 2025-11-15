# orders/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Order

User = get_user_model()

@api_view(['POST'])
def chatbot_handler(request):
    user_message = request.data.get('message', '').strip()
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    phone_number = request.data.get('phone_number')

    # Get user object if available
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    # Process the message and generate dynamic response
    response_text = process_chatbot_message(user_message, user, username)

    return Response({'reply': response_text})

def process_chatbot_message(message, user, username):
    message = message.strip()
    
    # Remove any emojis or special characters for easier matching
    clean_message = ''.join(char for char in message if char.isalnum() or char.isspace())
    
    print(f"Processing message: '{message}' from user: {username}")  # Debug log

    # Track order status
    if message in ['1', '1️⃣', 'order', 'track', 'حالة الطلب', 'طلب']:
        return get_order_status(user, username)
    
    # Contact designer
    elif message in ['2', '2️⃣', 'designer', 'مصمم', 'تصميم']:
        return get_designer_contact(user, username)
    
    # Contact marketer
    elif message in ['3', '3️⃣', 'marketer', 'مسوق', 'تسويق']:
        return get_marketer_contact(user, username)
    
    # Help or unknown message
    else:
        return get_help_message(username)

def get_order_status(user, username):
    if not user:
        return "👤 يرجى تسجيل الدخول لمشاهدة حالة طلباتك."
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(client=user).order_by('-created_at')[:5]
    
    if recent_orders.exists():
        response = "📦 **طلباتك الأخيرة:**\n\n"
        for order in recent_orders:
            status_ar = {
                'pending': '🟡 قيد الانتظار',
                'in_progress': '🟠 قيد التنفيذ', 
                'completed': '🟢 مكتمل',
                'delivered': '✅ تم التسليم'
            }.get(order.status, order.status)
            
            response += f"**{order.project_name}**\n"
            response += f"الحالة: {status_ar}\n"
            response += f"التاريخ: {order.created_at.strftime('%Y-%m-%d')}\n"
            response += f"المصمم: {order.designer.user.username if order.designer else 'لم يتم التعيين'}\n"
            response += "――――――――――\n"
        
        response += "\nللمزيد من التفاصيل، تفضل بزيارة لوحة التحكم."
        return response
    else:
        return "❌ **لم يتم العثور على أي طلبات**\n\nحسابك لا يحتوي على أي طلبات حالياً.\n\nيمكنك تقديم طلب جديد من خلال:\n• الذهاب إلى صفحة 'الباقات'\n• اختيار الباقة المناسبة\n• تعبئة نموذج الطلب\n\nهل تحتاج مساعدة في اختيار الباقة المناسبة؟ 😊"

def get_designer_contact(user, username):
    if user:
        # Check if user has any orders with assigned designers
        user_orders = Order.objects.filter(client=user).exclude(designer__isnull=True)
        
        if user_orders.exists():
            # Get the most recent order's designer
            recent_order = user_orders.first()
            designer = recent_order.designer
            return f"""🎨 **المصمم المختص بك:**

**الاسم:** {designer.user.get_full_name() or designer.user.username}
**التخصص:** {designer.specialty or 'تصميم عام'}
**الهاتف:** {designer.phone or 'غير متوفر'}
**البريد:** {designer.user.email}

يمكنك التواصل معه مباشرة خلال ساعات العمل (9 ص - 6 م)"""
        else:
            return f"""🎨 **فريق التصميم**

حالياً لا يوجد مصمم مختص بك لأنك لم تقدم أي طلبات بعد.

**للحصول على مصمم مختص:**
1️⃣ اختر باقة مناسبة
2️⃣ قدم طلب جديد
3️⃣ سنقوم بتعيين أفضل مصمم لمشروعك

**للاستفسارات العامة:**
📞 0501234567
✉️ designers@vivora.com"""
    else:
        return """🎨 **فريق التصميم:**

📞 0501234567
✉️ designers@vivora.com

**ساعات العمل:** 9 ص - 6 م
**أيام العمل:** الأحد - الخميس

اختر باقة مناسبة وسنقوم بتعيين أفضل مصمم لمشروعك! ✨"""

def get_marketer_contact():
    return """📊 **فريق التسويق:**

📞 0507654321
✉️ marketing@vivora.com

**الخدمات:**
• استراتيجيات التسويق
• تحليل الأداء
• إدارة الحملات
• تقارير الأداء

**ساعات العمل:** 9 ص - 6 م
**أيام العمل:** الأحد - الخميس

متاحون لمساعدتك في تطوير استراتيجية تسويق ناجحة لمشروعك! 🚀"""

def get_help_message(username):
    greeting = f"مرحباً {username} 👋" if username else "مرحباً 👋"
    
    return f"""{greeting}

اختر أحد الخيارات:

1️⃣ **حالة الطلب** - تتبع طلباتك الحالية والجديدة
2️⃣ **التواصل مع المصمم** - معلومات الاتصال بالمصمم المختص بك
3️⃣ **التواصل مع المسوق** - فريق التسويق والدعم الاستشاري

أو اكتب استفسارك المباشر وسنسعد بمساعدتك... 💫"""