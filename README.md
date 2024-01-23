# real-time-foot-pressure-plotter

Example API response:

```
{
    'birthdate': '1976',
    'disabled': True,
    'firstname': 'Elżbieta',
    'id': 12, 
    'lastname': 'Kochalska', 
    'trace': {
        'id': 13533005062019,
        'name': 'ela',
        'sensors': [
            {
                'anomaly': False,
                'id': 0,
                'name': 'L0',
                'value': 16
            }, 
            {
                'anomaly': False,
                 'id': 1, 
                 'name': 'L1', 
                 'value': 138
            }, 
            {
                 'anomaly': False, 
                 'id': 2, 
                 'name': 'L2', 
                 'value': 13
            },
            {
                'anomaly': False, 
                'id': 3, 
                'name': 'R0', 
                'value': 1023
            }, 
            {
                'anomaly': False, 
                'id': 4, 
                'name': 'R1', 
                'value': 1023
            }, 
            {
                'anomaly': False, 
                'id': 5, 
                'name': 'R2', 
                'value': 896
            }
        ]
    }
}
```

Valuable data:

```
{
    'firstname': 'Elżbieta',
    'id': 12, 
    'lastname': 'Kochalska', 
    'trace': {
        'id': 13533005062019,
        'name': 'ela',
        'sensors': [
            {
                'anomaly': False,
                'name': 'L0',
                'value': 16
            }, 
            {
                'anomaly': False,
                'name': 'L1', 
                'value': 138
            }, 
            {
                'anomaly': False, 
                'name': 'L2', 
                'value': 13
            },
            {
                'anomaly': False, 
                'name': 'R0', 
                'value': 1023
            }, 
            {
                'anomaly': False, 
                'name': 'R1', 
                'value': 1023
            }, 
            {
                'anomaly': False, 
                'name': 'R2', 
                'value': 896
            }
        ]
    }
}
```