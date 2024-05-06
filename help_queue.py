from typing import Optional
import threading


# Node class
class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next: Optional[Node] = None
        self.mutex: threading.Lock = threading.Lock()


# Queue class
class Queue:
    def __init__(self) -> None:
        dummy_value: int = 0
        self.dummy_node: Node = Node(dummy_value)
        self.head: Node = self.dummy_node
        self.tail: Node = self.dummy_node


# Function to try removing the front node
def try_remove_front(queue: Queue, front: int) -> bool:
    with queue.head.mutex:
        head: Node = queue.head
        if head.next is not None:
            with head.next.mutex:
                next_node: Node = head.next
                if next_node.value == front:
                    head.next = next_node.next
                    del next_node
                    return True
    return False


# Function to help finish enqueue
def help_finish_enq(queue: Queue) -> None:
    next_node: Optional[Node] = queue.tail.next
    if next_node is not None and next_node == queue.tail:
        with queue.tail.mutex:
            with queue.head.mutex:
                queue.tail.next = next_node
                queue.tail = next_node


# Function to enqueue a value
def enqueue(queue: Queue, value: int) -> None:
    node: Node = Node(value)
    with queue.tail.mutex:
        queue.tail.next = node
        help_finish_enq(queue)


# Main function
if __name__ == "__main__":
    q: Queue = Queue()
    front_value: int = 10
    enqueue(q, front_value)
    result: bool = try_remove_front(q, front_value)
    if result:
        print(f"Successfully removed front node: {front_value}")
    else:
        print("Failed to remove front node")
