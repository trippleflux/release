//
// Moma Report Generator
//
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;

public class Flags {
	public const int TODO = 1;
	public const int MISS = 2;
	public const int NIEX = 4;
	public const int PINV = 8;
}

class Moma  {
	public static Dictionary<string,int> API = new Dictionary<string, int> ();
	public static Dictionary<string,object> Valid = new Dictionary<string,object> ();
	public static Hashtable Invalid = new Hashtable ();
	public static Dictionary<string,string> TodoExplanation = new Dictionary<string, string> ();
	static StreamWriter sw;
	public static string outputdir;

	public static void LoadTodoExplanations (string fname)
	{
		using (FileStream fs = File.OpenRead (fname)){
			StreamReader sr = new StreamReader (fs);
			string s;

			while ((s = sr.ReadLine ()) != null){
				int p = s.IndexOf ('-');
				TodoExplanation [s.Substring (0, p)] = s.Substring (p + 1);
			}
		}
	}
	
	public static void Load (string fname, int kind)
	{
		using (FileStream fs = File.OpenRead (fname)){
			StreamReader sr = new StreamReader (fs);
			string s;

			while ((s = sr.ReadLine ()) != null){
				if (API.ContainsKey (s))
					API [s] = API [s] | kind;
				else
					API [s] = kind;
			}
		}
	}

	public static void LoadPublic ()
	{
		using (FileStream fs = File.OpenRead ("all.txt")){
			StreamReader sr = new StreamReader (fs);
			string s;

			while ((s = sr.ReadLine ()) != null){
				Valid [s] = s;
			}
		}
	}
	
	static string CleanHTML (string s)
	{
		return s.Replace ("<", "&lt;").Replace (">", "&gt;").Replace ("&", "&amp;");
	}
	       
	public static void p (string format, params object [] args)
	{
		sw.WriteLine (String.Format (format, args));
	}

	public static void concat (string fname)
	{
		using (FileStream fs = File.OpenRead (fname)){
			StreamReader sr = new StreamReader (fs);
			sw.Write (sr.ReadToEnd ());
			sr.Close ();
		}
	}

	static void Main (string [] args)
	{
		if (args.Length < 3){
			Console.WriteLine ("rgen ReportDirs ApiDir Output");
			Console.WriteLine ("example:\n");
			Console.WriteLine ("   rgen Reports 1.2.4 output");
			return;
		}

		Console.Write ("Loading public API... ");
		LoadPublic ();
		Console.WriteLine ("done");
		
		Console.Write ("Loading definitions... ");
		Load (Path.Combine (args [1], "todo.txt"), 1);
		Load (Path.Combine (args [1], "missing.txt"), 2);
		Load (Path.Combine (args [1], "exception.txt"), 4);
		LoadTodoExplanations (Path.Combine (args [1], "monotodo.txt"));
		Console.WriteLine ("done");

		outputdir = args [2];
		if (!Directory.Exists (outputdir)){
			try {
				Directory.CreateDirectory (outputdir);
			} catch {
				Console.Error.WriteLine ("Failed to create directory {0}", outputdir);
				return;
			}
		}
		
		if (File.Exists (Path.Combine (outputdir, "index.html"))){
			Console.Error.WriteLine ("File index.html exists in the target directory");
			return;
		}
		File.Copy ("moma.css", Path.Combine (outputdir, "moma.css"));
		
		sw = new StreamWriter (File.OpenWrite (Path.Combine (outputdir, "index.html")));

		Console.WriteLine ("Loaded {0} API definitions", API.Count);

		Console.Write ("Loading reports... ");
		string [] files = Directory.GetFiles (args [0], "*.txt");
		ArrayList reports = new ArrayList ();

		//files = new string []  { "/home/miguel/Results/Fresh/647a1dd1ab0546b0abfcd92127292c72.txt" };
		
		foreach (string f in files){
		
			// Ignore all the junk temporary files I have lying around
			if (Path.GetFileName (f).Length < 20)
				continue;

			Report r = null;
			try {
				r = new Report (f);
			} catch (Exception e) {
				Console.WriteLine ("Error on {0} {1}", f, e);
				return;
			}

			//if (reports.Count == 100)
			//break;
			
			reports.Add (r);
		}
		Console.WriteLine ("done");
		Console.WriteLine ("{0} API entry points", Report.GlobalApi.Count);
		Console.WriteLine ("{0} reports loaded", reports.Count);

#if false
		foreach (string s in Report.GlobalApi.Keys){
			int v = Report.GlobalApi [s];
			
			Console.WriteLine ("{0:x} {1} {2}", v >> 24, v & 0xffffff, s);
		}
#endif

		Console.Write ("Generating report... ");
		concat ("head");

		reports.Sort (Report.date_sorter);
		
		foreach (Report r in reports){
			if (r.invalid > 0)
				p ("<div class=\"subinvalid\">");
			else 
				p ("<div class=\"sub\">");
			p ("<div class='col1'>");
			p ("<p><b>Definitions:</b> {0}</p>", r.Definitions);
			p ("</div><div class='col2'>");
			p ("<p align='right'><b>Date:</b> {0}</p>", r.Date.Substring (0, r.Date.IndexOf (' ')));
			p ("</div>");
			if (r.Comments.Length > 0)
				p ("<p><b>Comments:</b> {0}</p>", CleanHTML (r.Comments));
			p ("<p align=\"right\"><b><a href=\"{0}\">Report</a></b><br>", r.Name);

			r.DumpStats (outputdir);
			p ("</div>");
		}
		p ("</div>");

		concat ("side");
		p ("<b>Submissions:</b> {0}", reports.Count);
		p ("<p><b>Totals:</b>");
		p ("<ul style=\"list-style-type: none;\">");
		p ("<li><a href='f-MISS.txt'>Missing</a>");
		p ("<li><a href='f-NIEX.txt'>Throw NotImplemented</a>");
		p ("<li><a href='f-TODO.txt'>TODO/Pending</a>");
		concat ("end");

		sw.Close ();

		//
		// Now render the total needs
		//
		GenerateStats (Flags.MISS, Path.Combine (outputdir, "f-MISS.txt"), "missing/not-present in Mono today");
		GenerateStats (Flags.TODO, Path.Combine (outputdir, "f-TODO.txt"), "methods flagged as TODO");
		GenerateStats (Flags.NIEX, Path.Combine (outputdir, "f-NIEX.txt"), "throwing NotImplementedException");
		Console.WriteLine ("done");

		DumpInvalid ();
	}

