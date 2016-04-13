public class EmptyCell extends Cell implements ICell {
	// ATTRIBUTES
	
	// Descriptor strings.
	public String cellName;
	public char cellID;
	public String cellDescriptor;
	public String cellFormatter;

	// Passability flags.
	public boolean isPassable;
	public boolean isOccupiable;
	public boolean isOccupied;

	// Breakablility and block property.
	public boolean isBreakable;
	public boolean hasHP;
	public double currentHP;
	public double maxHP;
	public boolean blockProperty;

	// CONSTRUCTORS
	public EmptyCell() {
		initialiseFlags();
		initialiseBreakability();
		createCell();
	}

	
	// METHODS
	// Helper methods.
	protected void setFlags() {
		isPassable = true;
		isOccupiable = true;
		isOccupied = false;
		blockProperty = false;
	}

	protected void setBreakable() {
		isBreakable = false;
	}

	protected void setCellHP() {
		hasHP = false;
		currentHP = 0;
		maxHP = 0;
	}

	protected void setCellInfo() {
		cellName = "Empty Cell";
		cellID = cellName.charAt(0);
		cellDescriptor = "A blank Empty Cell.";
		cellFormatter = "{ }";
	}

	// Implementation of interface contract methods.
	public void initialiseFlags() {
		setFlags();
	}

	public void initialiseBreakability() {
		setBreakable();
		setCellHP();
	}

	public void createCell() {
		setCellInfo();
	}
	
	public String toString() {
		return this.cellFormatter;
	}
}