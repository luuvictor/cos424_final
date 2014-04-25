import java.util.HashSet;
import java.util.List;




import com.echonest.api.v4.*;
//import com.echonest.api.v4.EchoNestAPI;
//import com.echonest.api.v4.EchoNestException;

public class Scraper {

	private Out out = new Out("en_dump_5.txt");
//	private In clean_names = new In("C:\\Users\\VLuu\\Dropbox\\Programming\\EchoNestScraper\\src\\clean_names_2");
	private In clean_names = new In("/u/vluu/EchoNestScraper/src/clean_names");
	private In ignore_these = new In("/u/vluu/EchoNestScraper/ignore_these_songs");
	private EchoNestAPI en;
	private HashSet<String> ignoreSongs = new HashSet<String>();
	
	public Scraper()
	{
		String API_KEY = "E19AFIXNFW7XHERXM";
		this.en = new EchoNestAPI(API_KEY);	
		
		while (ignore_these.hasNextLine())
		{
			String[] tokens = ignore_these.readLine().split(",");
			String song = tokens[0];
			String artist = tokens[1];
			
			System.out.println(song + "\t" + artist);
			ignoreSongs.add(song);
		}
	}
	
	public void scrapeSongs() throws EchoNestException
	{
		System.out.println("song" + "," + 
				"artist" + "," +
				"dur" + "," + 
				"BPM" + "," + 
				"Mode" + "," +
				"S hot" + "," + 
				"A hot" + "," +
				"A fam" + "," +
				"A loc" + ",");
		out.println("song" + "," + 
				"artist" + "," +
				"dur" + "," + 
				"BPM" + "," + 
				"Mode" + "," +
				"S hot" + "," + 
				"A hot" + "," +
				"A fam" + "," +
				"A loc" + ",");
		while (clean_names.hasNextLine())
		{
			String line = clean_names.readLine();
			String artist = line.split("-")[0];
			String song = line.split("-")[1];
			System.err.println(artist + "\t" + song);
			
//			if (!ignoreSongs.contains(song))			
			customDumpSong_3(song, artist, 1);
//			else
//				System.out.println("HASHSETTED OUT");
		}
	}
	
	public static void main(String[] args) throws EchoNestException 
	{	  
		Scraper s = new Scraper();
		s.scrapeSongs();
		
			
	}

	public void dumpSong(Song song) throws EchoNestException {
		System.out.printf("%s\n", song.getTitle());
		System.out.printf("   artist: %s\n", song.getArtistName());
		System.out.printf("   dur   : %.3f\n", song.getDuration());
		System.out.printf("   BPM   : %.3f\n", song.getTempo());
		System.out.printf("   Mode  : %d\n", song.getMode());
		System.out.printf("   S hot : %.3f\n", song.getSongHotttnesss());
		System.out.printf("   A hot : %.3f\n", song.getArtistHotttnesss());
		System.out.printf("   A fam : %.3f\n", song.getArtistFamiliarity());
		System.out.printf("   A loc : %s\n", song.getArtistLocation());
	}	

	public void searchSongsByTitle(String title, int results)
			throws EchoNestException {
		Params p = new Params();
		p.add("title", title);
		p.add("results", results);
		List<Song> songs = en.searchSongs(p);
		for (Song song : songs) {
			dumpSong(song);
			System.out.println();
		}
	}
	
	public void searchSongsByTitle(String title, String artist, int results)
			throws EchoNestException {
		
		
	}

