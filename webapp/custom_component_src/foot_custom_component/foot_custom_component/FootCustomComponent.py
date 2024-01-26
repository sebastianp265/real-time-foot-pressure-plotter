# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FootCustomComponent(Component):
    """A FootCustomComponent component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- data (string; optional):
    the string json encoded data from the sensors Example: [
    {                 'anomaly': False,                 'name': 'L0',
    'value': 16             },             {
    'anomaly': False,                 'name': 'L1',
    'value': 138             },             {
    'anomaly': False,                 'name': 'L2',
    'value': 13             },             {
    'anomaly': False,                 'name': 'R0',
    'value': 1023             },             {
    'anomaly': False,                 'name': 'R1',
    'value': 1023             },             {
    'anomaly': False,                 'name': 'R2',
    'value': 896             } ]."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'foot_custom_component'
    _type = 'FootCustomComponent'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(FootCustomComponent, self).__init__(**args)
