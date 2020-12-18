import * as React from "react";
import { Button } from "./Button";
import { Socket } from "./Socket";
import RemoveButton from "./RemoveButton";

export function Content() {
  const [items, setItems] = React.useState([]);

  function getNewItems() {
    React.useEffect(() => {
      Socket.on("items received", (data) => {
        console.log("Received items from server: " + data["allItems"]);
        setItems(data["allItems"]);
      });
    });
  }
  
  getNewItems();

  return (
    <div>
      <h1>Grocery List!</h1>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            {item}  <RemoveButton item = {item} />
          </li>
          
        ))}
      </ul>
      <Button />
    </div>
  );
}