	static void DumpInvalid ()
	{
		using (FileStream fs = File.OpenWrite ("generated-invalid.txt")){
			using (StreamWriter sw = new StreamWriter (fs)){
				
				foreach (string invalid in Invalid.Keys){
					sw.WriteLine (invalid);
				}
			}
		}
	}
	
	static void GenerateStats (int flag, string fname, string caption)
	{
		using (FileStream fs = File.OpenWrite (fname)){
			using (StreamWriter sw = new StreamWriter (fs)){

				// Currently broken
				//
				// I should recompute the tables after I have "upgraded"
				// the data to what is actually implemented, instead of
				// depending on the data from the raw reports
				//
				SortedDictionary<string,int> table = new SortedDictionary<string,int> (new Report.CountSorter ());
		
				foreach (string gapi in Report.GlobalApi.Keys){
					int n, k;

					n = Report.GlobalApi [gapi];
					if ((n >> 24) == flag){
						table [gapi] = n & 0xffffff;
					}
				}

				sw.WriteLine ("Total counts for {0} APIs = {1}\n", caption, table.Keys.Count);
				sw.WriteLine ("The numbers represent the number of applications depending on a given feature\n\n");

				foreach (string s in table.Keys){
					int p = s.IndexOf (' ');
					sw.WriteLine ("  {0,6} {1}", table [s], s.Substring (p + 1));

					// Be a bit more useful in TODO reports
					if (flag == Flags.TODO){
						sw.WriteLine ("         Details: {0}", TodoExplanation [s]);
						sw.WriteLine ();
					}
				}
			}
		}
	}
}

public class Report {
	Dictionary <string,string> meta = new Dictionary<string,string>();
	Dictionary <string,int> local;
	public static Dictionary <string,int> GlobalApi = new Dictionary<string,int> ();
	public string Date;
	public DateTime DateParsed;
	public string Ip;
	public string Definitions;
	public string Name;
	public string Comments;
	int change;
	public int invalid;
	Hashtable implemented = new Hashtable ();
	
	public static IComparer date_sorter = new DateSorter ();

	public class CountSorter : IComparer<string> {
		public int Compare (string x, string y)
		{
			int xn, yn;
			
			xn = GlobalApi [x];
			yn = GlobalApi [y];

			int d = (yn & 0xffffff) - (xn & 0xffffff);
			if (d != 0)
				return d;
			return y.CompareTo (x);
		}
	}
	