	private void customDumpSong_2(String title, String artist, int results) {
		try {
			Params p = new Params();
			p.add("title", title);
			p.add("results", results);
			p.add("artist", artist);
			List<Song> songs = en.searchSongs(p);
			System.out.print(title + "|" + artist + "|");
			out.print(title + "," + artist);
			assert(songs.size() <= results);
			for (Song song : songs) {

				System.out.print(song.getDanceability()
						+ "|" + song.getEnergy()
						+ "|" + song.getKey()
						+ "|" + song.getLoudness()
						+ "|" + song.getArtistFamiliarity() 
						+ "|" + song.getCoverArt());
				System.out.println();
				out.print(song.getDanceability()
						+ "|" + song.getEnergy()
						+ "|" + song.getKey()
						+ "|" + song.getLoudness()
						+ "|" + song.getArtistFamiliarity() 
						+ "|" + song.getCoverArt());
				out.println();				
			}
			if (songs.size() == 0)
			{
				System.out.println(",EMPTY!");
				out.println(",EMPTY!");
			}		
		}
		catch (EchoNestException e) {
			System.out.println(e.getMessage());
			System.out.println("sleeping...");
			
			out.println(e.getMessage());
			out.println("sleeping...");			
			
			try {
			Thread.sleep(60 * 1000);
			}
			catch (Exception io)
			{
				System.out.println("lol gg");
			}
			
			System.out.println("try again...");
			out.println("try again");
			customDumpSong_2(title, artist, results);
		}
	}
	
	private void customDumpSong_3(String title, String artist, int results) {
		try {
			Params p = new Params();
			p.add("title", title);
			p.add("results", results);
			p.add("artist", artist);
			List<Song> songs = en.searchSongs(p);
			System.out.print(title + "|" + artist + "|");
			out.print(title + "," + artist);
			assert(songs.size() <= results);
			for (Song song : songs) 
			{
				System.out.print("|" + song.getSongHotttnesss());
				out.println("|" + song.getSongHotttnesss());
			}
			if (songs.size() == 0)
			{
				System.out.println("|EMPTY!");
				out.println("|EMPTY!");
			}		
		}
		catch (EchoNestException e) {
			System.out.println(e.getMessage());
			System.out.println("sleeping...");
			
			out.println(e.getMessage());
			out.println("sleeping...");			
			
			try {
			Thread.sleep(60 * 1000);
			}
			catch (Exception io)
			{
				System.out.println("lol gg");
			}
			
			System.out.println("try again...");
			out.println("try again");
			customDumpSong_3(title, artist, results);
		}
	}
	
	private void customDumpSong(String title, String artist, int results) {
		try {			
			Params p = new Params();
			p.add("title", title);
			p.add("results", results);
			p.add("artist", artist);
			List<Song> songs = en.searchSongs(p);
			System.out.print(title + "," + artist);
			out.print(title + "," + artist);
			assert(songs.size() <= results);
			for (Song song : songs) {

				System.out.print(song.getTitle()
						+ "," + song.getArtistName()
						+ "," + song.getDuration()
						+ "," + song.getTempo()
						+ "," + song.getMode()
						+ "," + song.getSongHotttnesss()
						+ "," + song.getArtistFamiliarity()
						+ "," + song.getArtistLocation());
				System.out.println();
				out.println(song.getTitle()
						+ "," + song.getArtistName()
						+ "," + song.getDuration()
						+ "," + song.getTempo()
						+ "," + song.getMode()
						+ "," + song.getSongHotttnesss()
						+ "," + song.getArtistFamiliarity()
						+ "," + song.getArtistLocation());
				out.println();				
			}
			if (songs.size() == 0)
			{
				System.out.println(",EMPTY!");
				out.println(",EMPTY!");
			}		
		}
		catch (EchoNestException e) {
			System.out.println(e.getMessage());
			System.out.println("sleeping...");
			
			out.println(e.getMessage());
			out.println("sleeping...");			
			
			try {
			Thread.sleep(60 * 1000);
			}
			catch (Exception io)
			{
				System.out.println("lol gg");
			}
			
			System.out.println("try again...");
			out.println("try again");
			customDumpSong(title, artist, results);
		}
	}
	
	//logic - "catch a LIMIT REACHED", and respond by waiting for 60 seconds, or, i.e. calling the method again
	//output everything on the same line, if you hit an exception, PRINT OUT THAT, and call again, to write on a new line	
}
