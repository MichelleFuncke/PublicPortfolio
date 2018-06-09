using NUnit.Framework;
using System;
using TicTacToe;

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
            Assert.AreEqual('X', actual.Grid[x,y]);
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
            Assert.AreEqual('X', actual.Grid[x, y]);
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
            Assert.AreEqual(startx, actual.StartX);
            Assert.AreEqual(starty, actual.StartY);
        }

        [TestCase(0, 0, 2, 2)]
        [TestCase(0, 0, 0, 2)]
        [TestCase(0, 0, 2, 0)]
        public void EndCoordinate_Line_CorrectValues(int startx, int starty, int endx, int endy)
        {
            //Arrange\act
            var actual = new Line(startx, starty, endx, endy);

            //Assert
            Assert.AreEqual(endx, actual.EndX);
            Assert.AreEqual(endy, actual.EndY);
        }

        [TestCase(0, 0, 2, 2, 1, 1)]
        [TestCase(0, 0, 0, 2, 0, 1)]
        [TestCase(0, 0, 2, 0, 1, 0)]
        public void MidCoordinate_Line_CorrectValues(int startx, int starty, int endx, int endy, int expectedX, int expectedY)
        {
            //Arrange\act
            var actual = new Line(startx, starty, endx, endy);

            //Assert
            Assert.AreEqual(expectedX, actual.MidX);
            Assert.AreEqual(expectedY, actual.MidY);
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
