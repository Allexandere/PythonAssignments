import numpy as np


class MatrixMultiplier:
    """
    OOP class for multiplying two matrices using NumPy.
    """

    def __init__(self, matrix1, matrix2):
        # Convert the input 2D lists into NumPy arrays
        self.matrix1 = np.array(matrix1)
        self.matrix2 = np.array(matrix2)

        # Validate that both inputs are 2D
        if self.matrix1.ndim != 2 or self.matrix2.ndim != 2:
            raise ValueError("Both matrices must be 2D lists.")

        # Matrix multiplication requires:
        # columns in Matrix 1 == rows in Matrix 2
        if self.matrix1.shape[1] != self.matrix2.shape[0]:
            raise ValueError(
                f"Cannot multiply matrices: "
                f"Matrix 1 has {self.matrix1.shape[1]} columns, "
                f"but Matrix 2 has {self.matrix2.shape[0]} rows."
            )

    def multiply(self):
        """
        Multiply the two matrices using NumPy.
        """
        return np.matmul(self.matrix1, self.matrix2)

    def display(self):
        """
        Display the input matrices and the result.
        """
        print("Matrix 1:")
        print(self.matrix1)

        print("\nMatrix 2:")
        print(self.matrix2)

        result = self.multiply()

        print("\nResult:")
        print(result)


def main():
    # Example:
    # Matrix 1 = 2 x 3
    # Matrix 2 = 3 x 2
    matrix1 = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    matrix2 = [
        [10, 11],
        [20, 21],
        [30, 31]
    ]

    try:
        # Create an object
        multiplier = MatrixMultiplier(matrix1, matrix2)

        # Display the matrices and multiplication result
        multiplier.display()

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()