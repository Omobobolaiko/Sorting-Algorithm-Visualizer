import pygame
import random
import math

# Initialize Pygame
pygame.init()


class DrawInformation:
    COLORS = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "gradients": [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
    }
    
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val, self.max_val = min(lst), max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(DrawInformation.COLORS["white"])
    title = DrawInformation.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, DrawInformation.COLORS["green"])
    controls = DrawInformation.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, DrawInformation.COLORS["black"])
    ##sorting = DrawInformation.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, DrawInformation.COLORS["black"])
    sorting = DrawInformation.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort", 1, DrawInformation.COLORS["black"])
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))
    
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions=None, clear_bg=False):
    if color_positions is None:
        color_positions = {}
    
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, DrawInformation.COLORS["white"], clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = DrawInformation.COLORS["gradients"][i % 3]
        color = color_positions.get(i, color)

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1, num2 = lst[j], lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = num2, num1
                draw_list(draw_info, {j: DrawInformation.COLORS["green"], j + 1: DrawInformation.COLORS["red"]}, True)
                yield True


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while i > 0 and ((lst[i - 1] > current and ascending) or (lst[i - 1] < current and not ascending)):
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: DrawInformation.COLORS["green"], i: DrawInformation.COLORS["red"]}, True)
            yield True
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        idx_swap = i

        for j in range(i + 1, len(lst)):
            if ascending and lst[j] < lst[idx_swap]:
                idx_swap = j
            elif not ascending and lst[j] > lst[idx_swap]:
                idx_swap = j

            draw_list(draw_info, {j: DrawInformation.COLORS["red"], idx_swap: DrawInformation.COLORS["green"]}, True)
            yield True

        if idx_swap != i:
            lst[i], lst[idx_swap] = lst[idx_swap], lst[i]
            draw_list(draw_info, {i: DrawInformation.COLORS["green"], idx_swap: DrawInformation.COLORS["red"]}, True)
            yield True
def merge_sort(draw_info, start=0, end=None, ascending=True):
    if end is None:
        end = len(draw_info.lst)
        
    if end - start <= 1:
        return
    
    mid = (start + end) // 2
    
    yield from merge_sort(draw_info, start, mid, ascending)
    yield from merge_sort(draw_info, mid, end, ascending)
    yield from merge(draw_info, start, mid, end, ascending)
    
def merge(draw_info, start, mid, end, ascending=True):
    left = draw_info.lst[start:mid]
    right = draw_info.lst[mid:end]
    left_idx, right_idx = 0, 0
    current = start
    
    while left_idx < len(left) and right_idx < len(right):
        yield True

        left_val, right_val = left[left_idx], right[right_idx]
        if (ascending and left_val < right_val) or (not ascending and left_val > right_val):
            draw_info.lst[current] = left_val
            left_idx += 1
        else:
            draw_info.lst[current] = right_val
            right_idx += 1
            
        draw_list(draw_info, {current: DrawInformation.COLORS["green"]}, True)
        current += 1

    while left_idx < len(left):
        yield True
        draw_info.lst[current] = left[left_idx]
        left_idx += 1
        draw_list(draw_info, {current: DrawInformation.COLORS["green"]}, True)
        current += 1

    while right_idx < len(right):
        yield True
        draw_info.lst[current] = right[right_idx]
        right_idx += 1
        draw_list(draw_info, {current: DrawInformation.COLORS["green"]}, True)
        current += 1
    while left_idx < len(left) and right_idx < len(right):
        yield True

        left_val, right_val = left[left_idx], right[right_idx]
        if (ascending and left_val < right_val) or (not ascending and left_val > right_val):
            draw_info.lst[current] = left_val
            left_idx += 1
        else:
            draw_info.lst[current] = right_val
            right_idx += 1
            
        draw_list(draw_info, {current: DrawInformation.COLORS["green"]}, True)
        current += 1
        
def partition(draw_info, low, high, ascending=True):
    pivot = draw_info.lst[high]
    i = low - 1

    for j in range(low, high):
        compare = (draw_info.lst[j] < pivot) if ascending else (draw_info.lst[j] > pivot)
        if compare:
            i += 1
            draw_info.lst[i], draw_info.lst[j] = draw_info.lst[j], draw_info.lst[i]
            draw_list(draw_info, {i: DrawInformation.COLORS["green"], j: DrawInformation.COLORS["red"]}, True)
            yield True

    draw_info.lst[i+1], draw_info.lst[high] = draw_info.lst[high], draw_info.lst[i+1]
    draw_list(draw_info, {i+1: DrawInformation.COLORS["green"], high: DrawInformation.COLORS["red"]}, True)
    yield i+1

def quick_sort(draw_info, low=0, high=None, ascending=True):
    if high is None:
        high = len(draw_info.lst) - 1

    if low < high:
        pi = None
        generator = partition(draw_info, low, high, ascending)
        while True:
            try:
                pi = next(generator)
            except StopIteration:
                break

        if pi is not None:
            yield from quick_sort(draw_info, low, pi-1, ascending)
            yield from quick_sort(draw_info, pi+1, high, ascending)




def main():
    run = True
    clock = pygame.time.Clock()
    lst = generate_starting_list(50, 0, 100)
    draw_info = DrawInformation(1200, 800, lst)


    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(50, 0, 100)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_s and not sorting:
                    sorting_algorithm = selection_sort
                    sorting_algo_name = "Selection Sort"
                elif event.key == pygame.K_m and not sorting:
                    sorting_algorithm = merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pygame.K_q and not sorting:
                    sorting_algorithm = quick_sort
                    sorting_algo_name = "Quick Sort"



    pygame.quit()

if __name__ == "__main__":
    main()

