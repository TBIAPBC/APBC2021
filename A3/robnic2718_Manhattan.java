// Import classes
import java.util.Scanner;
import java.util.Vector;
import java.io.File;
import java.io.FileNotFoundException;

public class robnic2718_Manhattan
{
  // Class variables //
  // indexing of matrix (2D-vector): first ROW then COLUMN
  static Vector<Vector<Double>> northSouth, westEast, diagonals = null;
  static final char[] directions = new char[]{'S', 'E', 'D'};
  static boolean diagEdges = false, showBestPath = false, nextMatrix = false;
  static int rowCount = 0, colCount = 0, coldimNS = 0, rowdimWE = 0;
  // Instance variables //
  //[row, column], automatically initialised with 0s
  // The variable current position is a 2-dimensional array that keeps track of the current position of the "tourist"
  int[] currPos;
  double[][] dpMatrix;
  
  // Constructor
  public robnic2718_Manhattan()
  {
    currPos = new int[] {1, 1};
    dpMatrix = new double[rowdimWE][coldimNS];

    // Initialise DP-Matrix, i.e. assign cumulative weights on first row and column
    for(int index = 0; index < rowdimWE-1; index++)
      dpMatrix[index+1][0] = dpMatrix[index][0] 
                             + northSouth.elementAt(index).elementAt(0);
    for(int index = 0; index < coldimNS-1; index++)
      dpMatrix[0][index+1] = dpMatrix[0][index]
                             + westEast.elementAt(0).elementAt(index);
  }
  
  // Program entry point //
  public static void main(String[] args)
  {
    File inputFile;
    
    // Parse command line arguments and assing filename to variable inputFile
    inputFile = parse_cmd_args(args);
    // Read in data from file into matrices in line 11
    process_file(inputFile);
    
    // Initialise new instance of Manhattan Tourist Problem
    robnic2718_Manhattan tourist = new robnic2718_Manhattan();
    double result;
    result = tourist.explore_optimalPath();
    
    // Check if result can be rounded to integer and if yes do it
    if(result%1 == 0)
      System.out.println((int)result);
    else
    {
      System.out.printf("%.2f", result); System.out.print('\n');
    }
    
    if(showBestPath)
      System.out.println(tourist.backtrack());
  }
  
  // Performs backtracking until currPos is [0,0], i.e. until the upper left corner of DPmatrix has been reached
  private String backtrack()
  {
    String bestPath = new String("");
    
    while(!reached_start())
      bestPath = step_back() + bestPath;
    
    return bestPath;
  }
  
  /* The step_back method checks from the perspective of the current position in the DPmatrix,
  which weight of the possible paths leading to the starting point of the tourist could create the weight
  at the current position pointed at by the index array currPos (see line 18). Each weight is converted from
  double to float format in order to account for errors arising from floating point arithmetics. Otherwise a comparison
  with "==" would always result in the boolean value false.
  Example: 
  a) dpMatrix[currPos[0]][currPos[1]] … outputs the current score of the DPmatrix, where the tourist finds himself, when
  he walks back. 
  b) backtrack_weight('N') … outputs the weight of the street, from the perspective of the tourist's current position, when walking
  into the direction of North (opposite of South, because the tourist walks back).
  c) dpMatrix[currPos[0] - 1][currPos[1]] … outputs the score in the DPmatrix where the tourist would find himself after walking 
  North street.
  By checking whether the current position's score (a) minus the weight of the North path (b) equals the score of the position after
  walking the North street (c) we can infer that the the North path is the optimal path to go. However we output 'S' for South since we
  walked into the back direction.
  currPos[0] … gives the row position
  currPos[1] … gives the col position
  As an example [currPos[0]-1,currPos[1]] gives us the position one row above the current position.*/
  private char step_back()
  {
    if(currPos[0] != 0)
      if((float)(dpMatrix[currPos[0]][currPos[1]] -  backtrack_weight('N'))
         == (float)dpMatrix[currPos[0] - 1][currPos[1]])
      {
        currPos[0]--;
        return 'S';
      }
    if(currPos[1] != 0)
      if((float)(dpMatrix[currPos[0]][currPos[1]] -  backtrack_weight('W'))
         == (float)dpMatrix[currPos[0]][currPos[1] - 1])
      {
        currPos[1]--;
        return 'E'; 
      }
    if((float)(dpMatrix[currPos[0]][currPos[1]] -  backtrack_weight('D')) 
       == (float)dpMatrix[currPos[0] - 1][currPos[1] - 1])
    {
      currPos[0]--; currPos[1]--;
      return 'D';
    }
    try 
    {
      throw new Exception("Indexing error!"); 
    } catch(Exception e)
      {
        System.out.println(e.getMessage());
        System.exit(0);
      }
    return 'x';
  }
  
