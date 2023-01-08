import tkinter as tk

from Controller.example_controller import ExampleController
from Model.example_model import ExampleModel
from View.example_view import ExampleView


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')

        # create a model
        model = ExampleModel('hello@pythontutorial.net')

        # create a view and place it on the root window
        view = ExampleView(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = ExampleController(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
