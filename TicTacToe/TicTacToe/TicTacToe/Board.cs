using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TicTacToe
{
    public class Board
    {
        private char[,] _grid = new char[3, 3];
        private char _marker = 'X';

        public char[,] Grid => _grid;

        public Board()
        {
            for (int i = 0; i < 3; i++)
            {
                for (int k = 0; k < 3; k++)
                {
                    _grid[i, k] = 'B';
                }
            }
        }

        public void PlaceMarker(int x, int y)
        {
            if ((x < 3) && (y < 3) && (_grid[x, y] == 'B'))
            {
                _grid[x, y] = _marker;
                _marker = (_marker == 'X') ? 'O' : 'X';

                //Check if that was a winning move
                //If it is trigger the win drawing event
            }

            //We don't want this to trigger an error cause the user might have just clicked here.
        }

        public Boolean IsFreeSpace(int x, int y)
        {
            if ((x < 3) && (y < 3) && (_grid[x, y] == 'B'))
            {
                return true;
            }
            return false;
        }

        public List<Line> GetLines(int x, int y)
        {
            var theList = new List<Line>();
            if ((x > 2) || (y > 2))
            {
                return theList;
            }

            //The row win
            theList.Add(new Line(x, 0, x, 2));

            //The column win
            theList.Add(new Line(0, y, 2, y));

            //The diagonal wins
            if (x == y)
            {
                theList.Add(new Line(0, 0, 2, 2));
            }

            if ((x == 0 & y == 2) || (x == 2 & y == 0) || (x == 1 & y == 1))
            {
                theList.Add(new Line(0, 2, 2, 0));
            }

            return theList;
        }
    }

    public class Line
    {
        public Point StartPoint { get; set; }
        public Point EndPoint { get; set; }
        public Point MidPoint { get; set; }

        public Line(int startX, int startY, int endX, int endY)
        {
            StartPoint = new Point(startX, startY);
            EndPoint = new Point(endX, endY);

            int midX = (startX + endX) / 2;
            int midY = (startY + endY) / 2;
            MidPoint = new Point(midX, midY);
        }

        public Boolean IsOnLine(int x, int y)
        {
            if (StartPoint.Xaxis == x && StartPoint.Yaxis == y)
            {
                return true;
            }
            else if(EndPoint.Xaxis == x && EndPoint.Yaxis == y)
            {
                return true;
            }
            else if (MidPoint.Xaxis == x && MidPoint.Yaxis == y)
            {
                return true;
            }

            return false;
        }
    }

    public class Point
    {
        public int Xaxis { get; set; }
        public int Yaxis { get; set; }

        public Point(int x, int y)
        {
            Xaxis = x;
            Yaxis = y;
        }
    }
}
