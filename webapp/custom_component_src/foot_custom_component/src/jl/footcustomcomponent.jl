# AUTO GENERATED FILE - DO NOT EDIT

export footcustomcomponent

"""
    footcustomcomponent(;kwargs...)

A FootCustomComponent component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `data` (String; optional): the string json encoded data from the sensors
Example:
[
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
"""
function footcustomcomponent(; kwargs...)
        available_props = Symbol[:id, :data]
        wild_props = Symbol[]
        return Component("footcustomcomponent", "FootCustomComponent", "foot_custom_component", available_props, wild_props; kwargs...)
end

