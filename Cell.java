/**
 * Cell.java
 * 
 * A Cell is the most basic unit of measure in statplaying. The Cell class
 * handles the creation of and the statistics for this basic unit.
 * 
 * @author Jake "Eebit" Fryer
 * @since April 09, 2016
 */

public class Cell {
	// Attributes
	private char name;			// the "name" of the cell; letter or symbol to denote it on grid
	private boolean passable;	// 
	private boolean occupiable;
	private boolean blockRange;
//	private int currentHP;
//	private int maxHP;
//	private int defense;
//	private int spirit;
	private int con;

	// Constructors
	
	/**
	 * Dummy constructor to create a blank cell 
	 */
	public Cell() {
		// Set flags
		this.passable = true;
		this.occupiable = true;
		this.blockRange = false;
	}


	// Methods
	
	public char getName() {
		return name;
	}


	public void setName(char name) {
		this.name = name;
	}


	public boolean isOccupiable() {
		return occupiable;
	}


	public void setOccupiable(boolean occupiable) {
		this.occupiable = occupiable;
	}


	public boolean isBlockRange() {
		return blockRange;
	}


	public void setBlockRange(boolean blockRange) {
		this.blockRange = blockRange;
	}
	
	/* Commenting this out pending further discussion about setting up
	 * the Cells.
	public int getCurrentHP() {
		return currentHP;
	}


	public void setCurrentHP(int currentHP) {
		this.currentHP = currentHP;
	}


	public int getMaxHP() {
		return maxHP;
	}


	public void setMaxHP(int maxHP) {
		this.maxHP = maxHP;
	}


	public int getDefense() {
		return defense;
	}


	public void setDefense(int defense) {
		this.defense = defense;
	}


	public int getSpirit() {
		return spirit;
	}


	public void setSpirit(int spirit) {
		this.spirit = spirit;
	}
	*/

	/**
	 * Getter method to return the passability flag of the Cell.
	 * 
	 * @return The passable flag, a boolean. When 'true', the Cell is passable. False otherwise.
	 */
	public boolean getPassable() {
		return this.passable;
	}
	
	/**
	 * Setter method that updates the passability flag of the Cell. 
	 * 
	 * @param passable - Boolean value. True for passable, false for impassable.
	 */
	public void setPassable(boolean passable) {
		this.passable = passable;
	}

	/**
	 * Getter method to return the CON statistic of the Cell.
	 * 
	 * @return The CON statistic, an integer between 1-10
	 */
	public int getCon() {
		return this.con;
	}
	
	/**
	 * Setter method to update the CON statistic of the Cell.
	 * 
	 * @param con - the CON statistic, an integer between 1-10
	 */
	public void setCon(int con) {
		// NOTE: Will need to make sure that the value stays between
		// range of 1-10
		this.con = con;
	}
	
	/**
	 * The toString() method prints the current Cell as a String.
	 * 
	 * Currently it is just a dummy operation that prints a blank Cell
	 * to get things up and running. To be updated in the future.
	 */
	public String toString() {
		String s = "{ }";
		
		// String s = "{" + this.getName() + "}";
		
		return s;
	}
}