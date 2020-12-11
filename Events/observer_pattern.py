from typing import Union, List


class Observable:
    def __init__(self) -> None:
        self._observers = []

    def register_observer(self, observers: Union["Observer", List["Observer"]]) -> None:
        if isinstance(observers, list):
            self._observers.extend(observers)
        else:
            self._observers.append(observers)

    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)


class GenerateEvent1(Observable):
    def notify_observers(self):
        super().notify_observers(source="event1")


class GenerateEvent2(Observable):
    def notify_observers(self):
        super().notify_observers(source="event2")


class Observer:
    def __init__(self, observables: Union[Observable, List[Observable]]) -> None:
        if isinstance(observables, list):
            [observable.register_observer(self) for observable in observables]
        else:
            observables.register_observer(self)

    def notify(self, observable, *args, **kwargs) -> None:
        print(
            f"{id(self)} got args={args} kwargs={kwargs} from {observable.__class__.__name__}."
        )


event1 = GenerateEvent1()
observer1 = Observer(event1)

event1.notify_observers()

event2 = GenerateEvent2()
observer2 = Observer([event1, event2])

event1.notify_observers()
event2.notify_observers()