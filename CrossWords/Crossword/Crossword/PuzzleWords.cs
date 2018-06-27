using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows;
using System.ComponentModel;
using System.Collections.ObjectModel;
using System.IO;
using System.Xml;

namespace Crossword
{
    public enum Direction
    {
        across,
        down,
    }

    public class CrossWord
    {
        public int Columns { get; set; }
        public int Rows { get; set; }

        public ObservableCollection<PuzzleWord> Words { get; set; }
        public Grid TheGrid { get; set; }
        public bool[,] ControlPresent { get; set; }
        public List<PuzzleWord> InvalidWords { get; set; }

        public CrossWord(int column, int row, int size)
        {
            Columns = column;
            Rows = row;
            Words = new ObservableCollection<PuzzleWord>();

            CreateGrid(size);
        }

        public CrossWord(FileInfo file, int size)
        {
            Words = new ObservableCollection<PuzzleWord>();

            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load(file.FullName);

            //get root element of document
            XmlElement root = xmlDoc.DocumentElement;

            ReadGridSize(root);

            ReadWords(root);

            CreateGrid(size);
        }

        private void ReadGridSize(XmlElement root)
        {
            Columns = int.Parse(root.Attributes.GetNamedItem("numC").Value);
            Rows = int.Parse(root.Attributes.GetNamedItem("numR").Value);
        }

        private void ReadWords(XmlElement root)
        {
            //select all elements under the Default node
            XmlNodeList nodeList = root.ChildNodes;

            if (nodeList.Count == 0)
            {
                throw new Exception("The crossword file isn't formatted correctly.");
            }

            //loop through the nodelist
            foreach (XmlNode item in nodeList)
            {
                var word = item.Attributes.GetNamedItem("value").Value;
                var number = int.Parse(item.Attributes.GetNamedItem("number").Value);
                var clue = item.Attributes.GetNamedItem("clue").Value;
                var direction = item.Attributes.GetNamedItem("direction").Value;
                var startC = int.Parse(item.Attributes.GetNamedItem("startC").Value);
                var startR = int.Parse(item.Attributes.GetNamedItem("startR").Value);

                Words.Add(new PuzzleWord(word, number, clue, direction, startC, startR));
            }
        }

        public void Add(PuzzleWord newWord)
        {
            Words.Add(newWord);
        }

        public void Sort()
        {
            Words.MySort();
        }

        public void Save(FileInfo file)
        {
            XmlDocument xmlDoc = new XmlDocument();
            XmlElement root = xmlDoc.CreateElement("crossword");

            root.SetAttribute("numC", Columns.ToString());
            root.SetAttribute("numR", Rows.ToString());

            foreach (PuzzleWord item in Words)
            {
                XmlElement word = xmlDoc.CreateElement("word");
                word.SetAttribute("number", item.ClueNumber.ToString());
                word.SetAttribute("value", item.Word);
                word.SetAttribute("clue", item.Clue);
                word.SetAttribute("direction", item.WordDirection.ToString());
                word.SetAttribute("startC", item.StartColumn.ToString());
                word.SetAttribute("startR", item.StartRow.ToString());

                root.AppendChild(word);
            }

            xmlDoc.AppendChild(root);

            xmlDoc.Save(file.FullName);
        }

        private void CreateGrid(int Size, bool gridLines = false)
        {
            TheGrid = new Grid();
            TheGrid.Background = new SolidColorBrush(Colors.Black);

            for (int i = 0; i < Columns; i++)
            {
                ColumnDefinition Col = new ColumnDefinition();
                Col.Width = new GridLength(Size);

                TheGrid.ColumnDefinitions.Add(Col);
            }

            for (int i = 0; i < Rows; i++)
            {
                RowDefinition Row = new RowDefinition();
                Row.Height = new GridLength(Size);

                TheGrid.RowDefinitions.Add(Row);
            }

            ControlPresent = new bool[Columns, Rows];

            TheGrid.ShowGridLines = gridLines;
        }

        public void DrawPuzzle()
        {
            InvalidWords = new List<PuzzleWord>();

            foreach (PuzzleWord word in Words)
            {
                DrawPuzzleWord(word);
            }
        }

        public void DrawPuzzleWord(PuzzleWord word)
        {
            int startCol = word.StartColumn;
            int startRow = word.StartRow;

            //determine the direction
            int directionCol = Direction.across == word.WordDirection ? 1 : 0;
            int directionRow = Direction.down == word.WordDirection ? 1 : 0;

            //Check whether the puzzleword will fit on the grid with the existing Puzzleboxes
            if (PuzzleWordIsValid(word, startCol, startRow, directionCol, directionRow))
            {
                //foreach character in the word
                foreach (char letter in word.GetLetters())
                {
                    DrawLetterBox(word, startCol, startRow, letter);

                    //move in the direction
                    startCol += directionCol;
                    startRow += directionRow;
                }
            }
            else
            {
                //Throw a warning for this invalid word
                InvalidWords.Add(word);
            }
        }

