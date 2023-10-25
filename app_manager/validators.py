def verify_plan(plan_name, payment):
    packages = [
        {
            'name': 'standard',
            'price': 10
        },
        {
            'name': 'pro',
            'price': 25
        }
    ]

    if {'name': plan_name, 'price': payment} not in packages:
        return {'error': True, 'message': 'Incorrect price for the selected plan.'}

    return {'error': False}
