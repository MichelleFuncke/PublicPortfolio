using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace Crossword
{
    public class HeaderTemp
    {
        public static String GetDefaultNumber(DependencyObject obj)
        {
            return (String)obj.GetValue(WordNumberProperty);
        }
        public static void SetDefaultNumber(DependencyObject obj, String value)
        {
            obj.SetValue(WordNumberProperty, value);
        }

        public static readonly DependencyProperty WordNumberProperty =
            DependencyProperty.RegisterAttached(
            "WordNumber",
            typeof(String),
            typeof(HeaderTemp),
            new UIPropertyMetadata(null));
    }
}
