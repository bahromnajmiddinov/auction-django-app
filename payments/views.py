from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, order_id):
    try:
        order = get_object_or_404(request.user.order_set, pk=order_id)
        items = order.orderitem_set.all()
        
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.title,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
        })
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('payment/success/') + '?success=true',
            cancel_url=request.build_absolute_uri('payment/cancel/') + '?canceled=true',
        )
        return render(request, 'payments/stripe.html', {'session_id': checkout_session.id, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')

    # Verify the webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        # Get the session from the event
        session = event['data']['object']
        # Fetch the order_id from your database based on session metadata or identifier
        order_id = session.get('metadata', {}).get('order_id')

        if order_id:
            # Update your order as paid in the database
            try:
                order = Order.objects.get(pk=order_id)
                order.paid = True
                order.save()
                return JsonResponse({'message': 'Order updated successfully'})
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)

    # Return a response to acknowledge receipt of the event
    return JsonResponse({'message': 'Received'})


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