  // Check if backtracking has been finished, by checking whether we reached the upper left corner of DPmatrix
  private boolean reached_start()
  {
    if(currPos[0] == 0 && currPos[1] == 0)
      return true;
    
    return false;
  }
  
  /* Output the weight of the streets from the perspective of the current position in the DPmatrix.
  In order to avoid accessing not existant paths, whenever we are the a border of the DPmatrix, we avoid
  accessing a non-existant weight into the corresponding directions, by letting the method backtrack_weight
  output NEGATIVE_INFINITY, such that this direction will never be an option for maximizing the score.
  If we have no diagonal weights read in we immediately return NEGATIVE_INFINITY, such that the diagonal path will never
  be an option. (see diagEdges (boolean variable) in line 153)*/
  private double backtrack_weight(char direction)
  {
    switch(direction)
    {
      case 'N':
        if(currPos[0] == 0)
          return Double.NEGATIVE_INFINITY;
        return northSouth.elementAt(currPos[0] - 1).elementAt(currPos[1]);
      case 'W':
        if(currPos[1] == 0)
          return Double.NEGATIVE_INFINITY;
        return westEast.elementAt(currPos[0]).elementAt(currPos[1] - 1);
      case 'D':
        if(!diagEdges || currPos[0] == 0 || currPos[1] == 0)
          return Double.NEGATIVE_INFINITY;
        return diagonals.elementAt(currPos[0] - 1).elementAt(currPos[1] - 1);
    }
    try {
      throw new Exception("Indexing error!"); 
    } catch(Exception e)
      {
        System.out.println(e.getMessage());
        System.exit(0);
      }
    return 0.0;
  }
  
  // Fill up the initialized DPmatrix with the cumulating weights of the streets
  private double explore_optimalPath()
  { 
    while(!reached_goal())
    {
      get_maxNupdate();
      
      while(currPos[1]++ < coldimNS-1)
        get_maxNupdate();
      
      currPos[0]++; currPos[1] = 1;
    }
    currPos[0] = rowdimWE-1; currPos[1] = coldimNS-1;
    
    return dpMatrix[rowdimWE-1][coldimNS-1];
  }
  
  /* This method retrieves the weights of all possible paths from the perspective of the current position in
  the DPmatrix using the helper method get_weight. It then finds the maximum cumulative weight and enters the weight
  into the DPmatrix. */
  private void get_maxNupdate()
  {
    double[] pathWeights = new double[] {get_weight('S'), get_weight('E'), get_weight('D')};
    double maximum = Double.NEGATIVE_INFINITY;

    for(double weight : pathWeights)
      if(weight > maximum)
        maximum = weight;

    // Enter weight into DP-matrix
    dpMatrix[currPos[0]][currPos[1]] = maximum;
  }
  
  // Check whether the current position has reached the lower right corner of the DPmatrix
  private boolean reached_goal()
  {
    /* we only need to check whether we reached the last row in the DPmatrix since we fill up
    of the DPmatrix rowwise after initializing. */
    if(currPos[0] == rowdimWE)
      return true;
    
    return false;
  }
  
  /* Get the cumulative weights, i.e. weight/score at current position plus weight after walking
  into the chosen direction from the perspective of the current position in the DPmatrix.*/
  private double get_weight(char direction)
  {
    switch(direction)
    {
      case 'S':
        return dpMatrix[currPos[0] - 1][currPos[1]] + 
               northSouth.elementAt(currPos[0] - 1).elementAt(currPos[1]);
        
      case 'E':
        return dpMatrix[currPos[0]][currPos[1] - 1] +
               westEast.elementAt(currPos[0]).elementAt(currPos[1] - 1);
        
      case 'D':
        if(!diagEdges)
          return Double.NEGATIVE_INFINITY;
        
        return dpMatrix[currPos[0] - 1][currPos[1] - 1] +
               diagonals.elementAt(currPos[0] - 1).elementAt(currPos[1] - 1);
    }
    try {
      throw new Exception("Indexing error!"); 
    } catch(Exception e)
      {
        System.out.println(e.getMessage());
        System.exit(0);
      }
    return 0.0;
  }
  