	class DateSorter : IComparer {
		public int Compare (object x, object y)
		{
			return ((Report) y).DateParsed.CompareTo (((Report)x).DateParsed);
		}
	}
	
	class CountCompare : IComparer {
		Report r;
		
		public CountCompare (Report r)
		{
			this.r = r;
		}
		
		public int Compare (object x, object y)
		{
			int xn = r.local [(string) x];
			int yn = r.local [(string) y];

			int d = (yn & 0xffffff) - (xn & 0xffffff);
			if (d != 0)
				return d;

			return ((string) y).CompareTo (x);
		}
	}

	class PInvokeCompare : IComparer {

		// Some PINV declarations contain newlines in their definitions, skip if we fail
		public int Compare (object x, object y)
		{
			string sx = (string) x;
			int px = sx.IndexOf ('-');
			if (px == -1)
				return 0;
			
			string libx = sx.Substring (px+1);

			string sy = (string) y;
			int py = sy.IndexOf ('-');
			if (py == -1)
				return 0;
			string liby = sy.Substring (py+1);

			int c = libx.CompareTo (liby);
			if (c != 0)
				return c;

			string apix = "";
			try {
				apix = sx.Substring (0, px);
			} catch {
				Console.WriteLine ("Got [{0}] and {1}", sx, px);
			}
			string apiy = sy.Substring (0, py);

			return apix.CompareTo (apiy);
		}
	}
	
	PInvokeCompare pinvoke_compare = new PInvokeCompare();

	public Report (string f)
	{
		local = new Dictionary <string,int> ();

		Name = Path.GetFileName (f);
		using (FileStream fs = File.OpenRead (f)){
			StreamReader sr = new StreamReader (fs);

			Date = sr.ReadLine ();
			DateParsed = DateTime.Parse (Date);
			Ip = sr.ReadLine ();
			
			string r = ReadMeta (sr);

			Definitions = meta ["@Definitions"];
			Comments = meta ["@Comments"];
			
			for (; r != null && r.Length > 6; r = sr.ReadLine ()) {
				int ikind = 0;

				if (r [r.Length-1] == '\r')
					r = r.Substring (0, r.Length-1);

				switch (r.Substring (0, 6)){
				case "[TODO]": ikind = Flags.TODO; break;
				case "[NIEX]": ikind = Flags.NIEX; break;
				case "[MISS]": ikind = Flags.MISS; break;
				case "[PINV]": ikind = Flags.PINV; break;
				}
				string rest = r.Substring (7);

				if (rest.IndexOf (".Design") != -1){
					if (rest.IndexOf ("System.ComponentModel.Design") != -1 ||
					    rest.IndexOf ("System.Web.UI.Design") != -1 ||
					    rest.IndexOf ("System.Drawing.Design") != -1 ||
					    rest.IndexOf ("System.Data.Design") != -1 ||
					    rest.IndexOf ("System.Windows.Forms.Design") != -1)
						continue;
					    
				}

				//
				// If the API is not registered in the latest
				// API tables, do not register it, it means it
				// has been taken care of.
				//
				int n;
				if (ikind != Flags.PINV){
					if (!Moma.API.TryGetValue (rest, out n)){
						change++;
						if (!implemented.Contains (rest))
							implemented [rest] = rest;
						
						continue;
					}
					object obj;
					
					if (!Moma.Valid.TryGetValue (rest, out obj)){
						invalid++;
						if (!Moma.Invalid.Contains (rest))
							Moma.Invalid [rest] = Moma.Invalid;
						continue;
					}
				}

				ikind = ikind << 24;
				
				if (!Register (local, ikind, rest)){

					// Only count individual uses at the global level
					Register (GlobalApi, ikind, rest);
				}
			}
		}
	}

	//
	// Registers the given API string @rest with type @ikind on the
	// table called @api.
	//
	// Returns true if this was already registered
	//
	bool Register (Dictionary<string,int> api, int ikind, string rest)
	{
		if (api.ContainsKey (rest)){
			int v = api [rest];
			
			api [rest] = (ikind | (v & 0x7f000000)) |
				((v & 0xffffff) + 1);
			return true;
		} else {
			api [rest] = ikind + 1;
			return false;
		}
	}

	//
	// Reads the line that start with @ and sticks them in the metadata
	// dictionary.  Other entries (the ones that start with [ are returned
	// for processing
	//
	string ReadMeta (StreamReader sr)
	{
		string s;

		while ((s = sr.ReadLine ()) != null){
			if (s.Length == 0 || s [0] == '[')
				return s;

			if (s [0] != '@')
				return s;
			
			int p = s.IndexOf (':');
			string v = s.Substring (p + 2);
			meta [s.Substring (0,p)] = v;
		}
		return s;
	}

