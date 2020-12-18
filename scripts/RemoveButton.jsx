import * as React from "react";
import { Socket } from "./Socket";

export default function RemoveButton(props) {
  function handlePost(e) {
    e.preventDefault();
    console.log("Deleting item from server: " + props.item);
    Socket.emit("remove item", {
      item: props.item,
    });
  }

  return (
    <button type="button" onClick={handlePost}>
      Remove
    </button>
  );
}
