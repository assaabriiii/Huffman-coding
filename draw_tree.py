import tkinter as tk


window = tk.Tk()
window.title("Huffman Tree")

canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

def draw_tree(node, x, y, dx):
    if node is None:
        return

    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
    canvas.create_text(x, y, text=f"{node.data}\n{node.freq}", font="Arial 12 bold")

    if node.left is not None:
        x_left = x - dx
        y_left = y + 80
        canvas.create_line(x, y + 20, x_left, y_left - 20, width=2)
        draw_tree(node.left, x_left, y_left, dx // 2)

    if node.right is not None:
        x_right = x + dx
        y_right = y + 80
        canvas.create_line(x, y + 20, x_right, y_right - 20, width=2)
        draw_tree(node.right, x_right, y_right, dx // 2)
window.mainloop()