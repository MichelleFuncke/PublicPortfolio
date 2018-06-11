using NUnit.Framework;
using System;
using TicTacToe;
using System.Windows;

namespace TicTacTest
{
    [TestFixture]
    public class BoardTests
    {
        ///MethodName_StateUnderTest_ExpectedBehavior
        ///https://dzone.com/articles/7-popular-unit-test-naming

        #region Board class
        [TestCase(0, 0)]
        [TestCase(0, 1)]
        [TestCase(2, 1)]
        public void PlaceMarker_BoardAfterConstructor_MarkerAtXY(int x, int y)
        {
            //Arrange
            var actual = new Board();

            //Act
            actual.PlaceMarker(x, y);

            //Assert
            Assert.AreEqual(Marker.Cross, actual.Grid[x,y]);
        }

        [TestCase(1, 0)]
        [TestCase(0, 1)]
        [TestCase(2, 1)]
        public void PlaceMarker_BoardAfterTwoValidMarkers_MarkerAtXY(int x, int y)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(0, 0);
            actual.PlaceMarker(2, 0);

            //Act
            actual.PlaceMarker(x, y);

            //Assert
            Assert.AreEqual(Marker.Cross, actual.Grid[x, y]);
        }

        [TestCase(1, 0, true)]
        [TestCase(0, 0, false)]
        [TestCase(2, 0, false)]
        [TestCase(5, 0, false)]
        [TestCase(2, 6, false)]
        public void IsFreeSpace_BoardAfterTwoValidMarkers_Boolean(int x, int y, bool expected)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(0, 0);
            actual.PlaceMarker(2, 0);

