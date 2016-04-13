/**
 * GridDisplay.java
 * 
 * @author Jake "Eebit" Fryer
 * @since April 12, 2016
 */

public class GridDisplay {
	
	private int xVal, yVal;
	private Cell[][] grid;
	
	/**
	 * Constructor that, if no x and y values are assigned, defaults to 3.
	 * Why 3, you ask? Because I said so.
	 * 
	 * Also initializes all of the Cells as blank Cells.
	 */
	public GridDisplay() {
		this.xVal = 3;
		this.yVal = 3;
		
		this.grid = new Cell[yVal][xVal];
		
		// Nested for loops to initialize all elements of the array
		for(int i = 0; i < this.yVal; i++) {
			for(int j = 0; j < this.xVal; j++) {
				this.grid[i][j] = new EmptyCell();
			}
		}
	}
	
	/**
	 * Constructor that takes x and y parameters to determine the dimensions
	 * of the Grid. Also initializes all of the Cells to blank Cells. Because
	 * that's all I've coded so far. Yeah.
	 * 
	 * @param x - the width of the grid, an int
	 * @param y - the height of the grid, an int
	 */
	public GridDisplay(int x, int y) {
		this.xVal = x;
		this.yVal = y;
		
		this.grid = new Cell[yVal][xVal];
		
		for(int i = 0; i < this.yVal; i++) {
			for(int j = 0; j < this.xVal; j++) {
				this.grid[i][j] = new EmptyCell();
			}
		}
	}
	
	/**
	 * appendNum is a helper method that appends the column-indicating numbers
	 * to the bottom of the grid's display.
	 * 
	 * NOTE: Currently uses the first row as the loop condition, does not support
	 * variable-length arrays. This should be remedied in future versions.
	 */
	public void appendNum() {
		System.out.print("-");
		
		// we use < rather than <= so that we can make nice aesthetics and stuff
		for(int v = 1; v < this.grid[0].length; v++) {
			System.out.print(v + "---");
		}
		System.out.print(this.grid[0].length + "-");
	}
	
	/**
	 * Main method, for testing purposes.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		GridDisplay g = new GridDisplay(6,4);
		
		for(int c = 0; c < g.grid.length; c++) {
			for(int a = 0; a < g.grid[c].length; a++) {
				System.out.print(g.grid[c][a].toString() + " ");
			}
			// TODO: Method to append letter to row depending on the y variable
			int val = c + 65;
			System.out.print((char)val + "\n");
		}
		g.appendNum();
	}
}