        private bool PuzzleWordIsValid(PuzzleWord word, int startCol, int startRow, int directionCol, int directionRow)
        {
            for (int i = 0; i < word.Length; i++)
            {
                var currentCol = startCol + directionCol * i;
                var currentRow = startRow + directionRow * i;

                if ((currentCol >= ControlPresent.GetLength(0)) || (currentRow >= ControlPresent.GetLength(1)))
                {
                    return false;
                }

                if (ControlPresent[currentCol, currentRow])
                {
                    //Check expected letter if the textbox does exist
                    PuzzleLetter theBox = TheGrid.Children.Cast<PuzzleLetter>().Where(k => (Grid.GetRow(k) == currentRow) && (Grid.GetColumn(k) == currentCol)).FirstOrDefault();

                    //Check that the expected letter in the textbox is equal to the expected letter we were trying to add
                    //If they aren't then the puzzle isn't valid and shouldn't be loaded
                    if (Char.ToUpper(word.Word[i]) != theBox.ExpectedLetter)
                    {
                        return false;
                    }
                }
            }
            //If there were no conflicts then the word should fit on the grid
            return true;
        }

        private void DrawLetterBox(PuzzleWord word, int startCol, int startRow, char letter)
        {
            //Check the textbox doesn't exist
            if (ControlPresent[startCol, startRow])
            {
                EditExistingBox(word, startCol, startRow);
            }
            else
            {
                PuzzleLetter box = CreateNewBox(word, startCol, startRow, letter);

                TheGrid.Children.Add(box);
                ControlPresent[startCol, startRow] = true;
            }
        }

        private static PuzzleLetter CreateNewBox(PuzzleWord word, int startCol, int startRow, char letter)
        {
            string cornerNumber = "";
            if ((startCol == word.StartColumn) && (startRow == word.StartRow))
            {
                cornerNumber = word.ClueNumber.ToString();
            }
            //Create textbox because it doesn't already exist
            PuzzleLetter box = new PuzzleLetter(letter, cornerNumber);

            //determine the starting position
            Grid.SetColumn(box, startCol);
            Grid.SetRow(box, startRow);
            return box;
        }

        private void EditExistingBox(PuzzleWord word, int startCol, int startRow)
        {
            //Don't need to check if the expected letters are the same because we already checked them
            PuzzleLetter theBox = TheGrid.Children.Cast<PuzzleLetter>().Where(i => (Grid.GetRow(i) == startRow) && (Grid.GetColumn(i) == startCol)).FirstOrDefault();

            if ((HeaderTemp.GetDefaultNumber(theBox) == "") && ((startCol == word.StartColumn) && (startRow == word.StartRow)))
            {
                HeaderTemp.SetDefaultNumber(theBox, word.ClueNumber.ToString());
            }
        }
    }

    public class PuzzleWord : INotifyPropertyChanged
    {
        private int _clueNumber;
        private String _clue;

        public String Word { get; private set; }
        public int Length { get; private set; }
        
        public int ClueNumber
        {
            get { return _clueNumber; }
            set
            {
                if (value > 0)
                {
                    _clueNumber = value;
                    OnPropertyChanged("ClueNumber");
                }
            }
        }
        public String Clue
        {
            get { return _clue; }
            set
            {
                _clue = value;
                OnPropertyChanged("Clue");
            }
        }

        public Direction WordDirection { get; private set; }
        public int StartColumn { get; private set; }
        public int StartRow { get; private set; }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public PuzzleWord(string word, int cluenumber, string clue, string direction, int startC, int startR)
        {
            Word = word;
            Length = word.Length;

            ClueNumber = cluenumber;
            Clue = clue;            
            
            WordDirection = (Direction)Enum.Parse(typeof(Direction), direction.ToLower());
            StartColumn = startC;
            StartRow = startR;
        }

        public IEnumerable<char> GetLetters()
        {
            foreach (char item in Word)
            {
                yield return item;
            }
        }
    }

    public class PuzzleLetter : TextBox
    {
        public char ExpectedLetter { get; private set; }

        public PuzzleLetter()
        {
            this.Style = (Style)FindResource("TextBoxStyle");
        }

        public PuzzleLetter(char expectedLetter, string defaultNumber="")
        {
            ExpectedLetter = Char.ToUpper(expectedLetter);

            this.Style = (Style)FindResource("TextBoxStyle");
            HeaderTemp.SetDefaultNumber(this, defaultNumber);

            this.MaxLength = 1;
            this.Text = "";
            this.FontSize = 24;
            this.HorizontalContentAlignment = HorizontalAlignment.Center;
            this.VerticalContentAlignment = VerticalAlignment.Center;
            this.CharacterCasing = CharacterCasing.Upper;
            this.Background = new SolidColorBrush(Colors.White);
            this.Foreground = new SolidColorBrush(Colors.Black);
        }

        public Boolean CheckLetter()
        {
            return ExpectedLetter == this.Text.Cast<char>().FirstOrDefault();
        }
    }
}
