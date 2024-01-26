/* eslint no-magic-numbers: 0 */
import React, { useState } from 'react';

import { FootCustomComponent } from '../lib';

const App = () => {

    const [state, setState] = useState({value:'', label:'Type Here'});
    const setProps = (newProps) => {
            setState(newProps);
        };

    return (
        <div>
            <FootCustomComponent
                setProps={setProps}
                {...state}
            />
        </div>
    )
};


export default App;
