// MoonlightStatus.aspx.cs created with MonoDevelop
// User: rhowell at 6:03 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Web;
using System.Web.UI;
using System.Collections;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;


namespace MoonlightStatus
{
	
	
	public partial class MoonlightStatus : System.Web.UI.Page
	{
		static string timeStampFile = "MoonlightStatus_timestamp";
		static string cacheFile = "MoonlightStatus_cache";
		static string url = "http://anonsvn.mono-project.com/source/trunk/moon/demo-status.txt";

        protected void Page_Load(object sender, EventArgs e)
        {
			ArrayList sites = null;
			DateTime now = DateTime.Now;
			if (GetLastUpdateTime().AddMinutes(30) > now) // If cache is newer than 30 mins, use it.
			{
				Console.WriteLine("Reading data from cache");
				sites = GetDataFromFile();
			}
			else
			{
				Console.WriteLine("Reading data from url");
				UpdateTimeStamp(now);
				sites = MoonParser.ParseURL(url);
				WriteDataToFile(sites);
				
			}
			

            string html = getHeader();
            foreach(MoonSite site in sites)
            {
                    html += site.ToHtml();
            }

            html += getFooter();

            MoonContent.InnerHtml = html;


        }

		private DateTime GetLastUpdateTime()
		{
			DateTime lastupdate = DateTime.MinValue;
			
			if (File.Exists(timeStampFile))
			{
				Console.WriteLine("Found timestamp file");
				StreamReader reader = new StreamReader(timeStampFile);
				string line = reader.ReadLine();
				reader.Close();
				line = line.Trim();
				
				lastupdate = new DateTime(Convert.ToInt64(line));
			}
			else
			{
				Console.WriteLine("no timestamp file exists");
			}
			return lastupdate;
		}
		
		private ArrayList GetDataFromFile()
		{
			ArrayList list = null;
			if (File.Exists(cacheFile))
			{
			
				FileStream reader = new FileStream(cacheFile,FileMode.Open,FileAccess.Read);
				IFormatter formatter = new BinaryFormatter();
				list = (ArrayList)formatter.Deserialize(reader);
				reader.Close();
			}
			else
			{
				//get data from url
				UpdateTimeStamp(DateTime.Now);
				list = MoonParser.ParseURL(url);
				WriteDataToFile(list);
			}
			
			return list;
			
		}
		private void WriteDataToFile(ArrayList list)
		{
			FileStream writer = new FileStream(cacheFile,FileMode.Create,FileAccess.Write,FileShare.None);
			IFormatter formatter = new BinaryFormatter();
			formatter.Serialize(writer,list);
			writer.Close();
			
		}
		private void UpdateTimeStamp(DateTime time)
		{
			StreamWriter writer = new StreamWriter(timeStampFile);
			writer.WriteLine(time.Ticks);
			writer.Close();
		}
        private string getHeader()
        {
                string html = "<table class=\"wikitable\" border=\"1\" cellpadding=\"0\">";
                html += "<tr > <th width=\"100\"> Rating </th><th width=\"200\"> Name </th><th class=\"unsortable\"";
                html += "width=\"600\"> Issues </th></tr>";


                return html;
        }
        private string getFooter()
        {
                return "</table>\n";
        }

    }

}
