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
  int[] currPos;
  double[][] dpMatrix;
  
  // Constructor
  public robnic2718_Manhattan()
  {
    currPos = new int[] {1, 1};
    dpMatrix = new double[rowdimWE][coldimNS];

    // Initialise DP-Matrix
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
    
    inputFile = parse_cmd_args(args);
    process_file(inputFile);
    
    // Initialise new instance of Manhattan Tourist Problem
    robnic2718_Manhattan tourist = new robnic2718_Manhattan();
    double result;
    result = tourist.explore_optimalPath();
    
    if(result%1 == 0)
      System.out.println((int)result);
    else
    {
      System.out.printf("%.2f", result); System.out.print('\n');
    }
    
    if(showBestPath)
      System.out.println(tourist.backtrack());
  }
  
  private String backtrack()
  {
    String bestPath = new String("");
    
    while(!reached_start())
      bestPath = step_back() + bestPath;
    
    return bestPath;
  }
  
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
  
  private boolean reached_start()
  {
    if(currPos[0] == 0 && currPos[1] == 0)
      return true;
    
    return false;
  }
  
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
  
  private boolean reached_goal()
  {
    if(currPos[0] == rowdimWE)
      return true;
    
    return false;
  }

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
      Scanner fileScan = new Scanner(inputFile);
      
      while(fileScan.hasNextLine())
      { 
        line = fileScan.nextLine();
        lineScan = new Scanner(line);
        if(check_line(line))
          continue;
        
        processing_Done = process_HV(lineScan);
        
        if(processing_Done)
          break;
      }
      if(diagEdges)
      {
        diagonals = new Vector<Vector<Double>>();
        
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