% Auto-generated: do not edit by hand
\name{footCustomComponent}

\alias{footCustomComponent}

\title{FootCustomComponent component}

\description{
ExampleComponent is an example component. It takes a property, `label`, and displays it. It renders an input with the property `value` which is editable by the user.
}

\usage{
footCustomComponent(id=NULL, data=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{data}{Character. the string json encoded data from the sensors
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
]}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

