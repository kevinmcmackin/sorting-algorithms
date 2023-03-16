import pygame
import random
import math
pygame.init() 

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    # three colours for the rectangles
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    SIDE_PAD = 100 # padding on left & right
    TOP_PAD = 150 

    # constructor method for the class. self refers to the instance of the class being created
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        
        # creating window in pygame
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    # need to determine bar width & height depending on how many we have
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # ensure that max_val and min_val are not the same
        if self.max_val == self.min_val:
            self.max_val += 1

        # calculate width & height of bars
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        # where to start drawing
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # adding the title and instructions
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()
    

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    

    # draw over the rectangle with white
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        #draw the rectangle. starts from top left
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    # update the screen
    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []
    
    for _ in range(n):
        val = random.randint(min_val, max_val) 
        lst.append(val)

    return lst 


def merge_sort(draw_info, full_info, ascending=True, start_idx = 0):
    lst = draw_info.lst

    # using recursion for each division
    if len(lst) > 1:
        mid = len(lst) // 2
        left_lst = lst[:mid]
        right_lst = lst[mid:]

        # for event in merge_sort(DrawInformation(draw_info.width, draw_info.height, left_lst), full_info, ascending, start_idx):
        #     yield event
        # for event in merge_sort(DrawInformation(draw_info.width, draw_info.height, right_lst), full_info, ascending, start_idx + mid):
        #     yield event

        for event in merge_sort(DrawInformation(draw_info.width, draw_info.height, left_lst), full_info, ascending, start_idx):
            yield event
        for event in merge_sort(DrawInformation(draw_info.width, draw_info.height, right_lst), full_info, ascending, start_idx + mid):
            yield event

        i = 0
        j = 0
        k = 0

        # the indices are for that particular set of data (can be as small as one bar). needs to be for the whole thing as thats whats being drawn 

        while i < len(left_lst) and j < len(right_lst):
            if left_lst[i] < right_lst[j]:
                lst[k] = left_lst[i]
                full_info.lst[k + start_idx] = left_lst[i]

                i += 1
            else:
                lst[k] = right_lst[j]
                full_info.lst[k + start_idx] = right_lst[j]

                j += 1
            k += 1
            draw_list(full_info, {k - 1 + start_idx: draw_info.GREEN}, True)
            yield True

        while i < len(left_lst):
            lst[k] = left_lst[i]
            full_info.lst[k + start_idx] = left_lst[i]
            
            i += 1
            k += 1
            draw_list(full_info, {k - 1 + start_idx: draw_info.GREEN}, True)
            yield True

        while j < len(right_lst):
            lst[k] = right_lst[j]
            full_info.lst[k + start_idx] = right_lst[j]

            j += 1
            k += 1
            draw_list(full_info, {k - 1 + start_idx: draw_info.GREEN}, True)
            yield True

        draw_list(full_info, {}, True)
        yield True
    


def bubble_sort(draw_info, full_info, ascending = True, start_idx = 0):
    lst = draw_info.lst 

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # swap placed for ascending or descending
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                # yield pauses, but holds the current state of the fundction. then can resume. need to pause so that we can press buttons and such. this makes the method a generator
                yield True

    return lst


def insertion_sort(draw_info, full_info, ascending = True, start_idx = 0):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending 
            descending_sort = i > 0 and lst[i - 1] < current and not ascending 

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    
    return lst


def selection_sort(draw_info, full_info, ascending = True, start_idx = 0):
    lst = draw_info.lst

    for i in range(len(lst)):
        if ascending:
            min_index = i
            for j in range(i + 1, len(lst)):
                if lst[j] < lst[min_index]: 
                    min_index = j

        else:
            max_index = i
            for j in range(i + 1, len(lst)):
                if lst[j] > lst[max_index]:
                    max_index = j
            min_index = max_index

        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True

    return lst
    

def main():
    run = True 
    clock = pygame.time.Clock()

    n = 50
    min_val = 0 
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst) # create an instance of the DrawInformation class
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # in pygame need loop always running
    while run:
        clock.tick(40)

        # if we are sorting, try to call next. if the generator is done, set sorting to false. if its not done, then keep going
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # update display
        pygame.display.update()

        # pygame.event.get() is all events that occured since last call
        for event in pygame.event.get():

            # if we press the close button, then close window and stop running
            if event.type == pygame.QUIT:
                run = False

            # if no button pressed then do nothing
            if event.type != pygame.KEYDOWN:
                continue
                
            # reset sorter if 'R' key pressed
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            # start sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, draw_info, ascending)

            # to swap ascending/descending
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            # to swap sorting algorithms
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

    pygame.quit()

if __name__ == "__main__":
    main()