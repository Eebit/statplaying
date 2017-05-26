# The Statplaying Engine Project

## Objective
The **Statistical Roleplaying Engine** (or **Statplay Engine**) is a project by several members of the ZEJ Roleplaying Forums to model the popular "ShadowSystem" style of statistical roleplaying that is often conducted over the forums. The project is coded in Python, and is also [being ported to C# by Nebulon Ranger](https://github.com/DW01/SPEngineRedux) (aka DW01).

Check out the discussion thread at: https://www.zejroleplaying.org/threads/zej-statplay-engine.1938/

### Goals
* To create the framework for an appropriate Statistical Roleplay model, with functional Cells and a Grid upon which a single Unit can be placed and move around in.
* To create a statplay battle that can be conducted locally, with one player controlling all units
* To import a “GameState” G and generate a “successor GameState” G’ by a set of Turns {T1, T2, …, Tn} and output the progression of G |- G’ to a MyBB-compatible text file (i.e. simulate the process of GMing)
* To simulate basic enemy AI functionality, such that enemy agents can act independent of human control based on given “directives”.
