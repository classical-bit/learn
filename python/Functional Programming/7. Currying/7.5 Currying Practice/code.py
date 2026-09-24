from collections.abc import Callable

ResizeFunc = Callable[[int, int], tuple[int, int]]
SetMinSizeFunc = Callable[..., ResizeFunc]

# Don't touch above this line


def new_resizer(max_width: int, max_height: int) -> SetMinSizeFunc:
    def set_min_size(min_width: int = 0, min_height: int = 0) -> Callable[[int, int], tuple[int, int]]:
        if min_width > max_width or min_height > max_height:
            raise ValueError("minimum size cannot exceed maximum size")
        def set_image_size(width: int, height: int) -> tuple[int, int]:
            new_width = max(min(max_width, width), min_width)
            new_height = max(min(max_height, height), min_height)
            return new_width, new_height

        return set_image_size

    return set_min_size


# Step 1: Create the resizer with maximum dimensions
set_min_size: SetMinSizeFunc = new_resizer(800, 600)

# Step 2: Set the minimum dimensions
resize_image: ResizeFunc = set_min_size(200, 100)

# Step 3: Resize the image
new_width: int
new_height: int
new_width, new_height = resize_image(1000, 500)

# Step 4: Output the result
print(new_width, new_height)  # Output: 800, 500

# With currying syntax
print(new_resizer(800, 600)(200, 100)(1000, 500))  # Output: (800, 500)
