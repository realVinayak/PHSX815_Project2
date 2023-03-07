def smoothen_data(a, b, i, f2, f1):
    return (a * f2 - b * f1 + i * (b - a)) / (f2 - f1)


def smoothen_histogram(data_array):
    smoothened_data_array = []
    initial_anchor = 0
    final_anchor = 0
    # data = [0, 5, 3, 0, 3]
    index = 0
    while index < len(data_array):
        data = data_array[index]
        smoothened_data = data
        if data == 0:
            final_anchor = index
            while data[final_anchor] == 0 and final_anchor < len(data_array):
                final_anchor += 1
            final_anchor_data = data[final_anchor]
            initial_anchor_data = data[initial_anchor]
            smoothened_data = smoothen_data(initial_anchor_data,
                                            final_anchor_data, index,
                                            final_anchor, initial_anchor)
        smoothened_data_array.append(smoothened_data)
