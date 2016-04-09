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
	private char name;
	private boolean passable;
	private boolean occupiable;
	private boolean blockRange;
	private int currentHP;
	private int maxHP;
	private int defense;
	private int spirit;
	private int con;

	// Constructors
	
	/**
	 * Dummy constructor to create a blank cell 
	 */
	public Cell() {
		
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

	/**
	 * Getter method to return the passability flag of the Cell.
	 * 
	 * @return The passable flag, a boolean. When 'true', the Cell is passable. False otherwise.
	 */
	public boolean getPassable() {
		return this.passable;
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
	 * The toString() method prints the current Cell as a String.
	 * 
	 * Currently it is just a dummy operation that prints a blank Cell
	 * to get things up and running. To be updated in the future.
	 */
	public String toString() {
		String s = "{ }";
		return s;
	}
}