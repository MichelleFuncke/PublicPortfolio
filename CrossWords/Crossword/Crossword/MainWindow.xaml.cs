using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Crossword
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public Grid CrossWordGrid;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void CreateGrid(int ColumnCount, int RowCount, int Size)
        {
            CrossWordGrid = new Grid();
            CrossWordGrid.Background = new SolidColorBrush(Colors.Black);

            for (int i = 0; i < ColumnCount; i++)
            {
                ColumnDefinition Col = new ColumnDefinition();
                Col.Width = new GridLength(Size);

                CrossWordGrid.ColumnDefinitions.Add(Col);
            }

            for (int i = 0; i < RowCount; i++)
            {
                RowDefinition Row = new RowDefinition();
                Row.Height = new GridLength(Size);

                CrossWordGrid.RowDefinitions.Add(Row);
            }

            CrossWordGrid.ShowGridLines = true;
        }

        private void mnuLoad_Click(object sender, RoutedEventArgs e)
        {
            if (CrossWordGrid != null)
            {
                return;
            }

            CreateGrid(10, 10, 50);
            bool[,] ControlPresent = new bool[10, 10];
            spMainPage.Children.Add(CrossWordGrid);

            //Read words from a file
            List<PuzzleWord> theList = new List<PuzzleWord>();
            theList.Add(new PuzzleWord("CAT", 1, "blabla", Direction.across.ToString(), 0, 2));
            theList.Add(new PuzzleWord("CAN", 1, "blabla", Direction.down.ToString(), 1, 1));

            //foreach word in puzzle
            foreach (PuzzleWord word in theList)
            {
                int startCol = word.StartColumn;
                int startRow = word.StartRow;

                //determine the direction
                int directionCol = Direction.across == word.WordDirection ? 1 : 0;
                int directionRow = Direction.down == word.WordDirection ? 1 : 0;

                //foreach character in the word
                foreach (char letter in word.GetLetters())
                {
                    //Check the textbox doesn't exist
                    if (ControlPresent[startCol,startRow])
                    {
                        //Check expected letter if the textbox does exist
                        PuzzleLetter theBox = CrossWordGrid.Children.Cast<PuzzleLetter>().Where(i => (Grid.GetRow(i) == startRow) && (Grid.GetColumn(i) == startCol)).FirstOrDefault();

                        //Check that the expected letter in the textbox is equal to the expected letter we were trying to add
                        //If they aren't then the puzzle isn't valid and shouldn't be loaded
                        if (letter != theBox.ExpectedLetter)
                        {
                            throw new Exception();
                        }

                        //move in the direction
                        startCol += directionCol;
                        startRow += directionRow;
                    }
                    else
                    {
                        //Create textbox if it doesn't already exist
                        PuzzleLetter box = new PuzzleLetter(letter);

                        //determine the starting position
                        Grid.SetColumn(box, startCol);
                        Grid.SetRow(box, startRow);

                        CrossWordGrid.Children.Add(box);
                        ControlPresent[startCol, startRow] = true;

                        //move in the direction
                        startCol += directionCol;
                        startRow += directionRow;   
                    }                    
                }

                //Add the clue to a list to display
            }  
        }

        private void mnuReset_Click(object sender, RoutedEventArgs e)
        {
            if (CrossWordGrid == null)
            {
                return;
            }

            foreach (PuzzleLetter item in CrossWordGrid.Children)
            {
                item.Text = "";
            }

            CrossWordGrid.Background = new SolidColorBrush(Colors.Black);
        }

        private void mnuCheck_Click(object sender, RoutedEventArgs e)
        {
            if (CrossWordGrid == null)
            {
                return;
            }

            var solved = true;
            foreach (PuzzleLetter item in CrossWordGrid.Children)
            {
                solved = item.CheckLetter() && solved;
            }

            if (!solved)
            {
                CrossWordGrid.Background = new SolidColorBrush(Colors.Red);
            } 
        }
    }
}