            //Act\Assert
            Assert.AreEqual(expected, actual.IsFreeSpace(x, y));
        }

        [TestCase(1, 0, 2)]
        [TestCase(0, 0, 3)]
        [TestCase(2, 1, 2)]
        [TestCase(1, 1, 4)]
        [TestCase(0, 2, 3)]
        public void GetLines_BoardBlank_ExpectedCount(int x, int y, int expected)
        {
            //Arrange
            var Theboard = new Board();

            //Act
            var actual = Theboard.GetLines(x, y);

            //Assert
            Assert.AreEqual(expected, actual.Count);
        }

        [TestCase(1, 0)]
        [TestCase(0, 0)]
        [TestCase(2, 1)]
        [TestCase(1, 1)]
        [TestCase(0, 2)]
        public void GetLines_BoardBlank_PointIsOnLines(int x, int y)
        {
            //Arrange
            var Theboard = new Board();

            //Act
            var actual = Theboard.GetLines(x, y);

            //Assert
            foreach (Line item in actual)
            {
                Assert.IsTrue(item.IsOnLine(x, y));
            }
        }

        [TestCase(1, 1)]
        [TestCase(0, 1)]
        [TestCase(2, 0)]
        public void IsWinningMove_BoardAfterConstructor_False(int x, int y)
        {
            //Arrange
            var actual = new Board();

            //Act
            actual.PlaceMarker(x, y);
            var actualTest = actual.IsWinningMove(x, y);

            //Assert
            Assert.AreEqual(false, actualTest);
        }

        [TestCase(0, 0, true)]
        [TestCase(1, 2, false)]
        [TestCase(2, 2, true)]
        public void IsWinningMove_BoardInWinningState_Boolean(int x, int y, bool expected)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(2, 0); // X
            actual.PlaceMarker(1, 1); // O
            actual.PlaceMarker(1, 0); // X
            actual.PlaceMarker(0, 1); // O
            actual.PlaceMarker(2, 1); // X
            actual.PlaceMarker(0, 2); // O

            //Act
            actual.PlaceMarker(x, y);
            var actualTest = actual.IsWinningMove(x, y);

            //Assert
            Assert.AreEqual(expected, actualTest);
        }

        [TestCase(0, 0)]
        public void GetWinningLine_BoardInWinningState_FirstVertical(int x, int y)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(2, 0); // X
            actual.PlaceMarker(1, 1); // O
            actual.PlaceMarker(1, 0); // X
            actual.PlaceMarker(0, 1); // O
            actual.PlaceMarker(2, 1); // X
            actual.PlaceMarker(0, 2); // O
            actual.PlaceMarker(x, y);
            var expectedLine = new Line(0, 0, 2, 0);

            //Act
            var actualTest = actual.GetWinningLine(x, y);

            //Assert
            for (int i = 0; i < expectedLine.PointsList.Count; i++)
            {
                Assert.AreEqual(expectedLine.PointsList[i].X, actualTest.PointsList[i].X);
                Assert.AreEqual(expectedLine.PointsList[i].Y, actualTest.PointsList[i].Y);
            }
        }

        [TestCase(2, 2)]
        public void GetWinningLine_BoardInWinningState_LastHorizontal(int x, int y)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(2, 0); // X
            actual.PlaceMarker(1, 1); // O
            actual.PlaceMarker(1, 0); // X
            actual.PlaceMarker(0, 1); // O
            actual.PlaceMarker(2, 1); // X
            actual.PlaceMarker(0, 2); // O
            actual.PlaceMarker(x, y);
            var expectedLine = new Line(2, 0, 2, 2);

            //Act
            var actualTest = actual.GetWinningLine(x, y);

            //Assert
            for (int i = 0; i < expectedLine.PointsList.Count; i++)
            {
                Assert.AreEqual(expectedLine.PointsList[i].X, actualTest.PointsList[i].X);
                Assert.AreEqual(expectedLine.PointsList[i].Y, actualTest.PointsList[i].Y);
            }
        }

        [TestCase(1, 2)]
        public void GetWinningLine_BoardInWinningState_Null(int x, int y)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(2, 0); // X
            actual.PlaceMarker(1, 1); // O
            actual.PlaceMarker(1, 0); // X
            actual.PlaceMarker(0, 1); // O
            actual.PlaceMarker(2, 1); // X
            actual.PlaceMarker(0, 2); // O
            actual.PlaceMarker(x, y);

            //Act
            var actualTest = actual.GetWinningLine(x, y);

            //Assert
            Assert.AreEqual(null, actualTest);
        }
        #endregion

        #region Line class
        [TestCase(0, 0, 2, 2)]
        [TestCase(0, 0, 0, 2)]
        [TestCase(0, 0, 2, 0)]
        public void StartCoordinate_Line_CorrectValues(int startx, int starty, int endx, int endy)
        {
            //Arrange\act
            var actual = new Line(startx, starty, endx, endy);

            //Assert
            Assert.AreEqual(startx, actual.PointsList[0].X);
            Assert.AreEqual(starty, actual.PointsList[0].Y);
        }

        [TestCase(0, 0, 2, 2)]
        [TestCase(0, 0, 0, 2)]
        [TestCase(0, 0, 2, 0)]
        public void EndCoordinate_Line_CorrectValues(int startx, int starty, int endx, int endy)
        {
            //Arrange\act
            var actual = new Line(startx, starty, endx, endy);

            //Assert
            Assert.AreEqual(endx, actual.PointsList[2].X);
            Assert.AreEqual(endy, actual.PointsList[2].Y);
        }

        [TestCase(0, 0, 2, 2, 1, 1)]
        [TestCase(0, 0, 0, 2, 0, 1)]
        [TestCase(0, 0, 2, 0, 1, 0)]
        public void MidCoordinate_Line_CorrectValues(int startx, int starty, int endx, int endy, int expectedX, int expectedY)
        {
            //Arrange\act
            var actual = new Line(startx, starty, endx, endy);

            //Assert
            Assert.AreEqual(expectedX, actual.PointsList[1].X);
            Assert.AreEqual(expectedY, actual.PointsList[1].Y);
        }

        [TestCase(0, 0, false)]
        [TestCase(1, 1, true)]
        [TestCase(2, 0, false)]
        [TestCase(1, 0, true)]
        [TestCase(1, 2, true)]
        public void IsOnLine_RowLine_Boolean(int x, int y, bool expected)
        {
            //Arrange
            var theLine = new Line(1, 0, 1, 2);

            //Act
            var actual = theLine.IsOnLine(x, y);

            //Assert
            Assert.AreEqual(expected, actual);
        }

        [TestCase(0, 0, false)]
        [TestCase(1, 1, true)]
        [TestCase(2, 0, true)]
        [TestCase(1, 0, false)]
        public void IsOnLine_DiagonalLine_Boolean(int x, int y, bool expected)
        {
            //Arrange
            var theLine = new Line(0, 2, 2, 0);

            //Act
            var actual = theLine.IsOnLine(x, y);

            //Assert
            Assert.AreEqual(expected, actual);
        }
        #endregion
    }
}
