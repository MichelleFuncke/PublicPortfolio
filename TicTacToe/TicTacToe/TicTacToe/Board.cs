using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TicTacToe
{
    public enum Marker
    {
        Blank,
        Cross,
        Nought
    }

    public class Board
    {
        private Marker[,] _grid = new Marker[3, 3];
        private Marker _marker = Marker.Cross;

        public Marker[,] Grid => _grid;

        public Board()
        {
            for (int i = 0; i < 3; i++)
            {
                for (int k = 0; k < 3; k++)
                {
                    _grid[i, k] = Marker.Blank;
                }
            }
        }

        public void PlaceMarker(int x, int y)
        {
            if ((x < 3) && (y < 3) && (_grid[x, y] == Marker.Blank))
            {
                _grid[x, y] = _marker;
                _marker = (_marker == Marker.Cross) ? Marker.Nought : Marker.Cross;

                if (this.IsWinningMove(x, y))
                {
                    //If it is trigger the win drawing event
                }
            }
            //We don't want this to trigger an error cause the user might have just clicked here.
        }

        public Boolean IsFreeSpace(int x, int y)
        {
            if ((x < 3) && (y < 3) && (_grid[x, y] == Marker.Blank))
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

        public Boolean IsWinningMove(int x, int y)
        {
            var theMarker = _grid[x, y];
            foreach (Line item in this.GetLines(x, y))
            {
                var winner = true;
                foreach (Point xy in item.PointsList)
                {
                    winner = (_grid[xy.Xaxis, xy.Yaxis] == theMarker) & winner;
                }

                if (winner)
                {
                    return true;
                }
            }
            return false;
        }

        public Line GetWinningLine(int x, int y)
        {
            var theMarker = _grid[x, y];
            foreach (Line item in this.GetLines(x, y))
            {
                var winner = true;
                foreach (Point xy in item.PointsList)
                {
                    winner = (_grid[xy.Xaxis, xy.Yaxis] == theMarker) & winner;
                }

                if (winner)
                {
                    return item;
                }
            }
            return null;
        }
    }

    public class Line
    {
        public List<Point> PointsList = new List<Point>();

        public Line(int startX, int startY, int endX, int endY)
        {
            PointsList.Add(new Point(startX, startY));   

            int midX = (startX + endX) / 2;
            int midY = (startY + endY) / 2;
            PointsList.Add(new Point(midX, midY));

            PointsList.Add(new Point(endX, endY));
        }

        public Boolean IsOnLine(int x, int y)
        {
            foreach (Point item in PointsList)
            {
                if (item.Xaxis == x && item.Yaxis == y)
                {
                    return true;
                }
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
