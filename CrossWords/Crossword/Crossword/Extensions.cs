using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace Crossword
{
    public static class Extensions
    {
        public static void MySort(this ObservableCollection<PuzzleWord> collection)
        {
            var temp = collection.OrderBy(p => (p.ClueNumber - (p.WordDirection == Direction.across ? 100 : 0))).ToList();

            collection.Clear();
            foreach (var b in temp)
            {
                collection.Add(b);
            }
        }

        public static void ReadPuzzle(FileInfo file)
        {
            
        }


    }
}