	void p (StreamWriter sw, string format, params object [] args)
	{
		sw.WriteLine (String.Format (format, args));
	}

	static string map (int n)
	{
		// In order of usefulness in the report.
		
		if ((n & Flags.MISS) != 0)
			return "MISS";
		if ((n & Flags.NIEX) != 0)
			return "NIEX";
		if ((n & Flags.TODO) != 0)
			return "TODO";

		return "UNKN";
	}
	public void DumpStats (string outputdir)
	{
		int todo = 0, miss = 0, niex = 0, pinv = 0;

		ArrayList pinvokes = new ArrayList ();
		ArrayList issues = new ArrayList ();
		
		using (FileStream fs = File.OpenWrite (Path.Combine (outputdir, Name))){
			StreamWriter rw = new StreamWriter (fs);

			rw.WriteLine ("Definitions: {0}", Definitions);
			rw.WriteLine ("Date Submitted: {0}", Date);
			rw.WriteLine ("Comments: {0}", Comments);
			rw.WriteLine ("=========================================");
			rw.WriteLine ("");
			
			foreach (string apicall in local.Keys){
				int k;
				int c;
				
				c = local [apicall];
				if ((c & (8 << 24)) != 0){
					pinv++;
					pinvokes.Add (apicall);
				} else {
					if (Moma.API.TryGetValue (apicall, out k)){
						if ((k & Flags.TODO) != 0)
							todo++;
						else if ((k & Flags.MISS) != 0)
							miss++;
						else if ((k & Flags.NIEX) != 0)
							niex++;

						issues.Add (apicall);
					} 
				}
			}

			if (issues.Count > 0){
				p (rw, "");
				p (rw, "Pending issues:");

				issues.Sort (new CountCompare (this));
				foreach (string s in issues){
					int n;

					//
					// If its listed on the API file, use the info from that
					// file, instead of the one that was submitted
					//
					if (!Moma.API.TryGetValue (s, out n))
						n = local [s];
					
					p (rw, " {0,4}  [{1}] {2}", n & 0xffffff, map (n), s.Substring (s.IndexOf (' ')+1));

					// If it is a todo, add the annotation of what the message is
					if ((n & Flags.TODO) != 0){
						p (rw, "              Details: {0}", Moma.TodoExplanation [s]);
					}
				}
			}
			
			if (pinvokes.Count > 0){
				p (rw, "");
				p (rw, "****************************************************");
				p (rw, "P/Invokes made by this program");
				try {
				pinvokes.Sort (pinvoke_compare);
				} catch {
					Console.WriteLine ("On report {0}",Name);
				}
				string clib = "";
				
				foreach (string s in pinvokes){
					int pos = s.IndexOf ('-');
					if (pos == -1)
						pos = 0;
					string lib = s.Substring (pos + 1);

					if (lib != clib){
						p (rw, "");
						p (rw, "   Library: {0}", lib);
						clib = lib;
					}
					p (rw, "       {0}", s.Substring (0, pos));
				}
			}

			if (implemented.Count > 0){
				p (rw, "");
				p (rw, "****************************************************");
				p (rw, "Methods that have been implemented:");
				foreach (string s in implemented.Keys)
					p (rw, "   {0}", s.Substring (s.IndexOf (' ')+1));

			}
			rw.Flush ();
		}

		//
		// Summary
		//
		if (miss == 0 && niex == 0 && todo == 0){
			if (pinv == 0)
				Moma.p ("<b>All done</b>");
			else
				Moma.p ("<b>Only P/Invokes pending</b>");
			Moma.p ("<br>");
		}
		if (invalid == 0){
			Console.WriteLine ("SS: {0} {1} {2} {3} {4} {5}", miss == 0 && niex == 0 ? "GO" : "NG", miss, niex, todo, pinv,
					   meta["@Email"].IndexOf ("@") != -1);
		}
		if (miss != 0)
			Moma.p ("{0} miss.", miss);
		if (niex != 0)
			Moma.p ("{0} niex.", niex);
		if (todo != 0)
			Moma.p ("{0} todo.", todo);
		if (pinv != 0)
			Moma.p ("{0} pinv.", pinv);
		if (change != 0)
			Moma.p ("<span style='color: #0a0;'>change: {0}</span>", change);
		if (invalid != 0)
			Moma.p ("<span style='color: #a00;'>invalid: {0}</span>", invalid);
	}
}
