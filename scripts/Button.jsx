import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newItem = document.getElementById("item_input");
    Socket.emit('new item input', {
        'item': newItem.value,
    });
    
    console.log('Sent the item ' + newItem.value + ' to server!');
    newItem.value = ''
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="item_input" placeholder="Enter an item"></input>
            <button>Add!</button>
        </form>
    );
}