  // Class methods //
  // Process data file
  private static void process_file(File inputFile)
  {
    // Initialise matrices
    northSouth = new Vector<Vector<Double>>();
    westEast = new Vector<Vector<Double>>();
    // Helper variables
    Scanner lineScan;
    String line = new String();
    boolean processing_Done = false;
    
    try
    {
      // Scan through content of file using class Scanner
      Scanner fileScan = new Scanner(inputFile);
      
      // Keep iterating through lines in the file until there is no further line
      while(fileScan.hasNextLine())
      { 
        line = fileScan.nextLine();
        lineScan = new Scanner(line);
        // If lines contains '#' at any point or is empty jump to the next line
        if(check_line(line))
          continue;
        
        // Process the North-South and East-West weight matrices
        processing_Done = process_HV(lineScan);
        
        // Break out of while loop if NS and EW weights have been processed
        if(processing_Done)
          break;
      }
      // If -d is provided also read in diagonal weights matrix
      if(diagEdges)
      {
        diagonals = new Vector<Vector<Double>>();
        
        if(!fileScan.hasNextLine()) {
        	try {
        	  throw new Exception("You specified -d for reading diagonal weights, although file-format is HV.");
        	} catch(Exception e)
        	  {
        	  	System.out.println(e.getMessage());
        	  	System.exit(0);
        	  }
        }

        while(fileScan.hasNextLine())
        {
          line = fileScan.nextLine();
          lineScan = new Scanner(line);
          if(check_line(line))
            continue;
          
          process_D(lineScan);
        }
      }
      rowdimWE = rowCount;
      
      // Check if diagonal weights are present in file
       // if option -d has not been provided and throw Exception
      if(!diagEdges) {
        while(fileScan.hasNextLine()) {
      	  line = fileScan.nextLine();
      	  if(check_line(line))
      		  try {
      		    throw new Exception("Option -d was not specified although file contains diagonal-weights-matrix.");
      		  } catch(Exception e) {
                System.out.println(e.getMessage());
                System.exit(0);
      		    }
        }
      }

      fileScan.close();
    } 
      catch(FileNotFoundException e)
      { 
        System.out.println(e.getMessage());
        System.exit(0);
      }
  }
  
  // Read in NorthSouth and WestEast edge weights
  private static boolean process_HV(Scanner lineScan)
  {
    Vector<Double> rowVec = new Vector<Double>();
    
    while(lineScan.hasNextDouble())
      rowVec.addElement(lineScan.nextDouble());
    lineScan.close();
    
    if(rowVec.size() == colCount-1)
    {
      nextMatrix = true;
      coldimNS = colCount; 
    }
    colCount = rowVec.size();
    
    if(!nextMatrix) 
      northSouth.addElement(new Vector<Double>(rowVec));
    else
    {
      westEast.addElement(new Vector<Double>(rowVec));
      rowCount++;
    }
    rowVec.clear();
    
    if(nextMatrix && rowCount == coldimNS)
      return true;
    
    return false;
  }
  
  // If required, read in SouthEast edge weights
  private static void process_D(Scanner lineScan)
  {
    // Helper variables
    Vector<Double> rowVec = new Vector<Double>();
      
    while(lineScan.hasNextDouble())
      rowVec.addElement(lineScan.nextDouble());
      
    diagonals.addElement(new Vector<Double>(rowVec));
    rowVec.clear();
    
    lineScan.close();
  }
  
  // Check for empty and commented lines
  private static boolean check_line(String line)
  { 
    if(line.isEmpty()) 
      return true;
    if(line.trim().charAt(0) == '#')
      return true;
    
    return false;
  }
  
  // Parse command-line arguments and Exception handling
  private static File parse_cmd_args(String[] args)
  {
    boolean providedFile = false;
    File inputFile = null;
    
    try 
    {
      if(args.length == 0)
        throw new Exception("Error: please provide input file\nOptional flags:\n-t"
                            + "--> print optimal path\n-d --> process diagonal weights");
      if(args.length > 3)
        throw new Exception("Provide a maximum of three cmd-line arguments:\n"
                            + "> name of input file (obligatory)\n> optimal path flag "
                            + "-t (optional)\n> process diagonals flag -d (optional)");
      
      for(String arg : args)
      {
        if(!arg.equals("-d") && !arg.equals("-t"))
        {
          inputFile = new File(arg);
          providedFile = true;
        }
        if(arg.equals("-d"))
          diagEdges = true;
        if(arg.equals("-t"))
          showBestPath = true;
      }
      if(!providedFile)
        throw new Exception("Error: please provide an input file!");
    }
      catch(Exception e)
      {
        System.out.println(e.getMessage());
        System.exit(0);
      }
    
    return inputFile;
  }
}
