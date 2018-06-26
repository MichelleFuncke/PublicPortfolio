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

        public CrossWord(int column, int row)
        {
            Columns = column;
            Rows = row;
            Words = new ObservableCollection<PuzzleWord>();
        }

        public CrossWord(FileInfo file)
        {
            Words = new ObservableCollection<PuzzleWord>();

            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.Load(file.FullName);

            //get root element of document
            XmlElement root = xmlDoc.DocumentElement;

            ReadGridSize(root);

            ReadWords(root);
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
