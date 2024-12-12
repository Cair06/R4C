from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from robots.models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def notify_customers_about_robot(sender, instance, created, **kwargs):
    if created:
        pending_orders = Order.objects.filter(robot_serial=instance.serial)

        # Отправляем письма клиентам
        for order in pending_orders:
            customer_email = order.customer.email
            model = instance.model
            version = instance.version

            email_subject = 'Ваш робот теперь в наличии!'
            email_body = f'''
            Добрый день!
            Недавно вы интересовались нашим роботом модели {model}, версии {version}.
            Этот робот теперь в наличии. Если вам подходит этот вариант — пожалуйста, свяжитесь с нами.
            '''

            try:
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email='somework@gmail.com',
                    recipient_list=[customer_email],
                )
            except Exception as e:
                print(f'Ошибка при отправке письма для заказа {order.id}: {e}')