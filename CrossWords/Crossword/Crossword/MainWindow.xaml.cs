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

        private List<PuzzleWord> Puzzle1(out int colCount, out int rowCount)
        {
            colCount = 18;
            rowCount = 9;
            CreateGrid(colCount, rowCount, 50);

            spMain.Children.Add(CrossWordGrid);

            //Read words from a file
            List<PuzzleWord> theList = new List<PuzzleWord>();
            //across
            theList.Add(new PuzzleWord("MOTORWORKS", 1, "Get a $13.95 oil charge", Direction.across.ToString(), 8, 2));
            theList.Add(new PuzzleWord("CARPETLANDUSA", 2, "With your tax refund get carpet", Direction.across.ToString(), 0, 4));
            theList.Add(new PuzzleWord("CULVERS", 3, "Remodeling to serve you better", Direction.across.ToString(), 0, 6));
            theList.Add(new PuzzleWord("HEWITT", 4, "Jackson ____. Pay $50 less this year", Direction.across.ToString(), 12, 6));
            theList.Add(new PuzzleWord("VINNYSPIZZA", 5, "Home of the 24\" hurricane pizza", Direction.across.ToString(), 4, 8));

            //down
            theList.Add(new PuzzleWord("BELLAS", 1, "Featuring a \"Fairy Dust Fun Station\"", Direction.down.ToString(), 6, 1));
            theList.Add(new PuzzleWord("GIORDANOS", 2, "\"Love Takes Many Forms\"", Direction.down.ToString(), 9, 0));
            theList.Add(new PuzzleWord("ROSS", 3, "Hanser ___. A leader in eye care", Direction.down.ToString(), 11, 1));
            theList.Add(new PuzzleWord("MIKIMOTO", 4, "Japanese steakhouse in Dekalls featuring hibachi dinners", Direction.down.ToString(), 16, 0));

            return theList;
        }

        private List<PuzzleWord> Puzzle2(out int colCount, out int rowCount)
        {
            colCount = 18;
            rowCount = 13;
            CreateGrid(colCount, rowCount, 50);

            spMain.Children.Add(CrossWordGrid);

            //Read words from a file
            List<PuzzleWord> theList = new List<PuzzleWord>();
            //across
            theList.Add(new PuzzleWord("ULLRICH", 1, "__ Law, Estate Planning, Wills, Trusts, Elder law", Direction.across.ToString(), 10, 2));
            theList.Add(new PuzzleWord("FUNME", 2, "Excursions and Entertainment", Direction.across.ToString(), 1, 3));
            theList.Add(new PuzzleWord("DENTAL", 3, "__ Fields. Family & Cosmetic Dentistry", Direction.across.ToString(), 12, 4));
            theList.Add(new PuzzleWord("GARLISCH", 4, "__ Automotive Services, Inc, $13.50 oil change", Direction.across.ToString(), 3, 5));
            theList.Add(new PuzzleWord("MEDITERRANEO", 5, "Middle Eastern Sunday Buffet $11.95", Direction.across.ToString(), 3, 8));
            theList.Add(new PuzzleWord("KISHHEALTHSYSTEM", 6, "Now part of Northwestern Medicine", Direction.across.ToString(), 0, 10));
            theList.Add(new PuzzleWord("RUBYSASIAN", 7, "__ __ Market & Other Importal Goods", Direction.across.ToString(), 8, 12));

            //down
            theList.Add(new PuzzleWord("QUALITY", 1, "__ Mattress Warehouse. Get a free queen", Direction.down.ToString(), 1, 6));
            theList.Add(new PuzzleWord("JAMRAH", 2, "Chicken Shawarma Meal Deal, $7.99", Direction.down.ToString(), 4, 1));
            theList.Add(new PuzzleWord("LOSSCENTER", 3, "Sycamore Integrated Weight __ __.", Direction.down.ToString(), 8, 3));
            theList.Add(new PuzzleWord("MULCHWORKS", 4, "Where hundreds receive great service every year", Direction.down.ToString(), 10, 1));
            theList.Add(new PuzzleWord("HARVEST", 5, "__ Bible Chapel. Good Friday 7pm", Direction.down.ToString(), 13, 0));
            theList.Add(new PuzzleWord("LEHAN", 6, "We're more than medicine", Direction.down.ToString(), 17, 4));

            return theList;
        }

        private void PopulateGrid(int colCount, int rowCount, List<PuzzleWord> theList)
        {
            bool[,] ControlPresent = new bool[colCount, rowCount];

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
                    if (ControlPresent[startCol, startRow])
                    {
                        //Check expected letter if the textbox does exist
                        PuzzleLetter theBox = CrossWordGrid.Children.Cast<PuzzleLetter>().Where(i => (Grid.GetRow(i) == startRow) && (Grid.GetColumn(i) == startCol)).FirstOrDefault();

                        //Check that the expected letter in the textbox is equal to the expected letter we were trying to add
                        //If they aren't then the puzzle isn't valid and shouldn't be loaded
                        if (letter != theBox.ExpectedLetter)
                        {
                            throw new Exception();
                        }

                        if ((HeaderTemp.GetDefaultNumber(theBox) == "") && ((startCol == word.StartColumn) && (startRow == word.StartRow)))
                        {
                            HeaderTemp.SetDefaultNumber(theBox, word.ClueNumber.ToString());
                        }

                        //move in the direction
                        startCol += directionCol;
                        startRow += directionRow;
                    }
                    else
                    {
                        string cornerNumber = "";
                        if ((startCol == word.StartColumn) && (startRow == word.StartRow))
                        {
                            cornerNumber = word.ClueNumber.ToString();
                        }
                        //Create textbox if it doesn't already exist
                        PuzzleLetter box = new PuzzleLetter(letter, cornerNumber);

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
            }
        }

        private void mnuLoad_Click(object sender, RoutedEventArgs e)
        {
            if (CrossWordGrid != null)
            {
                return;
            }

            int colCount, rowCount;
            var theList = Puzzle1(out colCount, out rowCount);

            PopulateGrid(colCount, rowCount, theList);

            tabWindow.SelectedItem = tbiSolvePuzzle;
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

        private void mnuCreate_Click(object sender, RoutedEventArgs e)
        {
            tabWindow.SelectedItem = tbiCreatePuzzle;

            var colCount = 10;
            var rowCount = 10;
            CreateGrid(colCount, rowCount, 40);

            spMakePuzzle.Children.Add(CrossWordGrid);
        }

        private void btnResize_Click(object sender, RoutedEventArgs e)
        {
            var col = (int)udColumn.Value;
            var row = (int)udRow.Value;

            spMakePuzzle.Children.Remove(CrossWordGrid);

            CreateGrid(col, row, 40);
            spMakePuzzle.Children.Add(CrossWordGrid);
        }
    }
}
