from tkinter import filedialog


def get_file():
    filename = filedialog.askopenfilename(
        filetypes=(
            ("XY files", "*.xy"),
            ("Text files", "*.txt"),
            ("Python Files", ("*.py", "*.pyx")),
            ("All Files", "*.*")
        )
    )

    return filename
