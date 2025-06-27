/*
 * $Id: readfile.c 21901 2009-07-25 21:31:17Z blendix $
 *
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * The Original Code is Copyright (C) 2001-2002 by NaN Holding BV.
 * All rights reserved.
 *
 *
 * Contributor(s): Blender Foundation
 *
 * ***** END GPL LICENSE BLOCK *****
 *
 */
package blender.blenloader;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.net.URI;
import java.net.URL;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.GZIPInputStream;

import blender.blenkernel.CustomDataUtil;
import blender.blenkernel.LibraryUtil;
import blender.blenkernel.Main;
import blender.blenkernel.UtilDefines;
import blender.blenlib.ListBaseUtil;
import blender.blenlib.Rct;
import blender.blenlib.StringUtil;
import blender.makesdna.CustomDataTypes;
import blender.makesdna.DNAGenfile;
import blender.makesdna.DNA_ID;
import blender.makesdna.ObjectTypes;
import blender.makesdna.ScreenTypes;
import blender.makesdna.SpaceTypes;
import blender.makesdna.TextureTypes;
import blender.makesdna.SDNATypes.BHead;
import blender.makesdna.SDNATypes.BHeadN;
import blender.makesdna.SDNATypes.SDNA;
import blender.makesdna.sdna.ARegion;
import blender.makesdna.sdna.AnimData;
import blender.makesdna.sdna.AviCodecData;
import blender.makesdna.sdna.BGpic;
import blender.makesdna.sdna.Base;
import blender.makesdna.sdna.BoundBox;
import blender.makesdna.sdna.BulletSoftBody;
import blender.makesdna.sdna.Camera;
import blender.makesdna.sdna.CurveMapping;
import blender.makesdna.sdna.CustomData;
import blender.makesdna.sdna.CustomDataLayer;
import blender.makesdna.sdna.DNA;
import blender.makesdna.sdna.DNATools;
import blender.makesdna.sdna.Editing;
import blender.makesdna.sdna.FileGlobal;
import blender.makesdna.sdna.FluidsimSettings;
import blender.makesdna.sdna.Group;
import blender.makesdna.sdna.GroupObject;
import blender.makesdna.sdna.ID;
import blender.makesdna.sdna.IDProperty;
import blender.makesdna.sdna.Image;
import blender.makesdna.sdna.Lamp;
import blender.makesdna.sdna.Library;
import blender.makesdna.sdna.Link;
import blender.makesdna.sdna.ListBase;
import blender.makesdna.sdna.MCol;
import blender.makesdna.sdna.MDeformVert;
import blender.makesdna.sdna.MDeformWeight;
import blender.makesdna.sdna.MDisps;
import blender.makesdna.sdna.MEdge;
import blender.makesdna.sdna.MFace;
import blender.makesdna.sdna.MSticky;
import blender.makesdna.sdna.MTFace;
import blender.makesdna.sdna.MTex;
import blender.makesdna.sdna.MVert;
import blender.makesdna.sdna.Material;
import blender.makesdna.sdna.Mesh;
import blender.makesdna.sdna.MetaStack;
import blender.makesdna.sdna.PackedFile;
import blender.makesdna.sdna.Panel;
import blender.makesdna.sdna.PartDeflect;
import blender.makesdna.sdna.PartEff;
//import blender.makesdna.sdna.PartialVisibility;
import blender.makesdna.sdna.PointCache;
import blender.makesdna.sdna.PreviewImage;
import blender.makesdna.sdna.QuicktimeCodecData;
import blender.makesdna.sdna.RegionView3D;
import blender.makesdna.sdna.ReportList;
import blender.makesdna.sdna.SBVertex;
import blender.makesdna.sdna.Scene;
import blender.makesdna.sdna.SceneRenderLayer;
import blender.makesdna.sdna.ScrArea;
import blender.makesdna.sdna.ScrEdge;
import blender.makesdna.sdna.ScrVert;
import blender.makesdna.sdna.Script;
import blender.makesdna.sdna.Sculpt;
import blender.makesdna.sdna.Sequence;
import blender.makesdna.sdna.SoftBody;
import blender.makesdna.sdna.SpaceAction;
import blender.makesdna.sdna.SpaceButs;
import blender.makesdna.sdna.SpaceConsole;
import blender.makesdna.sdna.SpaceFile;
//import blender.makesdna.sdna.SpaceImaSel;
import blender.makesdna.sdna.SpaceImage;
import blender.makesdna.sdna.SpaceInfo;
import blender.makesdna.sdna.SpaceIpo;
import blender.makesdna.sdna.SpaceLink;
import blender.makesdna.sdna.SpaceLogic;
import blender.makesdna.sdna.SpaceNla;
import blender.makesdna.sdna.SpaceNode;
import blender.makesdna.sdna.SpaceOops;
import blender.makesdna.sdna.SpaceScript;
import blender.makesdna.sdna.SpaceSeq;
//import blender.makesdna.sdna.SpaceSound;
import blender.makesdna.sdna.SpaceText;
import blender.makesdna.sdna.TFace;
import blender.makesdna.sdna.Tex;
import blender.makesdna.sdna.Text;
import blender.makesdna.sdna.ToolSettings;
import blender.makesdna.sdna.TreeStore;
import blender.makesdna.sdna.TreeStoreElem;
import blender.makesdna.sdna.UserDef;
import blender.makesdna.sdna.VPaint;
import blender.makesdna.sdna.View3D;
import blender.makesdna.sdna.World;
import blender.makesdna.sdna.bAction;
import blender.makesdna.sdna.bActuator;
import blender.makesdna.sdna.bController;
import blender.makesdna.sdna.bDopeSheet;
import blender.makesdna.sdna.bGPdata;
import blender.makesdna.sdna.bObject;
import blender.makesdna.sdna.bPose;
import blender.makesdna.sdna.bProperty;
import blender.makesdna.sdna.bScreen;
import blender.makesdna.sdna.bSensor;
import blender.makesdna.sdna.bSound;
import blender.makesdna.sdna.wmWindow;
import blender.makesdna.sdna.wmWindowManager;

public class ReadFile {
	
// only used here in readfile.c
public static final long SWITCH_LONGINT(long a) {
//	byte s_i, *p_i;
//	p_i= (char *)&(a);
//	s_i=p_i[0]; p_i[0]=p_i[7]; p_i[7]=s_i;
//	s_i=p_i[1]; p_i[1]=p_i[6]; p_i[6]=s_i;
//	s_i=p_i[2]; p_i[2]=p_i[5]; p_i[5]=s_i;
//	s_i=p_i[3]; p_i[3]=p_i[4]; p_i[4]=s_i;
	
	return a&0xFFL | a&0xFF00L | a&0xFF0000L | a&0xFF000000L | a&0xFF00000000L | a&0xFF0000000000L | a&0xFF000000000000L | a&0xFF00000000000000L;
}

public static interface FDRead {
    public int run(FileData filedata, byte[] buffer, int size);
};

public static final int EOF = -1;

//typedef enum BlenFileType {
//	BLENFILETYPE_BLEND= 1,
//	BLENFILETYPE_PUB= 2,
//	BLENFILETYPE_RUNTIME= 3
//} BlenFileType;

public static class BlendFileData {
	public Main	main;
	public UserDef	user;

	public int winpos;
	public int fileflags;
	public int displaymode;
	public int globalf;

	public bScreen	curscreen;
	public Scene	curscene;

//	public BlenFileType	type;
};

public static class FileData {
	// linked list of BHeadN's
	public ListBase<BHeadN> listbase = new ListBase<BHeadN>();
	public int flags;
	public int eof;
	public int buffersize;
	public int seek;
	public FDRead read;

	// variables needed for reading from memory / stream
//	public char *buffer;
	// variables needed for reading from memfile (undo)
//	public struct MemFile *memfile;

	// variables needed for reading from file
//	public int filedes;
        public int filedes;
//	public gzFile gzfiledes;
        public ByteBuffer gzfiledes;

	// now only in use for library appending
//	public char filename[FILE_MAXDIR+FILE_MAXFILE];
        public String filename;

	// variables needed for reading from stream
	public char headerdone;
	public int inbuffer;

	// general reading variables
	public SDNA filesdna;
	public SDNA memsdna;
	public byte[] compflags;

	public int fileversion;
	public int id_name_offs;		/* used to retrieve ID names from (bhead+1) */

	public OldNewMap datamap;
	public OldNewMap globmap;
	public OldNewMap libmap;
	public OldNewMap imamap;

//	public struct bheadsort *bheadmap;
//	public int tot_bheadmap;

	public ListBase<Main> mainlist = new ListBase<Main>();

		/* ick ick, used to return
		 * data through streamglue.
		 */
//	public BlendFileData **bfd_r;
//	public struct ReportList *reports;
};

//public static class BHeadN extends Link<BHeadN> {
//	public BHead bhead;
//        public ByteBuffer data;
//        public BHeadN(int size, BHead bh) {
//            bhead = bh;
//            bhead.bheadN = this;
//            data = ByteBuffer.allocate(size);
//        }
//};


public static final int FD_FLAGS_SWITCH_ENDIAN=         (1<<0);
public static final int FD_FLAGS_FILE_POINTSIZE_IS_4=   (1<<1);
public static final int FD_FLAGS_POINTSIZE_DIFFERS=     (1<<2);
public static final int FD_FLAGS_FILE_OK=               (1<<3);
public static final int FD_FLAGS_NOT_MY_BUFFER=		(1<<4);
public static final int FD_FLAGS_NOT_MY_LIBMAP=		(1<<5);

public static final int SIZEOFBLENDERHEADER= 12;

///*
// Remark: still a weak point is the newadress() function, that doesnt solve reading from
// multiple files at the same time
//
// (added remark: oh, i thought that was solved? will look at that... (ton)
//
//READ
//- Existing Library (Main) push or free
//- allocate new Main
//- load file
//- read SDNA
//- for each LibBlock
//	- read LibBlock
//	- if a Library
//		- make a new Main
//		- attach ID's to it
//	- else
//		- read associated 'direct data'
//		- link direct data (internal and to LibBlock)
//- read FileGlobal
//- read USER data, only when indicated (file is ~/.B.blend or .B25.blend)
//- free file
//- per Library (per Main)
//	- read file
//	- read SDNA
//	- find LibBlocks and attach IDs to Main
//		- if external LibBlock
//			- search all Main's
//				- or it's already read,
//				- or not read yet
//				- or make new Main
//	- per LibBlock
//		- read recursive
//		- read associated direct data
//		- link direct data (internal and to LibBlock)
//	- free file
//- per Library with unread LibBlocks
//	- read file
//	- read SDNA
//	- per LibBlock
//               - read recursive
//               - read associated direct data
//               - link direct data (internal and to LibBlock)
//        - free file
//- join all Mains
//- link all LibBlocks and indirect pointers to libblocks
//- initialize FileGlobal and copy pointers to Global
//*/
//
///* also occurs in library.c */
///* GS reads the memory pointed at in a specific ordering. There are,
// * however two definitions for it. I have jotted them down here, both,
// * but I think the first one is actually used. The thing is that
// * big-endian systems might read this the wrong way round. OTOH, we
// * constructed the IDs that are read out with this macro explicitly as
// * well. I expect we'll sort it out soon... */
//
///* from blendef: */
//#define GS(a)	(*((short *)(a)))
//
///* from misc_util: flip the bytes from x  */
///*  #define GS(x) (((unsigned char *)(x))[0] << 8 | ((unsigned char *)(x))[1]) */
//
//// only used here in readfile.c
//#define SWITCH_LONGINT(a) { \
//    char s_i, *p_i; \
//    p_i= (char *)&(a);  \
//    s_i=p_i[0]; p_i[0]=p_i[7]; p_i[7]=s_i; \
//    s_i=p_i[1]; p_i[1]=p_i[6]; p_i[6]=s_i; \
//    s_i=p_i[2]; p_i[2]=p_i[5]; p_i[5]=s_i; \
//    s_i=p_i[3]; p_i[3]=p_i[4]; p_i[4]=s_i; }

/***/

public static class OldNew {
//	public void *old, *newp;
        public int old;
        public Object newp;
	public int nr;
};

public static class OldNewMap {
//	public OldNew[] entries;
        public List<OldNew> entries;
	public int nentries, entriessize;
	public int sorted;
	public int lasthit;
};

public static OldNewMap oldnewmap_new()
{
	OldNewMap onm= new OldNewMap();

	onm.entriessize= 1024;
//	onm.entries= MEM_mallocN(sizeof(*onm.entries)*onm.entriessize, "OldNewMap.entries");
//        onm.entries= new OldNew[onm.entriessize];
        onm.entries= new ArrayList(onm.entriessize);

	return onm;
}

//static int verg_oldnewmap(const void *v1, const void *v2)
//{
//	const struct OldNew *x1=v1, *x2=v2;
//
//	if( x1.old > x2.old) return 1;
//	else if( x1.old < x2.old) return -1;
//	return 0;
//}
//
//
//static void oldnewmap_sort(FileData *fd)
//{
//	qsort(fd.libmap.entries, fd.libmap.nentries, sizeof(OldNew), verg_oldnewmap);
//	fd.libmap.sorted= 1;
//}

/* nr is zero for data, and ID code for libdata */
public static void oldnewmap_insert(OldNewMap onm, int oldaddr, Object newaddr, int nr)
{
	OldNew entry;

	if(oldaddr==0 || newaddr==null) return;

//	if (onm.nentries==onm.entriessize) {
//		int osize= onm.entriessize;
//		OldNew *oentries= onm.entries;
//
//		onm.entriessize*= 2;
//		onm.entries= MEM_mallocN(sizeof(*onm.entries)*onm.entriessize, "OldNewMap.entries");
//
//		memcpy(onm.entries, oentries, sizeof(*oentries)*osize);
//		MEM_freeN(oentries);
//	}

//	entry= &onm.entries[onm.nentries++];
    entry = new OldNew();
    onm.entries.add(onm.nentries++, entry);
	entry.old= oldaddr;
	entry.newp= newaddr;
	entry.nr= nr;
}

public static Object oldnewmap_lookup_and_inc(OldNewMap onm, int addr)
{
	int i;

//	if (onm.lasthit<onm.nentries-1) {
//		OldNew *entry= &onm.entries[++onm.lasthit];
//
//		if (entry.old==addr) {
//			entry.nr++;
//			return entry.newp;
//		}
//	}

	for (i=0; i<onm.nentries; i++) {
		OldNew entry= onm.entries.get(i);

		if (entry.old==addr) {
			onm.lasthit= i;

			entry.nr++;
			return entry.newp;
		}
	}

	return null;
}

/* for libdata, nr has ID code, no increment */
public static ID oldnewmap_liblookup(OldNewMap onm, int addr, Object lib)
{
	int i;

	if(addr==0) return null;

//	/* lasthit works fine for non-libdata, linking there is done in same sequence as writing */
//	if(onm.sorted) {
//		OldNew entry_s, *entry;
//
//		entry_s.old= addr;
//
//		entry= bsearch(&entry_s, onm.entries, onm.nentries, sizeof(OldNew), verg_oldnewmap);
//		if(entry) {
//			ID *id= entry.newp;
//
//			if (id && (!lib || id.lib)) {
//				return entry.newp;
//			}
//		}
//	}

	for (i=0; i<onm.nentries; i++) {
		OldNew entry= onm.entries.get(i);

		if (entry.old==addr) {
			ID id= (ID)entry.newp;

			if (id!=null && (lib==null || id.lib!=null)) {
				return (ID)entry.newp;
			}
		}
	}

	return null;
}
//
//static void oldnewmap_free_unused(OldNewMap *onm)
//{
//	int i;
//
//	for (i=0; i<onm.nentries; i++) {
//		OldNew *entry= &onm.entries[i];
//		if (entry.nr==0) {
//			MEM_freeN(entry.newp);
//			entry.newp= NULL;
//		}
//	}
//}
//
//static void oldnewmap_clear(OldNewMap *onm)
//{
//	onm.nentries= 0;
//	onm.lasthit= 0;
//}
//
//static void oldnewmap_free(OldNewMap *onm)
//{
//	MEM_freeN(onm.entries);
//	MEM_freeN(onm);
//}
//
///***/
//
//static void read_libraries(FileData *basefd, ListBase *mainlist);
//
///* ************ help functions ***************** */
//
//static void add_main_to_main(Main *mainvar, Main *from)
//{
//	ListBase *lbarray[MAX_LIBARRAY], *fromarray[MAX_LIBARRAY];
//	int a;
//
//	a= set_listbasepointers(mainvar, lbarray);
//	a= set_listbasepointers(from, fromarray);
//	while(a--) {
//		addlisttolist(lbarray[a], fromarray[a]);
//	}
//}

public static void blo_join_main(ListBase<Main> mainlist) {
        Main tojoin, mainl;
        mainl = mainlist.first;
        while ((tojoin = mainl.next) != null) {
//		add_main_to_main(mainl, tojoin);
//		BLI_remlink(mainlist, tojoin);
//		MEM_freeN(tojoin);
        }
    }

//static void split_libdata(ListBase *lb, Main *first)
//{
//	ListBase *lbn;
//	ID *id, *idnext;
//	Main *mainvar;
//
//	id= lb.first;
//	while(id) {
//		idnext= id.next;
//		if(id.lib) {
//			mainvar= first;
//			while(mainvar) {
//				if(mainvar.curlib==id.lib) {
//					lbn= wich_libbase(mainvar, GS(id.name));
//					BLI_remlink(lb, id);
//					BLI_addtail(lbn, id);
//					break;
//				}
//				mainvar= mainvar.next;
//			}
//			if(mainvar==0) printf("error split_libdata\n");
//		}
//		id= idnext;
//	}
//}
//
//void blo_split_main(ListBase *mainlist, Main *main)
//{
//	ListBase *lbarray[MAX_LIBARRAY];
//	Library *lib;
//	int i;
//
//	mainlist.first= mainlist.last= main;
//	main.next= NULL;
//
//	if(main.library.first==NULL)
//		return;
//
//	for (lib= main.library.first; lib; lib= lib.id.next) {
//		Main *libmain= MEM_callocN(sizeof(Main), "libmain");
//		libmain.curlib= lib;
//		BLI_addtail(mainlist, libmain);
//	}
//
//	i= set_listbasepointers(main, lbarray);
//	while(i--)
//		split_libdata(lbarray[i], main.next);
//}
//
///* removes things like /blah/blah/../../blah/ etc, then writes in *name the full path */
//static void cleanup_path(const char *relabase, char *name)
//{
//	char filename[FILE_MAXFILE];
//
//	BLI_splitdirstring(name, filename);
//	BLI_cleanup_dir(relabase, name);
//	strcat(name, filename);
//}
//
//static void read_file_version(FileData *fd, Main *main)
//{
//	BHead *bhead;
//
//	for (bhead= blo_firstbhead(fd); bhead; bhead= blo_nextbhead(fd, bhead)) {
//		if (bhead.code==GLOB) {
//			FileGlobal *fg= read_struct(fd, bhead, "Global");
//			if(fg) {
//				main.subversionfile= fg.subversion;
//				main.minversionfile= fg.minversion;
//				main.minsubversionfile= fg.minsubversion;
//				MEM_freeN(fg);
//			}
//			else if (bhead.code==ENDB)
//				break;
//		}
//	}
//}
//
//
//static Main *blo_find_main(FileData *fd, ListBase *mainlist, const char *name, const char *relabase)
//{
//	Main *m;
//	Library *lib;
//	char name1[FILE_MAXDIR+FILE_MAXFILE];
//
//	strncpy(name1, name, sizeof(name1)-1);
//	cleanup_path(relabase, name1);
////	printf("blo_find_main: original in  %s\n", name);
////	printf("blo_find_main: converted to %s\n", name1);
//
//	for (m= mainlist.first; m; m= m.next) {
//		char *libname= (m.curlib)?m.curlib.filename:m.name;
//
//		if (BLI_streq(name1, libname)) {
//			if(G.f & G_DEBUG) printf("blo_find_main: found library %s\n", libname);
//			return m;
//		}
//	}
//
//	m= MEM_callocN(sizeof(Main), "find_main");
//	BLI_addtail(mainlist, m);
//
//	lib= alloc_libblock(&m.library, ID_LI, "lib");
//	strncpy(lib.name, name, sizeof(lib.name)-1);
//	BLI_strncpy(lib.filename, name1, sizeof(lib.filename));
//
//	m.curlib= lib;
//
//	read_file_version(fd, m);
//
//	if(G.f & G_DEBUG) printf("blo_find_main: added new lib %s\n", name);
//	return m;
//}
//
//
///* ************ FILE PARSING ****************** */
//
//static void switch_endian_bh4(BHead4 *bhead)
//{
//	/* the ID_.. codes */
//	if((bhead.code & 0xFFFF)==0) bhead.code >>=16;
//
//	if (bhead.code != ENDB) {
//		SWITCH_INT(bhead.len);
//		SWITCH_INT(bhead.SDNAnr);
//		SWITCH_INT(bhead.nr);
//	}
//}
//
//static void switch_endian_bh8(BHead8 *bhead)
//{
//	/* the ID_.. codes */
//	if((bhead.code & 0xFFFF)==0) bhead.code >>=16;
//
//	if (bhead.code != ENDB) {
//		SWITCH_INT(bhead.len);
//		SWITCH_INT(bhead.SDNAnr);
//		SWITCH_INT(bhead.nr);
//	}
//}

public static void bh4_from_bh8(BHead bhead, ByteBuffer bhead8, int do_endian_swap)
{
	BHead bhead4 = bhead;

	bhead4.code= BHead.getCodeInt(bhead8);
	bhead4.len= bhead8.getInt(4);

	if (bhead4.code != UtilDefines.ENDB) {
		
		long old = bhead8.getLong(8);

		//perform a endian swap on 64bit pointers, otherwise the pointer might map to zero
		//0x0000000000000000000012345678 would become 0x12345678000000000000000000000000
		if (do_endian_swap!=0) {
			//SWITCH_LONGINT(bhead8->old);
			old = SWITCH_LONGINT(old);
		}

		/* this patch is to avoid a long long being read from not-eight aligned positions
		   is necessary on any modern 64bit architecture) */
//		memcpy(&old, &bhead8.old, 8);
//		bhead4.old = (int) (old >> 3);
		//bhead4.old.putInt(0, (int) old);
//		bhead4.old.putLong(0, old);
//		bhead4.old = (int) bhead8.getLong(8);
		bhead4.old = (int) old;

		bhead4.SDNAnr= bhead8.getInt(16);
		bhead4.nr= bhead8.getInt(20);
	}
}

//static void bh8_from_bh4(BHead *bhead, BHead4 *bhead4)
//{
//	BHead8 *bhead8 = (BHead8 *) bhead;
//
//	bhead8.code= bhead4.code;
//	bhead8.len= bhead4.len;
//
//	if (bhead8.code != ENDB) {
//		bhead8.old= bhead4.old;
//		bhead8.SDNAnr= bhead4.SDNAnr;
//		bhead8.nr= bhead4.nr;
//	}
//}

public static BHeadN get_bhead(FileData fd)
{
//	BHead8 bhead8;
    ByteBuffer bhead8 = ByteBuffer.allocate(24);
//	BHead4 bhead4;
    ByteBuffer bhead4 = ByteBuffer.allocate(20);
	BHead  bhead = new BHead();
	BHeadN new_bhead = null;
	int readsize;

	if (fd!=null) {
		if (fd.eof==0) {

			/* not strictly needed but shuts valgrind up
			 * since uninitialized memory gets compared */
//			memset(&bhead8, 0, sizeof(BHead8));
//			memset(&bhead4, 0, sizeof(BHead4));
//			memset(&bhead,  0, sizeof(BHead));

			// First read the bhead structure.
			// Depending on the platform the file was written on this can
			// be a big or little endian BHead4 or BHead8 structure.

			// As usual 'ENDB' (the last *partial* bhead of the file)
			// needs some special handling. We don't want to EOF just yet.

			if ((fd.flags & FD_FLAGS_FILE_POINTSIZE_IS_4)!=0) {
//				bhead4.code = DATA;
                bhead4.put(0, (byte) 'D');
                bhead4.put(1, (byte) 'A');
                bhead4.put(2, (byte) 'T');
                bhead4.put(3, (byte) 'A');
				readsize = fd.read.run(fd, bhead4.array(), bhead4.capacity());

				if (readsize == bhead4.capacity() || BHead.getCodeInt(bhead4) == UtilDefines.ENDB) {
					if ((fd.flags & FD_FLAGS_SWITCH_ENDIAN)!=0) {
//						switch_endian_bh4(&bhead4);
                        bhead4.order(ByteOrder.LITTLE_ENDIAN);
					}

					if ((fd.flags & FD_FLAGS_POINTSIZE_DIFFERS)!=0) {
//						bh8_from_bh4(&bhead, &bhead4);
                        System.out.println("File pointer size is 4 but flag FD_FLAGS_POINTSIZE_DIFFERS is set.");
					} else {
						bhead.read(bhead4, 4);
					}
				} else {
					fd.eof = 1;
					bhead.len= 0;
				}
			} else {
//				bhead8.code = DATA;
                bhead8.put(0, (byte) 'D');
                bhead8.put(1, (byte) 'A');
                bhead8.put(2, (byte) 'T');
                bhead8.put(3, (byte) 'A');
				readsize = fd.read.run(fd, bhead8.array(), bhead8.capacity());

				if (readsize == bhead8.capacity() || BHead.getCodeInt(bhead8) == UtilDefines.ENDB) {
					if ((fd.flags & FD_FLAGS_SWITCH_ENDIAN)!=0) {
//						switch_endian_bh8(&bhead8);
                        bhead8.order(ByteOrder.LITTLE_ENDIAN);
					}

					if ((fd.flags & FD_FLAGS_POINTSIZE_DIFFERS)!=0) {
						bh4_from_bh8(bhead, bhead8, (fd.flags & FD_FLAGS_SWITCH_ENDIAN));
					} else {
						System.out.println("File pointer size is 8 but flag FD_FLAGS_POINTSIZE_DIFFERS is NOT set.");
					}
				} else {
					fd.eof = 1;
					bhead.len= 0;
				}
			}

			/* make sure people are not trying to pass bad blend files */
			if (bhead.len < 0) fd.eof = 1;

			// bhead now contains the (converted) bhead structure. Now read
			// the associated data and put everything in a BHeadN (creative naming !)

			if (fd.eof==0) {
				new_bhead = new BHeadN(bhead.len, bhead);
				if (new_bhead!=null) {
//					new_bhead.next = new_bhead.prev = null;
//					new_bhead.bhead = bhead;

					readsize = fd.read.run(fd, new_bhead.data.array(), bhead.len);

					if (readsize != bhead.len) {
						fd.eof = 1;
//						MEM_freeN(new_bhead);
						new_bhead = null;
					}
				} else {
					fd.eof = 1;
				}
			}
		}
	}

	// We've read a new block. Now add it to the list
	// of blocks.

	if (new_bhead!=null) {
		ListBaseUtil.BLI_addtail(fd.listbase, new_bhead);
	}

	return new_bhead;
}

public static BHead blo_firstbhead(FileData fd)
{
	BHeadN new_bhead;
	BHead bhead = null;

	// Rewind the file
	// Read in a new block if necessary

	new_bhead = fd.listbase.first;
	if (new_bhead == null) {
		new_bhead = get_bhead(fd);
	}

	if (new_bhead!=null) {
		bhead = new_bhead.bhead;
	}

	return bhead;
}

//BHead *blo_prevbhead(FileData *fd, BHead *thisblock)
//{
//	BHeadN *bheadn= (BHeadN *) (((char *) thisblock) - GET_INT_FROM_POINTER( &((BHeadN*)0).bhead) );
//	BHeadN *prev= bheadn.prev;
//
//	return prev?&prev.bhead:NULL;
//}

public static BHead blo_nextbhead(FileData fd, BHead thisblock)
{
	BHeadN new_bhead = null;
	BHead bhead = null;

	if (thisblock!=null) {
		// bhead is actually a sub part of BHeadN
		// We calculate the BHeadN pointer from the BHead pointer below
		new_bhead = thisblock.bheadN;

		// get the next BHeadN. If it doesn't exist we read in the next one
		new_bhead = new_bhead.next;
		if (new_bhead == null) {
			new_bhead = get_bhead(fd);
		}
	}

	if (new_bhead!=null) {
		// here we do the reverse:
		// go from the BHeadN pointer to the BHead pointer
		bhead = new_bhead.bhead;
	}

	return bhead;
}

public static void decode_blender_header(FileData fd)
{
    System.out.println("Starting decode blender header ...");
	byte[] header=new byte[SIZEOFBLENDERHEADER], num=new byte[3];
	int readsize;

	// read in the header data
	readsize = fd.read.run(fd, header, header.length);

	if (readsize == header.length) {
        String headerStr = new String(header);
        System.out.println(headerStr);
		if(headerStr.startsWith("BLENDER")) {
//			int remove_this_endian_test= 1;

			fd.flags |= FD_FLAGS_FILE_OK;

			// what size are pointers in the file ?
			if(headerStr.charAt(7) == '_') {
				fd.flags |= FD_FLAGS_FILE_POINTSIZE_IS_4;
				DNATools.pointerSize = 4;
                System.out.println("FD_FLAGS_FILE_POINTSIZE_IS_4");
//				if (sizeof(void *) != 4) {
//					fd.flags |= FD_FLAGS_POINTSIZE_DIFFERS;
//				}
			} else {
//				if (sizeof(void *) != 8) {
					fd.flags |= FD_FLAGS_POINTSIZE_DIFFERS;
					DNATools.pointerSize = 8;
                    System.out.println("FD_FLAGS_FILE_POINTSIZE_IS_8");
//				}
			}

			// is the file saved in a different endian than we need ?
			if (headerStr.charAt(8) == 'v') {
				fd.flags |= FD_FLAGS_SWITCH_ENDIAN;
                System.out.println("FD_FLAGS_SWITCH_ENDIAN");
			}

			// get the version number

			System.arraycopy(header, 9, num, 0, 3);
            String numStr = new String(num);
            fd.fileversion = Integer.parseInt(numStr);
            System.out.println("fileversion: " + fd.fileversion);
		}
	}
        System.out.println("Finished decode blender header.");
}

public static boolean read_file_dna(FileData fd)
{
    System.out.println("Starting read file dna ...");
	BHead bhead;

	for (bhead= blo_firstbhead(fd); bhead!=null; bhead= blo_nextbhead(fd, bhead)) {
		if (bhead.code==UtilDefines.DNA1) {
			boolean do_endian_swap= (fd.flags&FD_FLAGS_SWITCH_ENDIAN)!=0;

			fd.filesdna= DNAGenfile.DNA_sdna_from_data(bhead.bheadN.data, bhead.len, do_endian_swap);
			if (fd.filesdna!=null) {

				fd.compflags= DNAGenfile.DNA_struct_get_compareflags(fd.filesdna, fd.memsdna);
				/* used to retrieve ID names from (bhead+1) */
				fd.id_name_offs= DNAGenfile.DNA_elem_offset(fd.filesdna, "ID", "char", "name[]");
			}

            System.out.println("Finished read file dna.");
			return true;
		} else if (bhead.code==UtilDefines.ENDB)
			break;
	}

    System.out.println("ERROR READING FILE DNA.");
	return false;
}

//static int fd_read_from_file(FileData *filedata, void *buffer, unsigned int size)
//{
//	int readsize = read(filedata.filedes, buffer, size);
//
//	if (readsize < 0) {
//		readsize = EOF;
//	} else {
//		filedata.seek += readsize;
//	}
//
//	return (readsize);
//}

public static FDRead fd_read_gzip_from_file = new FDRead() {
public int run(FileData filedata, byte[] buffer, int size)
{
        int readsize;
        try {
            filedata.gzfiledes.get(buffer, 0, size);
            readsize = size;
        } catch(Exception ex) {
            readsize = -1;
        }

	if (readsize < 0) {
		readsize = EOF;
	} else {
		filedata.seek += readsize;
	}

	return readsize;
}
};

//static int fd_read_from_memory(FileData *filedata, void *buffer, unsigned int size)
//{
//		// don't read more bytes then there are available in the buffer
//	int readsize = MIN2(size, filedata.buffersize - filedata.seek);
//
//	memcpy(buffer, filedata.buffer + filedata.seek, readsize);
//	filedata.seek += readsize;
//
//	return (readsize);
//}
//
//static int fd_read_from_memfile(FileData *filedata, void *buffer, unsigned int size)
//{
//	static unsigned int seek= 1<<30;	/* the current position */
//	static unsigned int offset= 0;		/* size of previous chunks */
//	static MemFileChunk *chunk=NULL;
//	unsigned int chunkoffset, readsize, totread;
//
//	if(size==0) return 0;
//
//	if(seek != (unsigned int)filedata.seek) {
//		chunk= filedata.memfile.chunks.first;
//		seek= 0;
//
//		while(chunk) {
//			if(seek + chunk.size > (unsigned) filedata.seek) break;
//			seek+= chunk.size;
//			chunk= chunk.next;
//		}
//		offset= seek;
//		seek= filedata.seek;
//	}
//
//	if(chunk) {
//		totread= 0;
//
//		do {
//			/* first check if it's on the end if current chunk */
//			if(seek-offset == chunk.size) {
//				offset+= chunk.size;
//				chunk= chunk.next;
//			}
//
//			/* debug, should never happen */
//			if(chunk==NULL) {
//				printf("illegal read, chunk zero\n");
//				return 0;
//			}
//
//			chunkoffset= seek-offset;
//			readsize= size-totread;
//
//			/* data can be spread over multiple chunks, so clamp size
//			 * to within this chunk, and then it will read further in
//			 * the next chunk */
//			if(chunkoffset+readsize > chunk.size)
//				readsize= chunk.size-chunkoffset;
//
//			memcpy((char*)buffer+totread, chunk.buf+chunkoffset, readsize);
//			totread += readsize;
//			filedata.seek += readsize;
//			seek += readsize;
//		} while(totread < size);
//
//		return totread;
//	}
//
//	return 0;
//}

public static FileData filedata_new()
{
	FileData fd = new FileData();

	fd.filedes = -1;
	fd.gzfiledes = null;

		/* XXX, this doesn't need to be done all the time,
		 * but it keeps us reentrant,  remove once we have
		 * a lib that provides a nice lock. - zr
		 */
//	fd.memsdna = DNA_sdna_from_data(DNAstr,  DNAlen,  0);

	fd.datamap = oldnewmap_new();
	fd.globmap = oldnewmap_new();
	fd.libmap = oldnewmap_new();

	return fd;
}

public static FileData blo_decode_and_check(FileData fd, ReportList reports)
{
	decode_blender_header(fd);

	if ((fd.flags & FD_FLAGS_FILE_OK)!=0) {
		if (!read_file_dna(fd)) {
//			BKE_report(reports, RPT_ERROR, "File incomplete");
//			blo_freefiledata(fd);
			fd= null;
		}
	}
	else {
//		BKE_report(reports, RPT_ERROR, "File is not a Blender file");
//		blo_freefiledata(fd);
		fd= null;
	}

	return fd;
}

/* cannot be called with relative paths anymore! */
/* on each new library added, it now checks for the current FileData and expands relativeness */
//public static FileData blo_openblenderfile(String _name, ReportList reports)
public static FileData blo_openblenderfile(URL name, ReportList reports)
{
//	gzFile gzfile;
    ByteBuffer gzfile;
//    URL name;
//    try {
//    	name = new URL("file:/"+_name);
//    } catch (Exception e) {
//    	e.printStackTrace();
//    	return null;
//    }

//	gzfile= gzopen(name, "rb");
        try {
            byte[] chunk = new byte[4096];
//            File f = new File(name);
//            FileInputStream file = new FileInputStream(f);
            InputStream file = name.openStream();
            GZIPInputStream gzin = new GZIPInputStream(file);
//            ByteArrayOutputStream btmp = new ByteArrayOutputStream((int) f.length());
            ByteArrayOutputStream btmp = new ByteArrayOutputStream();
            while (true) {
                int len = gzin.read(chunk, 0, 4096);
                if (len != -1) {
                    btmp.write(chunk, 0, len);
                } else {
                    break;
                }
            }
            gzfile = ByteBuffer.wrap(btmp.toByteArray());
        } catch (Exception ex) {
            try {
//                FileInputStream file = new FileInputStream(name);
            	byte[] chunk = new byte[4096];
            	InputStream file = name.openStream();
//                FileInputStream file = new FileInputStream(name));
//                FileChannel fc = file.getChannel();
//                gzfile = fc.map(FileChannel.MapMode.READ_ONLY, 0, fc.size());
            	ByteArrayOutputStream btmp = new ByteArrayOutputStream();
            	while (true) {
                    int len = file.read(chunk, 0, 4096);
                    if (len != -1) {
                        btmp.write(chunk, 0, len);
                    } else {
                        break;
                    }
                }
            	gzfile = ByteBuffer.wrap(btmp.toByteArray());
            } catch(Exception ex2) {
                gzfile = null;
            }
        }

	if (null == gzfile) {
//		BKE_report(reports, RPT_ERROR, "Unable to open");
		System.out.println("Unable to open");
		return null;
	} else {
		FileData fd = filedata_new();
		fd.gzfiledes = gzfile;
		fd.read = fd_read_gzip_from_file;

		/* needed for library_append and read_libraries */
//		BLI_strncpy(fd.filename, name, sizeof(fd.filename));
        fd.filename = name.toString();

		return blo_decode_and_check(fd, reports);
	}
}

//FileData *blo_openblendermemory(void *mem, int memsize, ReportList *reports)
//{
//	if (!mem || memsize<SIZEOFBLENDERHEADER) {
//		BKE_report(reports, RPT_ERROR, (mem)? "Unable to read": "Unable to open");
//		return NULL;
//	} else {
//		FileData *fd= filedata_new();
//		fd.buffer= mem;
//		fd.buffersize= memsize;
//		fd.read= fd_read_from_memory;
//		fd.flags|= FD_FLAGS_NOT_MY_BUFFER;
//
//		return blo_decode_and_check(fd, reports);
//	}
//}
//
//FileData *blo_openblendermemfile(MemFile *memfile, ReportList *reports)
//{
//	if (!memfile) {
//		BKE_report(reports, RPT_ERROR, "Unable to open");
//		return NULL;
//	} else {
//		FileData *fd= filedata_new();
//		fd.memfile= memfile;
//
//		fd.read= fd_read_from_memfile;
//		fd.flags|= FD_FLAGS_NOT_MY_BUFFER;
//
//		return blo_decode_and_check(fd, reports);
//	}
//}
//
//
//void blo_freefiledata(FileData *fd)
//{
//	if (fd) {
//
//		if (fd.filedes != -1) {
//			close(fd.filedes);
//		}
//
//		if (fd.gzfiledes != NULL)
//		{
//			gzclose(fd.gzfiledes);
//		}
//
//		if (fd.buffer && !(fd.flags & FD_FLAGS_NOT_MY_BUFFER)) {
//			MEM_freeN(fd.buffer);
//			fd.buffer = 0;
//		}
//
//		// Free all BHeadN data blocks
//		BLI_freelistN(&fd.listbase);
//
//		if (fd.memsdna)
//			DNA_sdna_free(fd.memsdna);
//		if (fd.filesdna)
//			DNA_sdna_free(fd.filesdna);
//		if (fd.compflags)
//			MEM_freeN(fd.compflags);
//
//		if (fd.datamap)
//			oldnewmap_free(fd.datamap);
//		if (fd.globmap)
//			oldnewmap_free(fd.globmap);
//		if (fd.imamap)
//			oldnewmap_free(fd.imamap);
//		if (fd.libmap && !(fd.flags & FD_FLAGS_NOT_MY_LIBMAP))
//			oldnewmap_free(fd.libmap);
//		if (fd.bheadmap)
//			MEM_freeN(fd.bheadmap);
//
//		MEM_freeN(fd);
//	}
//}
//
///* ************ DIV ****************** */
//
//int BLO_has_bfile_extension(char *str)
//{
//	return (BLI_testextensie(str, ".ble") || BLI_testextensie(str, ".blend")||BLI_testextensie(str, ".blend.gz"));
//}

/* ************** OLD POINTERS ******************* */

public static Object newdataadr(FileData fd, Object adr)		/* only direct databocks */
{
	if (adr instanceof Integer) {
            return oldnewmap_lookup_and_inc(fd.datamap, (Integer) adr);
        } else {
            return adr;
        }
}

//static void *newglobadr(FileData *fd, void *adr)		/* direct datablocks with global linking */
//{
//	return oldnewmap_lookup_and_inc(fd.globmap, adr);
//}

    /* used to restore image data after undo */
    public static Object newimaadr(FileData fd, Object adr) {
        if (fd.imamap != null && adr != null) {
            if (adr instanceof Integer) {
                return oldnewmap_lookup_and_inc(fd.imamap, (Integer) adr);
            } else {
                return adr;
            }
        }
        return null;
    }

    /* only lib data */
    public static ID newlibadr(FileData fd, Object lib, Object adr) {
        if (adr instanceof Integer) {
            return oldnewmap_liblookup(fd.libmap, (Integer) adr, lib);
        } else {
            return (ID) adr;
        }
    }

    /* increases user number */
    public static ID newlibadr_us(FileData fd, Object lib, Object adr) {
        ID id = newlibadr(fd, lib, adr);
        if (id != null) {
            id.us++;
        }
        return id;
    }

    public static void change_idid_adr_fd(FileData fd, Object old, Object newObj) {
        for (int i = 0; i < fd.libmap.nentries; i++) {
            OldNew entry = fd.libmap.entries.get(i);

            if (old == entry.newp && entry.nr == DNA_ID.ID_ID) {
                entry.newp = newObj;
                if (newObj != null) {
                    entry.nr = LibraryUtil.GS(((ID) newObj).name);
                }
                break;
            }
        }
    }

    public static void change_idid_adr(ListBase<Main> mainlist, FileData basefd, Object old, Object newObj) {
        for (Main mainptr = mainlist.first; mainptr != null; mainptr = (Main) mainptr.next) {
            FileData fd;

            if (mainptr.curlib != null) {
                fd = (FileData) mainptr.curlib.filedata;
            } else {
                fd = basefd;
            }

            if (fd != null) {
                change_idid_adr_fd(fd, old, newObj);
            }
        }
    }

///* lib linked proxy objects point to our local data, we need
// * to clear that pointer before reading the undo memfile since
// * the object might be removed, it is set again in reading
// * if the local object still exists */
//void blo_clear_proxy_pointers_from_lib(FileData *fd, Main *oldmain)
//{
//	Object *ob= oldmain.object.first;
//
//	for(;ob; ob= ob.id.next)
//		if(ob.id.lib)
//			ob.proxy_from= NULL;
//}
//
//void blo_make_image_pointer_map(FileData *fd, Main *oldmain)
//{
//	Image *ima= oldmain.image.first;
//	Scene *sce= oldmain.scene.first;
//
//	fd.imamap= oldnewmap_new();
//
//	for(;ima; ima= ima.id.next) {
//		Link *ibuf= ima.ibufs.first;
//		for(; ibuf; ibuf= ibuf.next)
//			oldnewmap_insert(fd.imamap, ibuf, ibuf, 0);
//		if(ima.gputexture)
//			oldnewmap_insert(fd.imamap, ima.gputexture, ima.gputexture, 0);
//	}
//	for(; sce; sce= sce.id.next) {
//		if(sce.nodetree) {
//			bNode *node;
//			for(node= sce.nodetree.nodes.first; node; node= node.next)
//				oldnewmap_insert(fd.imamap, node.preview, node.preview, 0);
//		}
//	}
//}
//
///* set old main image ibufs to zero if it has been restored */
///* this works because freeing old main only happens after this call */
//void blo_end_image_pointer_map(FileData *fd, Main *oldmain)
//{
//	OldNew *entry= fd.imamap.entries;
//	Image *ima= oldmain.image.first;
//	Scene *sce= oldmain.scene.first;
//	int i;
//
//	/* used entries were restored, so we put them to zero */
//	for (i=0; i<fd.imamap.nentries; i++, entry++) {
//	 	if (entry.nr>0)
//			entry.newp= NULL;
//	}
//
//	for(;ima; ima= ima.id.next) {
//		Link *ibuf, *next;
//
//		/* this mirrors direct_link_image */
//		for(ibuf= ima.ibufs.first; ibuf; ibuf= next) {
//			next= ibuf.next;
//			if(NULL==newimaadr(fd, ibuf)) {	/* so was restored */
//				BLI_remlink(&ima.ibufs, ibuf);
//				ima.bindcode= 0;
//				ima.gputexture= NULL;
//			}
//		}
//
//		ima.gputexture= newimaadr(fd, ima.gputexture);
//	}
//	for(; sce; sce= sce.id.next) {
//		if(sce.nodetree) {
//			bNode *node;
//			for(node= sce.nodetree.nodes.first; node; node= node.next)
//				node.preview= newimaadr(fd, node.preview);
//		}
//	}
//}
//
///* undo file support: add all library pointers in lookup */
//void blo_add_library_pointer_map(ListBase *mainlist, FileData *fd)
//{
//	Main *ptr= mainlist.first;
//	ListBase *lbarray[MAX_LIBARRAY];
//
//	for(ptr= ptr.next; ptr; ptr= ptr.next) {
//		int i= set_listbasepointers(ptr, lbarray);
//		while(i--) {
//			ID *id;
//			for(id= lbarray[i].first; id; id= id.next)
//				oldnewmap_insert(fd.libmap, id, id, GS(id.name));
//		}
//	}
//}
//
//
///* ********** END OLD POINTERS ****************** */
///* ********** READ FILE ****************** */
//
//static void switch_endian_structs(struct SDNA *filesdna, BHead *bhead)
//{
//	int blocksize, nblocks;
//	char *data;
//
//	data= (char *)(bhead+1);
//	blocksize= filesdna.typelens[ filesdna.structs[bhead.SDNAnr][0] ];
//
//	nblocks= bhead.nr;
//	while(nblocks--) {
//		DNA_struct_switch_endian(filesdna, bhead.SDNAnr, data);
//
//		data+= blocksize;
//	}
//}

public static <T extends DNA> T read_struct(FileData fd, BHead bh, Class<T> blockname)
{
	T temp= null;

	if (bh.len!=0) {
//        System.out.printf("Started reading struct [%s] code=%s len=%d ptr=%d cnt=%d #%d...\n", blockname, Integer.toHexString(bh.code), bh.len, bh.old.getInt(0), bh.nr, bh.SDNAnr);
		/* switch is based on file dna */
		if (bh.SDNAnr!=0 && (fd.flags & FD_FLAGS_SWITCH_ENDIAN)!=0) {
//			switch_endian_structs(fd.filesdna, bh);
            bh.bheadN.data.order(ByteOrder.LITTLE_ENDIAN);
		}

		if (fd.compflags[bh.SDNAnr]!=0) {	/* flag==0: doesn't exist anymore */
			if(fd.compflags[bh.SDNAnr]==2) {
//				temp= DNA_struct_reconstruct(fd.memsdna, fd.filesdna, fd.compflags, bh.SDNAnr, bh.nr, (bh+1));
                System.out.println("dna_reconstruct");
			} else {
//				temp= MEM_mallocN(bh.len, blockname);
//				memcpy(temp, (bh+1), bh.len);
                try {
                    temp = DNATools.link(bh.old, blockname);
                    if (temp != null) {
                        temp.read(bh.bheadN.data);
//                                        System.out.println(temp);
                    }
                    if (bh.nr > 1) {
                        T[] ta = (T[]) Array.newInstance(blockname, bh.nr);
                        if (temp != null) {
                            ta[0] = temp;
                            for (int i = 1; i < ta.length; i++) {
                                ta[i] = blockname.newInstance();
                                ta[i].read(bh.bheadN.data);
//                                    System.out.println(ta[i]);
                            }
                            temp.setmyarray(ta);
                        }
                    }
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
			}
		}
	}

	return temp;
}

    /* only direct data */
    public static void link_list(FileData fd, ListBase lb) {
        Link ln, prev;

        if (lb.first == null) {
            return;
        }

        lb.first = newdataadr(fd, lb.first);
        ln = (Link) lb.first;
        prev = null;
        while (ln != null) {
            ln.next = newdataadr(fd, ln.next);
            ln.prev = prev;
            prev = ln;
            ln = (Link) ln.next;
        }
        lb.last = prev;
    }

//static void link_glob_list(FileData *fd, ListBase *lb)		/* for glob data */
//{
//	Link *ln, *prev;
//	void *poin;
//
//	if(lb.first==0) return;
//	poin= newdataadr(fd, lb.first);
//	if(lb.first) {
//		oldnewmap_insert(fd.globmap, lb.first, poin, 0);
//	}
//	lb.first= poin;
//
//	ln= lb.first;
//	prev= 0;
//	while(ln) {
//		poin= newdataadr(fd, ln.next);
//		if(ln.next) {
//			oldnewmap_insert(fd.globmap, ln.next, poin, 0);
//		}
//		ln.next= poin;
//		ln.prev= prev;
//		prev= ln;
//		ln= ln.next;
//	}
//	lb.last= prev;
//}
//
//static void test_pointer_array(FileData *fd, void **mat)
//{
//#if defined(WIN32) && !defined(FREE_WINDOWS)
//	__int64 *lpoin, *lmat;
//#else
//	long long *lpoin, *lmat;
//#endif
//	int len, *ipoin, *imat;
//
//		/* manually convert the pointer array in
//		 * the old dna format to a pointer array in
//		 * the new dna format.
//		 */
//	if(*mat) {
//		len= MEM_allocN_len(*mat)/fd.filesdna.pointerlen;
//
//		if(fd.filesdna.pointerlen==8 && fd.memsdna.pointerlen==4) {
//			ipoin=imat= MEM_mallocN( len*4, "newmatar");
//			lpoin= *mat;
//
//			while(len-- > 0) {
//				if((fd.flags & FD_FLAGS_SWITCH_ENDIAN))
//					SWITCH_LONGINT(*lpoin);
//				*ipoin= (int) ((*lpoin) >> 3);
//				ipoin++;
//				lpoin++;
//			}
//			MEM_freeN(*mat);
//			*mat= imat;
//		}
//
//		if(fd.filesdna.pointerlen==4 && fd.memsdna.pointerlen==8) {
//			lpoin=lmat= MEM_mallocN( len*8, "newmatar");
//			ipoin= *mat;
//
//			while(len-- > 0) {
//				*lpoin= *ipoin;
//				ipoin++;
//				lpoin++;
//			}
//			MEM_freeN(*mat);
//			*mat= lmat;
//		}
//	}
//}
//
///* ************ READ ID Properties *************** */
//
//void IDP_DirectLinkProperty(IDProperty *prop, int switch_endian, FileData *fd);
//void IDP_LibLinkProperty(IDProperty *prop, int switch_endian, FileData *fd);
//
//static void IDP_DirectLinkIDPArray(IDProperty *prop, int switch_endian, FileData *fd)
//{
//	IDProperty **array;
//	int i;
//
//	/*since we didn't save the extra buffer, set totallen to len.*/
//	prop.totallen = prop.len;
//	prop.data.pointer = newdataadr(fd, prop.data.pointer);
//
//	if (switch_endian) {
//		test_pointer_array(fd, prop.data.pointer);
//		array= (IDProperty**) prop.data.pointer;
//
//		for(i=0; i<prop.len; i++)
//			IDP_DirectLinkProperty(array[i], switch_endian, fd);
//	}
//}
//
//static void IDP_DirectLinkArray(IDProperty *prop, int switch_endian, FileData *fd)
//{
//	IDProperty **array;
//	int i;
//
//	/*since we didn't save the extra buffer, set totallen to len.*/
//	prop.totallen = prop.len;
//	prop.data.pointer = newdataadr(fd, prop.data.pointer);
//
//	if (switch_endian) {
//		if(prop.subtype == IDP_GROUP) {
//			test_pointer_array(fd, prop.data.pointer);
//			array= prop.data.pointer;
//
//			for(i=0; i<prop.len; i++)
//				IDP_DirectLinkProperty(array[i], switch_endian, fd);
//		}
//		else if(prop.subtype == IDP_DOUBLE) {
//			for (i=0; i<prop.len; i++) {
//				SWITCH_LONGINT(((double*)prop.data.pointer)[i]);
//			}
//		} else {
//			for (i=0; i<prop.len; i++) {
//				SWITCH_INT(((int*)prop.data.pointer)[i]);
//			}
//		}
//	}
//}
//
//static void IDP_DirectLinkString(IDProperty *prop, int switch_endian, FileData *fd)
//{
//	/*since we didn't save the extra string buffer, set totallen to len.*/
//	prop.totallen = prop.len;
//	prop.data.pointer = newdataadr(fd, prop.data.pointer);
//}
//
//static void IDP_DirectLinkGroup(IDProperty *prop, int switch_endian, FileData *fd)
//{
//	ListBase *lb = &prop.data.group;
//	IDProperty *loop;
//
//	link_list(fd, lb);
//
//	/*Link child id properties now*/
//	for (loop=prop.data.group.first; loop; loop=loop.next) {
//		IDP_DirectLinkProperty(loop, switch_endian, fd);
//	}
//}
//
//void IDP_DirectLinkProperty(IDProperty *prop, int switch_endian, FileData *fd)
//{
//	switch (prop.type) {
//		case IDP_GROUP:
//			IDP_DirectLinkGroup(prop, switch_endian, fd);
//			break;
//		case IDP_STRING:
//			IDP_DirectLinkString(prop, switch_endian, fd);
//			break;
//		case IDP_ARRAY:
//			IDP_DirectLinkArray(prop, switch_endian, fd);
//			break;
//		case IDP_IDPARRAY:
//			IDP_DirectLinkIDPArray(prop, switch_endian, fd);
//			break;
//		case IDP_DOUBLE:
//			/*erg, stupid doubles.  since I'm storing them
//			 in the same field as int val; val2 in the
//			 IDPropertyData struct, they have to deal with
//			 endianness specifically
//
//			 in theory, val and val2 would've already been swapped
//			 if switch_endian is true, so we have to first unswap
//			 them then reswap them as a single 64-bit entity.
//			 */
//
//			if (switch_endian) {
//				SWITCH_INT(prop.data.val);
//				SWITCH_INT(prop.data.val2);
//				SWITCH_LONGINT(prop.data.val);
//			}
//
//			break;
//	}
//}
//
///*stub function*/
//void IDP_LibLinkProperty(IDProperty *prop, int switch_endian, FileData *fd)
//{
//}
//
///* ************ READ CurveMapping *************** */
//
///* cuma itself has been read! */
//static void direct_link_curvemapping(FileData *fd, CurveMapping *cumap)
//{
//	int a;
//
//	/* flag seems to be able to hang? Maybe old files... not bad to clear anyway */
//	cumap.flag &= ~CUMA_PREMULLED;
//
//	for(a=0; a<CM_TOT; a++) {
//		cumap.cm[a].curve= newdataadr(fd, cumap.cm[a].curve);
//		cumap.cm[a].table= NULL;
//	}
//}
//
///* ************ READ Brush *************** */
///* library brush linking after fileread */
//static void lib_link_brush(FileData *fd, Main *main)
//{
//	Brush *brush;
//	MTex *mtex;
//	int a;
//
//	/* only link ID pointers */
//	for(brush= main.brush.first; brush; brush= brush.id.next) {
//		if(brush.id.flag & LIB_NEEDLINK) {
//			brush.id.flag -= LIB_NEEDLINK;
//
//			brush.clone.image= newlibadr_us(fd, brush.id.lib, brush.clone.image);
//
//			for(a=0; a<MAX_MTEX; a++) {
//				mtex= brush.mtex[a];
//				if(mtex)
//					mtex.tex= newlibadr_us(fd, brush.id.lib, mtex.tex);
//			}
//
//			brush.clone.image= newlibadr_us(fd, brush.id.lib, brush.clone.image);
//		}
//	}
//}
//
//static void direct_link_brush(FileData *fd, Brush *brush)
//{
//	/* brush itself has been read */
//	int a;
//
//	for(a=0; a<MAX_MTEX; a++)
//		brush.mtex[a]= newdataadr(fd, brush.mtex[a]);
//
//	/* fallof curve */
//	brush.curve= newdataadr(fd, brush.curve);
//	if(brush.curve)
//		direct_link_curvemapping(fd, brush.curve);
//	else
//		brush_curve_preset(brush, BRUSH_PRESET_SHARP);
//}
//
//static void direct_link_script(FileData *fd, Script *script)
//{
//	script.id.us = 1;
//	SCRIPT_SET_NULL(script)
//}


/* ************ READ PACKEDFILE *************** */

    public static PackedFile direct_link_packedfile(FileData fd, PackedFile oldpf) {
        PackedFile pf = (PackedFile) newdataadr(fd, oldpf);

        if (pf != null) {
            pf.data = newdataadr(fd, pf.data);
        }

        return pf;
    }

/* ************ READ IMAGE PREVIEW *************** */

public static PreviewImage direct_link_preview_image(FileData fd, PreviewImage old_prv) {
        PreviewImage prv = (PreviewImage) newdataadr(fd, old_prv);

        if (prv != null) {
            int i;
            for (i = 0; i < DNA_ID.PREVIEW_MIPMAPS; ++i) {
                if (prv.rect[i] != null) {
                    prv.rect[i] = newdataadr(fd, prv.rect[i]);
                }
            }
        }

        return prv;
    }

///* ************ READ ANIMATION STUFF ***************** */
//
///* Legacy Data Support (for Version Patching) ----------------------------- */
//
//// XXX depreceated - old animation system
//static void lib_link_ipo(FileData *fd, Main *main)
//{
//	Ipo *ipo;
//
//	ipo= main.ipo.first;
//	while(ipo) {
//		if(ipo.id.flag & LIB_NEEDLINK) {
//			IpoCurve *icu;
//			for(icu= ipo.curve.first; icu; icu= icu.next) {
//				if(icu.driver)
//					icu.driver.ob= newlibadr(fd, ipo.id.lib, icu.driver.ob);
//			}
//			ipo.id.flag -= LIB_NEEDLINK;
//		}
//		ipo= ipo.id.next;
//	}
//}
//
//// XXX depreceated - old animation system
//static void direct_link_ipo(FileData *fd, Ipo *ipo)
//{
//	IpoCurve *icu;
//
//	link_list(fd, &(ipo.curve));
//	icu= ipo.curve.first;
//	while(icu) {
//		icu.bezt= newdataadr(fd, icu.bezt);
//		icu.bp= newdataadr(fd, icu.bp);
//		icu.driver= newdataadr(fd, icu.driver);
//		icu= icu.next;
//	}
//}
//
//// XXX depreceated - old animation system
//static void lib_link_nlastrips(FileData *fd, ID *id, ListBase *striplist)
//{
//	bActionStrip *strip;
//	bActionModifier *amod;
//
//	for (strip=striplist.first; strip; strip=strip.next){
//		strip.object = newlibadr(fd, id.lib, strip.object);
//		strip.act = newlibadr_us(fd, id.lib, strip.act);
//		strip.ipo = newlibadr(fd, id.lib, strip.ipo);
//		for(amod= strip.modifiers.first; amod; amod= amod.next)
//			amod.ob= newlibadr(fd, id.lib, amod.ob);
//	}
//}
//
//// XXX depreceated - old animation system
//static void direct_link_nlastrips(FileData *fd, ListBase *strips)
//{
//	bActionStrip *strip;
//
//	link_list(fd, strips);
//
//	for(strip= strips.first; strip; strip= strip.next)
//		link_list(fd, &strip.modifiers);
//}
//
//// XXX depreceated - old animation system
//static void lib_link_constraint_channels(FileData *fd, ID *id, ListBase *chanbase)
//{
//	bConstraintChannel *chan;
//
//	for (chan=chanbase.first; chan; chan=chan.next){
//		chan.ipo = newlibadr_us(fd, id.lib, chan.ipo);
//	}
//}
//
///* Data Linking ----------------------------- */
//
//static void lib_link_fmodifiers(FileData *fd, ID *id, ListBase *list)
//{
//	FModifier *fcm;
//
//	for (fcm= list.first; fcm; fcm= fcm.next) {
//		/* data for specific modifiers */
//		switch (fcm.type) {
//			case FMODIFIER_TYPE_PYTHON:
//			{
//				FMod_Python *data= (FMod_Python *)fcm.data;
//				data.script = newlibadr(fd, id.lib, data.script);
//			}
//				break;
//		}
//	}
//}
//
//static void lib_link_fcurves(FileData *fd, ID *id, ListBase *list)
//{
//	FCurve *fcu;
//
//	/* relink ID-block references... */
//	for (fcu= list.first; fcu; fcu= fcu.next) {
//		/* driver data */
//		if (fcu.driver) {
//			ChannelDriver *driver= fcu.driver;
//			DriverTarget *dtar;
//
//			for (dtar= driver.targets.first; dtar; dtar= dtar.next)
//				dtar.id= newlibadr(fd, id.lib, dtar.id);
//		}
//
//		/* modifiers */
//		lib_link_fmodifiers(fd, id, &fcu.modifiers);
//	}
//}
//
//
///* NOTE: this assumes that link_list has already been called on the list */
//static void direct_link_fmodifiers(FileData *fd, ListBase *list)
//{
//	FModifier *fcm;
//
//	for (fcm= list.first; fcm; fcm= fcm.next) {
//		/* relink general data */
//		fcm.data = newdataadr(fd, fcm.data);
//		fcm.edata= NULL;
//
//		/* do relinking of data for specific types */
//		switch (fcm.type) {
//			case FMODIFIER_TYPE_GENERATOR:
//			{
//				FMod_Generator *data= (FMod_Generator *)fcm.data;
//
//				data.coefficients= newdataadr(fd, data.coefficients);
//			}
//				break;
//			case FMODIFIER_TYPE_ENVELOPE:
//			{
//				FMod_Envelope *data= (FMod_Envelope *)fcm.data;
//
//				data.data= newdataadr(fd, data.data);
//			}
//				break;
//			case FMODIFIER_TYPE_PYTHON:
//			{
//				FMod_Python *data= (FMod_Python *)fcm.data;
//
//				data.prop = newdataadr(fd, data.prop);
//				IDP_DirectLinkProperty(data.prop, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//			}
//				break;
//		}
//	}
//}
//
///* NOTE: this assumes that link_list has already been called on the list */
//static void direct_link_fcurves(FileData *fd, ListBase *list)
//{
//	FCurve *fcu;
//
//	/* link F-Curve data to F-Curve again (non ID-libs) */
//	for (fcu= list.first; fcu; fcu= fcu.next) {
//		/* curve data */
//		fcu.bezt= newdataadr(fd, fcu.bezt);
//		fcu.fpt= newdataadr(fd, fcu.fpt);
//
//		/* rna path */
//		fcu.rna_path= newdataadr(fd, fcu.rna_path);
//
//		/* group */
//		fcu.grp= newdataadr(fd, fcu.grp);
//
//		/* driver */
//		fcu.driver= newdataadr(fd, fcu.driver);
//		if (fcu.driver) {
//			ChannelDriver *driver= fcu.driver;
//			DriverTarget *dtar;
//
//			/* relink targets and their paths */
//			link_list(fd, &driver.targets);
//			for (dtar= driver.targets.first; dtar; dtar= dtar.next)
//				dtar.rna_path= newdataadr(fd, dtar.rna_path);
//		}
//
//		/* modifiers */
//		link_list(fd, &fcu.modifiers);
//		direct_link_fmodifiers(fd, &fcu.modifiers);
//	}
//}
//
//
//static void lib_link_action(FileData *fd, Main *main)
//{
//	bAction *act;
//	bActionChannel *chan;
//
//	for (act= main.action.first; act; act= act.id.next) {
//		if (act.id.flag & LIB_NEEDLINK) {
//			act.id.flag -= LIB_NEEDLINK;
//
//// XXX depreceated - old animation system <<<
//			for (chan=act.chanbase.first; chan; chan=chan.next) {
//				chan.ipo= newlibadr_us(fd, act.id.lib, chan.ipo);
//				lib_link_constraint_channels(fd, &act.id, &chan.constraintChannels);
//			}
//// >>> XXX depreceated - old animation system
//
//			lib_link_fcurves(fd, &act.id, &act.curves);
//		}
//	}
//}
//
//static void direct_link_action(FileData *fd, bAction *act)
//{
//	bActionChannel *achan; // XXX depreceated - old animation system
//	bActionGroup *agrp;
//
//	link_list(fd, &act.curves);
//	link_list(fd, &act.chanbase); // XXX depreceated - old animation system
//	link_list(fd, &act.groups);
//	link_list(fd, &act.markers);
//
//// XXX depreceated - old animation system <<<
//	for (achan = act.chanbase.first; achan; achan=achan.next) {
//		achan.grp= newdataadr(fd, achan.grp);
//
//		link_list(fd, &achan.constraintChannels);
//	}
//// >>> XXX depreceated - old animation system
//
//	direct_link_fcurves(fd, &act.curves);
//
//	for (agrp = act.groups.first; agrp; agrp= agrp.next) {
//		agrp.channels.first= newdataadr(fd, agrp.channels.first);
//		agrp.channels.last= newdataadr(fd, agrp.channels.last);
//	}
//}
//
//static void lib_link_nladata_strips(FileData *fd, ID *id, ListBase *list)
//{
//	NlaStrip *strip;
//
//	for (strip= list.first; strip; strip= strip.next) {
//		/* check strip's children */
//		lib_link_nladata_strips(fd, id, &strip.strips);
//
//		/* reassign the counted-reference to action */
//		strip.act = newlibadr_us(fd, id.lib, strip.act);
//	}
//}
//
//static void lib_link_nladata(FileData *fd, ID *id, ListBase *list)
//{
//	NlaTrack *nlt;
//
//	/* we only care about the NLA strips inside the tracks */
//	for (nlt= list.first; nlt; nlt= nlt.next) {
//		lib_link_nladata_strips(fd, id, &nlt.strips);
//	}
//}
//
///* This handles Animato NLA-Strips linking
// * NOTE: this assumes that link_list has already been called on the list
// */
//static void direct_link_nladata_strips(FileData *fd, ListBase *list)
//{
//	NlaStrip *strip;
//
//	for (strip= list.first; strip; strip= strip.next) {
//		/* strip's child strips */
//		link_list(fd, &strip.strips);
//		direct_link_nladata_strips(fd, &strip.strips);
//
//		/* strip's F-Curves */
//		link_list(fd, &strip.fcurves);
//		direct_link_fcurves(fd, &strip.fcurves);
//
//		/* strip's F-Modifiers */
//		link_list(fd, &strip.modifiers);
//		direct_link_fcurves(fd, &strip.modifiers);
//	}
//}
//
///* NOTE: this assumes that link_list has already been called on the list */
//static void direct_link_nladata(FileData *fd, ListBase *list)
//{
//	NlaTrack *nlt;
//
//	for (nlt= list.first; nlt; nlt= nlt.next) {
//		/* relink list of strips */
//		link_list(fd, &nlt.strips);
//
//		/* relink strip data */
//		direct_link_nladata_strips(fd, &nlt.strips);
//	}
//}
//
///* ------- */
//
//static void lib_link_keyingsets(FileData *fd, ID *id, ListBase *list)
//{
//	KeyingSet *ks;
//	KS_Path *ksp;
//
//	/* here, we're only interested in the ID pointer stored in some of the paths */
//	for (ks= list.first; ks; ks= ks.next) {
//		for (ksp= ks.paths.first; ksp; ksp= ksp.next) {
//			ksp.id= newlibadr(fd, id.lib, ksp.id);
//		}
//	}
//}
//
///* NOTE: this assumes that link_list has already been called on the list */
//static void direct_link_keyingsets(FileData *fd, ListBase *list)
//{
//	KeyingSet *ks;
//	KS_Path *ksp;
//
//	/* link KeyingSet data to KeyingSet again (non ID-libs) */
//	for (ks= list.first; ks; ks= ks.next) {
//		/* paths */
//		link_list(fd, &ks.paths);
//
//		for (ksp= ks.paths.first; ksp; ksp= ksp.next) {
//			/* rna path */
//			ksp.rna_path= newdataadr(fd, ksp.rna_path);
//		}
//	}
//}
//
///* ------- */
//
//static void lib_link_animdata(FileData *fd, ID *id, AnimData *adt)
//{
//	if (adt == NULL)
//		return;
//
//	/* link action data */
//	adt.action= newlibadr_us(fd, id.lib, adt.action);
//	adt.tmpact= newlibadr_us(fd, id.lib, adt.tmpact);
//
//	/* link drivers */
//	lib_link_fcurves(fd, id, &adt.drivers);
//
//	/* overrides don't have lib-link for now, so no need to do anything */
//
//	/* link NLA-data */
//	lib_link_nladata(fd, id, &adt.nla_tracks);
//}
//
//static void direct_link_animdata(FileData *fd, AnimData *adt)
//{
//	/* NOTE: must have called newdataadr already before doing this... */
//	if (adt == NULL)
//		return;
//
//	/* link drivers */
//	link_list(fd, &adt.drivers);
//	direct_link_fcurves(fd, &adt.drivers);
//
//	/* link overrides */
//	// TODO...
//
//	/* link NLA-data */
//	link_list(fd, &adt.nla_tracks);
//	direct_link_nladata(fd, &adt.nla_tracks);
//
//	/* clear temp pointers that may have been set... */
//	// TODO: it's probably only a small cost to reload this anyway...
//	adt.actstrip= NULL;
//}
//
///* ************ READ NODE TREE *************** */
//
///* singe node tree (also used for material/scene trees), ntree is not NULL */
//static void lib_link_ntree(FileData *fd, ID *id, bNodeTree *ntree)
//{
//	bNode *node;
//
//	if(ntree.adt) lib_link_animdata(fd, &ntree.id, ntree.adt);
//
//	for(node= ntree.nodes.first; node; node= node.next)
//		node.id= newlibadr_us(fd, id.lib, node.id);
//}
//
///* library ntree linking after fileread */
//static void lib_link_nodetree(FileData *fd, Main *main)
//{
//	bNodeTree *ntree;
//
//	/* only link ID pointers */
//	for(ntree= main.nodetree.first; ntree; ntree= ntree.id.next) {
//		if(ntree.id.flag & LIB_NEEDLINK) {
//			ntree.id.flag -= LIB_NEEDLINK;
//			lib_link_ntree(fd, &ntree.id, ntree);
//		}
//	}
//}

/* verify types for nodes and groups, all data has to be read */
/* open = 0: appending/linking, open = 1: open new file (need to clean out dynamic
* typedefs*/
public static void lib_verify_nodetree(Main main, int open)
{
//	Scene *sce;
//	Material *ma;
//	Tex *tx;
//	bNodeTree *ntree;
//
//	/* this crashes blender on undo/redo
//		if(open==1) {
//			reinit_nodesystem();
//		}*/
//
//	/* now create the own typeinfo structs an verify nodes */
//	/* here we still assume no groups in groups */
//	for(ntree= main.nodetree.first; ntree; ntree= ntree.id.next) {
//		ntreeVerifyTypes(ntree);	/* internal nodes, no groups! */
//		ntreeMakeOwnType(ntree);	/* for group usage */
//	}
//
//	/* now verify all types in material trees, groups are set OK now */
//	for(ma= main.mat.first; ma; ma= ma.id.next) {
//		if(ma.nodetree)
//			ntreeVerifyTypes(ma.nodetree);
//	}
//	/* and scene trees */
//	for(sce= main.scene.first; sce; sce= sce.id.next) {
//		if(sce.nodetree)
//			ntreeVerifyTypes(sce.nodetree);
//	}
//	/* and texture trees */
//	for(tx= main.tex.first; tx; tx= tx.id.next) {
//		if(tx.nodetree)
//			ntreeVerifyTypes(tx.nodetree);
//	}
}



///* ntree itself has been read! */
//static void direct_link_nodetree(FileData *fd, bNodeTree *ntree)
//{
//	/* note: writing and reading goes in sync, for speed */
//	bNode *node;
//	bNodeSocket *sock;
//	bNodeLink *link;
//
//	ntree.init= 0;		/* to set callbacks and force setting types */
//	ntree.owntype= NULL;
//	ntree.timecursor= NULL;
//
//	ntree.adt= newdataadr(fd, ntree.adt);
//	direct_link_animdata(fd, ntree.adt);
//
//	link_list(fd, &ntree.nodes);
//	for(node= ntree.nodes.first; node; node= node.next) {
//		if(node.type == NODE_DYNAMIC) {
//			node.custom1= 0;
//			node.custom1= BSET(node.custom1, NODE_DYNAMIC_LOADED);
//			node.typeinfo= NULL;
//		}
//
//		node.storage= newdataadr(fd, node.storage);
//		if(node.storage) {
//
//			/* could be handlerized at some point */
//			if(ntree.type==NTREE_SHADER && (node.type==SH_NODE_CURVE_VEC || node.type==SH_NODE_CURVE_RGB))
//				direct_link_curvemapping(fd, node.storage);
//			else if(ntree.type==NTREE_COMPOSIT) {
//				if( ELEM3(node.type, CMP_NODE_TIME, CMP_NODE_CURVE_VEC, CMP_NODE_CURVE_RGB))
//					direct_link_curvemapping(fd, node.storage);
//				else if(ELEM3(node.type, CMP_NODE_IMAGE, CMP_NODE_VIEWER, CMP_NODE_SPLITVIEWER))
//					((ImageUser *)node.storage).ok= 1;
//			}
//			else if( ntree.type==NTREE_TEXTURE && (node.type==TEX_NODE_CURVE_RGB || node.type==TEX_NODE_CURVE_TIME) ) {
//				direct_link_curvemapping(fd, node.storage);
//			}
//		}
//		link_list(fd, &node.inputs);
//		link_list(fd, &node.outputs);
//	}
//	link_list(fd, &ntree.links);
//
//	/* and we connect the rest */
//	for(node= ntree.nodes.first; node; node= node.next) {
//		node.preview= newimaadr(fd, node.preview);
//		node.lasty= 0;
//		for(sock= node.inputs.first; sock; sock= sock.next)
//			sock.link= newdataadr(fd, sock.link);
//		for(sock= node.outputs.first; sock; sock= sock.next)
//			sock.ns.data= NULL;
//	}
//	for(link= ntree.links.first; link; link= link.next) {
//		link.fromnode= newdataadr(fd, link.fromnode);
//		link.tonode= newdataadr(fd, link.tonode);
//		link.fromsock= newdataadr(fd, link.fromsock);
//		link.tosock= newdataadr(fd, link.tosock);
//	}
//
//	/* set selin and selout */
//	for(node= ntree.nodes.first; node; node= node.next) {
//		for(sock= node.inputs.first; sock; sock= sock.next) {
//			if(sock.flag & SOCK_SEL) {
//				ntree.selin= sock;
//				break;
//			}
//		}
//		for(sock= node.outputs.first; sock; sock= sock.next) {
//			if(sock.flag & SOCK_SEL) {
//				ntree.selout= sock;
//				break;
//			}
//		}
//	}
//
//	/* type verification is in lib-link */
//}
//
///* ************ READ ARMATURE ***************** */
//
//static void lib_link_constraints(FileData *fd, ID *id, ListBase *conlist)
//{
//	bConstraint *con;
//
//	for (con = conlist.first; con; con=con.next) {
//		/* patch for error introduced by changing constraints (dunno how) */
//		/* if con.data type changes, dna cannot resolve the pointer! (ton) */
//		if(con.data==NULL) {
//			con.type= CONSTRAINT_TYPE_NULL;
//		}
//		/* own ipo, all constraints have it */
//		con.ipo= newlibadr_us(fd, id.lib, con.ipo); // XXX depreceated - old animation system
//
//		switch (con.type) {
//		case CONSTRAINT_TYPE_PYTHON:
//			{
//				bPythonConstraint *data= (bPythonConstraint*)con.data;
//				bConstraintTarget *ct;
//
//				for (ct= data.targets.first; ct; ct= ct.next)
//					ct.tar = newlibadr(fd, id.lib, ct.tar);
//
//				data.text = newlibadr(fd, id.lib, data.text);
//				//IDP_LibLinkProperty(data.prop, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//			}
//			break;
//		case CONSTRAINT_TYPE_ACTION:
//			{
//				bActionConstraint *data;
//				data= ((bActionConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//				data.act = newlibadr(fd, id.lib, data.act);
//			}
//			break;
//		case CONSTRAINT_TYPE_LOCLIKE:
//			{
//				bLocateLikeConstraint *data;
//				data= ((bLocateLikeConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_ROTLIKE:
//			{
//				bRotateLikeConstraint *data;
//				data= ((bRotateLikeConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_SIZELIKE:
//			{
//				bSizeLikeConstraint *data;
//				data= ((bSizeLikeConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_KINEMATIC:
//			{
//				bKinematicConstraint *data;
//				data = ((bKinematicConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//				data.poletar = newlibadr(fd, id.lib, data.poletar);
//			}
//			break;
//		case CONSTRAINT_TYPE_TRACKTO:
//			{
//				bTrackToConstraint *data;
//				data = ((bTrackToConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_MINMAX:
//			{
//				bMinMaxConstraint *data;
//				data = ((bMinMaxConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_LOCKTRACK:
//			{
//				bLockTrackConstraint *data;
//				data= ((bLockTrackConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_FOLLOWPATH:
//			{
//				bFollowPathConstraint *data;
//				data= ((bFollowPathConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_STRETCHTO:
//			{
//				bStretchToConstraint *data;
//				data= ((bStretchToConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_RIGIDBODYJOINT:
//			{
//				bRigidBodyJointConstraint *data;
//				data= ((bRigidBodyJointConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_CLAMPTO:
//			{
//				bClampToConstraint *data;
//				data= ((bClampToConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_CHILDOF:
//			{
//				bChildOfConstraint *data;
//				data= ((bChildOfConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_TRANSFORM:
//			{
//				bTransformConstraint *data;
//				data= ((bTransformConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_DISTLIMIT:
//			{
//				bDistLimitConstraint *data;
//				data= ((bDistLimitConstraint*)con.data);
//				data.tar = newlibadr(fd, id.lib, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_SHRINKWRAP:
//			{
//				bShrinkwrapConstraint *data;
//				data= ((bShrinkwrapConstraint*)con.data);
//				data.target = newlibadr(fd, id.lib, data.target);
//			}
//			break;
//		case CONSTRAINT_TYPE_NULL:
//			break;
//		}
//	}
//}
//
//static void direct_link_constraints(FileData *fd, ListBase *lb)
//{
//	bConstraint *cons;
//
//	link_list(fd, lb);
//	for (cons=lb.first; cons; cons=cons.next) {
//		cons.data = newdataadr(fd, cons.data);
//
//		if (cons.type == CONSTRAINT_TYPE_PYTHON) {
//			bPythonConstraint *data= cons.data;
//
//			link_list(fd, &data.targets);
//
//			data.prop = newdataadr(fd, data.prop);
//			if (data.prop)
//				IDP_DirectLinkProperty(data.prop, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//		}
//	}
//}
//
//static void lib_link_pose(FileData *fd, Object *ob, bPose *pose)
//{
//	bPoseChannel *pchan;
//	bArmature *arm= ob.data;
//	int rebuild;
//
//	if (!pose || !arm)
//		return;
//
//	/* always rebuild to match proxy or lib changes */
//	rebuild= ob.proxy || (ob.id.lib==NULL && arm.id.lib);
//
//	for (pchan = pose.chanbase.first; pchan; pchan=pchan.next) {
//		lib_link_constraints(fd, (ID *)ob, &pchan.constraints);
//
//		/* hurms... loop in a loop, but yah... later... (ton) */
//		pchan.bone= get_named_bone(arm, pchan.name);
//
//		pchan.custom= newlibadr(fd, arm.id.lib, pchan.custom);
//		if(pchan.bone==NULL)
//			rebuild= 1;
//		else if(ob.id.lib==NULL && arm.id.lib) {
//			/* local pose selection copied to armature, bit hackish */
//			pchan.bone.flag &= ~(BONE_SELECTED|BONE_ACTIVE);
//			pchan.bone.flag |= pchan.selectflag;
//		}
//	}
//
//	if(rebuild) {
//		ob.recalc= OB_RECALC;
//		pose.flag |= POSE_RECALC;
//	}
//}
//
//static void lib_link_armature(FileData *fd, Main *main)
//{
//	bArmature *arm;
//
//	arm= main.armature.first;
//
//	while(arm) {
//		if(arm.id.flag & LIB_NEEDLINK) {
//			arm.id.flag -= LIB_NEEDLINK;
//		}
//		arm= arm.id.next;
//	}
//}
//
//static void direct_link_bones(FileData *fd, Bone* bone)
//{
//	Bone	*child;
//
//	bone.parent= newdataadr(fd, bone.parent);
//
//	link_list(fd, &bone.childbase);
//
//	for (child=bone.childbase.first; child; child=child.next) {
//		direct_link_bones(fd, child);
//	}
//}
//
//static void direct_link_armature(FileData *fd, bArmature *arm)
//{
//	Bone	*bone;
//
//	link_list(fd, &arm.bonebase);
//	arm.edbo= NULL;
//	arm.sketch = NULL;
//
//	bone=arm.bonebase.first;
//	while (bone) {
//		direct_link_bones(fd, bone);
//		bone=bone.next;
//	}
//}

/* ************ READ CAMERA ***************** */

public static void lib_link_camera(FileData fd, Main main)
{
	Camera ca;

	ca= main.camera.first;
	while(ca!=null) {
		if((ca.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
//			if (ca.adt) lib_link_animdata(fd, &ca.id, ca.adt);

//			ca.ipo= newlibadr_us(fd, ca.id.lib, ca.ipo); // XXX depreceated - old animation system

			ca.dof_ob= (bObject)newlibadr_us(fd, ca.id.lib, ca.dof_ob);

			ca.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
		ca= (Camera)ca.id.next;
	}
}

public static void direct_link_camera(FileData fd, Camera ca)
{
	ca.adt= (AnimData)newdataadr(fd, ca.adt);
//	direct_link_animdata(fd, ca.adt);
}


/* ************ READ LAMP ***************** */

public static void lib_link_lamp(FileData fd, Main main)
{
	Lamp la;
	MTex mtex;
	int a;

	la= main.lamp.first;
	while(la!=null) {
		if((la.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
//			if (la.adt) lib_link_animdata(fd, &la.id, la.adt);

			for(a=0; a<TextureTypes.MAX_MTEX; a++) {
				mtex= la.mtex[a];
				if(mtex!=null) {
					mtex.tex= (Tex)newlibadr_us(fd, la.id.lib, mtex.tex);
					mtex.object= (bObject)newlibadr(fd, la.id.lib, mtex.object);
				}
			}

//			la.ipo= newlibadr_us(fd, la.id.lib, la.ipo); // XXX depreceated - old animation system

			la.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
		la= (Lamp)la.id.next;
	}
}

public static void direct_link_lamp(FileData fd, Lamp la)
{
	int a;

	la.adt= (AnimData)newdataadr(fd, la.adt);
//	direct_link_animdata(fd, la.adt);

	for(a=0; a<TextureTypes.MAX_MTEX; a++) {
		la.mtex[a]= (MTex)newdataadr(fd, la.mtex[a]);
	}

	la.curfalloff= (CurveMapping)newdataadr(fd, la.curfalloff);
//	if(la.curfalloff)
//		direct_link_curvemapping(fd, la.curfalloff);

	la.preview = direct_link_preview_image(fd, la.preview);
}

///* ************ READ keys ***************** */
//
//static void lib_link_key(FileData *fd, Main *main)
//{
//	Key *key;
//
//	key= main.key.first;
//	while(key) {
//		if(key.id.flag & LIB_NEEDLINK) {
//			if(key.adt) lib_link_animdata(fd, &key.id, key.adt);
//
//			key.ipo= newlibadr_us(fd, key.id.lib, key.ipo); // XXX depreceated - old animation system
//			key.from= newlibadr(fd, key.id.lib, key.from);
//
//			key.id.flag -= LIB_NEEDLINK;
//		}
//		key= key.id.next;
//	}
//}
//
//static void switch_endian_keyblock(Key *key, KeyBlock *kb)
//{
//	int elemsize, a, b;
//	char *data, *poin, *cp;
//
//	elemsize= key.elemsize;
//	data= kb.data;
//
//	for(a=0; a<kb.totelem; a++) {
//
//		cp= key.elemstr;
//		poin= data;
//
//		while( cp[0] ) {	/* cp[0]==amount */
//
//			switch(cp[1]) {		/* cp[1]= type */
//			case IPO_FLOAT:
//			case IPO_BPOINT:
//			case IPO_BEZTRIPLE:
//				b= cp[0];
//				while(b--) {
//					SWITCH_INT((*poin));
//					poin+= 4;
//				}
//				break;
//			}
//
//			cp+= 2;
//
//		}
//		data+= elemsize;
//	}
//}
//
//static void direct_link_key(FileData *fd, Key *key)
//{
//	KeyBlock *kb;
//
//	link_list(fd, &(key.block));
//
//	key.adt= newdataadr(fd, key.adt);
//	direct_link_animdata(fd, key.adt);
//
//	key.refkey= newdataadr(fd, key.refkey);
//
//	kb= key.block.first;
//	while(kb) {
//
//		kb.data= newdataadr(fd, kb.data);
//
//		if(fd.flags & FD_FLAGS_SWITCH_ENDIAN)
//			switch_endian_keyblock(key, kb);
//
//		kb= kb.next;
//	}
//}
//
///* ************ READ mball ***************** */
//
//static void lib_link_mball(FileData *fd, Main *main)
//{
//	MetaBall *mb;
//	int a;
//
//	mb= main.mball.first;
//	while(mb) {
//		if(mb.id.flag & LIB_NEEDLINK) {
//
//			for(a=0; a<mb.totcol; a++) mb.mat[a]= newlibadr_us(fd, mb.id.lib, mb.mat[a]);
//
//			mb.ipo= newlibadr_us(fd, mb.id.lib, mb.ipo); // XXX depreceated - old animation system
//
//			mb.id.flag -= LIB_NEEDLINK;
//		}
//		mb= mb.id.next;
//	}
//}
//
//static void direct_link_mball(FileData *fd, MetaBall *mb)
//{
//	mb.mat= newdataadr(fd, mb.mat);
//	test_pointer_array(fd, (void **)&mb.mat);
//
//	link_list(fd, &(mb.elems));
//
//	mb.disp.first= mb.disp.last= NULL;
//	mb.editelems= NULL;
//	mb.bb= NULL;
//}

/* ************ READ WORLD ***************** */

public static void lib_link_world(FileData fd, Main main)
{
	World wrld;
	MTex mtex;
	int a;

	wrld= main.world.first;
	while(wrld!=null) {
		if((wrld.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
//			if (wrld.adt) lib_link_animdata(fd, &wrld.id, wrld.adt);

//			wrld.ipo= newlibadr_us(fd, wrld.id.lib, wrld.ipo); // XXX depreceated - old animation system

			for(a=0; a<TextureTypes.MAX_MTEX; a++) {
				mtex= wrld.mtex[a];
				if(mtex!=null) {
					mtex.tex= (Tex)newlibadr_us(fd, wrld.id.lib, mtex.tex);
					mtex.object= (bObject)newlibadr(fd, wrld.id.lib, mtex.object);
				}
			}

			wrld.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
		wrld= (World)wrld.id.next;
	}
}

public static void direct_link_world(FileData fd, World wrld)
{
	int a;

	wrld.adt= (AnimData)newdataadr(fd, wrld.adt);
//	direct_link_animdata(fd, wrld.adt);

	for(a=0; a<TextureTypes.MAX_MTEX; a++) {
		wrld.mtex[a]= (MTex)newdataadr(fd, wrld.mtex[a]);
	}
	wrld.preview = direct_link_preview_image(fd, wrld.preview);
}


///* ************ READ VFONT ***************** */
//
//static void lib_link_vfont(FileData *fd, Main *main)
//{
//	VFont *vf;
//
//	vf= main.vfont.first;
//	while(vf) {
//		if(vf.id.flag & LIB_NEEDLINK) {
//			vf.id.flag -= LIB_NEEDLINK;
//		}
//		vf= vf.id.next;
//	}
//}
//
//static void direct_link_vfont(FileData *fd, VFont *vf)
//{
//	vf.data= NULL;
//	vf.packedfile= direct_link_packedfile(fd, vf.packedfile);
//}
//
///* ************ READ TEXT ****************** */
//
//static void lib_link_text(FileData *fd, Main *main)
//{
//	Text *text;
//
//	text= main.text.first;
//	while(text) {
//		if(text.id.flag & LIB_NEEDLINK) {
//			text.id.flag -= LIB_NEEDLINK;
//		}
//		text= text.id.next;
//	}
//}
//
//static void direct_link_text(FileData *fd, Text *text)
//{
//	TextLine *ln;
//
//	text.name= newdataadr(fd, text.name);
//
//	text.undo_pos= -1;
//	text.undo_len= TXT_INIT_UNDO;
//	text.undo_buf= MEM_mallocN(text.undo_len, "undo buf");
//
//	text.compiled= NULL;
//
///*
//	if(text.flags & TXT_ISEXT) {
//		reopen_text(text);
//	} else {
//*/
//
//	link_list(fd, &text.lines);
//	link_list(fd, &text.markers);
//
//	text.curl= newdataadr(fd, text.curl);
//	text.sell= newdataadr(fd, text.sell);
//
//	ln= text.lines.first;
//	while(ln) {
//		ln.line= newdataadr(fd, ln.line);
//		ln.format= NULL;
//
//		if (ln.len != (int) strlen(ln.line)) {
//			printf("Error loading text, line lengths differ\n");
//			ln.len = strlen(ln.line);
//		}
//
//		ln= ln.next;
//	}
//
//	text.flags = (text.flags) & ~TXT_ISEXT;
//
//	text.id.us= 1;
//}

/* ************ READ IMAGE ***************** */

public static void lib_link_image(FileData fd, Main main)
{
	Image ima;

	ima= (Image)main.image.first;
	while (ima!=null) {
		if((ima.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
//			if (ima.id.properties) IDP_LibLinkProperty(ima.id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);

			ima.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
		ima= (Image)ima.id.next;
	}
}

    public static void link_ibuf_list(FileData fd, ListBase lb) {
        Link ln, prev;

        if (lb.first == null) {
            return;
        }

        lb.first = newimaadr(fd, lb.first);
        ln = (Link) lb.first;
        prev = null;
        while (ln != null) {
            ln.next = newimaadr(fd, ln.next);
            ln.prev = prev;
            prev = ln;
            ln = (Link) ln.next;
        }
        lb.last = prev;
    }

    public static void direct_link_image(FileData fd, Image ima) {
        /* for undo system, pointers could be restored */
        if (fd.imamap != null) {
            link_ibuf_list(fd, ima.ibufs);
        } else {
            ima.ibufs.first = ima.ibufs.last = null;
        }

        /* if not restored, we keep the binded opengl index */
        if (ima.ibufs.first == null) {
            ima.bindcode = 0;
            ima.gputexture = null;
        }

        ima.anim = null;
        ima.rr = null;
        ima.repbind = null;
//        ima.render_text= newdataadr(fd, ima.render_text);

        ima.packedfile = direct_link_packedfile(fd, ima.packedfile);
        ima.preview = direct_link_preview_image(fd, ima.preview);
        ima.ok = 1;
    }


///* ************ READ CURVE ***************** */
//
//static void lib_link_curve(FileData *fd, Main *main)
//{
//	Curve *cu;
//	int a;
//
//	cu= main.curve.first;
//	while(cu) {
//		if(cu.id.flag & LIB_NEEDLINK) {
//			if(cu.adt) lib_link_animdata(fd, &cu.id, cu.adt);
//
//			for(a=0; a<cu.totcol; a++) cu.mat[a]= newlibadr_us(fd, cu.id.lib, cu.mat[a]);
//
//			cu.bevobj= newlibadr(fd, cu.id.lib, cu.bevobj);
//			cu.taperobj= newlibadr(fd, cu.id.lib, cu.taperobj);
//			cu.textoncurve= newlibadr(fd, cu.id.lib, cu.textoncurve);
//			cu.vfont= newlibadr_us(fd, cu.id.lib, cu.vfont);
//			cu.vfontb= newlibadr_us(fd, cu.id.lib, cu.vfontb);
//			cu.vfonti= newlibadr_us(fd, cu.id.lib, cu.vfonti);
//			cu.vfontbi= newlibadr_us(fd, cu.id.lib, cu.vfontbi);
//
//			cu.ipo= newlibadr_us(fd, cu.id.lib, cu.ipo); // XXX depreceated - old animation system
//			cu.key= newlibadr_us(fd, cu.id.lib, cu.key);
//
//			cu.id.flag -= LIB_NEEDLINK;
//		}
//		cu= cu.id.next;
//	}
//}
//
//
//static void switch_endian_knots(Nurb *nu)
//{
//	int len;
//
//	if(nu.knotsu) {
//		len= KNOTSU(nu);
//		while(len--) {
//			SWITCH_INT(nu.knotsu[len]);
//		}
//	}
//	if(nu.knotsv) {
//		len= KNOTSV(nu);
//		while(len--) {
//			SWITCH_INT(nu.knotsv[len]);
//		}
//	}
//}
//
//static void direct_link_curve(FileData *fd, Curve *cu)
//{
//	Nurb *nu;
//	TextBox *tb;
//
//	cu.adt= newdataadr(fd, cu.adt);
//	direct_link_animdata(fd, cu.adt);
//
//	cu.mat= newdataadr(fd, cu.mat);
//	test_pointer_array(fd, (void **)&cu.mat);
//	cu.str= newdataadr(fd, cu.str);
//	cu.strinfo= newdataadr(fd, cu.strinfo);
//	cu.tb= newdataadr(fd, cu.tb);
//
//	if(cu.vfont==0) link_list(fd, &(cu.nurb));
//	else {
//		cu.nurb.first=cu.nurb.last= 0;
//
//		tb= MEM_callocN(MAXTEXTBOX*sizeof(TextBox), "TextBoxread");
//		if (cu.tb) {
//			memcpy(tb, cu.tb, cu.totbox*sizeof(TextBox));
//			MEM_freeN(cu.tb);
//			cu.tb= tb;
//		} else {
//			cu.totbox = 1;
//			cu.actbox = 1;
//			cu.tb = tb;
//			cu.tb[0].w = cu.linewidth;
//		}
//		if (cu.wordspace == 0.0) cu.wordspace = 1.0;
//	}
//
//	cu.bev.first=cu.bev.last= NULL;
//	cu.disp.first=cu.disp.last= NULL;
//	cu.editnurb= NULL;
//	cu.lastselbp= NULL;
//	cu.path= NULL;
//	cu.editfont= NULL;
//
//	nu= cu.nurb.first;
//	while(nu) {
//		nu.bezt= newdataadr(fd, nu.bezt);
//		nu.bp= newdataadr(fd, nu.bp);
//		nu.knotsu= newdataadr(fd, nu.knotsu);
//		nu.knotsv= newdataadr(fd, nu.knotsv);
//		if (cu.vfont==0) nu.charidx= nu.mat_nr;
//
//		if(fd.flags & FD_FLAGS_SWITCH_ENDIAN) {
//			switch_endian_knots(nu);
//		}
//
//		nu= nu.next;
//	}
//	cu.bb= NULL;
//}
//
///* ************ READ TEX ***************** */
//
//static void lib_link_texture(FileData *fd, Main *main)
//{
//	Tex *tex;
//
//	tex= main.tex.first;
//	while(tex) {
//		if(tex.id.flag & LIB_NEEDLINK) {
//			if(tex.adt) lib_link_animdata(fd, &tex.id, tex.adt);
//
//			tex.ima= newlibadr_us(fd, tex.id.lib, tex.ima);
//			tex.ipo= newlibadr_us(fd, tex.id.lib, tex.ipo);
//			if(tex.env) tex.env.object= newlibadr(fd, tex.id.lib, tex.env.object);
//
//			if(tex.nodetree)
//				lib_link_ntree(fd, &tex.id, tex.nodetree);
//
//			tex.id.flag -= LIB_NEEDLINK;
//		}
//		tex= tex.id.next;
//	}
//}
//
//static void direct_link_texture(FileData *fd, Tex *tex)
//{
//	tex.adt= newdataadr(fd, tex.adt);
//	direct_link_animdata(fd, tex.adt);
//
//	tex.plugin= newdataadr(fd, tex.plugin);
//	if(tex.plugin) {
//		tex.plugin.handle= 0;
//		open_plugin_tex(tex.plugin);
//		/* initialize data for this instance, if an initialization
//		 * function exists.
//		 */
//		if (tex.plugin.instance_init)
//			tex.plugin.instance_init((void *) tex.plugin.data);
//	}
//	tex.coba= newdataadr(fd, tex.coba);
//	tex.env= newdataadr(fd, tex.env);
//	if(tex.env) {
//		tex.env.ima= NULL;
//		memset(tex.env.cube, 0, 6*sizeof(void *));
//		tex.env.ok= 0;
//	}
//
//	tex.nodetree= newdataadr(fd, tex.nodetree);
//	if(tex.nodetree)
//		direct_link_nodetree(fd, tex.nodetree);
//
//	tex.preview = direct_link_preview_image(fd, tex.preview);
//
//	tex.iuser.ok= 1;
//}
//
//
//
///* ************ READ MATERIAL ***************** */
//
//static void lib_link_material(FileData *fd, Main *main)
//{
//	Material *ma;
//	MTex *mtex;
//	int a;
//
//	ma= main.mat.first;
//	while(ma) {
//		if(ma.id.flag & LIB_NEEDLINK) {
//			if(ma.adt) lib_link_animdata(fd, &ma.id, ma.adt);
//
//			/*Link ID Properties -- and copy this comment EXACTLY for easy finding
//			of library blocks that implement this.*/
//			if (ma.id.properties) IDP_LibLinkProperty(ma.id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//
//			ma.ipo= newlibadr_us(fd, ma.id.lib, ma.ipo);
//			ma.group= newlibadr_us(fd, ma.id.lib, ma.group);
//
//			for(a=0; a<MAX_MTEX; a++) {
//				mtex= ma.mtex[a];
//				if(mtex) {
//					mtex.tex= newlibadr_us(fd, ma.id.lib, mtex.tex);
//					mtex.object= newlibadr(fd, ma.id.lib, mtex.object);
//				}
//			}
//
//			if(ma.nodetree)
//				lib_link_ntree(fd, &ma.id, ma.nodetree);
//
//			ma.id.flag -= LIB_NEEDLINK;
//		}
//		ma= ma.id.next;
//	}
//}
//
//static void direct_link_material(FileData *fd, Material *ma)
//{
//	int a;
//
//	ma.adt= newdataadr(fd, ma.adt);
//	direct_link_animdata(fd, ma.adt);
//
//	for(a=0; a<MAX_MTEX; a++) {
//		ma.mtex[a]= newdataadr(fd, ma.mtex[a]);
//	}
//
//	ma.ramp_col= newdataadr(fd, ma.ramp_col);
//	ma.ramp_spec= newdataadr(fd, ma.ramp_spec);
//
//	ma.nodetree= newdataadr(fd, ma.nodetree);
//	if(ma.nodetree)
//		direct_link_nodetree(fd, ma.nodetree);
//
//	ma.preview = direct_link_preview_image(fd, ma.preview);
//	ma.gpumaterial.first = ma.gpumaterial.last = NULL;
//}
//
///* ************ READ PARTICLE SETTINGS ***************** */
//
//static void direct_link_pointcache(FileData *fd, PointCache *cache)
//{
//	if((cache.flag & PTCACHE_DISK_CACHE)==0) {
//		PTCacheMem *pm;
//
//		link_list(fd, &cache.mem_cache);
//
//		pm = cache.mem_cache.first;
//
//		for(; pm; pm=pm.next)
//			pm.data = newdataadr(fd, pm.data);
//	}
//	else
//		cache.mem_cache.first = cache.mem_cache.last = NULL;
//
//	cache.flag &= ~(PTCACHE_SIMULATION_VALID|PTCACHE_BAKE_EDIT_ACTIVE);
//	cache.simframe= 0;
//}
//
//static void lib_link_particlesettings(FileData *fd, Main *main)
//{
//	ParticleSettings *part;
//
//	part= main.particle.first;
//	while(part) {
//		if(part.id.flag & LIB_NEEDLINK) {
//			if (part.adt) lib_link_animdata(fd, &part.id, part.adt);
//			part.ipo= newlibadr_us(fd, part.id.lib, part.ipo); // XXX depreceated - old animation system
//
//			part.dup_ob = newlibadr(fd, part.id.lib, part.dup_ob);
//			part.dup_group = newlibadr(fd, part.id.lib, part.dup_group);
//			part.eff_group = newlibadr(fd, part.id.lib, part.eff_group);
//			part.bb_ob = newlibadr(fd, part.id.lib, part.bb_ob);
//			if(part.boids) {
//				BoidState *state = part.boids.states.first;
//				BoidRule *rule;
//				for(; state; state=state.next) {
//					rule = state.rules.first;
//				for(; rule; rule=rule.next)
//					switch(rule.type) {
//						case eBoidRuleType_Goal:
//						case eBoidRuleType_Avoid:
//						{
//							BoidRuleGoalAvoid *brga = (BoidRuleGoalAvoid*)rule;
//							brga.ob = newlibadr(fd, part.id.lib, brga.ob);
//							break;
//						}
//						case eBoidRuleType_FollowLeader:
//						{
//							BoidRuleFollowLeader *brfl = (BoidRuleFollowLeader*)rule;
//							brfl.ob = newlibadr(fd, part.id.lib, brfl.ob);
//							break;
//						}
//					}
//				}
//			}
//			part.id.flag -= LIB_NEEDLINK;
//		}
//		part= part.id.next;
//	}
//}
//
//static void direct_link_particlesettings(FileData *fd, ParticleSettings *part)
//{
//	part.adt= newdataadr(fd, part.adt);
//	part.pd= newdataadr(fd, part.pd);
//	part.pd2= newdataadr(fd, part.pd2);
//
//	part.boids= newdataadr(fd, part.boids);
//
//	if(part.boids) {
//		BoidState *state;
//		link_list(fd, &part.boids.states);
//
//		for(state=part.boids.states.first; state; state=state.next) {
//			link_list(fd, &state.rules);
//			link_list(fd, &state.conditions);
//			link_list(fd, &state.actions);
//		}
//	}
//}
//
//static void lib_link_particlesystems(FileData *fd, Object *ob, ID *id, ListBase *particles)
//{
//	ParticleSystem *psys, *psysnext;
//	int a;
//
//	for(psys=particles.first; psys; psys=psysnext){
//		ParticleData *pa;
//
//		psysnext= psys.next;
//
//		psys.part = newlibadr_us(fd, id.lib, psys.part);
//		if(psys.part) {
//			ParticleTarget *pt = psys.targets.first;
//
//			for(; pt; pt=pt.next)
//				pt.ob=newlibadr(fd, id.lib, pt.ob);
//
//			psys.target_ob = newlibadr(fd, id.lib, psys.target_ob);
//
//			for(a=0,pa=psys.particles; a<psys.totpart; a++,pa++){
//				pa.stick_ob=newlibadr(fd, id.lib, pa.stick_ob);
//			}
//
//
//		}
//		else {
//			/* particle modifier must be removed before particle system */
//			ParticleSystemModifierData *psmd= psys_get_modifier(ob,psys);
//			BLI_remlink(&ob.modifiers, psmd);
//			modifier_free((ModifierData *)psmd);
//
//			BLI_remlink(particles, psys);
//			MEM_freeN(psys);
//		}
//	}
//}
//static void direct_link_particlesystems(FileData *fd, ListBase *particles)
//{
//	ParticleSystem *psys;
//	ParticleData *pa;
//	int a;
//
//	for(psys=particles.first; psys; psys=psys.next) {
//		psys.particles=newdataadr(fd,psys.particles);
//
//		if(psys.particles && psys.particles.hair){
//			for(a=0,pa=psys.particles; a<psys.totpart; a++, pa++)
//				pa.hair=newdataadr(fd,pa.hair);
//		}
//
//		if(psys.particles && psys.particles.keys){
//			for(a=0,pa=psys.particles; a<psys.totpart; a++, pa++) {
//				pa.keys= NULL;
//				pa.totkey= 0;
//			}
//
//			psys.flag &= ~PSYS_KEYED;
//		}
//
//		if(psys.particles.boid) {
//			pa = psys.particles;
//			pa.boid = newdataadr(fd, pa.boid);
//			for(a=1,pa++; a<psys.totpart; a++, pa++)
//				pa.boid = (pa-1).boid + 1;
//		}
//		else {
//			for(a=0,pa=psys.particles; a<psys.totpart; a++, pa++)
//				pa.boid = NULL;
//		}
//
//
//		psys.child=newdataadr(fd,psys.child);
//		psys.effectors.first=psys.effectors.last=0;
//
//		psys.soft= newdataadr(fd, psys.soft);
//		if(psys.soft) {
//			SoftBody *sb = psys.soft;
//			sb.particles = psys;
//			sb.bpoint= NULL;	// init pointers so it gets rebuilt nicely
//			sb.bspring= NULL;
//			sb.scratch= NULL;
//
//			sb.pointcache= newdataadr(fd, sb.pointcache);
//			if(sb.pointcache)
//				direct_link_pointcache(fd, sb.pointcache);
//		}
//
//		link_list(fd, &psys.targets);
//
//		psys.edit = 0;
//		psys.free_edit = NULL;
//		psys.pathcache = 0;
//		psys.childcache = 0;
//		psys.pathcachebufs.first = psys.pathcachebufs.last = 0;
//		psys.childcachebufs.first = psys.childcachebufs.last = 0;
//		psys.reactevents.first = psys.reactevents.last = 0;
//
//		psys.pointcache= newdataadr(fd, psys.pointcache);
//		if(psys.pointcache)
//			direct_link_pointcache(fd, psys.pointcache);
//
//		psys.tree = NULL;
//	}
//	return;
//}

/* ************ READ MESH ***************** */

public static void lib_link_mtface(FileData fd, Mesh me, MTFace[] mtfaces, int totface)
{
	MTFace[] tfs= mtfaces;
	int i, tf_p;

	for (i=0, tf_p=0; i<totface; i++, tf_p++) {
                MTFace tf = tfs[tf_p];
		tf.tpage= (Image)newlibadr(fd, me.id.lib, tf.tpage);
		if(tf.tpage!=null && tf.tpage.id.us==0)
			tf.tpage.id.us= 1;
	}
}

public static void lib_link_customdata_mtface(FileData fd, Mesh me, CustomData fdata, int totface)
{
	int i;
	for(i=0; i<fdata.totlayer; i++) {
		CustomDataLayer layer = fdata.layers.myarray[i];

		if(layer.type == CustomDataTypes.CD_MTFACE)
			lib_link_mtface(fd, me, ((MTFace)layer.data).myarray, totface);
	}

}

public static void lib_link_mesh(FileData fd, Main main)
{
	Mesh me;

	me= main.mesh.first;
	while(me!=null) {
		if((me.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
			int i;

			/*Link ID Properties -- and copy this comment EXACTLY for easy finding
			of library blocks that implement this.*/
//			if (me.id.properties) IDP_LibLinkProperty(me.id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);

			/* this check added for python created meshes */
			if(me.mat!=null) {
				for(i=0; i<me.totcol; i++) {
					me.mat[i]= (Material)newlibadr_us(fd, me.id.lib, me.mat[i]);
				}
			}
			else me.totcol= 0;

//			me.ipo= newlibadr_us(fd, me.id.lib, me.ipo);
//			me.key= newlibadr_us(fd, me.id.lib, me.key);
			me.texcomesh= (Mesh)newlibadr_us(fd, me.id.lib, me.texcomesh);

			lib_link_customdata_mtface(fd, me, me.fdata, me.totface);
//			if(me.mr && me.mr.levels.first)
//				lib_link_customdata_mtface(fd, me, &me.mr.fdata,
//							   ((MultiresLevel*)me.mr.levels.first).totface);

			me.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
		me= (Mesh)me.id.next;
	}
}

    public static void direct_link_dverts(FileData fd, int count, MDeformVert mdverts) {
        if (mdverts == null) {
            return;
        }

        for (int i = 0; i < count; i++) {
            mdverts.myarray[i].dw = (MDeformWeight) newdataadr(fd, mdverts.myarray[i].dw);
            if (mdverts.myarray[i].dw == null) {
                mdverts.myarray[i].totweight = 0;
            }
        }
    }

public static void direct_link_mdisps(FileData fd, int count, MDisps mdisps)
{
	if(mdisps!=null) {
		int i;

		for(i = 0; i < count; ++i) {
			mdisps.myarray[i].disps = (Float)newdataadr(fd, mdisps.myarray[i].disps);
			if(mdisps.myarray[i].disps==0)
				mdisps.myarray[i].totdisp = 0;
		}
	}
}

    public static void direct_link_customdata(FileData fd, CustomData data, int count) {
        int i = 0;

        data.layers = (CustomDataLayer) newdataadr(fd, data.layers);

        while (i < data.totlayer) {
            CustomDataLayer layer = data.layers.myarray[i];

            if (CustomDataUtil.CustomData_verify_versions(data, i) != 0) {
                layer.data = (Object) newdataadr(fd, layer.data);
                if(layer.type == CustomDataTypes.CD_MDISPS) {
                        direct_link_mdisps(fd, count, (MDisps)layer.data);
                }
                i++;
            }
        }
    }

public static void direct_link_mesh(FileData fd, Mesh mesh)
{
	mesh.mat= (Material[])newdataadr(fd, mesh.mat);
//	test_pointer_array(fd, (void **)&mesh.mat);

	mesh.mvert= (MVert)newdataadr(fd, mesh.mvert);
	mesh.medge= (MEdge)newdataadr(fd, mesh.medge);
	mesh.mface= (MFace)newdataadr(fd, mesh.mface);
	mesh.tface= (TFace)newdataadr(fd, mesh.tface);
	mesh.mtface= (MTFace)newdataadr(fd, mesh.mtface);
	mesh.mcol= (MCol)newdataadr(fd, mesh.mcol);
	mesh.msticky= (MSticky)newdataadr(fd, mesh.msticky);
	mesh.dvert= (MDeformVert)newdataadr(fd, mesh.dvert);

//	/* Partial-mesh visibility (do this before using totvert, totface, or totedge!) */
//	mesh.pv= (PartialVisibility)newdataadr(fd, mesh.pv);
//	if(mesh.pv!=null) {
//		mesh.pv.vert_map= (Integer)newdataadr(fd, mesh.pv.vert_map);
//		mesh.pv.edge_map= (Integer)newdataadr(fd, mesh.pv.edge_map);
//		mesh.pv.old_faces= (MFace)newdataadr(fd, mesh.pv.old_faces);
//		mesh.pv.old_edges= (MEdge)newdataadr(fd, mesh.pv.old_edges);
//	}

	/* normally direct_link_dverts should be called in direct_link_customdata,
	   but for backwards compat in do_versions to work we do it here */
	//direct_link_dverts(fd, mesh.pv!=null ? mesh.pv.totvert : mesh.totvert, mesh.dvert);
	direct_link_dverts(fd, mesh.totvert, mesh.dvert);

	//direct_link_customdata(fd, mesh.vdata, mesh.pv!=null ? mesh.pv.totvert : mesh.totvert);
	direct_link_customdata(fd, mesh.vdata, mesh.totvert);
	//direct_link_customdata(fd, mesh.edata, mesh.pv!=null ? mesh.pv.totedge : mesh.totedge);
	direct_link_customdata(fd, mesh.edata, mesh.totedge);
	//direct_link_customdata(fd, mesh.fdata, mesh.pv!=null ? mesh.pv.totface : mesh.totface);
	direct_link_customdata(fd, mesh.fdata, mesh.totface);

	mesh.bb= null;
	mesh.mselect = null;
	mesh.edit_mesh= null;

//	/* Multires data */
//	mesh.mr= newdataadr(fd, mesh.mr);
//	if(mesh.mr) {
//		MultiresLevel *lvl;
//
//		link_list(fd, &mesh.mr.levels);
//		lvl= mesh.mr.levels.first;
//
//		direct_link_customdata(fd, &mesh.mr.vdata, lvl.totvert);
//		direct_link_dverts(fd, lvl.totvert, CustomData_get(&mesh.mr.vdata, 0, CD_MDEFORMVERT));
//		direct_link_customdata(fd, &mesh.mr.fdata, lvl.totface);
//
//		mesh.mr.edge_flags= newdataadr(fd, mesh.mr.edge_flags);
//		mesh.mr.edge_creases= newdataadr(fd, mesh.mr.edge_creases);
//
//		mesh.mr.verts = newdataadr(fd, mesh.mr.verts);
//
//		for(; lvl; lvl= lvl.next) {
//			lvl.verts= newdataadr(fd, lvl.verts);
//			lvl.faces= newdataadr(fd, lvl.faces);
//			lvl.edges= newdataadr(fd, lvl.edges);
//			lvl.colfaces= newdataadr(fd, lvl.colfaces);
//		}
//	}
//
//	/* Gracefully handle corrupted mesh */
//	if(mesh.mr && !mesh.mr.verts) {
//		/* If totals match, simply load the current mesh verts into multires */
//		if(mesh.totvert == ((MultiresLevel*)mesh.mr.levels.last).totvert)
//			mesh.mr.verts = MEM_dupallocN(mesh.mvert);
//		else {
//			/* Otherwise, we can't recover the data, silently remove multires */
//			multires_free(mesh.mr);
//			mesh.mr = NULL;
//		}
//	}
//
//	if((fd.flags & FD_FLAGS_SWITCH_ENDIAN) && mesh.tface) {
//		TFace *tf= mesh.tface;
//		unsigned int i;
//
//		for (i=0; i< (mesh.pv ? mesh.pv.totface : mesh.totface); i++, tf++) {
//			SWITCH_INT(tf.col[0]);
//			SWITCH_INT(tf.col[1]);
//			SWITCH_INT(tf.col[2]);
//			SWITCH_INT(tf.col[3]);
//		}
//	}
}

///* ************ READ LATTICE ***************** */
//
//static void lib_link_latt(FileData *fd, Main *main)
//{
//	Lattice *lt;
//
//	lt= main.latt.first;
//	while(lt) {
//		if(lt.id.flag & LIB_NEEDLINK) {
//
//			lt.ipo= newlibadr_us(fd, lt.id.lib, lt.ipo); // XXX depreceated - old animation system
//			lt.key= newlibadr_us(fd, lt.id.lib, lt.key);
//
//			lt.id.flag -= LIB_NEEDLINK;
//		}
//		lt= lt.id.next;
//	}
//}
//
//static void direct_link_latt(FileData *fd, Lattice *lt)
//{
//	lt.def= newdataadr(fd, lt.def);
//
//	lt.dvert= newdataadr(fd, lt.dvert);
//	direct_link_dverts(fd, lt.pntsu*lt.pntsv*lt.pntsw, lt.dvert);
//
//	lt.editlatt= NULL;
//}
//
//
///* ************ READ OBJECT ***************** */
//
//static void lib_link_modifiers__linkModifiers(void *userData, Object *ob,
//                                              ID **idpoin)
//{
//	FileData *fd = userData;
//
//	*idpoin = newlibadr(fd, ob.id.lib, *idpoin);
//	/* hardcoded bad exception; non-object modifier data gets user count (texture, displace) */
//	if(*idpoin && GS((*idpoin).name)!=ID_OB)
//		(*idpoin).us++;
//}
//static void lib_link_modifiers(FileData *fd, Object *ob)
//{
//	modifiers_foreachIDLink(ob, lib_link_modifiers__linkModifiers, fd);
//}

public static void lib_link_object(FileData fd, Main main)
{
	bObject ob;
	PartEff paf;
	bSensor sens;
	bController cont;
	bActuator act;
	Object poin;
	int warn=0, a;

	ob= main.object.first;
	while(ob!=null) {
		if((ob.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
//			if (ob.id.properties) IDP_LibLinkProperty(ob.id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//			if (ob.adt) lib_link_animdata(fd, &ob.id, ob.adt);

//// XXX depreceated - old animation system <<<
//			ob.ipo= newlibadr_us(fd, ob.id.lib, ob.ipo);
//			ob.action = newlibadr_us(fd, ob.id.lib, ob.action);
//// >>> XXX depreceated - old animation system

			ob.parent= (bObject)newlibadr(fd, ob.id.lib, ob.parent);
			ob.track= (bObject)newlibadr(fd, ob.id.lib, ob.track);
			ob.poselib= (bAction)newlibadr_us(fd, ob.id.lib, ob.poselib);
			ob.dup_group= (Group)newlibadr_us(fd, ob.id.lib, ob.dup_group);

			ob.proxy= (bObject)newlibadr_us(fd, ob.id.lib, ob.proxy);
			if(ob.proxy!=null) {
				/* paranoia check, actually a proxy_from pointer should never be written... */
				if(ob.proxy.id.lib==null) {
					ob.proxy.proxy_from= null;
					ob.proxy= null;
				}
				else {
					/* this triggers object_update to always use a copy */
					ob.proxy.proxy_from= ob;
					/* force proxy updates after load/undo, a bit weak */
					ob.recalc= ob.proxy.recalc= ObjectTypes.OB_RECALC;
				}
			}
			ob.proxy_group= (bObject)newlibadr(fd, ob.id.lib, ob.proxy_group);

			poin= ob.data;
			ob.data= newlibadr_us(fd, ob.id.lib, ob.data);

			if(ob.data==null && poin!=null) {
				ob.type= ObjectTypes.OB_EMPTY;
				warn= 1;
				if(ob.id.lib!=null) System.out.printf("Can't find obdata of %s lib %s\n", StringUtil.toJString(ob.id.name, 2), StringUtil.toJString(ob.id.lib.name, 0));
				else System.out.printf("Object %s lost data.\n", StringUtil.toJString(ob.id.name, 2));

				if(ob.pose!=null) {
//					free_pose(ob.pose);
					ob.pose= null;
					ob.flag &= ~ObjectTypes.OB_POSEMODE;
				}
			}
//			for(a=0; a<ob.totcol; a++) ob.mat[a]= newlibadr_us(fd, ob.id.lib, ob.mat[a]);

			ob.id.flag -= DNA_ID.LIB_NEEDLINK;
			/* if id.us==0 a new base will be created later on */

			/* WARNING! Also check expand_object(), should reflect the stuff below. */
//			lib_link_pose(fd, ob, ob.pose);
//			lib_link_constraints(fd, &ob.id, &ob.constraints);

//// XXX depreceated - old animation system <<<
//			lib_link_constraint_channels(fd, &ob.id, &ob.constraintChannels);
//			lib_link_nlastrips(fd, &ob.id, &ob.nlastrips);
//// >>> XXX depreceated - old animation system

//			for(paf= ob.effect.first; paf; paf= paf.next) {
//				if(paf.type==EFF_PARTICLE) {
//					paf.group= newlibadr_us(fd, ob.id.lib, paf.group);
//				}
//			}
//
//			sens= ob.sensors.first;
//			while(sens) {
//				for(a=0; a<sens.totlinks; a++)
//					sens.links[a]= newglobadr(fd, sens.links[a]);
//
//				if(sens.type==SENS_TOUCH) {
//					bTouchSensor *ts= sens.data;
//					ts.ma= newlibadr(fd, ob.id.lib, ts.ma);
//				}
//				else if(sens.type==SENS_MESSAGE) {
//					bMessageSensor *ms= sens.data;
//					ms.fromObject=
//					    newlibadr(fd, ob.id.lib, ms.fromObject);
//				}
//				sens= sens.next;
//			}
//
//			cont= ob.controllers.first;
//			while(cont) {
//				for(a=0; a<cont.totlinks; a++)
//					cont.links[a]= newglobadr(fd, cont.links[a]);
//
//				if(cont.type==CONT_PYTHON) {
//					bPythonCont *pc= cont.data;
//					pc.text= newlibadr(fd, ob.id.lib, pc.text);
//				}
//				cont.slinks= NULL;
//				cont.totslinks= 0;
//
//				cont= cont.next;
//			}
//
//			act= ob.actuators.first;
//			while(act) {
//				if(act.type==ACT_SOUND) {
//					bSoundActuator *sa= act.data;
//					sa.sound= newlibadr_us(fd, ob.id.lib, sa.sound);
//				}
//				else if(act.type==ACT_CD) {
//					/* bCDActuator *cda= act.data; */
//				}
//				else if(act.type==ACT_GAME) {
//					/* bGameActuator *ga= act.data; */
//				}
//				else if(act.type==ACT_CAMERA) {
//					bCameraActuator *ca= act.data;
//					ca.ob= newlibadr(fd, ob.id.lib, ca.ob);
//				}
//					/* leave this one, it's obsolete but necessary to read for conversion */
//				else if(act.type==ACT_ADD_OBJECT) {
//					bAddObjectActuator *eoa= act.data;
//					if(eoa) eoa.ob= newlibadr(fd, ob.id.lib, eoa.ob);
//				}
//				else if(act.type==ACT_OBJECT) {
//					bObjectActuator *oa= act.data;
//					oa.reference= newlibadr(fd, ob.id.lib, oa.reference);
//				}
//				else if(act.type==ACT_EDIT_OBJECT) {
//					bEditObjectActuator *eoa= act.data;
//					if(eoa==NULL) {
//						init_actuator(act);
//					}
//					else {
//						eoa.ob= newlibadr(fd, ob.id.lib, eoa.ob);
//						eoa.me= newlibadr(fd, ob.id.lib, eoa.me);
//					}
//				}
//				else if(act.type==ACT_OBJECT) {
//					bObjectActuator *oa= act.data;
//					if(oa==NULL) {
//						init_actuator(act);
//					}
//					else {
//						oa.reference= newlibadr(fd, ob.id.lib, oa.reference);
//					}
//				}
//				else if(act.type==ACT_SCENE) {
//					bSceneActuator *sa= act.data;
//					sa.camera= newlibadr(fd, ob.id.lib, sa.camera);
//					sa.scene= newlibadr(fd, ob.id.lib, sa.scene);
//				}
//				else if(act.type==ACT_ACTION) {
//					bActionActuator *aa= act.data;
//					aa.act= newlibadr(fd, ob.id.lib, aa.act);
//				}
//				else if(act.type==ACT_SHAPEACTION) {
//					bActionActuator *aa= act.data;
//					aa.act= newlibadr(fd, ob.id.lib, aa.act);
//				}
//				else if(act.type==ACT_PROPERTY) {
//					bPropertyActuator *pa= act.data;
//					pa.ob= newlibadr(fd, ob.id.lib, pa.ob);
//				}
//				else if(act.type==ACT_MESSAGE) {
//					bMessageActuator *ma= act.data;
//					ma.toObject= newlibadr(fd, ob.id.lib, ma.toObject);
//				}
//				else if(act.type==ACT_2DFILTER){
//					bTwoDFilterActuator *_2dfa = act.data;
//					_2dfa.text= newlibadr(fd, ob.id.lib, _2dfa.text);
//				}
//				else if(act.type==ACT_PARENT) {
//					bParentActuator *parenta = act.data;
//					parenta.ob = newlibadr(fd, ob.id.lib, parenta.ob);
//				}
//				else if(act.type==ACT_STATE) {
//					/* bStateActuator *statea = act.data; */
//				}
//				act= act.next;
//			}
//
//			{
//				FluidsimModifierData *fluidmd = (FluidsimModifierData *)modifiers_findByType(ob, eModifierType_Fluidsim);
//
//				if(fluidmd && fluidmd.fss)
//					fluidmd.fss.ipo = newlibadr_us(fd, ob.id.lib, fluidmd.fss.ipo);
//			}

			/* texture field */
			if(ob.pd!=null)
				if(ob.pd.tex!=null)
					ob.pd.tex=(Tex)newlibadr_us(fd, ob.id.lib, ob.pd.tex);

//			lib_link_particlesystems(fd, ob, &ob.id, &ob.particlesystem);
//			lib_link_modifiers(fd, ob);
		}
		ob= (bObject)ob.id.next;
	}

//	if(warn)
//		BKE_report(fd.reports, RPT_WARNING, "Warning in console");
}


//static void direct_link_pose(FileData *fd, bPose *pose)
//{
//	bPoseChannel *pchan;
//
//	if (!pose)
//		return;
//
//	link_list(fd, &pose.chanbase);
//	link_list(fd, &pose.agroups);
//
//	for (pchan = pose.chanbase.first; pchan; pchan=pchan.next) {
//		pchan.bone= NULL;
//		pchan.parent= newdataadr(fd, pchan.parent);
//		pchan.child= newdataadr(fd, pchan.child);
//
//		direct_link_constraints(fd, &pchan.constraints);
//
//		pchan.prop = newdataadr(fd, pchan.prop);
//		if (pchan.prop)
//			IDP_DirectLinkProperty(pchan.prop, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//
//		pchan.iktree.first= pchan.iktree.last= NULL;
//		pchan.path= NULL;
//	}
//}
//
//static void direct_link_modifiers(FileData *fd, ListBase *lb)
//{
//	ModifierData *md;
//
//	link_list(fd, lb);
//
//	for (md=lb.first; md; md=md.next) {
//		md.error = NULL;
//		md.scene = NULL;
//
//		/* if modifiers disappear, or for upward compatibility */
//		if(NULL==modifierType_getInfo(md.type))
//			md.type= eModifierType_None;
//
//		if (md.type==eModifierType_Subsurf) {
//			SubsurfModifierData *smd = (SubsurfModifierData*) md;
//
//			smd.emCache = smd.mCache = 0;
//		}
//		else if (md.type==eModifierType_Armature) {
//			ArmatureModifierData *amd = (ArmatureModifierData*) md;
//
//			amd.prevCos= NULL;
//		}
//		else if (md.type==eModifierType_Cloth) {
//			ClothModifierData *clmd = (ClothModifierData*) md;
//
//			clmd.clothObject = NULL;
//
//			clmd.sim_parms= newdataadr(fd, clmd.sim_parms);
//			clmd.coll_parms= newdataadr(fd, clmd.coll_parms);
//			clmd.point_cache= newdataadr(fd, clmd.point_cache);
//
//			if(clmd.point_cache)
//				direct_link_pointcache(fd, clmd.point_cache);
//
//			if(clmd.sim_parms) {
//				if(clmd.sim_parms.presets > 10)
//					clmd.sim_parms.presets = 0;
//			}
//
//		}
//		else if (md.type==eModifierType_Fluidsim) {
//			FluidsimModifierData *fluidmd = (FluidsimModifierData*) md;
//
//			fluidmd.fss= newdataadr(fd, fluidmd.fss);
//			fluidmd.fss.meshSurfNormals = 0;
//		}
//		else if (md.type==eModifierType_Collision) {
//
//			CollisionModifierData *collmd = (CollisionModifierData*) md;
//			/*
//			// TODO: CollisionModifier should use pointcache
//			// + have proper reset events before enabling this
//			collmd.x = newdataadr(fd, collmd.x);
//			collmd.xnew = newdataadr(fd, collmd.xnew);
//			collmd.mfaces = newdataadr(fd, collmd.mfaces);
//
//			collmd.current_x = MEM_callocN(sizeof(MVert)*collmd.numverts,"current_x");
//			collmd.current_xnew = MEM_callocN(sizeof(MVert)*collmd.numverts,"current_xnew");
//			collmd.current_v = MEM_callocN(sizeof(MVert)*collmd.numverts,"current_v");
//			*/
//
//			collmd.x = NULL;
//			collmd.xnew = NULL;
//			collmd.current_x = NULL;
//			collmd.current_xnew = NULL;
//			collmd.current_v = NULL;
//			collmd.time = -1;
//			collmd.numverts = 0;
//			collmd.bvhtree = NULL;
//			collmd.mfaces = NULL;
//
//		}
//		else if (md.type==eModifierType_Surface) {
//			SurfaceModifierData *surmd = (SurfaceModifierData*) md;
//
//			surmd.dm = NULL;
//			surmd.bvhtree = NULL;
//			surmd.x = NULL;
//			surmd.v = NULL;
//			surmd.numverts = 0;
//		}
//		else if (md.type==eModifierType_Hook) {
//			HookModifierData *hmd = (HookModifierData*) md;
//
//			hmd.indexar= newdataadr(fd, hmd.indexar);
//			if(fd.flags & FD_FLAGS_SWITCH_ENDIAN) {
//				int a;
//				for(a=0; a<hmd.totindex; a++) {
//					SWITCH_INT(hmd.indexar[a]);
//				}
//			}
//		} else if (md.type==eModifierType_ParticleSystem) {
//			ParticleSystemModifierData *psmd = (ParticleSystemModifierData*) md;
//
//			psmd.dm=0;
//			psmd.psys=newdataadr(fd, psmd.psys);
//			psmd.flag &= ~eParticleSystemFlag_psys_updated;
//		} else if (md.type==eModifierType_Explode) {
//			ExplodeModifierData *psmd = (ExplodeModifierData*) md;
//
//			psmd.facepa=0;
//		}
//		else if (md.type==eModifierType_MeshDeform) {
//			MeshDeformModifierData *mmd = (MeshDeformModifierData*) md;
//
//			mmd.bindweights= newdataadr(fd, mmd.bindweights);
//			mmd.bindcos= newdataadr(fd, mmd.bindcos);
//			mmd.dyngrid= newdataadr(fd, mmd.dyngrid);
//			mmd.dyninfluences= newdataadr(fd, mmd.dyninfluences);
//			mmd.dynverts= newdataadr(fd, mmd.dynverts);
//
//			if(fd.flags & FD_FLAGS_SWITCH_ENDIAN) {
//				int a;
//
//				if(mmd.bindweights)
//					for(a=0; a<mmd.totcagevert*mmd.totvert; a++)
//						SWITCH_INT(mmd.bindweights[a])
//				if(mmd.bindcos)
//					for(a=0; a<mmd.totcagevert*3; a++)
//						SWITCH_INT(mmd.bindcos[a])
//				if(mmd.dynverts)
//					for(a=0; a<mmd.totvert; a++)
//						SWITCH_INT(mmd.dynverts[a])
//			}
//		}
//		else if (md.type==eModifierType_Multires) {
//			MultiresModifierData *mmd = (MultiresModifierData*) md;
//
//			mmd.undo_verts = newdataadr(fd, mmd.undo_verts);
//			mmd.undo_signal = !!mmd.undo_verts;
//		}
//	}
//}

public static void direct_link_object(FileData fd, bObject ob)
{
	PartEff paf;
	bProperty prop;
	bSensor sens;
	bController cont;
	bActuator act;
	int a;

	/* weak weak... this was only meant as draw flag, now is used in give_base too */
	ob.flag &= ~ObjectTypes.OB_FROMGROUP;

	ob.disp.first=ob.disp.last= null;

	ob.adt= (AnimData)newdataadr(fd, ob.adt);
//	direct_link_animdata(fd, ob.adt);

	ob.pose= (bPose)newdataadr(fd, ob.pose);
//	direct_link_pose(fd, ob.pose);

	link_list(fd, ob.defbase);
//// XXX depreceated - old animation system <<<
//	direct_link_nlastrips(fd, &ob.nlastrips);
//	link_list(fd, &ob.constraintChannels);
//// >>> XXX depreceated - old animation system

	ob.mat= (Material[])newdataadr(fd, ob.mat);
//	test_pointer_array(fd, (void **)&ob.mat);
	ob.matbits= newdataadr(fd, ob.matbits);

	/* do it here, below old data gets converted */
//	direct_link_modifiers(fd, ob.modifiers);

	link_list(fd, ob.effect);
//	paf= ob.effect.first;
//	while(paf) {
//		if(paf.type==EFF_PARTICLE) {
//			paf.keys= NULL;
//		}
//		if(paf.type==EFF_WAVE) {
//			WaveEff *wav = (WaveEff*) paf;
//			PartEff *next = paf.next;
//			WaveModifierData *wmd = (WaveModifierData*) modifier_new(eModifierType_Wave);
//
//			wmd.damp = wav.damp;
//			wmd.flag = wav.flag;
//			wmd.height = wav.height;
//			wmd.lifetime = wav.lifetime;
//			wmd.narrow = wav.narrow;
//			wmd.speed = wav.speed;
//			wmd.startx = wav.startx;
//			wmd.starty = wav.startx;
//			wmd.timeoffs = wav.timeoffs;
//			wmd.width = wav.width;
//
//			BLI_addtail(&ob.modifiers, wmd);
//
//			BLI_remlink(&ob.effect, paf);
//			MEM_freeN(paf);
//
//			paf = next;
//			continue;
//		}
//		if(paf.type==EFF_BUILD) {
//			BuildEff *baf = (BuildEff*) paf;
//			PartEff *next = paf.next;
//			BuildModifierData *bmd = (BuildModifierData*) modifier_new(eModifierType_Build);
//
//			bmd.start = baf.sfra;
//			bmd.length = baf.len;
//			bmd.randomize = 0;
//			bmd.seed = 1;
//
//			BLI_addtail(&ob.modifiers, bmd);
//
//			BLI_remlink(&ob.effect, paf);
//			MEM_freeN(paf);
//
//			paf = next;
//			continue;
//		}
//		paf= paf.next;
//	}

	ob.pd= (PartDeflect)newdataadr(fd, ob.pd);
	ob.soft= (SoftBody)newdataadr(fd, ob.soft);
	if(ob.soft!=null) {
		SoftBody sb= ob.soft;

		sb.bpoint= null;	// init pointers so it gets rebuilt nicely
		sb.bspring= null;
		sb.scratch= null;
		/* although not used anymore */
		/* still have to be loaded to be compatible with old files */
		sb.keys= (SBVertex[])newdataadr(fd, sb.keys);
//		test_pointer_array(fd, (void **)&sb.keys);
		if(sb.keys!=null) {
			for(a=0; a<sb.totkey; a++) {
				sb.keys[a]= (SBVertex)newdataadr(fd, sb.keys[a]);
			}
		}

		sb.pointcache= (PointCache)newdataadr(fd, sb.pointcache);
//		if(sb.pointcache!=null)
//			direct_link_pointcache(fd, sb.pointcache);
	}
	ob.bsoft= (BulletSoftBody)newdataadr(fd, ob.bsoft);
	ob.fluidsimSettings= (FluidsimSettings)newdataadr(fd, ob.fluidsimSettings); /* NT */

	link_list(fd, ob.particlesystem);
//	direct_link_particlesystems(fd,&ob.particlesystem);

	link_list(fd, ob.prop);
//	prop= ob.prop.first;
//	while(prop!=null) {
//		prop.poin= newdataadr(fd, prop.poin);
//		if(prop.poin==0) prop.poin= &prop.data;
//		prop= prop.next;
//	}

	link_list(fd, ob.sensors);
	sens= (bSensor)ob.sensors.first;
	while(sens!=null) {
		sens.data= newdataadr(fd, sens.data);
		sens.links= (bController[])newdataadr(fd, sens.links);
//		test_pointer_array(fd, (void **)&sens.links);
		sens= sens.next;
	}

//	direct_link_constraints(fd, ob.constraints);

//	link_glob_list(fd, &ob.controllers);
//	if (ob.init_state) {
//		/* if a known first state is specified, set it so that the game will start ok */
//		ob.state = ob.init_state;
//	} else if (!ob.state) {
//		ob.state = 1;
//	}
//	cont= ob.controllers.first;
//	while(cont) {
//		cont.data= newdataadr(fd, cont.data);
//		cont.links= newdataadr(fd, cont.links);
//		test_pointer_array(fd, (void **)&cont.links);
//		if (cont.state_mask == 0)
//			cont.state_mask = 1;
//		cont= cont.next;
//	}
//
//	link_glob_list(fd, &ob.actuators);
//	act= ob.actuators.first;
//	while(act) {
//		act.data= newdataadr(fd, act.data);
//		act= act.next;
//	}
//
//	link_list(fd, &ob.hooks);
//	while (ob.hooks.first) {
//		ObHook *hook = ob.hooks.first;
//		HookModifierData *hmd = (HookModifierData*) modifier_new(eModifierType_Hook);
//
//		hook.indexar= newdataadr(fd, hook.indexar);
//		if(fd.flags & FD_FLAGS_SWITCH_ENDIAN) {
//			int a;
//			for(a=0; a<hook.totindex; a++) {
//				SWITCH_INT(hook.indexar[a]);
//			}
//		}
//
//			/* Do conversion here because if we have loaded
//			 * a hook we need to make sure it gets converted
//			 * and free'd, regardless of version.
//			 */
//		VECCOPY(hmd.cent, hook.cent);
//		hmd.falloff = hook.falloff;
//		hmd.force = hook.force;
//		hmd.indexar = hook.indexar;
//		hmd.object = hook.parent;
//		memcpy(hmd.parentinv, hook.parentinv, sizeof(hmd.parentinv));
//		hmd.totindex = hook.totindex;
//
//		BLI_addhead(&ob.modifiers, hmd);
//		BLI_remlink(&ob.hooks, hook);
//
//		MEM_freeN(hook);
//	}

	ob.bb= null;
	ob.derivedDeform= null;
	ob.derivedFinal= null;
	ob.gpulamp.first= ob.gpulamp.last= null;
}

///* ************ READ SCENE ***************** */
//
///* patch for missing scene IDs, can't be in do-versions */
//static void composite_patch(bNodeTree *ntree, Scene *scene)
//{
//	bNode *node;
//
//	for(node= ntree.nodes.first; node; node= node.next)
//		if(node.id==NULL && ELEM(node.type, CMP_NODE_R_LAYERS, CMP_NODE_COMPOSITE))
//			node.id= &scene.id;
//}


public static void lib_link_scene(FileData fd, Main main)
{
	Scene sce;
	Base base, next;
	Sequence seq;
	SceneRenderLayer srl;

	sce= main.scene.first;
	while(sce!=null) {
		if((sce.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
			/*Link ID Properties -- and copy this comment EXACTLY for easy finding
			of library blocks that implement this.*/
//			if (sce.id.properties!=null) IDP_LibLinkProperty(sce.id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//			if (sce.adt!=null) lib_link_animdata(fd, sce.id, sce.adt);

//			lib_link_keyingsets(fd, &sce.id, &sce.keyingsets);

			sce.camera= (bObject)newlibadr(fd, sce.id.lib, sce.camera);
			sce.world= (World)newlibadr_us(fd, sce.id.lib, sce.world);
			sce.set= (Scene)newlibadr(fd, sce.id.lib, sce.set);
//			sce.ima= (Image)newlibadr_us(fd, sce.id.lib, sce.ima);

//			sce.toolsettings.imapaint.brush=
//				(Brush)newlibadr_us(fd, sce.id.lib, sce.toolsettings.imapaint.brush);
//			if(sce.toolsettings.sculpt!=null)
//				sce.toolsettings.sculpt.brush=
//					(Brush)newlibadr_us(fd, sce.id.lib, sce.toolsettings.sculpt.brush);
//			if(sce.toolsettings.vpaint!=null)
//				sce.toolsettings.vpaint.brush=
//					(Brush)newlibadr_us(fd, sce.id.lib, sce.toolsettings.vpaint.brush);
//			if(sce.toolsettings.wpaint!=null)
//				sce.toolsettings.wpaint.brush=
//					(Brush)newlibadr_us(fd, sce.id.lib, sce.toolsettings.wpaint.brush);

			sce.toolsettings.skgen_template = (bObject)newlibadr(fd, sce.id.lib, sce.toolsettings.skgen_template);

			for(base= (Base)sce.base.first; base!=null; base= next) {
				next= base.next;

				/* base.object= newlibadr_us(fd, sce.id.lib, base.object); */
				base.object= (bObject)newlibadr_us(fd, sce.id.lib, base.object);

				/* when save during radiotool, needs cleared */
				base.flag &= ~ObjectTypes.OB_RADIO;

				if(base.object==null) {
					System.out.printf("LIB ERROR: base removed\n");
					ListBaseUtil.BLI_remlink(sce.base, base);
					if(base==sce.basact) sce.basact= null;
				}
			}

//			if (sce.ed) {
//				Editing *ed= sce.ed;
//				ed.act_seq= NULL; //	ed.act_seq=  newlibadr(fd, ed.act_seq); // FIXME
//			}
//
//			SEQ_BEGIN(sce.ed, seq) {
//				if(seq.ipo) seq.ipo= newlibadr_us(fd, sce.id.lib, seq.ipo);
//				if(seq.scene) seq.scene= newlibadr(fd, sce.id.lib, seq.scene);
//				if(seq.sound) {
//					seq.sound= newlibadr(fd, sce.id.lib, seq.sound);
//					if (seq.sound) {
//						seq.sound.id.us++;
//						seq.sound.flags |= SOUND_FLAGS_SEQUENCE;
//					}
//				}
//				seq.anim= 0;
//				seq.hdaudio = 0;
//			}
//			SEQ_END
//
//			if(sce.nodetree) {
//				lib_link_ntree(fd, &sce.id, sce.nodetree);
//				composite_patch(sce.nodetree, sce);
//			}

			for(srl= (SceneRenderLayer)sce.r.layers.first; srl!=null; srl= srl.next) {
				srl.mat_override= (Material)newlibadr_us(fd, sce.id.lib, srl.mat_override);
				srl.light_override= (Group)newlibadr_us(fd, sce.id.lib, srl.light_override);
			}
//			/*Game Settings: Dome Warp Text*/
////			sce.r.dometext= newlibadr_us(fd, sce.id.lib, sce.r.dometext); // XXX deprecated since 2.5
//			sce.gm.dome.warptext= newlibadr_us(fd, sce.id.lib, sce.gm.dome.warptext);

			sce.id.flag -= DNA_ID.LIB_NEEDLINK;
		}

		sce= (Scene)sce.id.next;
	}
}

//static void link_recurs_seq(FileData *fd, ListBase *lb)
//{
//	Sequence *seq;
//
//	link_list(fd, lb);
//
//	for(seq=lb.first; seq; seq=seq.next)
//		if(seq.seqbase.first)
//			link_recurs_seq(fd, &seq.seqbase);
//}

public static void direct_link_scene(FileData fd, Scene sce)
{
	Editing ed;
	Sequence seq;
	MetaStack ms;

	sce.theDag = null;
	sce.dagisvalid = 0;
	sce.obedit= null;

	/* set users to one by default, not in lib-link, this will increase it for compo nodes */
	sce.id.us= 1;

	link_list(fd, sce.base);

//	sce.adt= (AnimData)newdataadr(fd, sce.adt);
//	direct_link_animdata(fd, sce.adt);

	link_list(fd, sce.keyingsets);
//	direct_link_keyingsets(fd, &sce.keyingsets);

	sce.basact= (Base)newdataadr(fd, sce.basact);

	sce.toolsettings= (ToolSettings)newdataadr(fd, sce.toolsettings);
	if(sce.toolsettings!=null) {
		sce.toolsettings.vpaint= (VPaint)newdataadr(fd, sce.toolsettings.vpaint);
		sce.toolsettings.wpaint= (VPaint)newdataadr(fd, sce.toolsettings.wpaint);
		sce.toolsettings.sculpt= (Sculpt)newdataadr(fd, sce.toolsettings.sculpt);
		sce.toolsettings.imapaint.paintcursor= null;
		sce.toolsettings.particle.paintcursor= null;

//		if(sce.toolsettings.sculpt!=null)
//			sce.toolsettings.sculpt.session= new SculptSession();
	}

//	if(sce.ed) {
//		ListBase *old_seqbasep= &((Editing *)sce.ed).seqbase;
//
//		ed= sce.ed= newdataadr(fd, sce.ed);
//		ed.act_seq= NULL; //		ed.act_seq=  newdataadr(fd, ed.act_seq); // FIXME
//
//		/* recursive link sequences, lb will be correctly initialized */
//		link_recurs_seq(fd, &ed.seqbase);
//
//		SEQ_BEGIN(ed, seq) {
//			seq.seq1= newdataadr(fd, seq.seq1);
//			seq.seq2= newdataadr(fd, seq.seq2);
//			seq.seq3= newdataadr(fd, seq.seq3);
//			/* a patch: after introduction of effects with 3 input strips */
//			if(seq.seq3==0) seq.seq3= seq.seq2;
//
//			seq.plugin= newdataadr(fd, seq.plugin);
//			seq.effectdata= newdataadr(fd, seq.effectdata);
//
//			if (seq.type & SEQ_EFFECT) {
//				seq.flag |= SEQ_EFFECT_NOT_LOADED;
//			}
//
//			seq.strip= newdataadr(fd, seq.strip);
//			if(seq.strip && seq.strip.done==0) {
//				seq.strip.done= 1;
//				seq.strip.tstripdata = 0;
//				seq.strip.tstripdata_startstill = 0;
//				seq.strip.tstripdata_endstill = 0;
//				seq.strip.ibuf_startstill = 0;
//				seq.strip.ibuf_endstill = 0;
//
//				if(seq.type == SEQ_IMAGE ||
//				   seq.type == SEQ_MOVIE ||
//				   seq.type == SEQ_RAM_SOUND ||
//				   seq.type == SEQ_HD_SOUND) {
//					seq.strip.stripdata = newdataadr(
//						fd, seq.strip.stripdata);
//				} else {
//					seq.strip.stripdata = 0;
//				}
//				if (seq.flag & SEQ_USE_CROP) {
//					seq.strip.crop = newdataadr(
//						fd, seq.strip.crop);
//				} else {
//					seq.strip.crop = 0;
//				}
//				if (seq.flag & SEQ_USE_TRANSFORM) {
//					seq.strip.transform = newdataadr(
//						fd, seq.strip.transform);
//				} else {
//					seq.strip.transform = 0;
//				}
//				if (seq.flag & SEQ_USE_PROXY) {
//					seq.strip.proxy = newdataadr(
//						fd, seq.strip.proxy);
//					seq.strip.proxy.anim = 0;
//				} else {
//					seq.strip.proxy = 0;
//				}
//				if (seq.flag & SEQ_USE_COLOR_BALANCE) {
//					seq.strip.color_balance = newdataadr(
//						fd, seq.strip.color_balance);
//				} else {
//					seq.strip.color_balance = 0;
//				}
//				if (seq.strip.color_balance) {
//					// seq.strip.color_balance.gui = 0; // XXX - peter, is this relevant in 2.5?
//				}
//			}
//		}
//		SEQ_END
//
//		/* link metastack, slight abuse of structs here, have to restore pointer to internal part in struct */
//		{
//			Sequence temp;
//			char *poin;
//			intptr_t offset;
//
//			offset= ((intptr_t)&(temp.seqbase)) - ((intptr_t)&temp);
//
//			/* root pointer */
//			if(ed.seqbasep == old_seqbasep) {
//				ed.seqbasep= &ed.seqbase;
//			}
//			else {
//
//				poin= (char *)ed.seqbasep;
//				poin -= offset;
//
//				poin= newdataadr(fd, poin);
//				if(poin) ed.seqbasep= (ListBase *)(poin+offset);
//				else ed.seqbasep= &ed.seqbase;
//			}
//			/* stack */
//			link_list(fd, &(ed.metastack));
//
//			for(ms= ed.metastack.first; ms; ms= ms.next) {
//				ms.parseq= newdataadr(fd, ms.parseq);
//
//				if(ms.oldbasep == old_seqbasep)
//					ms.oldbasep= &ed.seqbase;
//				else {
//					poin= (char *)ms.oldbasep;
//					poin -= offset;
//					poin= newdataadr(fd, poin);
//					if(poin) ms.oldbasep= (ListBase *)(poin+offset);
//					else ms.oldbasep= &ed.seqbase;
//				}
//			}
//		}
//	}

	sce.r.avicodecdata = (AviCodecData)newdataadr(fd, sce.r.avicodecdata);
	if (sce.r.avicodecdata!=null) {
		sce.r.avicodecdata.lpFormat = newdataadr(fd, sce.r.avicodecdata.lpFormat);
		sce.r.avicodecdata.lpParms = newdataadr(fd, sce.r.avicodecdata.lpParms);
	}

	sce.r.qtcodecdata = (QuicktimeCodecData)newdataadr(fd, sce.r.qtcodecdata);
	if (sce.r.qtcodecdata!=null) {
		sce.r.qtcodecdata.cdParms = newdataadr(fd, sce.r.qtcodecdata.cdParms);
	}
	if (sce.r.ffcodecdata.properties!=null) {
		sce.r.ffcodecdata.properties = (IDProperty)newdataadr(
			fd, sce.r.ffcodecdata.properties);
//		if (sce.r.ffcodecdata.properties) {
//			IDP_DirectLinkProperty(
//				sce.r.ffcodecdata.properties,
//				(fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//		}
	}

	link_list(fd, sce.markers);
	link_list(fd, sce.transform_spaces);
	link_list(fd, sce.r.layers);

//	sce.nodetree= newdataadr(fd, sce.nodetree);
//	if(sce.nodetree)
//		direct_link_nodetree(fd, sce.nodetree);

}

/* ************ READ WM ***************** */

public static void direct_link_windowmanager(FileData fd, wmWindowManager wm)
{
	wmWindow win;

	wm.id.us= 1;
	link_list(fd, wm.windows);

	for(win= (wmWindow)wm.windows.first; win!=null; win= win.next) {
		win.ghostwin= null;
		win.eventstate= null;
		win.curswin= null;
		win.tweak= null;

//		win.timers.first= win.timers.last= null;
		win.queue.first= win.queue.last= null;
		win.handlers.first= win.handlers.last= null;
		win.subwindows.first= win.subwindows.last= null;
		win.gesture.first= win.gesture.last= null;

		win.drawdata= null;
		win.drawmethod= -1;
		win.drawfail= 0;
	}

	wm.timers.first = wm.timers.last = null;
	wm.operators.first= wm.operators.last= null;
	wm.keyconfigs.first= wm.keyconfigs.last= null;
	wm.paintcursors.first= wm.paintcursors.last= null;
	wm.queue.first= wm.queue.last= null;
//	BKE_reports_init(&wm.reports, RPT_STORE);

	wm.jobs.first= wm.jobs.last= null;

	wm.windrawable= null;
	wm.initialized= 0;
}

public static void lib_link_windowmanager(FileData fd, Main main)
{
	wmWindowManager wm;

	for(wm= (wmWindowManager)main.wm.first; wm!=null; wm= (wmWindowManager)wm.id.next) {
		wmWindow win;
		for(win= (wmWindow)wm.windows.first; win!=null; win= win.next) {
			win.screen= (bScreen)newlibadr(fd, null, win.screen);
		}
	}
}

///* ****************** READ GREASE PENCIL ***************** */
//
///* relinks grease-pencil data - used for direct_link and old file linkage */
//static void direct_link_gpencil(FileData *fd, bGPdata *gpd)
//{
//	bGPDlayer *gpl;
//	bGPDframe *gpf;
//	bGPDstroke *gps;
//
//	/* we must firstly have some grease-pencil data to link! */
//	if (gpd == NULL)
//		return;
//
//	/* relink layers */
//	link_list(fd, &gpd.layers);
//
//	for (gpl= gpd.layers.first; gpl; gpl= gpl.next) {
//		/* relink frames */
//		link_list(fd, &gpl.frames);
//		gpl.actframe= newdataadr(fd, gpl.actframe);
//
//		for (gpf= gpl.frames.first; gpf; gpf= gpf.next) {
//			/* relink strokes (and their points) */
//			link_list(fd, &gpf.strokes);
//
//			for (gps= gpf.strokes.first; gps; gps= gps.next) {
//				gps.points= newdataadr(fd, gps.points);
//			}
//		}
//	}
//}
//
///* ****************** READ SCREEN ***************** */
//
//static void butspace_version_132(SpaceButs *buts)
//{
//	buts.v2d.tot.xmin= 0.0f;
//	buts.v2d.tot.ymin= 0.0f;
//	buts.v2d.tot.xmax= 1279.0f;
//	buts.v2d.tot.ymax= 228.0f;
//
//	buts.v2d.min[0]= 256.0f;
//	buts.v2d.min[1]= 42.0f;
//
//	buts.v2d.max[0]= 2048.0f;
//	buts.v2d.max[1]= 450.0f;
//
//	buts.v2d.minzoom= 0.5f;
//	buts.v2d.maxzoom= 1.21f;
//
//	buts.v2d.scroll= 0;
//	buts.v2d.keepzoom= 1;
//	buts.v2d.keeptot= 1;
//}

/* note: file read without screens option G_FILE_NO_UI;
   check lib pointers in call below */
public static void lib_link_screen(FileData fd, Main main)
{
	bScreen sc;
	ScrArea sa;

	for(sc= (bScreen)main.screen.first; sc!=null; sc= (bScreen)sc.id.next) {
		if((sc.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
			sc.id.us= 1;
			sc.scene= (Scene)newlibadr(fd, sc.id.lib, sc.scene);

			sa= (ScrArea)sc.areabase.first;
			while(sa!=null) {
				SpaceLink sl;

				sa.full= (bScreen)newlibadr(fd, sc.id.lib, sa.full);

				for (sl= (SpaceLink)sa.spacedata.first; sl!=null; sl= (SpaceLink)sl.next) {
					if(sl.spacetype==SpaceTypes.SPACE_VIEW3D) {
						View3D v3d = (View3D) sl;

                                                v3d.camera = (bObject) newlibadr(fd, sc.id.lib, v3d.camera);
                                                v3d.ob_centre = (bObject) newlibadr(fd, sc.id.lib, v3d.ob_centre);

                                                if (v3d.bgpic != null) {
                                                    v3d.bgpic.ima = (Image) newlibadr_us(fd, sc.id.lib, v3d.bgpic.ima);
                                                }
                                                if (v3d.localvd != null) {
                                                    v3d.localvd.camera = (bObject) newlibadr(fd, sc.id.lib, v3d.localvd.camera);
                                                }
					}
					else if(sl.spacetype==SpaceTypes.SPACE_IPO) {
						SpaceIpo sipo= (SpaceIpo)sl;

						if(sipo.ads!=null)
							sipo.ads.source= newlibadr(fd, sc.id.lib, sipo.ads.source);
					}
					else if(sl.spacetype==SpaceTypes.SPACE_BUTS) {
						SpaceButs sbuts= (SpaceButs)sl;
						//sbuts.ri= null;
						sbuts.pinid= newlibadr(fd, sc.id.lib, sbuts.pinid);
						sbuts.mainbo= sbuts.mainb;
						sbuts.mainbuser= sbuts.mainb;
//						if(main.versionfile<132)
//							butspace_version_132(sbuts);
					}
					else if(sl.spacetype==SpaceTypes.SPACE_FILE) {
						SpaceFile sfile= (SpaceFile)sl;
						sfile.files= null;
						sfile.params= null;
						sfile.op= null;
						sfile.layout= null;
						sfile.folders_prev= null;
						sfile.folders_next= null;
					}
//					else if(sl.spacetype==SpaceTypes.SPACE_IMASEL) {
//						SpaceImaSel simasel= (SpaceImaSel)sl;
//
//						simasel.files = null;
//						simasel.returnfunc= null;
//						simasel.menup= null;
//						simasel.pupmenu= null;
//						simasel.img= null;
//					}
					else if(sl.spacetype==SpaceTypes.SPACE_ACTION) {
						SpaceAction saction= (SpaceAction)sl;
						saction.action = (bAction)newlibadr(fd, sc.id.lib, saction.action);
						saction.ads.source= newlibadr(fd, sc.id.lib, saction.ads.source);
					}
					else if(sl.spacetype==SpaceTypes.SPACE_IMAGE) {
						SpaceImage sima= (SpaceImage)sl;

						sima.image= (Image)newlibadr_us(fd, sc.id.lib, sima.image);
					}
					else if(sl.spacetype==SpaceTypes.SPACE_NLA){
						/* SpaceNla *snla= (SpaceNla *)sl;	*/
					}
					else if(sl.spacetype==SpaceTypes.SPACE_TEXT) {
						SpaceText st= (SpaceText)sl;

						st.text= (Text)newlibadr(fd, sc.id.lib, st.text);

					}
					else if(sl.spacetype==SpaceTypes.SPACE_SCRIPT) {

						SpaceScript scpt= (SpaceScript)sl;
						/*scpt.script = NULL; - 2.45 set to null, better re-run the script */
						if (scpt.script!=null) {
							scpt.script= (Script)newlibadr(fd, sc.id.lib, scpt.script);
							if (scpt.script!=null) {
//								SCRIPT_SET_NULL(scpt.script)
                                                                scpt.script.py_draw = scpt.script.py_event = scpt.script.py_button = scpt.script.py_browsercallback = scpt.script.py_globaldict = null;
                                                                scpt.script.flags = 0;
							}
						}
					}
					else if(sl.spacetype==SpaceTypes.SPACE_OUTLINER) {
						SpaceOops so= (SpaceOops)sl;
						TreeStoreElem[] tselems;
                                                int tselem_p;
						int a;

						so.tree.first= so.tree.last= null;
						so.search_tse.id= newlibadr(fd, null, so.search_tse.id);

						if(so.treestore!=null) {
							tselems= so.treestore.data.myarray;
                                                        tselem_p = 0;
							for(a=0; a<so.treestore.usedelem; a++, tselem_p++) {
                                                                TreeStoreElem tselem = tselems[tselem_p];
								tselem.id= newlibadr(fd, null, tselem.id);
							}
						}
					}
//					else if(sl.spacetype==SpaceTypes.SPACE_SOUND) {
//						SpaceSound ssound= (SpaceSound)sl;
//
//						ssound.sound= (bSound)newlibadr_us(fd, sc.id.lib, ssound.sound);
//					}
					else if(sl.spacetype==SpaceTypes.SPACE_NODE) {
						SpaceNode snode= (SpaceNode)sl;

						snode.id= newlibadr(fd, sc.id.lib, snode.id);

						/* internal data, a bit patchy */
						if(snode.id!=null) {
							if(LibraryUtil.GS(((ID)snode.id).name)==DNA_ID.ID_MA)
								snode.nodetree= ((Material)snode.id).nodetree;
							else if(LibraryUtil.GS(((ID)snode.id).name)==DNA_ID.ID_SCE)
								snode.nodetree= ((Scene)snode.id).nodetree;
							else if(LibraryUtil.GS(((ID)snode.id).name)==DNA_ID.ID_TE)
								snode.nodetree= ((Tex)snode.id).nodetree;
						}
					}
				}
				sa= sa.next;
			}
			sc.id.flag -= DNA_ID.LIB_NEEDLINK;
		}
	}
}

    /* Only for undo files, or to restore a screen after reading without UI... */
    public static ID restore_pointer_by_name(Main mainp, ID id, int user) {
        if (id != null) {
            ListBase lb = LibraryUtil.wich_libbase(mainp, LibraryUtil.GS(id.name));

            if (lb != null) {	// there's still risk of checking corrupt mem (freed Ids in oops)
                ID idn = (ID) lb.first;
                String name = new String(id.name).substring(2);

                while (idn != null) {
                    String idnName = new String(idn.name);
                    if (idnName.charAt(2) == name.charAt(0) && name.compareTo(idnName.substring(2)) == 0) {
                        if (idn.lib == id.lib) {
                            if (user != 0 && idn.us == 0) {
                                idn.us++;
                            }
                            break;
                        }
                    }
                    idn = (ID) idn.next;
                }
                return idn;
            }
        }
        return null;
    }

/* called from kernel/blender.c */
/* used to link a file (without UI) to the current UI */
/* note that it assumes the old pointers in UI are still valid, so old Main is not freed */
public static void lib_link_screen_restore(Main newmain, bScreen curscreen, Scene curscene)
{
	wmWindow win;
	wmWindowManager wm;
	bScreen sc;
	ScrArea sa;

	/* first windowmanager */
	for(wm= (wmWindowManager)newmain.wm.first; wm!=null; wm= (wmWindowManager)wm.id.next) {
		for(win= (wmWindow)wm.windows.first; win!=null; win= win.next) {
			win.screen= (bScreen)restore_pointer_by_name(newmain, (ID)win.screen, 1);

			if(win.screen==null)
				win.screen= curscreen;

			win.screen.winid= (short)win.winid;
		}
	}


	for(sc= (bScreen)newmain.screen.first; sc!=null; sc= (bScreen)sc.id.next) {

		sc.scene= (Scene)restore_pointer_by_name(newmain, (ID)sc.scene, 1);
		if(sc.scene==null)
			sc.scene= curscene;

		sa= (ScrArea)sc.areabase.first;
		while(sa!=null) {
			SpaceLink sl;

			for (sl= (SpaceLink)sa.spacedata.first; sl!=null; sl= (SpaceLink)sl.next) {
				if(sl.spacetype==SpaceTypes.SPACE_VIEW3D) {
					View3D v3d= (View3D) sl;

					v3d.camera= (bObject)restore_pointer_by_name(newmain, (ID)v3d.camera, 1);
					if(v3d.camera==null)
						v3d.camera= sc.scene.camera;
					v3d.ob_centre= (bObject)restore_pointer_by_name(newmain, (ID)v3d.ob_centre, 1);

					if(v3d.bgpic!=null) {
						v3d.bgpic.ima= (Image)restore_pointer_by_name(newmain, (ID)v3d.bgpic.ima, 1);
					}
					if(v3d.localvd!=null) {
						/*Base *base;*/

						v3d.localvd.camera= sc.scene.camera;

						/* localview can become invalid during undo/redo steps, so we exit it when no could be found */
						/* XXX  regionlocalview ?
						for(base= sc.scene.base.first; base; base= base.next) {
							if(base.lay & v3d.lay) break;
						}
						if(base==NULL) {
							v3d.lay= v3d.localvd.lay;
							v3d.layact= v3d.localvd.layact;
							MEM_freeN(v3d.localvd);
							v3d.localvd= NULL;
							v3d.localview= 0;
						}
						*/
					}
					else if(v3d.scenelock!=0) v3d.lay= sc.scene.lay;

					/* not very nice, but could help */
					if((v3d.layact & v3d.lay)==0) v3d.layact= v3d.lay;

				}
//				else if(sl.spacetype==SPACE_IPO) {
//					/* XXX animato */
//#if 0
//					SpaceIpo *sipo= (SpaceIpo *)sl;
//
//					sipo.ipo= restore_pointer_by_name(newmain, (ID *)sipo.ipo, 0);
//					if(sipo.blocktype==ID_SEQ)
//						sipo.from= (ID *)find_sequence_from_ipo_helper(newmain, sipo.ipo);
//					else
//						sipo.from= restore_pointer_by_name(newmain, (ID *)sipo.from, 0);
//
//					// not free sipo.ipokey, creates dependency with src/
//					if(sipo.editipo) MEM_freeN(sipo.editipo);
//					sipo.editipo= NULL;
//#endif
//				}
				else if(sl.spacetype==SpaceTypes.SPACE_BUTS) {
//					SpaceButs *sbuts= (SpaceButs *)sl;
//					sbuts.pinid = restore_pointer_by_name(newmain, sbuts.pinid, 0);
//					//XXX if (sbuts.ri) sbuts.ri.curtile = 0;
				}
				else if(sl.spacetype==SpaceTypes.SPACE_FILE) {
//
//					SpaceFile *sfile= (SpaceFile *)sl;
//					sfile.files= NULL;
//					sfile.folders_prev= NULL;
//					sfile.folders_next= NULL;
//					sfile.params= NULL;
//					sfile.op= NULL;
				}
				else if(sl.spacetype==SpaceTypes.SPACE_IMASEL) {
//                    SpaceImaSel *simasel= (SpaceImaSel *)sl;
//					if (simasel.files) {
//						//XXX BIF_filelist_freelib(simasel.files);
//					}
				}
				else if(sl.spacetype==SpaceTypes.SPACE_ACTION) {
//					SpaceAction *saction= (SpaceAction *)sl;
//					saction.action = restore_pointer_by_name(newmain, (ID *)saction.action, 1);
//					saction.ads.source= restore_pointer_by_name(newmain, (ID *)saction.ads.source, 1);
				}
				else if(sl.spacetype==SpaceTypes.SPACE_IMAGE) {
					SpaceImage sima= (SpaceImage)sl;

					sima.image= (Image)restore_pointer_by_name(newmain, (ID)sima.image, 1);
				}
				else if(sl.spacetype==SpaceTypes.SPACE_NLA){
					/* SpaceNla *snla= (SpaceNla *)sl;	*/
				}
				else if(sl.spacetype==SpaceTypes.SPACE_TEXT) {
//					SpaceText *st= (SpaceText *)sl;
//
//					st.text= restore_pointer_by_name(newmain, (ID *)st.text, 1);
//					if(st.text==NULL) st.text= newmain.text.first;
				}
				else if(sl.spacetype==SpaceTypes.SPACE_SCRIPT) {
//					SpaceScript *scpt= (SpaceScript *)sl;
//
//					scpt.script= restore_pointer_by_name(newmain, (ID *)scpt.script, 1);
//
//					/*sc.script = NULL; - 2.45 set to null, better re-run the script */
//					if (scpt.script) {
//						SCRIPT_SET_NULL(scpt.script)
//					}
				}
				else if(sl.spacetype==SpaceTypes.SPACE_OUTLINER) {
//					SpaceOops *so= (SpaceOops *)sl;
//					int a;
//
//					so.search_tse.id= restore_pointer_by_name(newmain, so.search_tse.id, 0);
//
//					if(so.treestore) {
//						TreeStore *ts= so.treestore;
//						TreeStoreElem *tselem=ts.data;
//						for(a=0; a<ts.usedelem; a++, tselem++) {
//							tselem.id= restore_pointer_by_name(newmain, tselem.id, 0);
//						}
//					}
				}
				else if(sl.spacetype==SpaceTypes.SPACE_SOUND) {
//					SpaceSound *ssound= (SpaceSound *)sl;
//
//					ssound.sound= restore_pointer_by_name(newmain, (ID *)ssound.sound, 1);
				}
				else if(sl.spacetype==SpaceTypes.SPACE_NODE) {
//					SpaceNode *snode= (SpaceNode *)sl;
//
//					snode.id= restore_pointer_by_name(newmain, snode.id, 1);
//					snode.edittree= NULL;
//
//					if(snode.id==NULL)
//						snode.nodetree= NULL;
//					else {
//						if(GS(snode.id.name)==ID_MA)
//							snode.nodetree= ((Material *)snode.id).nodetree;
//						else if(GS(snode.id.name)==ID_SCE)
//							snode.nodetree= ((Scene *)snode.id).nodetree;
//						else if(GS(snode.id.name)==ID_TE)
//							snode.nodetree= ((Tex *)snode.id).nodetree;
//					}
				}
			}
			sa= sa.next;
		}
	}
}

public static void direct_link_region(FileData fd, ARegion ar, int spacetype)
{
	Panel pa;

	link_list(fd, ar.panels);

	for(pa= (Panel)ar.panels.first; pa!=null; pa=pa.next) {
		pa.paneltab= (Panel)newdataadr(fd, pa.paneltab);
		pa.runtime_flag= 0;
		pa.activedata= null;
		pa.type= null;
	}

	ar.regiondata= newdataadr(fd, ar.regiondata);
	if(ar.regiondata!=null) {
		if(spacetype==SpaceTypes.SPACE_VIEW3D) {
			RegionView3D rv3d= (RegionView3D)ar.regiondata;

			rv3d.localvd= (RegionView3D)newdataadr(fd, rv3d.localvd);
			rv3d.clipbb= (BoundBox)newdataadr(fd, rv3d.clipbb);

			rv3d.depths= null;
//			rv3d.retopo_view_data= null;
			rv3d.ri= null;
			rv3d.sms= null;
			rv3d.smooth_timer= null;
//			rv3d.lastmode= 0;
		}
	}

	ar.handlers.first= ar.handlers.last= null;
	ar.uiblocks.first= ar.uiblocks.last= null;
	ar.headerstr= null;
	ar.swinid= 0;
	ar.type= null;
	ar.swap= 0;
	ar.do_draw= 0;
//	memset(&ar.drawrct, 0, sizeof(ar.drawrct));
//    ar.drawrct = new rcti();
    Rct.clear(ar.drawrct);
}

/* for the saved 2.50 files without regiondata */
/* and as patch for 2.48 and older */
public static void view3d_split_250(View3D v3d, ListBase<ARegion> regions)
{
	ARegion ar;

	for(ar= regions.first; ar!=null; ar= ar.next) {
		if(ar.regiontype==ScreenTypes.RGN_TYPE_WINDOW && ar.regiondata==null) {
			RegionView3D rv3d;

			ar.regiondata= rv3d = new RegionView3D();
			rv3d.persp= (byte)v3d.persp;
			rv3d.view= (byte)v3d.view;
			rv3d.dist= v3d.dist;
			UtilDefines.VECCOPY(rv3d.ofs, v3d.ofs);
			UtilDefines.QUATCOPY(rv3d.viewquat, v3d.viewquat);
		}
	}
}

public static void direct_link_screen(FileData fd, bScreen sc)
{
	ScrArea sa;
	ScrVert sv;
	ScrEdge se;
	int a;

	link_list(fd, sc.vertbase);
	link_list(fd, sc.edgebase);
	link_list(fd, sc.areabase);
	sc.regionbase.first= sc.regionbase.last= null;
	sc.context= null;

	sc.mainwin= sc.subwinactive= 0;	/* indices */
	sc.swap= 0;

//	/* hacky patch... but people have been saving files with the verse-blender,
//	   causing the handler to keep running for ever, with no means to disable it */
//	for(a=0; a<SCREEN_MAXHANDLER; a+=2) {
//		if( sc.handler[a]==SCREEN_HANDLER_VERSE) {
//			sc.handler[a]= 0;
//			break;
//		}
//	}

	/* edges */
	for(se= (ScrEdge)sc.edgebase.first; se!=null; se= se.next) {
		se.v1= (ScrVert)newdataadr(fd, se.v1);
		se.v2= (ScrVert)newdataadr(fd, se.v2);
//		if( (intptr_t)se.v1 > (intptr_t)se.v2) {
//			sv= se.v1;
//			se.v1= se.v2;
//			se.v2= sv;
//		}

		if(se.v1==null) {
			System.out.printf("error reading screen... file corrupt\n");
			se.v1= se.v2;
		}
	}

	/* areas */
	for(sa= (ScrArea)sc.areabase.first; sa!=null; sa= sa.next) {
		SpaceLink sl;
		ARegion ar;

		link_list(fd, sa.spacedata);
		link_list(fd, sa.regionbase);

		sa.handlers.first= sa.handlers.last= null;
		sa.type= null;	/* spacetype callbacks */

		for(ar= (ARegion)sa.regionbase.first; ar!=null; ar= ar.next)
			direct_link_region(fd, ar, sa.spacetype);

		/* accident can happen when read/save new file with older version */
		/* 2.50: we now always add spacedata for info */
		if(sa.spacedata.first==null) {
			SpaceInfo sinfo= new SpaceInfo();
                        sinfo.spacetype= SpaceTypes.SPACE_INFO;
			sa.spacetype= SpaceTypes.SPACE_INFO;
			ListBaseUtil.BLI_addtail(sa.spacedata, sinfo);
		}
		/* add local view3d too */
		else if(sa.spacetype==SpaceTypes.SPACE_VIEW3D)
			view3d_split_250((View3D)sa.spacedata.first, sa.regionbase);

		for (sl= (SpaceLink)sa.spacedata.first; sl!=null; sl= (SpaceLink)sl.next) {
			link_list(fd, sl.regionbase);

			for(ar= (ARegion)sl.regionbase.first; ar!=null; ar= ar.next)
				direct_link_region(fd, ar, sl.spacetype);

			if (sl.spacetype==SpaceTypes.SPACE_VIEW3D) {
				View3D v3d= (View3D) sl;
				v3d.bgpic= (BGpic)newdataadr(fd, v3d.bgpic);
				if(v3d.bgpic!=null)
					v3d.bgpic.iuser.ok= 1;
//				if(v3d.gpd) {
//					v3d.gpd= newdataadr(fd, v3d.gpd);
//					direct_link_gpencil(fd, v3d.gpd);
//				}
				v3d.localvd= (View3D)newdataadr(fd, v3d.localvd);
//				v3d.afterdraw.first= v3d.afterdraw.last= null;
				v3d.properties_storage= null;

				view3d_split_250(v3d, sl.regionbase);
			}
			else if (sl.spacetype==SpaceTypes.SPACE_IPO) {
				SpaceIpo sipo= (SpaceIpo)sl;

				sipo.ads= (bDopeSheet)newdataadr(fd, sipo.ads);
				sipo.ghostCurves.first= sipo.ghostCurves.last= null;
			}
			else if (sl.spacetype==SpaceTypes.SPACE_NLA) {
				SpaceNla snla= (SpaceNla)sl;

				snla.ads= (bDopeSheet)newdataadr(fd, snla.ads);
			}
			else if (sl.spacetype==SpaceTypes.SPACE_OUTLINER) {
				SpaceOops soops= (SpaceOops) sl;

				soops.treestore= (TreeStore)newdataadr(fd, soops.treestore);
				if(soops.treestore!=null) {
					soops.treestore.data= (TreeStoreElem)newdataadr(fd, soops.treestore.data);
					/* we only saved what was used */
					soops.treestore.totelem= soops.treestore.usedelem;
					soops.storeflag |= SpaceTypes.SO_TREESTORE_CLEANUP;	// at first draw
				}
			}
			else if(sl.spacetype==SpaceTypes.SPACE_IMAGE) {
				SpaceImage sima= (SpaceImage)sl;

				sima.cumap= (CurveMapping)newdataadr(fd, sima.cumap);
				sima.gpd= (bGPdata)newdataadr(fd, sima.gpd);
//				if (sima.gpd)
//					direct_link_gpencil(fd, sima.gpd);
//				if(sima.cumap)
//					direct_link_curvemapping(fd, sima.cumap);
				sima.iuser.scene= null;
				sima.iuser.ok= 1;
			}
			else if(sl.spacetype==SpaceTypes.SPACE_NODE) {
				SpaceNode snode= (SpaceNode)sl;

//				if(snode.gpd) {
//					snode.gpd= newdataadr(fd, snode.gpd);
//					direct_link_gpencil(fd, snode.gpd);
//				}
				snode.nodetree= snode.edittree= null;
			}
			else if(sl.spacetype==SpaceTypes.SPACE_LOGIC) {
				SpaceLogic slogic= (SpaceLogic)sl;

//				if(slogic.gpd) {
//					slogic.gpd= newdataadr(fd, slogic.gpd);
//					direct_link_gpencil(fd, slogic.gpd);
//				}
			}
			else if(sl.spacetype==SpaceTypes.SPACE_SEQ) {
				SpaceSeq sseq= (SpaceSeq )sl;
//				if(sseq.gpd) {
//					sseq.gpd= newdataadr(fd, sseq.gpd);
//					direct_link_gpencil(fd, sseq.gpd);
//				}
			}
			else if(sl.spacetype==SpaceTypes.SPACE_BUTS) {
				SpaceButs sbuts= (SpaceButs)sl;
				sbuts.path= null;
			}
			else if(sl.spacetype==SpaceTypes.SPACE_CONSOLE) {
				SpaceConsole sconsole= (SpaceConsole)sl;
				//ConsoleLine *cl;

				link_list(fd, sconsole.scrollback);
				link_list(fd, sconsole.history);

				//for(cl= sconsole.scrollback.first; cl; cl= cl.next)
				//	cl.line= newdataadr(fd, cl.line);

				//for(cl= sconsole.history.first; cl; cl= cl.next)
				//	cl.line= newdataadr(fd, cl.line);

			}
		}

		sa.actionzones.first= sa.actionzones.last= null;

		sa.v1= (ScrVert)newdataadr(fd, sa.v1);
		sa.v2= (ScrVert)newdataadr(fd, sa.v2);
		sa.v3= (ScrVert)newdataadr(fd, sa.v3);
		sa.v4= (ScrVert)newdataadr(fd, sa.v4);
	}
}

/* ********** READ LIBRARY *************** */


public static void direct_link_library(FileData fd, Library lib, Main main)
{
	Main newmain;

	for(newmain= fd.mainlist.first; newmain!=null; newmain= newmain.next) {
		if(newmain.curlib!=null) {
			if(StringUtil.strcmp(newmain.curlib.filepath,0, lib.filepath,0)==0) {
				System.out.printf("Fixed error in file; multiple instances of lib:\n %s\n", lib.filepath);

				change_idid_adr(fd.mainlist, fd, lib, newmain.curlib);

				ListBaseUtil.BLI_remlink(main.library, lib);
//				MEM_freeN(lib);

//				BKE_report(fd.reports, RPT_WARNING, "Library had multiple instances, save and reload!");

				return;
			}
		}
	}
	/* make sure we have full path in lib.filename */
	StringUtil.BLI_strncpy(lib.filepath,0, lib.name,0, lib.name.length);
//	cleanup_path(fd.filename, lib.filename);

	/* new main */
	newmain= new Main();
	ListBaseUtil.BLI_addtail(fd.mainlist, newmain);
	newmain.curlib= lib;

	lib.parent= null;
}

public static void lib_link_library(FileData fd, Main main)
{
	Library lib;
	for(lib= (Library)main.library.first; lib!=null; lib= (Library)lib.id.next) {
		lib.id.us= 1;
	}
}

///* Always call this once you havbe loaded new library data to set the relative paths correctly in relation to the blend file */
//static void fix_relpaths_library(const char *basepath, Main *main)
//{
//	Library *lib;
//	/* BLO_read_from_memory uses a blank filename */
//	if (basepath==NULL || basepath[0] == '\0')
//		return;
//
//	for(lib= main.library.first; lib; lib= lib.id.next) {
//		/* Libraries store both relative and abs paths, recreate relative paths,
//		 * relative to the blend file since indirectly linked libs will be relative to their direct linked library */
//		if (strncmp(lib.name, "//", 2)==0) { /* if this is relative to begin with? */
//			strncpy(lib.name, lib.filename, sizeof(lib.name));
//			BLI_makestringcode(basepath, lib.name);
//		}
//	}
//}
//
///* ************** READ SOUND ******************* */
//
//static void direct_link_sound(FileData *fd, bSound *sound)
//{
//	sound.sample = NULL;
//	sound.snd_sound = NULL;
//
//	sound.packedfile = direct_link_packedfile(fd, sound.packedfile);
//	sound.newpackedfile = direct_link_packedfile(fd, sound.newpackedfile);
//}
//
//static void lib_link_sound(FileData *fd, Main *main)
//{
//	bSound *sound;
//
//	sound= main.sound.first;
//	while(sound) {
//		if(sound.id.flag & LIB_NEEDLINK) {
//			sound.id.flag -= LIB_NEEDLINK;
//			sound.ipo= newlibadr_us(fd, sound.id.lib, sound.ipo); // XXX depreceated - old animation system
//			sound.stream = 0;
//		}
//		sound= sound.id.next;
//	}
//}
/* ***************** READ GROUP *************** */

public static void direct_link_group(FileData fd, Group group)
{
	link_list(fd, group.gobject);
}

public static void lib_link_group(FileData fd, Main main)
{
	Group group= main.group.first;
	GroupObject go;
	boolean add_us;
	
	while(group!=null) {
		if((group.id.flag & DNA_ID.LIB_NEEDLINK)!=0) {
			group.id.flag -= DNA_ID.LIB_NEEDLINK;
			
			add_us= false;
			
			go= (GroupObject)group.gobject.first;
			while(go!=null) {
				go.ob= (bObject)newlibadr(fd, group.id.lib, go.ob);
				if(go.ob!=null) {
					go.ob.flag |= ObjectTypes.OB_FROMGROUP;
					/* if group has an object, it increments user... */
					add_us= true;
					if(go.ob.id.us==0) 
						go.ob.id.us= 1;
				}
				go= go.next;
			}
			if(add_us) group.id.us++;
//			rem_from_group(group, null, null, null);	/* removes NULL entries */
		}
		group= (Group)group.id.next;
	}
}

///* ************** GENERAL & MAIN ******************** */
//
//
//static char *dataname(short id_code)
//{
//
//	switch( id_code ) {
//		case ID_OB: return "Data from OB";
//		case ID_ME: return "Data from ME";
//		case ID_IP: return "Data from IP";
//		case ID_SCE: return "Data from SCE";
//		case ID_MA: return "Data from MA";
//		case ID_TE: return "Data from TE";
//		case ID_CU: return "Data from CU";
//		case ID_GR: return "Data from GR";
//		case ID_AR: return "Data from AR";
//		case ID_AC: return "Data from AC";
//		case ID_LI: return "Data from LI";
//		case ID_MB: return "Data from MB";
//		case ID_IM: return "Data from IM";
//		case ID_LT: return "Data from LT";
//		case ID_LA: return "Data from LA";
//		case ID_CA: return "Data from CA";
//		case ID_KE: return "Data from KE";
//		case ID_WO: return "Data from WO";
//		case ID_SCR: return "Data from SCR";
//		case ID_VF: return "Data from VF";
//		case ID_TXT	: return "Data from TXT";
//		case ID_SO: return "Data from SO";
//		case ID_NT: return "Data from NT";
//		case ID_BR: return "Data from BR";
//		case ID_PA: return "Data from PA";
//		case ID_GD: return "Data from GD";
//	}
//	return "Data from Lib Block";
//
//}

public static BHead read_libblock(FileData fd, Main main, BHead bhead, int flag, ID[] id_r)
{
	/* this routine reads a libblock and its direct data. Use link functions
	 * to connect it all
	 */

	ID id;
	ListBase lb;
//	char *allocname;
    BHead nextBHead; // TMP

	/* read libblock */
	id = (ID)read_struct(fd, bhead, DNATools.getClassType(bhead.SDNAnr));
	if (id_r!=null)
		id_r[0]= id;
	if (id==null)
		return blo_nextbhead(fd, bhead);

	oldnewmap_insert(fd.libmap, bhead.old, id, bhead.code);	/* for ID_ID check */

	/* do after read_struct, for dna reconstruct */
	if(bhead.code==DNA_ID.ID_ID) {
		lb= LibraryUtil.wich_libbase(main, LibraryUtil.GS(id.name));
	}
	else {
		lb= LibraryUtil.wich_libbase(main, (short)(bhead.code>>16));
	}

	ListBaseUtil.BLI_addtail(lb, id);

	/* clear first 8 bits */
	id.flag= (short)((id.flag & 0xFF00) | flag | DNA_ID.LIB_NEEDLINK);
	id.lib= main.curlib;
	if((id.flag & DNA_ID.LIB_FAKEUSER)!=0) id.us= 1;
	else id.us= 0;
	id.icon_id = 0;

	/* this case cannot be direct_linked: it's just the ID part */
	if(bhead.code==DNA_ID.ID_ID) {
		return blo_nextbhead(fd, bhead);
	}

	nextBHead = blo_nextbhead(fd, bhead);

//	/* need a name for the mallocN, just for debugging and sane prints on leaks */
//	allocname= dataname(GS(id.name));

	/* read all data */

	while(nextBHead!=null && nextBHead.code==UtilDefines.DATA) {
        if (nextBHead.SDNAnr != 0) { // HACK shouldn't have to check this
            Object data;
            data= read_struct(fd, nextBHead, DNATools.getClassType(nextBHead.SDNAnr));

            if (data!=null) {
                oldnewmap_insert(fd.datamap, nextBHead.old, data, 0);
            }
        }

		nextBHead = blo_nextbhead(fd, nextBHead);
	}

	/* init pointers direct data */
	switch( LibraryUtil.GS(id.name) ) {
		case DNA_ID.ID_WM:
			direct_link_windowmanager(fd, (wmWindowManager)id);
			break;
		case DNA_ID.ID_SCR:
			direct_link_screen(fd, (bScreen)id);
			break;
		case DNA_ID.ID_SCE:
			direct_link_scene(fd, (Scene)id);
			break;
		case DNA_ID.ID_OB:
			direct_link_object(fd, (bObject)id);
			break;
		case DNA_ID.ID_ME:
			direct_link_mesh(fd, (Mesh)id);
			break;
		case DNA_ID.ID_CU:
//			direct_link_curve(fd, (Curve *)id);
			break;
		case DNA_ID.ID_MB:
//			direct_link_mball(fd, (MetaBall *)id);
			break;
		case DNA_ID.ID_MA:
//			direct_link_material(fd, (Material *)id);
			break;
		case DNA_ID.ID_TE:
//			direct_link_texture(fd, (Tex *)id);
			break;
		case DNA_ID.ID_IM:
			direct_link_image(fd, (Image)id);
			break;
		case DNA_ID.ID_LA:
			direct_link_lamp(fd, (Lamp)id);
			break;
		case DNA_ID.ID_VF:
//			direct_link_vfont(fd, (VFont *)id);
			break;
		case DNA_ID.ID_TXT:
//			direct_link_text(fd, (Text *)id);
			break;
		case DNA_ID.ID_IP:
//			direct_link_ipo(fd, (Ipo *)id);
			break;
		case DNA_ID.ID_KE:
//			direct_link_key(fd, (Key *)id);
			break;
		case DNA_ID.ID_LT:
//			direct_link_latt(fd, (Lattice *)id);
			break;
		case DNA_ID.ID_WO:
			direct_link_world(fd, (World)id);
			break;
		case DNA_ID.ID_LI:
			direct_link_library(fd, (Library)id, main);
			break;
		case DNA_ID.ID_CA:
			direct_link_camera(fd, (Camera)id);
			break;
		case DNA_ID.ID_SO:
//			direct_link_sound(fd, (bSound *)id);
			break;
		case DNA_ID.ID_GR:
			direct_link_group(fd, (Group)id);
			break;
		case DNA_ID.ID_AR:
//			direct_link_armature(fd, (bArmature*)id);
			break;
		case DNA_ID.ID_AC:
//			direct_link_action(fd, (bAction*)id);
			break;
		case DNA_ID.ID_NT:
//			direct_link_nodetree(fd, (bNodeTree*)id);
			break;
		case DNA_ID.ID_BR:
//			direct_link_brush(fd, (Brush*)id);
			break;
		case DNA_ID.ID_PA:
//			direct_link_particlesettings(fd, (ParticleSettings*)id);
			break;
		case DNA_ID.ID_SCRIPT:
//			direct_link_script(fd, (Script*)id);
			break;
		case DNA_ID.ID_GD:
//			direct_link_gpencil(fd, (bGPdata *)id);
			break;
	}

	/*link direct data of ID properties*/
//	if (id.properties!=null) {
//		id.properties = (IDProperty)newdataadr(fd, id.properties);
//		if (id.properties!=null) { /* this case means the data was written incorrectly, it should not happen */
//			IDP_DirectLinkProperty(id.properties, (fd.flags & FD_FLAGS_SWITCH_ENDIAN), fd);
//		}
//	}

//	oldnewmap_free_unused(fd.datamap);
//	oldnewmap_clear(fd.datamap);

	return nextBHead;
}

/* note, this has to be kept for reading older files... */
/* also version info is written here */
public static BHead read_global(BlendFileData bfd, FileData fd, BHead bhead)
{
	FileGlobal fg= read_struct(fd, bhead, FileGlobal.class);

	/* copy to bfd handle */
	bfd.main.subversionfile= fg.subversion;
	bfd.main.minversionfile= fg.minversion;
	bfd.main.minsubversionfile= fg.minsubversion;

	bfd.winpos= fg.winpos;
	bfd.fileflags= fg.fileflags;
	bfd.displaymode= fg.displaymode;
	bfd.globalf= fg.globalf;

	bfd.curscreen= fg.curscreen;
	bfd.curscene= fg.curscene;

//	MEM_freeN(fg);

	return blo_nextbhead(fd, bhead);
}

/* note, this has to be kept for reading older files... */
public static void link_global(FileData fd, BlendFileData bfd)
{

	bfd.curscreen= (bScreen)newlibadr(fd, 0, bfd.curscreen);
	bfd.curscene= (Scene)newlibadr(fd, 0, bfd.curscene);
	// this happens in files older than 2.35
	if(bfd.curscene==null) {
		if(bfd.curscreen!=null) bfd.curscene= bfd.curscreen.scene;
	}
}

//static void vcol_to_fcol(Mesh *me)
//{
//	MFace *mface;
//	unsigned int *mcol, *mcoln, *mcolmain;
//	int a;
//
//	if(me.totface==0 || me.mcol==0) return;
//
//	mcoln= mcolmain= MEM_mallocN(4*sizeof(int)*me.totface, "mcoln");
//	mcol = (unsigned int *)me.mcol;
//	mface= me.mface;
//	for(a=me.totface; a>0; a--, mface++) {
//		mcoln[0]= mcol[mface.v1];
//		mcoln[1]= mcol[mface.v2];
//		mcoln[2]= mcol[mface.v3];
//		mcoln[3]= mcol[mface.v4];
//		mcoln+= 4;
//	}
//
//	MEM_freeN(me.mcol);
//	me.mcol= (MCol *)mcolmain;
//}
//
//static int map_223_keybd_code_to_224_keybd_code(int code)
//{
//	switch (code) {
//		case 312:	return 311; /* F12KEY */
//		case 159:	return 161; /* PADSLASHKEY */
//		case 161:	return 150; /* PAD0 */
//		case 154:	return 151; /* PAD1 */
//		case 150:	return 152; /* PAD2 */
//		case 155:	return 153; /* PAD3 */
//		case 151:	return 154; /* PAD4 */
//		case 156:	return 155; /* PAD5 */
//		case 152:	return 156; /* PAD6 */
//		case 157:	return 157; /* PAD7 */
//		case 153:	return 158; /* PAD8 */
//		case 158:	return 159; /* PAD9 */
//		default: return code;
//	}
//}
//
//static void bone_version_238(ListBase *lb)
//{
//	Bone *bone;
//
//	for(bone= lb.first; bone; bone= bone.next) {
//		if(bone.rad_tail==0.0f && bone.rad_head==0.0f) {
//			bone.rad_head= 0.25f*bone.length;
//			bone.rad_tail= 0.1f*bone.length;
//
//			bone.dist-= bone.rad_head;
//			if(bone.dist<=0.0f) bone.dist= 0.0f;
//		}
//		bone_version_238(&bone.childbase);
//	}
//}
//
//static void bone_version_239(ListBase *lb)
//{
//	Bone *bone;
//
//	for(bone= lb.first; bone; bone= bone.next) {
//		if(bone.layer==0)
//			bone.layer= 1;
//		bone_version_239(&bone.childbase);
//	}
//}
//
//static void ntree_version_241(bNodeTree *ntree)
//{
//	bNode *node;
//
//	if(ntree.type==NTREE_COMPOSIT) {
//		for(node= ntree.nodes.first; node; node= node.next) {
//			if(node.type==CMP_NODE_BLUR) {
//				if(node.storage==NULL) {
//					NodeBlurData *nbd= MEM_callocN(sizeof(NodeBlurData), "node blur patch");
//					nbd.sizex= node.custom1;
//					nbd.sizey= node.custom2;
//					nbd.filtertype= R_FILTER_QUAD;
//					node.storage= nbd;
//				}
//			}
//			else if(node.type==CMP_NODE_VECBLUR) {
//				if(node.storage==NULL) {
//					NodeBlurData *nbd= MEM_callocN(sizeof(NodeBlurData), "node blur patch");
//					nbd.samples= node.custom1;
//					nbd.maxspeed= node.custom2;
//					nbd.fac= 1.0f;
//					node.storage= nbd;
//				}
//			}
//		}
//	}
//}
//
//static void ntree_version_242(bNodeTree *ntree)
//{
//	bNode *node;
//
//	if(ntree.type==NTREE_COMPOSIT) {
//		for(node= ntree.nodes.first; node; node= node.next) {
//			if(node.type==CMP_NODE_HUE_SAT) {
//				if(node.storage) {
//					NodeHueSat *nhs= node.storage;
//					if(nhs.val==0.0f) nhs.val= 1.0f;
//				}
//			}
//		}
//	}
//	else if(ntree.type==NTREE_SHADER) {
//		for(node= ntree.nodes.first; node; node= node.next)
//			if(node.type == SH_NODE_GEOMETRY && node.storage == NULL)
//				node.storage= MEM_callocN(sizeof(NodeGeometry), "NodeGeometry");
//	}
//
//}
//
//
///* somehow, probably importing via python, keyblock adrcodes are not in order */
//static void sort_shape_fix(Main *main)
//{
//	Key *key;
//	KeyBlock *kb;
//	int sorted= 0;
//
//	while(sorted==0) {
//		sorted= 1;
//		for(key= main.key.first; key; key= key.id.next) {
//			for(kb= key.block.first; kb; kb= kb.next) {
//				if(kb.next && kb.adrcode>kb.next.adrcode) {
//					KeyBlock *next= kb.next;
//					BLI_remlink(&key.block, kb);
//					BLI_insertlink(&key.block, next, kb);
//					kb= next;
//					sorted= 0;
//				}
//			}
//		}
//		if(sorted==0) printf("warning, shape keys were sorted incorrect, fixed it!\n");
//	}
//}
//
//static void customdata_version_242(Mesh *me)
//{
//	CustomDataLayer *layer;
//	MTFace *mtf;
//	MCol *mcol;
//	TFace *tf;
//	int a, mtfacen, mcoln;
//
//	if (!me.vdata.totlayer) {
//		CustomData_add_layer(&me.vdata, CD_MVERT, CD_ASSIGN, me.mvert, me.totvert);
//
//		if (me.msticky)
//			CustomData_add_layer(&me.vdata, CD_MSTICKY, CD_ASSIGN, me.msticky, me.totvert);
//		if (me.dvert)
//			CustomData_add_layer(&me.vdata, CD_MDEFORMVERT, CD_ASSIGN, me.dvert, me.totvert);
//	}
//
//	if (!me.edata.totlayer)
//		CustomData_add_layer(&me.edata, CD_MEDGE, CD_ASSIGN, me.medge, me.totedge);
//
//	if (!me.fdata.totlayer) {
//		CustomData_add_layer(&me.fdata, CD_MFACE, CD_ASSIGN, me.mface, me.totface);
//
//		if (me.tface) {
//			if (me.mcol)
//				MEM_freeN(me.mcol);
//
//			me.mcol= CustomData_add_layer(&me.fdata, CD_MCOL, CD_CALLOC, NULL, me.totface);
//			me.mtface= CustomData_add_layer(&me.fdata, CD_MTFACE, CD_CALLOC, NULL, me.totface);
//
//			mtf= me.mtface;
//			mcol= me.mcol;
//			tf= me.tface;
//
//			for (a=0; a < me.totface; a++, mtf++, tf++, mcol+=4) {
//				memcpy(mcol, tf.col, sizeof(tf.col));
//				memcpy(mtf.uv, tf.uv, sizeof(tf.uv));
//
//				mtf.flag= tf.flag;
//				mtf.unwrap= tf.unwrap;
//				mtf.mode= tf.mode;
//				mtf.tile= tf.tile;
//				mtf.tpage= tf.tpage;
//				mtf.transp= tf.transp;
//			}
//
//			MEM_freeN(me.tface);
//			me.tface= NULL;
//		}
//		else if (me.mcol) {
//			me.mcol= CustomData_add_layer(&me.fdata, CD_MCOL, CD_ASSIGN, me.mcol, me.totface);
//		}
//	}
//
//	if (me.tface) {
//		MEM_freeN(me.tface);
//		me.tface= NULL;
//	}
//
//	for (a=0, mtfacen=0, mcoln=0; a < me.fdata.totlayer; a++) {
//		layer= &me.fdata.layers[a];
//
//		if (layer.type == CD_MTFACE) {
//			if (layer.name[0] == 0) {
//				if (mtfacen == 0) strcpy(layer.name, "UVTex");
//				else sprintf(layer.name, "UVTex.%.3d", mtfacen);
//			}
//			mtfacen++;
//		}
//		else if (layer.type == CD_MCOL) {
//			if (layer.name[0] == 0) {
//				if (mcoln == 0) strcpy(layer.name, "Col");
//				else sprintf(layer.name, "Col.%.3d", mcoln);
//			}
//			mcoln++;
//		}
//	}
//
//	mesh_update_customdata_pointers(me);
//}
//
///*only copy render texface layer from active*/
//static void customdata_version_243(Mesh *me)
//{
//	CustomDataLayer *layer;
//	int a;
//
//	for (a=0; a < me.fdata.totlayer; a++) {
//		layer= &me.fdata.layers[a];
//		layer.active_rnd = layer.active;
//	}
//}
//
///* struct NodeImageAnim moved to ImageUser, and we make it default available */
//static void do_version_ntree_242_2(bNodeTree *ntree)
//{
//	bNode *node;
//
//	if(ntree.type==NTREE_COMPOSIT) {
//		for(node= ntree.nodes.first; node; node= node.next) {
//			if(ELEM3(node.type, CMP_NODE_IMAGE, CMP_NODE_VIEWER, CMP_NODE_SPLITVIEWER)) {
//				/* only image had storage */
//				if(node.storage) {
//					NodeImageAnim *nia= node.storage;
//					ImageUser *iuser= MEM_callocN(sizeof(ImageUser), "ima user node");
//
//					iuser.frames= nia.frames;
//					iuser.sfra= nia.sfra;
//					iuser.offset= nia.nr-1;
//					iuser.cycl= nia.cyclic;
//					iuser.fie_ima= 2;
//					iuser.ok= 1;
//
//					node.storage= iuser;
//					MEM_freeN(nia);
//				}
//				else {
//					ImageUser *iuser= node.storage= MEM_callocN(sizeof(ImageUser), "node image user");
//					iuser.sfra= 1;
//					iuser.fie_ima= 2;
//					iuser.ok= 1;
//				}
//			}
//		}
//	}
//}
//
//static void ntree_version_245(FileData *fd, Library *lib, bNodeTree *ntree)
//{
//	bNode *node;
//	NodeTwoFloats *ntf;
//	ID *nodeid;
//	Image *image;
//	ImageUser *iuser;
//
//	if(ntree.type==NTREE_COMPOSIT) {
//		for(node= ntree.nodes.first; node; node= node.next) {
//			if(node.type == CMP_NODE_ALPHAOVER) {
//				if(!node.storage) {
//					ntf= MEM_callocN(sizeof(NodeTwoFloats), "NodeTwoFloats");
//					node.storage= ntf;
//					if(node.custom1)
//						ntf.x= 1.0f;
//				}
//			}
//
//			/* fix for temporary flag changes during 245 cycle */
//			nodeid= newlibadr(fd, lib, node.id);
//			if(node.storage && nodeid && GS(nodeid.name) == ID_IM) {
//				image= (Image*)nodeid;
//				iuser= node.storage;
//				if(iuser.flag & IMA_OLD_PREMUL) {
//					iuser.flag &= ~IMA_OLD_PREMUL;
//					iuser.flag |= IMA_DO_PREMUL;
//				}
//				if(iuser.flag & IMA_DO_PREMUL) {
//					image.flag &= ~IMA_OLD_PREMUL;
//					image.flag |= IMA_DO_PREMUL;
//				}
//			}
//		}
//	}
//}
//
//static void idproperties_fix_groups_lengths_recurse(IDProperty *prop)
//{
//	IDProperty *loop;
//	int i;
//
//	for (loop=prop.data.group.first, i=0; loop; loop=loop.next, i++) {
//		if (loop.type == IDP_GROUP) idproperties_fix_groups_lengths_recurse(loop);
//	}
//
//	if (prop.len != i) {
//		printf("Found and fixed bad id property group length.\n");
//		prop.len = i;
//	}
//}
//
//static void idproperties_fix_group_lengths(ListBase idlist)
//{
//	ID *id;
//
//	for (id=idlist.first; id; id=id.next) {
//		if (id.properties) {
//			idproperties_fix_groups_lengths_recurse(id.properties);
//		}
//	}
//}
//
//static void alphasort_version_246(FileData *fd, Library *lib, Mesh *me)
//{
//	Material *ma;
//	MFace *mf;
//	MTFace *tf;
//	int a, b, texalpha;
//
//	/* verify we have a tface layer */
//	for(b=0; b<me.fdata.totlayer; b++)
//		if(me.fdata.layers[b].type == CD_MTFACE)
//			break;
//
//	if(b == me.fdata.totlayer)
//		return;
//
//	/* if we do, set alpha sort if the game engine did it before */
//	for(a=0, mf=me.mface; a<me.totface; a++, mf++) {
//		if(mf.mat_nr < me.totcol) {
//			ma= newlibadr(fd, lib, me.mat[(int)mf.mat_nr]);
//			texalpha = 0;
//
//			/* we can't read from this if it comes from a library,
//			 * because direct_link might not have happened on it,
//			 * so ma.mtex is not pointing to valid memory yet */
//			if(ma && ma.id.lib)
//				ma= NULL;
//
//			for(b=0; ma && b<MAX_MTEX; b++)
//				if(ma.mtex && ma.mtex[b] && ma.mtex[b].mapto & MAP_ALPHA)
//					texalpha = 1;
//		}
//		else {
//			ma= NULL;
//			texalpha = 0;
//		}
//
//		for(b=0; b<me.fdata.totlayer; b++) {
//			if(me.fdata.layers[b].type == CD_MTFACE) {
//				tf = ((MTFace*)me.fdata.layers[b].data) + a;
//
//				tf.mode &= ~TF_ALPHASORT;
//				if(ma && (ma.mode & MA_ZTRA))
//					if(ELEM(tf.transp, TF_ALPHA, TF_ADD) || (texalpha && (tf.transp != TF_CLIP)))
//						tf.mode |= TF_ALPHASORT;
//			}
//		}
//	}
//}
//
///* 2.50 patch */
//static void area_add_header_region(ScrArea *sa, ListBase *lb)
//{
//	ARegion *ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//
//	BLI_addtail(lb, ar);
//	ar.regiontype= RGN_TYPE_HEADER;
//	if(sa.headertype==1)
//		ar.alignment= RGN_ALIGN_BOTTOM;
//	else
//		ar.alignment= RGN_ALIGN_TOP;
//
//	/* initialise view2d data for header region, to allow panning */
//	/* is copy from ui_view2d.c */
//	ar.v2d.keepzoom = (V2D_LOCKZOOM_X|V2D_LOCKZOOM_Y|V2D_KEEPZOOM|V2D_KEEPASPECT);
//	ar.v2d.keepofs = V2D_LOCKOFS_Y;
//	ar.v2d.keeptot = V2D_KEEPTOT_STRICT;
//	ar.v2d.align = V2D_ALIGN_NO_NEG_X|V2D_ALIGN_NO_NEG_Y;
//	ar.v2d.flag = (V2D_PIXELOFS_X|V2D_PIXELOFS_Y);
//}
//
///* 2.50 patch */
//static void area_add_window_regions(ScrArea *sa, SpaceLink *sl, ListBase *lb)
//{
//	ARegion *ar;
//
//	if(sl) {
//		/* first channels for ipo action nla... */
//		switch(sl.spacetype) {
//			case SPACE_IPO:
//				ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_LEFT;
//				ar.v2d.scroll= (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM);
//				break;
//
//			case SPACE_ACTION:
//				ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_LEFT;
//				ar.v2d.scroll= V2D_SCROLL_BOTTOM;
//				ar.v2d.flag = V2D_VIEWSYNC_AREA_VERTICAL;
//				break;
//
//			case SPACE_NLA:
//				ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_LEFT;
//				ar.v2d.scroll= V2D_SCROLL_BOTTOM;
//				ar.v2d.flag = V2D_VIEWSYNC_AREA_VERTICAL;
//				break;
//
//			case SPACE_NODE:
//				ar= MEM_callocN(sizeof(ARegion), "nodetree area for node");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_LEFT;
//				ar.v2d.scroll = (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM);
//				ar.v2d.flag = V2D_VIEWSYNC_AREA_VERTICAL;
//				/* temporarily hide it */
//				ar.flag = RGN_FLAG_HIDDEN;
//				break;
//			case SPACE_FILE:
//				ar= MEM_callocN(sizeof(ARegion), "nodetree area for node");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_LEFT;
//
//				ar= MEM_callocN(sizeof(ARegion), "ui area for file");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_UI;
//				ar.alignment= RGN_ALIGN_TOP;
//				break;
//#if 0
//			case SPACE_BUTS:
//				/* context UI region */
//				ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//				BLI_addtail(lb, ar);
//				ar.regiontype= RGN_TYPE_CHANNELS;
//				ar.alignment= RGN_ALIGN_TOP;
//				break;
//#endif
//		}
//	}
//
//	/* main region */
//	ar= MEM_callocN(sizeof(ARegion), "area region from do_versions");
//
//	BLI_addtail(lb, ar);
//	ar.winrct= sa.totrct;
//
//	ar.regiontype= RGN_TYPE_WINDOW;
//
//	if(sl) {
//		/* if active spacetype has view2d data, copy that over to main region */
//		/* and we split view3d */
//		switch(sl.spacetype) {
//			case SPACE_VIEW3D:
//				view3d_split_250((View3D *)sl, lb);
//				break;
//
//			case SPACE_OUTLINER:
//			{
//				SpaceOops *soops= (SpaceOops *)sl;
//
//				memcpy(&ar.v2d, &soops.v2d, sizeof(View2D));
//
//				ar.v2d.scroll &= ~V2D_SCROLL_LEFT;
//				ar.v2d.scroll |= (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM_O);
//				ar.v2d.align = (V2D_ALIGN_NO_NEG_X|V2D_ALIGN_NO_POS_Y);
//				ar.v2d.keepzoom |= (V2D_LOCKZOOM_X|V2D_LOCKZOOM_Y|V2D_KEEPASPECT);
//				ar.v2d.keeptot = V2D_KEEPTOT_STRICT;
//				ar.v2d.minzoom= ar.v2d.maxzoom= 1.0f;
//				//ar.v2d.flag |= V2D_IS_INITIALISED;
//			}
//				break;
//			case SPACE_TIME:
//			{
//				SpaceTime *stime= (SpaceTime *)sl;
//				memcpy(&ar.v2d, &stime.v2d, sizeof(View2D));
//
//				ar.v2d.scroll |= (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.align |= V2D_ALIGN_NO_NEG_Y;
//				ar.v2d.keepofs |= V2D_LOCKOFS_Y;
//				ar.v2d.keepzoom |= V2D_LOCKZOOM_Y;
//				ar.v2d.tot.ymin= ar.v2d.cur.ymin= -10.0;
//				ar.v2d.min[1]= ar.v2d.max[1]= 20.0;
//			}
//				break;
//			case SPACE_IPO:
//			{
//				SpaceIpo *sipo= (SpaceIpo *)sl;
//				memcpy(&ar.v2d, &sipo.v2d, sizeof(View2D));
//
//				/* init mainarea view2d */
//				ar.v2d.scroll |= (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.scroll |= (V2D_SCROLL_LEFT|V2D_SCROLL_SCALE_VERTICAL);
//
//				//ar.v2d.flag |= V2D_IS_INITIALISED;
//				break;
//			}
//			case SPACE_SOUND:
//			{
//				SpaceSound *ssound= (SpaceSound *)sl;
//				memcpy(&ar.v2d, &ssound.v2d, sizeof(View2D));
//
//				ar.v2d.scroll |= (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.scroll |= (V2D_SCROLL_LEFT);
//				//ar.v2d.flag |= V2D_IS_INITIALISED;
//				break;
//			}
//			case SPACE_NLA:
//			{
//				SpaceNla *snla= (SpaceNla *)sl;
//				memcpy(&ar.v2d, &snla.v2d, sizeof(View2D));
//
//				ar.v2d.scroll |= (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.scroll |= (V2D_SCROLL_RIGHT);
//				ar.v2d.align = V2D_ALIGN_NO_POS_Y;
//				ar.v2d.flag |= V2D_VIEWSYNC_AREA_VERTICAL;
//				break;
//			}
//			case SPACE_ACTION:
//			{
//				/* we totally reinit the view for the Action Editor, as some old instances had some weird cruft set */
//				ar.v2d.tot.xmin= -20.0f;
//				ar.v2d.tot.ymin= (float)(-sa.winy);
//				ar.v2d.tot.xmax= (float)((sa.winx > 120)? (sa.winx) : 120);
//				ar.v2d.tot.ymax= 0.0f;
//
//				ar.v2d.cur= ar.v2d.tot;
//
//				ar.v2d.min[0]= 0.0f;
// 				ar.v2d.min[1]= 0.0f;
//
//				ar.v2d.max[0]= MAXFRAMEF;
// 				ar.v2d.max[1]= 10000.0f;
//
//				ar.v2d.minzoom= 0.01f;
//				ar.v2d.maxzoom= 50;
//				ar.v2d.scroll = (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.scroll |= (V2D_SCROLL_RIGHT);
//				ar.v2d.keepzoom= V2D_LOCKZOOM_Y;
//				ar.v2d.align= V2D_ALIGN_NO_POS_Y;
//				ar.v2d.flag = V2D_VIEWSYNC_AREA_VERTICAL;
//				break;
//			}
//			case SPACE_SEQ:
//			{
//				SpaceSeq *sseq= (SpaceSeq *)sl;
//				memcpy(&ar.v2d, &sseq.v2d, sizeof(View2D));
//
//				ar.v2d.scroll |= (V2D_SCROLL_BOTTOM|V2D_SCROLL_SCALE_HORIZONTAL);
//				ar.v2d.scroll |= (V2D_SCROLL_LEFT|V2D_SCROLL_SCALE_VERTICAL);
//				ar.v2d.align= V2D_ALIGN_NO_NEG_Y;
//				ar.v2d.flag |= V2D_IS_INITIALISED;
//				break;
//			}
//			case SPACE_NODE:
//			{
//				SpaceNode *snode= (SpaceNode *)sl;
//				memcpy(&ar.v2d, &snode.v2d, sizeof(View2D));
//
//				ar.v2d.scroll= (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM);
//				ar.v2d.keepzoom= V2D_KEEPZOOM|V2D_KEEPASPECT;
//				break;
//			}
//			case SPACE_BUTS:
//			{
//				SpaceButs *sbuts= (SpaceButs *)sl;
//				memcpy(&ar.v2d, &sbuts.v2d, sizeof(View2D));
//
//				ar.v2d.scroll |= (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM);
//				break;
//			}
//			case SPACE_FILE:
// 			{
//				// SpaceFile *sfile= (SpaceFile *)sl;
//				ar.v2d.tot.xmin = ar.v2d.tot.ymin = 0;
//				ar.v2d.tot.xmax = ar.winx;
//				ar.v2d.tot.ymax = ar.winy;
//				ar.v2d.cur = ar.v2d.tot;
//				ar.regiontype= RGN_TYPE_WINDOW;
//				ar.v2d.scroll = (V2D_SCROLL_RIGHT|V2D_SCROLL_BOTTOM_O);
//				ar.v2d.align = (V2D_ALIGN_NO_NEG_X|V2D_ALIGN_NO_POS_Y);
//				ar.v2d.keepzoom = (V2D_LOCKZOOM_X|V2D_LOCKZOOM_Y|V2D_KEEPZOOM|V2D_KEEPASPECT);
//				break;
//			}
//			case SPACE_TEXT:
//			{
//				SpaceText *st= (SpaceText *)sl;
//				st.flags |= ST_FIND_WRAP;
//			}
//				//case SPACE_XXX: // FIXME... add other ones
//				//	memcpy(&ar.v2d, &((SpaceXxx *)sl).v2d, sizeof(View2D));
//				//	break;
//		}
//	}
//}
//
//static void do_versions_windowmanager_2_50(bScreen *screen)
//{
//	ScrArea *sa;
//	SpaceLink *sl;
//
//	/* add regions */
//	for(sa= screen.areabase.first; sa; sa= sa.next) {
//
//		/* we keep headertype variable to convert old files only */
//		if(sa.headertype)
//			area_add_header_region(sa, &sa.regionbase);
//
//		area_add_window_regions(sa, sa.spacedata.first, &sa.regionbase);
//
//		/* space imageselect is depricated */
//		for(sl= sa.spacedata.first; sl; sl= sl.next) {
//			if(sl.spacetype==SPACE_IMASEL)
//				sl.spacetype= SPACE_INFO;	/* spacedata then matches */
//		}
//
//		/* pushed back spaces also need regions! */
//		if(sa.spacedata.first) {
//			sl= sa.spacedata.first;
//			for(sl= sl.next; sl; sl= sl.next) {
//				if(sa.headertype)
//					area_add_header_region(sa, &sl.regionbase);
//				area_add_window_regions(sa, sl, &sl.regionbase);
//			}
//		}
//	}
//}
//
//static void versions_gpencil_add_main(ListBase *lb, ID *id, char *name)
//{
//
//	BLI_addtail(lb, id);
//	id.us= 1;
//	id.flag= LIB_FAKEUSER;
//	*( (short *)id.name )= ID_GD;
//
//	new_id(lb, id, name);
//	/* alphabetic insterion: is in new_id */
//
//	if(G.f & G_DEBUG)
//		printf("Converted GPencil to ID: %s\n", id.name+2);
//}
//
//static void do_versions_gpencil_2_50(Main *main, bScreen *screen)
//{
//	ScrArea *sa;
//	SpaceLink *sl;
//
//	/* add regions */
//	for(sa= screen.areabase.first; sa; sa= sa.next) {
//		for(sl= sa.spacedata.first; sl; sl= sl.next) {
//			if (sl.spacetype==SPACE_VIEW3D) {
//				View3D *v3d= (View3D*) sl;
//				if(v3d.gpd) {
//					versions_gpencil_add_main(&main.gpencil, (ID *)v3d.gpd, "GPencil View3D");
//					v3d.gpd= NULL;
//				}
//			}
//			else if (sl.spacetype==SPACE_NODE) {
//				SpaceNode *snode= (SpaceNode *)sl;
//				if(snode.gpd) {
//					versions_gpencil_add_main(&main.gpencil, (ID *)snode.gpd, "GPencil Node");
//					snode.gpd= NULL;
//				}
//			}
//			else if (sl.spacetype==SPACE_SEQ) {
//				SpaceSeq *sseq= (SpaceSeq *)sl;
//				if(sseq.gpd) {
//					versions_gpencil_add_main(&main.gpencil, (ID *)sseq.gpd, "GPencil Node");
//					sseq.gpd= NULL;
//				}
//			}
//			else if (sl.spacetype==SPACE_IMAGE) {
//				SpaceImage *sima= (SpaceImage *)sl;
//				if(sima.gpd) {
//					versions_gpencil_add_main(&main.gpencil, (ID *)sima.gpd, "GPencil Image");
//					sima.gpd= NULL;
//				}
//			}
//		}
//	}
//}
//
//
//
//static void do_versions(FileData *fd, Library *lib, Main *main)
//{
//	/* WATCH IT!!!: pointers from libdata have not been converted */
//
//	if(G.f & G_DEBUG)
//		printf("read file %s\n  Version %d sub %d\n", fd.filename, main.versionfile, main.subversionfile);
//
//	if(main.versionfile == 100) {
//		/* tex.extend and tex.imageflag have changed: */
//		Tex *tex = main.tex.first;
//		while(tex) {
//			if(tex.id.flag & LIB_NEEDLINK) {
//
//				if(tex.extend==0) {
//					if(tex.xrepeat || tex.yrepeat) tex.extend= TEX_REPEAT;
//					else {
//						tex.extend= TEX_EXTEND;
//						tex.xrepeat= tex.yrepeat= 1;
//					}
//				}
//
//			}
//			tex= tex.id.next;
//		}
//	}
//	if(main.versionfile <= 101) {
//		/* frame mapping */
//		Scene *sce = main.scene.first;
//		while(sce) {
//			sce.r.framapto= 100;
//			sce.r.images= 100;
//			sce.r.framelen= 1.0;
//			sce= sce.id.next;
//		}
//	}
//	if(main.versionfile <= 102) {
//		/* init halo's at 1.0 */
//		Material *ma = main.mat.first;
//		while(ma) {
//			ma.add= 1.0;
//			ma= ma.id.next;
//		}
//	}
//	if(main.versionfile <= 103) {
//		/* new variable in object: colbits */
//		Object *ob = main.object.first;
//		int a;
//		while(ob) {
//			ob.colbits= 0;
//			if(ob.totcol) {
//				for(a=0; a<ob.totcol; a++) {
//					if(ob.mat[a]) ob.colbits |= (1<<a);
//				}
//			}
//			ob= ob.id.next;
//		}
//	}
//	if(main.versionfile <= 104) {
//		/* timeoffs moved */
//		Object *ob = main.object.first;
//		while(ob) {
//			if(ob.transflag & 1) {
//				ob.transflag -= 1;
//				ob.ipoflag |= OB_OFFS_OB;
//			}
//			ob= ob.id.next;
//		}
//	}
//	if(main.versionfile <= 105) {
//		Object *ob = main.object.first;
//		while(ob) {
//			ob.dupon= 1; ob.dupoff= 0;
//			ob.dupsta= 1; ob.dupend= 100;
//			ob= ob.id.next;
//		}
//	}
//	if(main.versionfile <= 106) {
//		/* mcol changed */
//		Mesh *me = main.mesh.first;
//		while(me) {
//			if(me.mcol) vcol_to_fcol(me);
//			me= me.id.next;
//		}
//
//	}
//	if(main.versionfile <= 107) {
//		Object *ob;
//		Scene *sce = main.scene.first;
//		while(sce) {
//			sce.r.mode |= R_GAMMA;
//			sce= sce.id.next;
//		}
//		ob= main.object.first;
//		while(ob) {
//			ob.ipoflag |= OB_OFFS_PARENT;
//			if(ob.dt==0) ob.dt= OB_SOLID;
//			ob= ob.id.next;
//		}
//
//	}
//	if(main.versionfile <= 109) {
//		/* new variable: gridlines */
//		bScreen *sc = main.screen.first;
//		while(sc) {
//			ScrArea *sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl= sa.spacedata.first;
//				while (sl) {
//					if (sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D*) sl;
//
//						if (v3d.gridlines==0) v3d.gridlines= 20;
//					}
//					sl= sl.next;
//				}
//				sa= sa.next;
//			}
//			sc= sc.id.next;
//		}
//	}
//	if(main.versionfile <= 112) {
//		Mesh *me = main.mesh.first;
//		while(me) {
//			me.cubemapsize= 1.0;
//			me= me.id.next;
//		}
//	}
//	if(main.versionfile <= 113) {
//		Material *ma = main.mat.first;
//		while(ma) {
//			if(ma.flaresize==0.0) ma.flaresize= 1.0;
//			ma.subsize= 1.0;
//			ma.flareboost= 1.0;
//			ma= ma.id.next;
//		}
//	}
//
//	if(main.versionfile <= 134) {
//		Tex *tex = main.tex.first;
//		while (tex) {
//			if ((tex.rfac == 0.0) &&
//			    (tex.gfac == 0.0) &&
//			    (tex.bfac == 0.0)) {
//				tex.rfac = 1.0;
//				tex.gfac = 1.0;
//				tex.bfac = 1.0;
//				tex.filtersize = 1.0;
//			}
//			tex = tex.id.next;
//		}
//	}
//	if(main.versionfile <= 140) {
//		/* r-g-b-fac in texure */
//		Tex *tex = main.tex.first;
//		while (tex) {
//			if ((tex.rfac == 0.0) &&
//			    (tex.gfac == 0.0) &&
//			    (tex.bfac == 0.0)) {
//				tex.rfac = 1.0;
//				tex.gfac = 1.0;
//				tex.bfac = 1.0;
//				tex.filtersize = 1.0;
//			}
//			tex = tex.id.next;
//		}
//	}
//	if(main.versionfile <= 153) {
//		Scene *sce = main.scene.first;
//		while(sce) {
//			if(sce.r.blurfac==0.0) sce.r.blurfac= 1.0;
//			sce= sce.id.next;
//		}
//	}
//	if(main.versionfile <= 163) {
//		Scene *sce = main.scene.first;
//		while(sce) {
//			if(sce.r.frs_sec==0) sce.r.frs_sec= 25;
//			sce= sce.id.next;
//		}
//	}
//	if(main.versionfile <= 164) {
//		Mesh *me= main.mesh.first;
//		while(me) {
//			me.smoothresh= 30;
//			me= me.id.next;
//		}
//	}
//	if(main.versionfile <= 165) {
//		Mesh *me= main.mesh.first;
//		TFace *tface;
//		int nr;
//		char *cp;
//
//		while(me) {
//			if(me.tface) {
//				nr= me.totface;
//				tface= me.tface;
//				while(nr--) {
//					cp= (char *)&tface.col[0];
//					if(cp[1]>126) cp[1]= 255; else cp[1]*=2;
//					if(cp[2]>126) cp[2]= 255; else cp[2]*=2;
//					if(cp[3]>126) cp[3]= 255; else cp[3]*=2;
//					cp= (char *)&tface.col[1];
//					if(cp[1]>126) cp[1]= 255; else cp[1]*=2;
//					if(cp[2]>126) cp[2]= 255; else cp[2]*=2;
//					if(cp[3]>126) cp[3]= 255; else cp[3]*=2;
//					cp= (char *)&tface.col[2];
//					if(cp[1]>126) cp[1]= 255; else cp[1]*=2;
//					if(cp[2]>126) cp[2]= 255; else cp[2]*=2;
//					if(cp[3]>126) cp[3]= 255; else cp[3]*=2;
//					cp= (char *)&tface.col[3];
//					if(cp[1]>126) cp[1]= 255; else cp[1]*=2;
//					if(cp[2]>126) cp[2]= 255; else cp[2]*=2;
//					if(cp[3]>126) cp[3]= 255; else cp[3]*=2;
//
//					tface++;
//				}
//			}
//			me= me.id.next;
//		}
//	}
//
//	if(main.versionfile <= 169) {
//		Mesh *me= main.mesh.first;
//		while(me) {
//			if(me.subdiv==0) me.subdiv= 1;
//			me= me.id.next;
//		}
//	}
//
//	if(main.versionfile <= 169) {
//		bScreen *sc= main.screen.first;
//		while(sc) {
//			ScrArea *sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl= sa.spacedata.first;
//				while(sl) {
//					if(sl.spacetype==SPACE_IPO) {
//						SpaceIpo *sipo= (SpaceIpo*) sl;
//						sipo.v2d.max[0]= 15000.0;
//					}
//					sl= sl.next;
//				}
//				sa= sa.next;
//			}
//			sc= sc.id.next;
//		}
//	}
//
//	if(main.versionfile <= 170) {
//		Object *ob = main.object.first;
//		PartEff *paf;
//		while (ob) {
//			paf = give_parteff(ob);
//			if (paf) {
//				if (paf.staticstep == 0) {
//					paf.staticstep= 5;
//				}
//			}
//			ob = ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 171) {
//		bScreen *sc= main.screen.first;
//		while(sc) {
//			ScrArea *sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl= sa.spacedata.first;
//				while(sl) {
//					if(sl.spacetype==SPACE_TEXT) {
//						SpaceText *st= (SpaceText*) sl;
//						st.lheight= 12;
//					}
//					sl= sl.next;
//				}
//				sa= sa.next;
//			}
//			sc= sc.id.next;
//		}
//	}
//
//	if(main.versionfile <= 173) {
//		int a, b;
//		Mesh *me= main.mesh.first;
//		while(me) {
//			if(me.tface) {
//				TFace *tface= me.tface;
//				for(a=0; a<me.totface; a++, tface++) {
//					for(b=0; b<4; b++) {
//						tface.uv[b][0]/= 32767.0;
//						tface.uv[b][1]/= 32767.0;
//					}
//				}
//			}
//			me= me.id.next;
//		}
//	}
//
//	if(main.versionfile <= 191) {
//		Object *ob= main.object.first;
//		Material *ma = main.mat.first;
//
//		/* let faces have default add factor of 0.0 */
//		while(ma) {
//		  if (!(ma.mode & MA_HALO)) ma.add = 0.0;
//		  ma = ma.id.next;
//		}
//
//		while(ob) {
//			ob.mass= 1.0f;
//			ob.damping= 0.1f;
//			/*ob.quat[1]= 1.0f;*/ /* quats arnt used yet */
//			ob= ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 193) {
//		Object *ob= main.object.first;
//		while(ob) {
//			ob.inertia= 1.0f;
//			ob.rdamping= 0.1f;
//			ob= ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 196) {
//		Mesh *me= main.mesh.first;
//		int a, b;
//		while(me) {
//			if(me.tface) {
//				TFace *tface= me.tface;
//				for(a=0; a<me.totface; a++, tface++) {
//					for(b=0; b<4; b++) {
//						tface.mode |= TF_DYNAMIC;
//						tface.mode &= ~TF_INVISIBLE;
//					}
//				}
//			}
//			me= me.id.next;
//		}
//	}
//
//	if(main.versionfile <= 200) {
//		Object *ob= main.object.first;
//		while(ob) {
//			ob.scaflag = ob.gameflag & (64+128+256+512+1024+2048);
//			    /* 64 is do_fh */
//			ob.gameflag &= ~(128+256+512+1024+2048);
//			ob = ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 201) {
//		/* add-object + end-object are joined to edit-object actuator */
//		Object *ob = main.object.first;
//		bProperty *prop;
//		bActuator *act;
//		bIpoActuator *ia;
//		bEditObjectActuator *eoa;
//		bAddObjectActuator *aoa;
//		while (ob) {
//			act = ob.actuators.first;
//			while (act) {
//				if(act.type==ACT_IPO) {
//					ia= act.data;
//					prop= get_ob_property(ob, ia.name);
//					if(prop) {
//						ia.type= ACT_IPO_FROM_PROP;
//					}
//				}
//				else if(act.type==ACT_ADD_OBJECT) {
//					aoa= act.data;
//					eoa= MEM_callocN(sizeof(bEditObjectActuator), "edit ob act");
//					eoa.type= ACT_EDOB_ADD_OBJECT;
//					eoa.ob= aoa.ob;
//					eoa.time= aoa.time;
//					MEM_freeN(aoa);
//					act.data= eoa;
//					act.type= act.otype= ACT_EDIT_OBJECT;
//				}
//				else if(act.type==ACT_END_OBJECT) {
//					eoa= MEM_callocN(sizeof(bEditObjectActuator), "edit ob act");
//					eoa.type= ACT_EDOB_END_OBJECT;
//					act.data= eoa;
//					act.type= act.otype= ACT_EDIT_OBJECT;
//				}
//				act= act.next;
//			}
//			ob = ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 202) {
//		/* add-object and end-object are joined to edit-object
//		 * actuator */
//		Object *ob= main.object.first;
//		bActuator *act;
//		bObjectActuator *oa;
//		while(ob) {
//			act= ob.actuators.first;
//			while(act) {
//				if(act.type==ACT_OBJECT) {
//					oa= act.data;
//					oa.flag &= ~(ACT_TORQUE_LOCAL|ACT_DROT_LOCAL);		/* this actuator didn't do local/glob rot before */
//				}
//				act= act.next;
//			}
//			ob= ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 204) {
//		/* patches for new physics */
//		Object *ob= main.object.first;
//		bActuator *act;
//		bObjectActuator *oa;
//		bSound *sound;
//		while(ob) {
//
//			/* please check this for demo20 files like
//			 * original Egypt levels etc.  converted
//			 * rotation factor of 50 is not workable */
//			act= ob.actuators.first;
//			while(act) {
//				if(act.type==ACT_OBJECT) {
//					oa= act.data;
//
//					oa.forceloc[0]*= 25.0;
//					oa.forceloc[1]*= 25.0;
//					oa.forceloc[2]*= 25.0;
//
//					oa.forcerot[0]*= 10.0;
//					oa.forcerot[1]*= 10.0;
//					oa.forcerot[2]*= 10.0;
//				}
//				act= act.next;
//			}
//			ob= ob.id.next;
//		}
//
//		sound = main.sound.first;
//		while (sound) {
//			if (sound.volume < 0.01) {
//				sound.volume = 1.0;
//			}
//			sound = sound.id.next;
//		}
//	}
//
//	if(main.versionfile <= 205) {
//		/* patches for new physics */
//		Object *ob= main.object.first;
//		bActuator *act;
//		bSensor *sens;
//		bEditObjectActuator *oa;
//		bRaySensor *rs;
//		bCollisionSensor *cs;
//		while(ob) {
//		    /* Set anisotropic friction off for old objects,
//		     * values to 1.0.  */
//			ob.gameflag &= ~OB_ANISOTROPIC_FRICTION;
//			ob.anisotropicFriction[0] = 1.0;
//			ob.anisotropicFriction[1] = 1.0;
//			ob.anisotropicFriction[2] = 1.0;
//
//			act= ob.actuators.first;
//			while(act) {
//				if(act.type==ACT_EDIT_OBJECT) {
//					/* Zero initial velocity for newly
//					 * added objects */
//					oa= act.data;
//					oa.linVelocity[0] = 0.0;
//					oa.linVelocity[1] = 0.0;
//					oa.linVelocity[2] = 0.0;
//					oa.localflag = 0;
//				}
//				act= act.next;
//			}
//
//			sens= ob.sensors.first;
//			while (sens) {
//				/* Extra fields for radar sensors. */
//				if(sens.type == SENS_RADAR) {
//					bRadarSensor *s = sens.data;
//					s.range = 10000.0;
//				}
//
//				/* Pulsing: defaults for new sensors. */
//				if(sens.type != SENS_ALWAYS) {
//					sens.pulse = 0;
//					sens.freq = 0;
//				} else {
//					sens.pulse = 1;
//				}
//
//				/* Invert: off. */
//				sens.invert = 0;
//
//				/* Collision and ray: default = trigger
//				 * on property. The material field can
//				 * remain empty. */
//				if(sens.type == SENS_COLLISION) {
//					cs = (bCollisionSensor*) sens.data;
//					cs.mode = 0;
//				}
//				if(sens.type == SENS_RAY) {
//					rs = (bRaySensor*) sens.data;
//					rs.mode = 0;
//				}
//				sens = sens.next;
//			}
//			ob= ob.id.next;
//		}
//		/* have to check the exact multiplier */
//	}
//
//	if(main.versionfile <= 211) {
//		/* Render setting: per scene, the applicable gamma value
//		 * can be set. Default is 1.0, which means no
//		 * correction.  */
//		bActuator *act;
//		bObjectActuator *oa;
//		Object *ob;
//
//		/* added alpha in obcolor */
//		ob= main.object.first;
//		while(ob) {
//			ob.col[3]= 1.0;
//			ob= ob.id.next;
//		}
//
//		/* added alpha in obcolor */
//		ob= main.object.first;
//		while(ob) {
//			act= ob.actuators.first;
//			while(act) {
//				if (act.type==ACT_OBJECT) {
//					/* multiply velocity with 50 in old files */
//					oa= act.data;
//					if (fabs(oa.linearvelocity[0]) >= 0.01f)
//						oa.linearvelocity[0] *= 50.0;
//					if (fabs(oa.linearvelocity[1]) >= 0.01f)
//						oa.linearvelocity[1] *= 50.0;
//					if (fabs(oa.linearvelocity[2]) >= 0.01f)
//						oa.linearvelocity[2] *= 50.0;
//					if (fabs(oa.angularvelocity[0])>=0.01f)
//						oa.angularvelocity[0] *= 50.0;
//					if (fabs(oa.angularvelocity[1])>=0.01f)
//						oa.angularvelocity[1] *= 50.0;
//					if (fabs(oa.angularvelocity[2])>=0.01f)
//						oa.angularvelocity[2] *= 50.0;
//				}
//				act= act.next;
//			}
//			ob= ob.id.next;
//		}
//	}
//
//	if(main.versionfile <= 212) {
//
//		bSound* sound;
//		bProperty *prop;
//		Object *ob;
//		Mesh *me;
//
//		sound = main.sound.first;
//		while (sound)
//		{
//			sound.max_gain = 1.0;
//			sound.min_gain = 0.0;
//			sound.distance = 1.0;
//
//			if (sound.attenuation > 0.0)
//				sound.flags |= SOUND_FLAGS_3D;
//			else
//				sound.flags &= ~SOUND_FLAGS_3D;
//
//			sound = sound.id.next;
//		}
//
//		ob = main.object.first;
//
//		while (ob) {
//			prop= ob.prop.first;
//			while(prop) {
//				if (prop.type == GPROP_TIME) {
//					// convert old GPROP_TIME values from int to float
//					*((float *)&prop.data) = (float) prop.data;
//				}
//
//				prop= prop.next;
//			}
//			ob = ob.id.next;
//		}
//
//			/* me.subdiv changed to reflect the actual reparametization
//			 * better, and smeshes were removed - if it was a smesh make
//			 * it a subsurf, and reset the subdiv level because subsurf
//			 * takes a lot more work to calculate.
//			 */
//		for (me= main.mesh.first; me; me= me.id.next) {
//			if (me.flag&ME_SMESH) {
//				me.flag&= ~ME_SMESH;
//				me.flag|= ME_SUBSURF;
//
//				me.subdiv= 1;
//			} else {
//				if (me.subdiv<2)
//					me.subdiv= 1;
//				else
//					me.subdiv--;
//			}
//		}
//	}
//
//	if(main.versionfile <= 220) {
//		Object *ob;
//		Mesh *me;
//
//		ob = main.object.first;
//
//		/* adapt form factor in order to get the 'old' physics
//		 * behaviour back...*/
//
//		while (ob) {
//			/* in future, distinguish between different
//			 * object bounding shapes */
//			ob.formfactor = 0.4f;
//			/* patch form factor , note that inertia equiv radius
//			 * of a rotation symmetrical obj */
//			if (ob.inertia != 1.0) {
//				ob.formfactor /= ob.inertia * ob.inertia;
//			}
//			ob = ob.id.next;
//		}
//
//			/* Began using alpha component of vertex colors, but
//			 * old file vertex colors are undefined, reset them
//			 * to be fully opaque. -zr
//			 */
//		for (me= main.mesh.first; me; me= me.id.next) {
//			if (me.mcol) {
//				int i;
//
//				for (i=0; i<me.totface*4; i++) {
//					MCol *mcol= &me.mcol[i];
//					mcol.a= 255;
//				}
//			}
//			if (me.tface) {
//				int i, j;
//
//				for (i=0; i<me.totface; i++) {
//					TFace *tf= &((TFace*) me.tface)[i];
//
//					for (j=0; j<4; j++) {
//						char *col= (char*) &tf.col[j];
//
//						col[0]= 255;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 221) {
//		Scene *sce= main.scene.first;
//
//		// new variables for std-alone player and runtime
//		while(sce) {
//
//			sce.r.xplay= 640;
//			sce.r.yplay= 480;
//			sce.r.freqplay= 60;
//
//			sce= sce.id.next;
//		}
//
//	}
//	if(main.versionfile <= 222) {
//		Scene *sce= main.scene.first;
//
//		// new variables for std-alone player and runtime
//		while(sce) {
//
//			sce.r.depth= 32;
//
//			sce= sce.id.next;
//		}
//	}
//
//
//	if(main.versionfile <= 223) {
//		VFont *vf;
//		Image *ima;
//		Object *ob;
//
//		for (vf= main.vfont.first; vf; vf= vf.id.next) {
//			if (BLI_streq(vf.name+strlen(vf.name)-6, ".Bfont")) {
//				strcpy(vf.name, "<builtin>");
//			}
//		}
//
//		/* Old textures animate at 25 FPS */
//		for (ima = main.image.first; ima; ima=ima.id.next){
//			ima.animspeed = 25;
//		}
//
//			/* Zr remapped some keyboard codes to be linear (stupid zr) */
//		for (ob= main.object.first; ob; ob= ob.id.next) {
//			bSensor *sens;
//
//			for (sens= ob.sensors.first; sens; sens= sens.next) {
//				if (sens.type==SENS_KEYBOARD) {
//					bKeyboardSensor *ks= sens.data;
//
//					ks.key= map_223_keybd_code_to_224_keybd_code(ks.key);
//					ks.qual= map_223_keybd_code_to_224_keybd_code(ks.qual);
//					ks.qual2= map_223_keybd_code_to_224_keybd_code(ks.qual2);
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 224) {
//		bSound* sound;
//		Scene *sce;
//		Mesh *me;
//		bScreen *sc;
//
//		for (sound=main.sound.first; sound; sound=sound.id.next) {
//			if (sound.packedfile) {
//				if (sound.newpackedfile == NULL) {
//					sound.newpackedfile = sound.packedfile;
//				}
//				sound.packedfile = NULL;
//			}
//		}
//		/* Make sure that old subsurf meshes don't have zero subdivision level for rendering */
//		for (me=main.mesh.first; me; me=me.id.next){
//			if ((me.flag & ME_SUBSURF) && (me.subdivr==0))
//				me.subdivr=me.subdiv;
//		}
//
//		for (sce= main.scene.first; sce; sce= sce.id.next) {
//			sce.r.stereomode = 1;  // no stereo
//		}
//
//			/* some oldfile patch, moved from set_func_space */
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if (sl.spacetype==SPACE_IPO) {
//						SpaceSeq *sseq= (SpaceSeq*) sl;
//						sseq.v2d.keeptot= 0;
//					}
//				}
//			}
//		}
//
//	}
//
//
//	if(main.versionfile <= 225) {
//		World *wo;
//		/* Use Sumo for old games */
//		for (wo = main.world.first; wo; wo= wo.id.next) {
//			wo.physicsEngine = 2;
//		}
//	}
//
//	if(main.versionfile <= 227) {
//		Scene *sce;
//		Material *ma;
//		bScreen *sc;
//		Object *ob;
//
//		/*  As of now, this insures that the transition from the old Track system
//		    to the new full constraint Track is painless for everyone. - theeth
//		*/
//		ob = main.object.first;
//
//		while (ob) {
//			ListBase *list;
//			list = &ob.constraints;
//
//			/* check for already existing TrackTo constraint
//			   set their track and up flag correctly */
//
//			if (list){
//				bConstraint *curcon;
//				for (curcon = list.first; curcon; curcon=curcon.next){
//					if (curcon.type == CONSTRAINT_TYPE_TRACKTO){
//						bTrackToConstraint *data = curcon.data;
//						data.reserved1 = ob.trackflag;
//						data.reserved2 = ob.upflag;
//					}
//				}
//			}
//
//			if (ob.type == OB_ARMATURE) {
//				if (ob.pose){
//					bConstraint *curcon;
//					bPoseChannel *pchan;
//					for (pchan = ob.pose.chanbase.first;
//						 pchan; pchan=pchan.next){
//						for (curcon = pchan.constraints.first;
//							 curcon; curcon=curcon.next){
//							if (curcon.type == CONSTRAINT_TYPE_TRACKTO){
//								bTrackToConstraint *data = curcon.data;
//								data.reserved1 = ob.trackflag;
//								data.reserved2 = ob.upflag;
//							}
//						}
//					}
//                }
//			}
//
//			/* Change Ob.Track in real TrackTo constraint */
//
//			if (ob.track){
//				bConstraint *con;
//				bConstraintTypeInfo *cti;
//				bTrackToConstraint *data;
//				void *cdata;
//
//				list = &ob.constraints;
//				if (list)
//				{
//					con = MEM_callocN(sizeof(bConstraint), "constraint");
//					strcpy (con.name, "AutoTrack");
//					unique_constraint_name(con, list);
//					con.flag |= CONSTRAINT_EXPAND;
//					con.enforce=1.0F;
//					con.type = CONSTRAINT_TYPE_TRACKTO;
//
//					cti= get_constraint_typeinfo(CONSTRAINT_TYPE_TRACKTO);
//					cdata= MEM_callocN(cti.size, cti.structName);
//					cti.new_data(cdata);
//					data = (bTrackToConstraint *)cdata;
//
//					data.tar = ob.track;
//					data.reserved1 = ob.trackflag;
//					data.reserved2 = ob.upflag;
//					con.data= (void*) data;
//					BLI_addtail(list, con);
//				}
//				ob.track = 0;
//			}
//
//			ob = ob.id.next;
//		}
//
//
//		for (sce= main.scene.first; sce; sce= sce.id.next) {
//			sce.audio.mixrate = 44100;
//			sce.audio.flag |= AUDIO_SCRUB;
//			sce.r.mode |= R_ENVMAP;
//		}
//		// init new shader vars
//		for (ma= main.mat.first; ma; ma= ma.id.next) {
//			ma.refrac= 4.0f;
//			ma.roughness= 0.5f;
//			ma.param[0]= 0.5f;
//			ma.param[1]= 0.1f;
//			ma.param[2]= 0.1f;
//			ma.param[3]= 0.05f;
//		}
//		// patch for old wrong max view2d settings, allows zooming out more
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if (sl.spacetype==SPACE_ACTION) {
//						SpaceAction *sac= (SpaceAction *) sl;
//						sac.v2d.max[0]= 32000;
//					}
//					else if (sl.spacetype==SPACE_NLA) {
//						SpaceNla *sla= (SpaceNla *) sl;
//						sla.v2d.max[0]= 32000;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 228) {
//		Scene *sce;
//		bScreen *sc;
//		Object *ob;
//
//
//		/*  As of now, this insures that the transition from the old Track system
//		    to the new full constraint Track is painless for everyone.*/
//		ob = main.object.first;
//
//		while (ob) {
//			ListBase *list;
//			list = &ob.constraints;
//
//			/* check for already existing TrackTo constraint
//			   set their track and up flag correctly */
//
//			if (list){
//				bConstraint *curcon;
//				for (curcon = list.first; curcon; curcon=curcon.next){
//					if (curcon.type == CONSTRAINT_TYPE_TRACKTO){
//						bTrackToConstraint *data = curcon.data;
//						data.reserved1 = ob.trackflag;
//						data.reserved2 = ob.upflag;
//					}
//				}
//			}
//
//			if (ob.type == OB_ARMATURE) {
//				if (ob.pose){
//					bConstraint *curcon;
//					bPoseChannel *pchan;
//					for (pchan = ob.pose.chanbase.first;
//						 pchan; pchan=pchan.next){
//						for (curcon = pchan.constraints.first;
//							 curcon; curcon=curcon.next){
//							if (curcon.type == CONSTRAINT_TYPE_TRACKTO){
//								bTrackToConstraint *data = curcon.data;
//								data.reserved1 = ob.trackflag;
//								data.reserved2 = ob.upflag;
//							}
//						}
//					}
//                }
//			}
//
//			ob = ob.id.next;
//		}
//
//		for (sce= main.scene.first; sce; sce= sce.id.next) {
//			sce.r.mode |= R_ENVMAP;
//		}
//
//		// convert old mainb values for new button panels
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if (sl.spacetype==SPACE_BUTS) {
//						SpaceButs *sbuts= (SpaceButs *) sl;
//
//						sbuts.v2d.maxzoom= 1.2f;
//						sbuts.align= 1;	/* horizontal default */
//
//						if(sbuts.mainb==BUTS_LAMP) {
//							sbuts.mainb= CONTEXT_SHADING;
//							//sbuts.tab[CONTEXT_SHADING]= TAB_SHADING_LAMP;
//						}
//						else if(sbuts.mainb==BUTS_MAT) {
//							sbuts.mainb= CONTEXT_SHADING;
//							//sbuts.tab[CONTEXT_SHADING]= TAB_SHADING_MAT;
//						}
//						else if(sbuts.mainb==BUTS_TEX) {
//							sbuts.mainb= CONTEXT_SHADING;
//							//sbuts.tab[CONTEXT_SHADING]= TAB_SHADING_TEX;
//						}
//						else if(sbuts.mainb==BUTS_ANIM) {
//							sbuts.mainb= CONTEXT_OBJECT;
//						}
//						else if(sbuts.mainb==BUTS_WORLD) {
//							sbuts.mainb= CONTEXT_SCENE;
//							//sbuts.tab[CONTEXT_SCENE]= TAB_SCENE_WORLD;
//						}
//						else if(sbuts.mainb==BUTS_RENDER) {
//							sbuts.mainb= CONTEXT_SCENE;
//							//sbuts.tab[CONTEXT_SCENE]= TAB_SCENE_RENDER;
//						}
//						else if(sbuts.mainb==BUTS_GAME) {
//							sbuts.mainb= CONTEXT_LOGIC;
//						}
//						else if(sbuts.mainb==BUTS_FPAINT) {
//							sbuts.mainb= CONTEXT_EDITING;
//						}
//						else if(sbuts.mainb==BUTS_RADIO) {
//							sbuts.mainb= CONTEXT_SHADING;
//							//sbuts.tab[CONTEXT_SHADING]= TAB_SHADING_RAD;
//						}
//						else if(sbuts.mainb==BUTS_CONSTRAINT) {
//							sbuts.mainb= CONTEXT_OBJECT;
//						}
//						else if(sbuts.mainb==BUTS_SCRIPT) {
//							sbuts.mainb= CONTEXT_OBJECT;
//						}
//						else if(sbuts.mainb==BUTS_EDIT) {
//							sbuts.mainb= CONTEXT_EDITING;
//						}
//						else sbuts.mainb= CONTEXT_SCENE;
//					}
//				}
//			}
//		}
//	}
//	/* ton: made this 230 instead of 229,
//	   to be sure (tuho files) and this is a reliable check anyway
//	   nevertheless, we might need to think over a fitness (initialize)
//	   check apart from the do_versions() */
//
//	if(main.versionfile <= 230) {
//		bScreen *sc;
//
//		// new variable blockscale, for panels in any area
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.blockscale==0.0) sl.blockscale= 0.7f;
//					/* added: 5x better zoom in for action */
//					if(sl.spacetype==SPACE_ACTION) {
//						SpaceAction *sac= (SpaceAction *)sl;
//						sac.v2d.maxzoom= 50;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 231) {
//		/* new bit flags for showing/hiding grid floor and axes */
//		bScreen *sc = main.screen.first;
//		while(sc) {
//			ScrArea *sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl= sa.spacedata.first;
//				while (sl) {
//					if (sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D*) sl;
//
//						if (v3d.gridflag==0) {
//							v3d.gridflag |= V3D_SHOW_X;
//							v3d.gridflag |= V3D_SHOW_Y;
//							v3d.gridflag |= V3D_SHOW_FLOOR;
//							v3d.gridflag &= ~V3D_SHOW_Z;
//						}
//					}
//					sl= sl.next;
//				}
//				sa= sa.next;
//			}
//			sc= sc.id.next;
//		}
//	}
//	if(main.versionfile <= 231) {
//		Material *ma= main.mat.first;
//		bScreen *sc = main.screen.first;
//		Scene *sce;
//		Lamp *la;
//		World *wrld;
//
//		/* introduction of raytrace */
//		while(ma) {
//			if(ma.fresnel_tra_i==0.0) ma.fresnel_tra_i= 1.25;
//			if(ma.fresnel_mir_i==0.0) ma.fresnel_mir_i= 1.25;
//
//			ma.ang= 1.0;
//			ma.ray_depth= 2;
//			ma.ray_depth_tra= 2;
//			ma.fresnel_tra= 0.0;
//			ma.fresnel_mir= 0.0;
//
//			ma= ma.id.next;
//		}
//		sce= main.scene.first;
//		while(sce) {
//			if(sce.r.gauss==0.0) sce.r.gauss= 1.0;
//			sce= sce.id.next;
//		}
//		la= main.lamp.first;
//		while(la) {
//			if(la.k==0.0) la.k= 1.0;
//			if(la.ray_samp==0) la.ray_samp= 1;
//			if(la.ray_sampy==0) la.ray_sampy= 1;
//			if(la.ray_sampz==0) la.ray_sampz= 1;
//			if(la.area_size==0.0) la.area_size= 1.0;
//			if(la.area_sizey==0.0) la.area_sizey= 1.0;
//			if(la.area_sizez==0.0) la.area_sizez= 1.0;
//			la= la.id.next;
//		}
//		wrld= main.world.first;
//		while(wrld) {
//			if(wrld.range==0.0) {
//				wrld.range= 1.0f/wrld.exposure;
//			}
//			wrld= wrld.id.next;
//		}
//
//		/* new bit flags for showing/hiding grid floor and axes */
//
//		while(sc) {
//			ScrArea *sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl= sa.spacedata.first;
//				while (sl) {
//					if (sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D*) sl;
//
//						if (v3d.gridflag==0) {
//							v3d.gridflag |= V3D_SHOW_X;
//							v3d.gridflag |= V3D_SHOW_Y;
//							v3d.gridflag |= V3D_SHOW_FLOOR;
//							v3d.gridflag &= ~V3D_SHOW_Z;
//						}
//					}
//					sl= sl.next;
//				}
//				sa= sa.next;
//			}
//			sc= sc.id.next;
//		}
//	}
//	if(main.versionfile <= 232) {
//		Tex *tex= main.tex.first;
//		World *wrld= main.world.first;
//		bScreen *sc;
//		Scene *sce;
//
//		while(tex) {
//			if((tex.flag & (TEX_CHECKER_ODD+TEX_CHECKER_EVEN))==0) {
//				tex.flag |= TEX_CHECKER_ODD;
//			}
//			/* copied from kernel texture.c */
//			if(tex.ns_outscale==0.0) {
//				/* musgrave */
//				tex.mg_H = 1.0f;
//				tex.mg_lacunarity = 2.0f;
//				tex.mg_octaves = 2.0f;
//				tex.mg_offset = 1.0f;
//				tex.mg_gain = 1.0f;
//				tex.ns_outscale = 1.0f;
//				/* distnoise */
//				tex.dist_amount = 1.0f;
//				/* voronoi */
//				tex.vn_w1 = 1.0f;
//				tex.vn_mexp = 2.5f;
//			}
//			tex= tex.id.next;
//		}
//
//		while(wrld) {
//			if(wrld.aodist==0.0) {
//				wrld.aodist= 10.0f;
//				wrld.aobias= 0.05f;
//			}
//			if(wrld.aosamp==0.0) wrld.aosamp= 5;
//			if(wrld.aoenergy==0.0) wrld.aoenergy= 1.0;
//			wrld= wrld.id.next;
//		}
//
//
//		// new variable blockscale, for panels in any area, do again because new
//		// areas didnt initialize it to 0.7 yet
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.blockscale==0.0) sl.blockscale= 0.7f;
//
//					/* added: 5x better zoom in for nla */
//					if(sl.spacetype==SPACE_NLA) {
//						SpaceNla *snla= (SpaceNla *)sl;
//						snla.v2d.maxzoom= 50;
//					}
//				}
//			}
//		}
//		sce= main.scene.first;
//		while(sce) {
//			if(sce.r.ocres==0) sce.r.ocres= 64;
//			sce= sce.id.next;
//		}
//
//	}
//	if(main.versionfile <= 233) {
//		bScreen *sc;
//		Material *ma= main.mat.first;
//		Object *ob= main.object.first;
//
//		while(ma) {
//			if(ma.rampfac_col==0.0) ma.rampfac_col= 1.0;
//			if(ma.rampfac_spec==0.0) ma.rampfac_spec= 1.0;
//			if(ma.pr_lamp==0) ma.pr_lamp= 3;
//			ma= ma.id.next;
//		}
//
//		/* this should have been done loooong before! */
//		while(ob) {
//			if(ob.ipowin==0) ob.ipowin= ID_OB;
//			ob= ob.id.next;
//		}
//
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D *)sl;
//						v3d.flag |= V3D_SELECT_OUTLINE;
//					}
//				}
//			}
//		}
//	}
//
//
//
//
//	if(main.versionfile <= 234) {
//		World *wo;
//		bScreen *sc;
//
//		// force sumo engine to be active
//		for (wo = main.world.first; wo; wo= wo.id.next) {
//			if(wo.physicsEngine==0) wo.physicsEngine = 2;
//		}
//
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D *)sl;
//						v3d.flag |= V3D_ZBUF_SELECT;
//					}
//					else if(sl.spacetype==SPACE_TEXT) {
//						SpaceText *st= (SpaceText *)sl;
//						if(st.tabnumber==0) st.tabnumber= 2;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 235) {
//		Tex *tex= main.tex.first;
//		Scene *sce= main.scene.first;
//		Sequence *seq;
//		Editing *ed;
//
//		while(tex) {
//			if(tex.nabla==0.0) tex.nabla= 0.025f;
//			tex= tex.id.next;
//		}
//		while(sce) {
//			ed= sce.ed;
//			if(ed) {
//				SEQ_BEGIN(sce.ed, seq) {
//					if(seq.type==SEQ_IMAGE || seq.type==SEQ_MOVIE)
//						seq.flag |= SEQ_MAKE_PREMUL;
//				}
//				SEQ_END
//			}
//
//			sce= sce.id.next;
//		}
//	}
//	if(main.versionfile <= 236) {
//		Object *ob;
//		Camera *cam= main.camera.first;
//		Material *ma;
//		bScreen *sc;
//
//		while(cam) {
//			if(cam.ortho_scale==0.0) {
//				cam.ortho_scale= 256.0f/cam.lens;
//				if(cam.type==CAM_ORTHO) printf("NOTE: ortho render has changed, tweak new Camera 'scale' value.\n");
//			}
//			cam= cam.id.next;
//		}
//		/* set manipulator type */
//		/* force oops draw if depgraph was set*/
//		/* set time line var */
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D *)sl;
//						if(v3d.twtype==0) v3d.twtype= V3D_MANIP_TRANSLATE;
//					}
//					else if(sl.spacetype==SPACE_TIME) {
//						SpaceTime *stime= (SpaceTime *)sl;
//						if(stime.redraws==0)
//							stime.redraws= TIME_ALL_3D_WIN|TIME_ALL_ANIM_WIN;
//					}
//				}
//			}
//		}
//		// init new shader vars
//		for (ma= main.mat.first; ma; ma= ma.id.next) {
//			if(ma.darkness==0.0) {
//				ma.rms=0.1f;
//				ma.darkness=1.0f;
//			}
//		}
//
//		/* softbody init new vars */
//		for(ob= main.object.first; ob; ob= ob.id.next) {
//			if(ob.soft) {
//				if(ob.soft.defgoal==0.0) ob.soft.defgoal= 0.7f;
//				if(ob.soft.physics_speed==0.0) ob.soft.physics_speed= 1.0f;
//
//				if(ob.soft.interval==0) {
//					ob.soft.interval= 2;
//					ob.soft.sfra= 1;
//					ob.soft.efra= 100;
//				}
//			}
//			if(ob.soft && ob.soft.vertgroup==0) {
//				bDeformGroup *locGroup = get_named_vertexgroup(ob, "SOFTGOAL");
//				if(locGroup){
//					/* retrieve index for that group */
//					ob.soft.vertgroup =  1 + get_defgroup_num(ob, locGroup);
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 237) {
//		bArmature *arm;
//		bConstraint *con;
//		Object *ob;
//
//		// armature recode checks
//		for(arm= main.armature.first; arm; arm= arm.id.next) {
//			where_is_armature(arm);
//		}
//		for(ob= main.object.first; ob; ob= ob.id.next) {
//			if(ob.parent) {
//				Object *parent= newlibadr(fd, lib, ob.parent);
//				if (parent && parent.type==OB_LATTICE)
//					ob.partype = PARSKEL;
//			}
//
//			// btw. armature_rebuild_pose is further only called on leave editmode
//			if(ob.type==OB_ARMATURE) {
//				if(ob.pose)
//					ob.pose.flag |= POSE_RECALC;
//				ob.recalc |= OB_RECALC;	// cannot call stuff now (pointers!), done in setup_app_data
//
//				/* new generic xray option */
//				arm= newlibadr(fd, lib, ob.data);
//				if(arm.flag & ARM_DRAWXRAY) {
//					ob.dtx |= OB_DRAWXRAY;
//				}
//			} else if (ob.type==OB_MESH) {
//				Mesh *me = newlibadr(fd, lib, ob.data);
//
//				if ((me.flag&ME_SUBSURF)) {
//					SubsurfModifierData *smd = (SubsurfModifierData*) modifier_new(eModifierType_Subsurf);
//
//					smd.levels = MAX2(1, me.subdiv);
//					smd.renderLevels = MAX2(1, me.subdivr);
//					smd.subdivType = me.subsurftype;
//
//					smd.modifier.mode = 0;
//					if (me.subdiv!=0)
//						smd.modifier.mode |= 1;
//					if (me.subdivr!=0)
//						smd.modifier.mode |= 2;
//					if (me.flag&ME_OPT_EDGES)
//						smd.flags |= eSubsurfModifierFlag_ControlEdges;
//
//					BLI_addtail(&ob.modifiers, smd);
//				}
//			}
//
//			// follow path constraint needs to set the 'path' option in curves...
//			for(con=ob.constraints.first; con; con= con.next) {
//				if(con.type==CONSTRAINT_TYPE_FOLLOWPATH) {
//					bFollowPathConstraint *data = con.data;
//					Object *obc= newlibadr(fd, lib, data.tar);
//
//					if(obc && obc.type==OB_CURVE) {
//						Curve *cu= newlibadr(fd, lib, obc.data);
//						if(cu) cu.flag |= CU_PATH;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 238) {
//		Lattice *lt;
//		Object *ob;
//		bArmature *arm;
//		Mesh *me;
//		Key *key;
//		Scene *sce= main.scene.first;
//
//		while(sce){
//			if(sce.toolsettings == NULL){
//				sce.toolsettings = MEM_callocN(sizeof(struct ToolSettings),"Tool Settings Struct");
//				sce.toolsettings.cornertype=0;
//				sce.toolsettings.degr = 90;
//				sce.toolsettings.step = 9;
//				sce.toolsettings.turn = 1;
//				sce.toolsettings.extr_offs = 1;
//				sce.toolsettings.doublimit = 0.001f;
//				sce.toolsettings.segments = 32;
//				sce.toolsettings.rings = 32;
//				sce.toolsettings.vertices = 32;
//				sce.toolsettings.editbutflag =1;
//			}
//			sce= sce.id.next;
//		}
//
//		for (lt=main.latt.first; lt; lt=lt.id.next) {
//			if (lt.fu==0.0 && lt.fv==0.0 && lt.fw==0.0) {
//				calc_lat_fudu(lt.flag, lt.pntsu, &lt.fu, &lt.du);
//				calc_lat_fudu(lt.flag, lt.pntsv, &lt.fv, &lt.dv);
//				calc_lat_fudu(lt.flag, lt.pntsw, &lt.fw, &lt.dw);
//			}
//		}
//
//		for(ob=main.object.first; ob; ob= ob.id.next) {
//			ModifierData *md;
//			PartEff *paf;
//
//			for (md=ob.modifiers.first; md; md=md.next) {
//				if (md.type==eModifierType_Subsurf) {
//					SubsurfModifierData *smd = (SubsurfModifierData*) md;
//
//					smd.flags &= ~(eSubsurfModifierFlag_Incremental|eSubsurfModifierFlag_DebugIncr);
//				}
//			}
//
//			if ((ob.softflag&OB_SB_ENABLE) && !modifiers_findByType(ob, eModifierType_Softbody)) {
//				if (ob.softflag&OB_SB_POSTDEF) {
//					md = ob.modifiers.first;
//
//					while (md && modifierType_getInfo(md.type).type==eModifierTypeType_OnlyDeform) {
//						md = md.next;
//					}
//
//					BLI_insertlinkbefore(&ob.modifiers, md, modifier_new(eModifierType_Softbody));
//				} else {
//					BLI_addhead(&ob.modifiers, modifier_new(eModifierType_Softbody));
//				}
//
//				ob.softflag &= ~OB_SB_ENABLE;
//			}
//			if(ob.pose) {
//				bPoseChannel *pchan;
//				bConstraint *con;
//				for(pchan= ob.pose.chanbase.first; pchan; pchan= pchan.next) {
//					// note, pchan.bone is also lib-link stuff
//					if (pchan.limitmin[0] == 0.0f && pchan.limitmax[0] == 0.0f) {
//						pchan.limitmin[0]= pchan.limitmin[1]= pchan.limitmin[2]= -180.0f;
//						pchan.limitmax[0]= pchan.limitmax[1]= pchan.limitmax[2]= 180.0f;
//
//						for(con= pchan.constraints.first; con; con= con.next) {
//							if(con.type == CONSTRAINT_TYPE_KINEMATIC) {
//								bKinematicConstraint *data = (bKinematicConstraint*)con.data;
//								data.weight = 1.0f;
//								data.orientweight = 1.0f;
//								data.flag &= ~CONSTRAINT_IK_ROT;
//
//								/* enforce conversion from old IK_TOPARENT to rootbone index */
//								data.rootbone= -1;
//
//								/* update_pose_etc handles rootbone==-1 */
//								ob.pose.flag |= POSE_RECALC;
//							}
//						}
//					}
//				}
//			}
//
//			paf = give_parteff(ob);
//			if (paf) {
//				if(paf.disp == 0)
//					paf.disp = 100;
//				if(paf.speedtex == 0)
//					paf.speedtex = 8;
//				if(paf.omat == 0)
//					paf.omat = 1;
//			}
//		}
//
//		for(arm=main.armature.first; arm; arm= arm.id.next) {
//			bone_version_238(&arm.bonebase);
//			arm.deformflag |= ARM_DEF_VGROUP;
//		}
//
//		for(me=main.mesh.first; me; me= me.id.next) {
//			if (!me.medge) {
//				make_edges(me, 1);	/* 1 = use mface.edcode */
//			} else {
//				mesh_strip_loose_faces(me);
//			}
//		}
//
//		for(key= main.key.first; key; key= key.id.next) {
//			KeyBlock *kb;
//			int index= 1;
//
//			/* trick to find out if we already introduced adrcode */
//			for(kb= key.block.first; kb; kb= kb.next)
//				if(kb.adrcode) break;
//
//			if(kb==NULL) {
//				for(kb= key.block.first; kb; kb= kb.next) {
//					if(kb==key.refkey) {
//						if(kb.name[0]==0)
//							strcpy(kb.name, "Basis");
//					}
//					else {
//						if(kb.name[0]==0)
//							sprintf(kb.name, "Key %d", index);
//						kb.adrcode= index++;
//					}
//				}
//			}
//		}
//	}
//	if(main.versionfile <= 239) {
//		bArmature *arm;
//		Object *ob;
//		Scene *sce= main.scene.first;
//		Camera *cam= main.camera.first;
//		Material *ma= main.mat.first;
//		int set_passepartout= 0;
//
//		/* deformflag is local in modifier now */
//		for(ob=main.object.first; ob; ob= ob.id.next) {
//			ModifierData *md;
//
//			for (md=ob.modifiers.first; md; md=md.next) {
//				if (md.type==eModifierType_Armature) {
//					ArmatureModifierData *amd = (ArmatureModifierData*) md;
//					if(amd.object && amd.deformflag==0) {
//						Object *oba= newlibadr(fd, lib, amd.object);
//						bArmature *arm= newlibadr(fd, lib, oba.data);
//						amd.deformflag= arm.deformflag;
//					}
//				}
//			}
//		}
//
//		/* updating stepsize for ghost drawing */
//		for(arm= main.armature.first; arm; arm= arm.id.next) {
//			if (arm.ghostsize==0) arm.ghostsize=1;
//			bone_version_239(&arm.bonebase);
//			if(arm.layer==0) arm.layer= 1;
//		}
//
//		for(;sce;sce= sce.id.next) {
//			/* make 'innervert' the default subdivide type, for backwards compat */
//			sce.toolsettings.cornertype=1;
//
//			if(sce.r.scemode & R_PASSEPARTOUT) {
//				set_passepartout= 1;
//				sce.r.scemode &= ~R_PASSEPARTOUT;
//			}
//			/* gauss is filter variable now */
//			if(sce.r.mode & R_GAUSS) {
//				sce.r.filtertype= R_FILTER_GAUSS;
//				sce.r.mode &= ~R_GAUSS;
//			}
//		}
//
//		for(;cam; cam= cam.id.next) {
//			if(set_passepartout)
//				cam.flag |= CAM_SHOWPASSEPARTOUT;
//
//			/* make sure old cameras have title safe on */
//			if (!(cam.flag & CAM_SHOWTITLESAFE))
//			 cam.flag |= CAM_SHOWTITLESAFE;
//
//			/* set an appropriate camera passepartout alpha */
//			if (!(cam.passepartalpha)) cam.passepartalpha = 0.2f;
//		}
//
//		for(; ma; ma= ma.id.next) {
//			if(ma.strand_sta==0.0f) {
//				ma.strand_sta= ma.strand_end= 1.0f;
//				ma.mode |= MA_TANGENT_STR;
//			}
//			if(ma.mode & MA_TRACEBLE) ma.mode |= MA_SHADBUF;
//		}
//	}
//
//	if(main.versionfile <= 241) {
//		Object *ob;
//		Tex *tex;
//		Scene *sce;
//		World *wo;
//		Lamp *la;
//		Material *ma;
//		bArmature *arm;
//		bNodeTree *ntree;
//
//		for (wo = main.world.first; wo; wo= wo.id.next) {
//			/* Migrate to Bullet for games, except for the NaN versions */
//			/* People can still explicitely choose for Sumo (after 2.42 is out) */
//			if(main.versionfile > 225)
//				wo.physicsEngine = WOPHY_BULLET;
//			if(WO_AODIST == wo.aomode)
//				wo.aocolor= WO_AOPLAIN;
//		}
//
//		/* updating layers still */
//		for(arm= main.armature.first; arm; arm= arm.id.next) {
//			bone_version_239(&arm.bonebase);
//			if(arm.layer==0) arm.layer= 1;
//		}
//		for(sce= main.scene.first; sce; sce= sce.id.next) {
//			if(sce.jumpframe==0) sce.jumpframe= 10;
//			if(sce.audio.mixrate==0) sce.audio.mixrate= 44100;
//
//			if(sce.r.xparts<2) sce.r.xparts= 4;
//			if(sce.r.yparts<2) sce.r.yparts= 4;
//			/* adds default layer */
//			if(sce.r.layers.first==NULL)
//				scene_add_render_layer(sce);
//			else {
//				SceneRenderLayer *srl;
//				/* new layer flag for sky, was default for solid */
//				for(srl= sce.r.layers.first; srl; srl= srl.next) {
//					if(srl.layflag & SCE_LAY_SOLID)
//						srl.layflag |= SCE_LAY_SKY;
//					srl.passflag &= (SCE_PASS_COMBINED|SCE_PASS_Z|SCE_PASS_NORMAL|SCE_PASS_VECTOR);
//				}
//			}
//
//			/* node version changes */
//			if(sce.nodetree)
//				ntree_version_241(sce.nodetree);
//
//			/* uv calculation options moved to toolsettings */
//			if (sce.toolsettings.uvcalc_radius == 0.0) {
//				sce.toolsettings.uvcalc_radius = 1.0f;
//				sce.toolsettings.uvcalc_cubesize = 1.0f;
//				sce.toolsettings.uvcalc_mapdir = 1;
//				sce.toolsettings.uvcalc_mapalign = 1;
//				sce.toolsettings.uvcalc_flag = UVCALC_FILLHOLES;
//				sce.toolsettings.unwrapper = 1;
//			}
//
//			if(sce.r.mode & R_PANORAMA) {
//				/* all these checks to ensure saved files with cvs version keep working... */
//				if(sce.r.xsch < sce.r.ysch) {
//					Object *obc= newlibadr(fd, lib, sce.camera);
//					if(obc && obc.type==OB_CAMERA) {
//						Camera *cam= newlibadr(fd, lib, obc.data);
//						if(cam.lens>=10.0f) {
//							sce.r.xsch*= sce.r.xparts;
//							cam.lens*= (float)sce.r.ysch/(float)sce.r.xsch;
//						}
//					}
//				}
//			}
//		}
//
//		for(ntree= main.nodetree.first; ntree; ntree= ntree.id.next)
//			ntree_version_241(ntree);
//
//		for(la= main.lamp.first; la; la= la.id.next)
//			if(la.buffers==0)
//				la.buffers= 1;
//
//		for(tex= main.tex.first; tex; tex= tex.id.next) {
//			if(tex.env && tex.env.viewscale==0.0f)
//				tex.env.viewscale= 1.0f;
////			tex.imaflag |= TEX_GAUSS_MIP;
//		}
//
//		/* for empty drawsize and drawtype */
//		for(ob=main.object.first; ob; ob= ob.id.next) {
//			if(ob.empty_drawsize==0.0f) {
//				ob.empty_drawtype = OB_ARROWS;
//				ob.empty_drawsize = 1.0;
//			}
//		}
//
//		for(ma= main.mat.first; ma; ma= ma.id.next) {
//			/* stucci returns intensity from now on */
//			int a;
//			for(a=0; a<MAX_MTEX; a++) {
//				if(ma.mtex[a] && ma.mtex[a].tex) {
//					Tex *tex= newlibadr(fd, lib, ma.mtex[a].tex);
//					if(tex && tex.type==TEX_STUCCI)
//						ma.mtex[a].mapto &= ~(MAP_COL|MAP_SPEC|MAP_REF);
//				}
//			}
//			/* transmissivity defaults */
//			if(ma.tx_falloff==0.0) ma.tx_falloff= 1.0;
//		}
//
//		/* during 2.41 images with this name were used for viewer node output, lets fix that */
//		if(main.versionfile == 241) {
//			Image *ima;
//			for(ima= main.image.first; ima; ima= ima.id.next)
//				if(strcmp(ima.name, "Compositor")==0) {
//					strcpy(ima.id.name+2, "Viewer Node");
//					strcpy(ima.name, "Viewer Node");
//				}
//		}
//	}
//
//	if(main.versionfile <= 242) {
//		Scene *sce;
//		bScreen *sc;
//		Object *ob;
//		Curve *cu;
//		Material *ma;
//		Mesh *me;
//		Group *group;
//		Nurb *nu;
//		BezTriple *bezt;
//		BPoint *bp;
//		bNodeTree *ntree;
//		int a;
//
//		for(sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//			sa= sc.areabase.first;
//			while(sa) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					if(sl.spacetype==SPACE_VIEW3D) {
//						View3D *v3d= (View3D*) sl;
//						if (v3d.gridsubdiv == 0)
//							v3d.gridsubdiv = 10;
//					}
//				}
//				sa = sa.next;
//			}
//		}
//
//		for(sce= main.scene.first; sce; sce= sce.id.next) {
//			if (sce.toolsettings.select_thresh == 0.0f)
//				sce.toolsettings.select_thresh= 0.01f;
//			if (sce.toolsettings.clean_thresh == 0.0f)
//				sce.toolsettings.clean_thresh = 0.1f;
//
//			if (sce.r.threads==0) {
//				if (sce.r.mode & R_THREADS)
//					sce.r.threads= 2;
//				else
//					sce.r.threads= 1;
//			}
//			if(sce.nodetree)
//				ntree_version_242(sce.nodetree);
//		}
//
//		for(ntree= main.nodetree.first; ntree; ntree= ntree.id.next)
//			ntree_version_242(ntree);
//
//		/* add default radius values to old curve points */
//		for(cu= main.curve.first; cu; cu= cu.id.next) {
//			for(nu= cu.nurb.first; nu; nu= nu.next) {
//				if (nu) {
//					if(nu.bezt) {
//						for(bezt=nu.bezt, a=0; a<nu.pntsu; a++, bezt++) {
//							if (!bezt.radius) bezt.radius= 1.0;
//						}
//					}
//					else if(nu.bp) {
//						for(bp=nu.bp, a=0; a<nu.pntsu*nu.pntsv; a++, bp++) {
//							if(!bp.radius) bp.radius= 1.0;
//						}
//					}
//				}
//			}
//		}
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			ModifierData *md;
//			ListBase *list;
//			list = &ob.constraints;
//
//			/* check for already existing MinMax (floor) constraint
//			   and update the sticky flagging */
//
//			if (list){
//				bConstraint *curcon;
//				for (curcon = list.first; curcon; curcon=curcon.next){
//					switch (curcon.type) {
//						case CONSTRAINT_TYPE_MINMAX:
//						{
//							bMinMaxConstraint *data = curcon.data;
//							if (data.sticky==1)
//								data.flag |= MINMAX_STICKY;
//							else
//								data.flag &= ~MINMAX_STICKY;
//						}
//							break;
//						case CONSTRAINT_TYPE_ROTLIKE:
//						{
//							bRotateLikeConstraint *data = curcon.data;
//
//							/* version patch from buttons_object.c */
//							if(data.flag==0)
//								data.flag = ROTLIKE_X|ROTLIKE_Y|ROTLIKE_Z;
//						}
//							break;
//					}
//				}
//			}
//
//			if (ob.type == OB_ARMATURE) {
//				if (ob.pose){
//					bConstraint *curcon;
//					bPoseChannel *pchan;
//					for (pchan = ob.pose.chanbase.first; pchan; pchan=pchan.next){
//						for (curcon = pchan.constraints.first; curcon; curcon=curcon.next){
//							switch (curcon.type) {
//								case CONSTRAINT_TYPE_MINMAX:
//								{
//									bMinMaxConstraint *data = curcon.data;
//									if (data.sticky==1)
//										data.flag |= MINMAX_STICKY;
//									else
//										data.flag &= ~MINMAX_STICKY;
//								}
//									break;
//								case CONSTRAINT_TYPE_KINEMATIC:
//								{
//									bKinematicConstraint *data = curcon.data;
//									if (!(data.flag & CONSTRAINT_IK_POS)) {
//										data.flag |= CONSTRAINT_IK_POS;
//										data.flag |= CONSTRAINT_IK_STRETCH;
//									}
//								}
//									break;
//								case CONSTRAINT_TYPE_ROTLIKE:
//								{
//									bRotateLikeConstraint *data = curcon.data;
//
//									/* version patch from buttons_object.c */
//									if(data.flag==0)
//										data.flag = ROTLIKE_X|ROTLIKE_Y|ROTLIKE_Z;
//								}
//									break;
//							}
//						}
//					}
//				}
//			}
//
//			/* copy old object level track settings to curve modifers */
//			for (md=ob.modifiers.first; md; md=md.next) {
//				if (md.type==eModifierType_Curve) {
//					CurveModifierData *cmd = (CurveModifierData*) md;
//
//					if (cmd.defaxis == 0) cmd.defaxis = ob.trackflag+1;
//				}
//			}
//
//		}
//
//		for(ma = main.mat.first; ma; ma= ma.id.next) {
//			if(ma.shad_alpha==0.0f)
//				ma.shad_alpha= 1.0f;
//			if(ma.nodetree)
//				ntree_version_242(ma.nodetree);
//		}
//
//		for(me=main.mesh.first; me; me=me.id.next)
//			customdata_version_242(me);
//
//		for(group= main.group.first; group; group= group.id.next)
//			if(group.layer==0)
//			   group.layer= (1<<20)-1;
//
//		/* History fix (python?), shape key adrcode numbers have to be sorted */
//		sort_shape_fix(main);
//
//		/* now, subversion control! */
//		if(main.subversionfile < 3) {
//			bScreen *sc;
//			Image *ima;
//			Tex *tex;
//
//			/* Image refactor initialize */
//			for(ima= main.image.first; ima; ima= ima.id.next) {
//				ima.source= IMA_SRC_FILE;
//				ima.type= IMA_TYPE_IMAGE;
//
//				ima.gen_x= 256; ima.gen_y= 256;
//				ima.gen_type= 1;
//
//				if(0==strncmp(ima.id.name+2, "Viewer Node", sizeof(ima.id.name+2))) {
//					ima.source= IMA_SRC_VIEWER;
//					ima.type= IMA_TYPE_COMPOSITE;
//				}
//				if(0==strncmp(ima.id.name+2, "Render Result", sizeof(ima.id.name+2))) {
//					ima.source= IMA_SRC_VIEWER;
//					ima.type= IMA_TYPE_R_RESULT;
//				}
//
//			}
//			for(tex= main.tex.first; tex; tex= tex.id.next) {
//				if(tex.type==TEX_IMAGE && tex.ima) {
//					ima= newlibadr(fd, lib, tex.ima);
//					if(tex.imaflag & TEX_ANIM5_)
//						ima.source= IMA_SRC_MOVIE;
//					if(tex.imaflag & TEX_FIELDS_)
//						ima.flag |= IMA_FIELDS;
//					if(tex.imaflag & TEX_STD_FIELD_)
//						ima.flag |= IMA_STD_FIELD;
//					if(tex.imaflag & TEX_ANTIALI_)
//						ima.flag |= IMA_ANTIALI;
//				}
//				tex.iuser.frames= tex.frames;
//				tex.iuser.fie_ima= tex.fie_ima;
//				tex.iuser.offset= tex.offset;
//				tex.iuser.sfra= tex.sfra;
//				tex.iuser.cycl= (tex.imaflag & TEX_ANIMCYCLIC_)!=0;
//			}
//			for(sce= main.scene.first; sce; sce= sce.id.next) {
//				if(sce.nodetree)
//					do_version_ntree_242_2(sce.nodetree);
//			}
//			for(ntree= main.nodetree.first; ntree; ntree= ntree.id.next)
//				do_version_ntree_242_2(ntree);
//			for(ma = main.mat.first; ma; ma= ma.id.next)
//				if(ma.nodetree)
//					do_version_ntree_242_2(ma.nodetree);
//
//			for(sc= main.screen.first; sc; sc= sc.id.next) {
//				ScrArea *sa;
//				for(sa= sc.areabase.first; sa; sa= sa.next) {
//					SpaceLink *sl;
//					for (sl= sa.spacedata.first; sl; sl= sl.next) {
//						if(sl.spacetype==SPACE_IMAGE)
//							((SpaceImage *)sl).iuser.fie_ima= 2;
//						else if(sl.spacetype==SPACE_VIEW3D) {
//							View3D *v3d= (View3D *)sl;
//							if(v3d.bgpic)
//								v3d.bgpic.iuser.fie_ima= 2;
//						}
//					}
//				}
//			}
//		}
//
//		if(main.subversionfile < 4) {
//			for(sce= main.scene.first; sce; sce= sce.id.next) {
//				sce.r.bake_mode= 1;	/* prevent to include render stuff here */
//				sce.r.bake_filter= 2;
//				sce.r.bake_osa= 5;
//				sce.r.bake_flag= R_BAKE_CLEAR;
//			}
//		}
//
//		if(main.subversionfile < 5) {
//			for(sce= main.scene.first; sce; sce= sce.id.next) {
//				/* improved triangle to quad conversion settings */
//				if(sce.toolsettings.jointrilimit==0.0f)
//					sce.toolsettings.jointrilimit= 0.8f;
//			}
//		}
//	}
//	if(main.versionfile <= 243) {
//		Object *ob= main.object.first;
//		Camera *cam = main.camera.first;
//		Material *ma;
//
//		for(; cam; cam= cam.id.next) {
//			cam.angle= 360.0f * (float)atan(16.0f/cam.lens) / (float)M_PI;
//		}
//
//		for(ma=main.mat.first; ma; ma= ma.id.next) {
//			if(ma.sss_scale==0.0f) {
//				ma.sss_radius[0]= 1.0f;
//				ma.sss_radius[1]= 1.0f;
//				ma.sss_radius[2]= 1.0f;
//				ma.sss_col[0]= 0.8f;
//				ma.sss_col[1]= 0.8f;
//				ma.sss_col[2]= 0.8f;
//				ma.sss_error= 0.05f;
//				ma.sss_scale= 0.1f;
//				ma.sss_ior= 1.3f;
//				ma.sss_colfac= 1.0f;
//				ma.sss_texfac= 0.0f;
//			}
//			if(ma.sss_front==0 && ma.sss_back==0) {
//				ma.sss_front= 1.0f;
//				ma.sss_back= 1.0f;
//			}
//			if(ma.sss_col[0]==0 && ma.sss_col[1]==0 && ma.sss_col[2]==0) {
//				ma.sss_col[0]= ma.r;
//				ma.sss_col[1]= ma.g;
//				ma.sss_col[2]= ma.b;
//			}
//		}
//
//		for(; ob; ob= ob.id.next) {
//			bDeformGroup *curdef;
//
//			for(curdef= ob.defbase.first; curdef; curdef=curdef.next) {
//				/* replace an empty-string name with unique name */
//				if (curdef.name[0] == '\0') {
//					unique_vertexgroup_name(curdef, ob);
//				}
//			}
//
//			if(main.versionfile < 243 || main.subversionfile < 1) {
//				ModifierData *md;
//
//				/* translate old mirror modifier axis values to new flags */
//				for (md=ob.modifiers.first; md; md=md.next) {
//					if (md.type==eModifierType_Mirror) {
//						MirrorModifierData *mmd = (MirrorModifierData*) md;
//
//						switch(mmd.axis)
//						{
//						case 0:
//							mmd.flag |= MOD_MIR_AXIS_X;
//							break;
//						case 1:
//							mmd.flag |= MOD_MIR_AXIS_Y;
//							break;
//						case 2:
//							mmd.flag |= MOD_MIR_AXIS_Z;
//							break;
//						}
//
//						mmd.axis = 0;
//					}
//				}
//			}
//		}
//
//		/* render layer added, this is not the active layer */
//		if(main.versionfile <= 243 || main.subversionfile < 2) {
//			Mesh *me;
//			for(me=main.mesh.first; me; me=me.id.next)
//				customdata_version_243(me);
//		}
//
//	}
//
//	if(main.versionfile <= 244) {
//		Scene *sce;
//		bScreen *sc;
//		Lamp *la;
//		World *wrld;
//
//		if(main.versionfile != 244 || main.subversionfile < 2) {
//			for(sce= main.scene.first; sce; sce= sce.id.next)
//				sce.r.mode |= R_SSS;
//
//			/* correct older action editors - incorrect scrolling */
//			for(sc= main.screen.first; sc; sc= sc.id.next) {
//				ScrArea *sa;
//				sa= sc.areabase.first;
//				while(sa) {
//					SpaceLink *sl;
//
//					for (sl= sa.spacedata.first; sl; sl= sl.next) {
//						if(sl.spacetype==SPACE_ACTION) {
//							SpaceAction *saction= (SpaceAction*) sl;
//
//							saction.v2d.tot.ymin= -1000.0;
//							saction.v2d.tot.ymax= 0.0;
//
//							saction.v2d.cur.ymin= -75.0;
//							saction.v2d.cur.ymax= 5.0;
//						}
//					}
//					sa = sa.next;
//				}
//			}
//		}
//		if (main.versionfile != 244 || main.subversionfile < 3) {
//			/* constraints recode version patch used to be here. Moved to 245 now... */
//
//
//			for(wrld=main.world.first; wrld; wrld= wrld.id.next) {
//				if (wrld.mode & WO_AMB_OCC)
//					wrld.ao_samp_method = WO_AOSAMP_CONSTANT;
//				else
//					wrld.ao_samp_method = WO_AOSAMP_HAMMERSLEY;
//
//				wrld.ao_adapt_thresh = 0.005f;
//			}
//
//			for(la=main.lamp.first; la; la= la.id.next) {
//				if (la.type == LA_AREA)
//					la.ray_samp_method = LA_SAMP_CONSTANT;
//				else
//					la.ray_samp_method = LA_SAMP_HALTON;
//
//				la.adapt_thresh = 0.001f;
//			}
//		}
//	}
//	if(main.versionfile <= 245) {
//		Scene *sce;
//		bScreen *sc;
//		Object *ob;
//		Image *ima;
//		Lamp *la;
//		Material *ma;
//		ParticleSettings *part;
//		World *wrld;
//		Mesh *me;
//		bNodeTree *ntree;
//		Tex *tex;
//		ModifierData *md;
//		ParticleSystem *psys;
//
//		/* unless the file was created 2.44.3 but not 2.45, update the constraints */
//		if ( !(main.versionfile==244 && main.subversionfile==3) &&
//			 ((main.versionfile<245) || (main.versionfile==245 && main.subversionfile==0)) )
//		{
//			for (ob = main.object.first; ob; ob= ob.id.next) {
//				ListBase *list;
//				list = &ob.constraints;
//
//				/* fix up constraints due to constraint recode changes (originally at 2.44.3) */
//				if (list) {
//					bConstraint *curcon;
//					for (curcon = list.first; curcon; curcon=curcon.next) {
//						/* old CONSTRAINT_LOCAL check . convert to CONSTRAINT_SPACE_LOCAL */
//						if (curcon.flag & 0x20) {
//							curcon.ownspace = CONSTRAINT_SPACE_LOCAL;
//							curcon.tarspace = CONSTRAINT_SPACE_LOCAL;
//						}
//
//						switch (curcon.type) {
//							case CONSTRAINT_TYPE_LOCLIMIT:
//							{
//								bLocLimitConstraint *data= (bLocLimitConstraint *)curcon.data;
//
//								/* old limit without parent option for objects */
//								if (data.flag2)
//									curcon.ownspace = CONSTRAINT_SPACE_LOCAL;
//							}
//								break;
//						}
//					}
//				}
//
//				/* correctly initialise constinv matrix */
//				Mat4One(ob.constinv);
//
//				if (ob.type == OB_ARMATURE) {
//					if (ob.pose) {
//						bConstraint *curcon;
//						bPoseChannel *pchan;
//
//						for (pchan = ob.pose.chanbase.first; pchan; pchan=pchan.next) {
//							/* make sure constraints are all up to date */
//							for (curcon = pchan.constraints.first; curcon; curcon=curcon.next) {
//								/* old CONSTRAINT_LOCAL check . convert to CONSTRAINT_SPACE_LOCAL */
//								if (curcon.flag & 0x20) {
//									curcon.ownspace = CONSTRAINT_SPACE_LOCAL;
//									curcon.tarspace = CONSTRAINT_SPACE_LOCAL;
//								}
//
//								switch (curcon.type) {
//									case CONSTRAINT_TYPE_ACTION:
//									{
//										bActionConstraint *data= (bActionConstraint *)curcon.data;
//
//										/* 'data.local' used to mean that target was in local-space */
//										if (data.local)
//											curcon.tarspace = CONSTRAINT_SPACE_LOCAL;
//									}
//										break;
//								}
//							}
//
//							/* correctly initialise constinv matrix */
//							Mat4One(pchan.constinv);
//						}
//					}
//				}
//			}
//		}
//
//		/* fix all versions before 2.45 */
//		if (main.versionfile != 245) {
//
//			/* repair preview from 242 - 244*/
//			for(ima= main.image.first; ima; ima= ima.id.next) {
//				ima.preview = NULL;
//			}
//
//			/* repair imasel space - completely reworked */
//			for(sc= main.screen.first; sc; sc= sc.id.next) {
//				ScrArea *sa;
//				sa= sc.areabase.first;
//				while(sa) {
//					SpaceLink *sl;
//
//					for (sl= sa.spacedata.first; sl; sl= sl.next) {
//						if(sl.spacetype==SPACE_IMASEL) {
//							SpaceImaSel *simasel= (SpaceImaSel*) sl;
//							simasel.blockscale= 0.7f;
//							/* view 2D */
//							simasel.v2d.tot.xmin=  -10.0f;
//							simasel.v2d.tot.ymin=  -10.0f;
//							simasel.v2d.tot.xmax= (float)sa.winx + 10.0f;
//							simasel.v2d.tot.ymax= (float)sa.winy + 10.0f;
//							simasel.v2d.cur.xmin=  0.0f;
//							simasel.v2d.cur.ymin=  0.0f;
//							simasel.v2d.cur.xmax= (float)sa.winx;
//							simasel.v2d.cur.ymax= (float)sa.winy;
//							simasel.v2d.min[0]= 1.0;
//							simasel.v2d.min[1]= 1.0;
//							simasel.v2d.max[0]= 32000.0f;
//							simasel.v2d.max[1]= 32000.0f;
//							simasel.v2d.minzoom= 0.5f;
//							simasel.v2d.maxzoom= 1.21f;
//							simasel.v2d.scroll= 0;
//							simasel.v2d.keepzoom= V2D_KEEPZOOM|V2D_KEEPASPECT;
//							simasel.v2d.keeptot= 0;
//							simasel.prv_h = 96;
//							simasel.prv_w = 96;
//							simasel.flag = 7; /* ??? elubie */
//							strcpy (simasel.dir,  U.textudir);	/* TON */
//							strcpy (simasel.file, "");
//
//							simasel.returnfunc     =  0;
//							simasel.title[0]       =  0;
//						}
//					}
//					sa = sa.next;
//				}
//			}
//		}
//
//		/* add point caches */
//		for(ob=main.object.first; ob; ob=ob.id.next) {
//			if(ob.soft && !ob.soft.pointcache)
//				ob.soft.pointcache= BKE_ptcache_add();
//
//			for(psys=ob.particlesystem.first; psys; psys=psys.next) {
//				if(psys.soft && !psys.soft.pointcache)
//					psys.soft.pointcache= BKE_ptcache_add();
//				if(!psys.pointcache)
//					psys.pointcache= BKE_ptcache_add();
//			}
//
//			for(md=ob.modifiers.first; md; md=md.next) {
//				if(md.type==eModifierType_Cloth) {
//					ClothModifierData *clmd = (ClothModifierData*) md;
//					if(!clmd.point_cache)
//						clmd.point_cache= BKE_ptcache_add();
//				}
//			}
//		}
//
//		/* Copy over old per-level multires vertex data
//		   into a single vertex array in struct Multires */
//		for(me = main.mesh.first; me; me=me.id.next) {
//			if(me.mr && !me.mr.verts) {
//				MultiresLevel *lvl = me.mr.levels.last;
//				if(lvl) {
//					me.mr.verts = lvl.verts;
//					lvl.verts = NULL;
//					/* Don't need the other vert arrays */
//					for(lvl = lvl.prev; lvl; lvl = lvl.prev) {
//						MEM_freeN(lvl.verts);
//						lvl.verts = NULL;
//					}
//				}
//			}
//		}
//
//		if (main.versionfile != 245 || main.subversionfile < 1) {
//			for(la=main.lamp.first; la; la= la.id.next) {
//				if (la.mode & LA_QUAD) la.falloff_type = LA_FALLOFF_SLIDERS;
//				else la.falloff_type = LA_FALLOFF_INVLINEAR;
//
//				if (la.curfalloff == NULL) {
//					la.curfalloff = curvemapping_add(1, 0.0f, 1.0f, 1.0f, 0.0f);
//					curvemapping_initialize(la.curfalloff);
//				}
//			}
//		}
//
//		for(ma=main.mat.first; ma; ma= ma.id.next) {
//			if(ma.samp_gloss_mir == 0) {
//				ma.gloss_mir = ma.gloss_tra= 1.0f;
//				ma.aniso_gloss_mir = 1.0f;
//				ma.samp_gloss_mir = ma.samp_gloss_tra= 18;
//				ma.adapt_thresh_mir = ma.adapt_thresh_tra = 0.005f;
//				ma.dist_mir = 0.0f;
//				ma.fadeto_mir = MA_RAYMIR_FADETOSKY;
//			}
//
//			if(ma.strand_min == 0.0f)
//				ma.strand_min= 1.0f;
//		}
//
//		for(part=main.particle.first; part; part=part.id.next) {
//			if(part.ren_child_nbr==0)
//				part.ren_child_nbr= part.child_nbr;
//
//			if(part.simplify_refsize==0) {
//				part.simplify_refsize= 1920;
//				part.simplify_rate= 1.0f;
//				part.simplify_transition= 0.1f;
//				part.simplify_viewport= 0.8f;
//			}
//		}
//
//		for(wrld=main.world.first; wrld; wrld= wrld.id.next) {
//			if(wrld.ao_approx_error == 0.0f)
//				wrld.ao_approx_error= 0.25f;
//		}
//
//		for(sce= main.scene.first; sce; sce= sce.id.next) {
//			if(sce.nodetree)
//				ntree_version_245(fd, lib, sce.nodetree);
//
//			if(sce.r.simplify_shadowsamples == 0) {
//				sce.r.simplify_subsurf= 6;
//				sce.r.simplify_particles= 1.0f;
//				sce.r.simplify_shadowsamples= 16;
//				sce.r.simplify_aosss= 1.0f;
//			}
//
//			if(sce.r.cineongamma == 0) {
//				sce.r.cineonblack= 95;
//				sce.r.cineonwhite= 685;
//				sce.r.cineongamma= 1.7f;
//			}
//		}
//
//		for(ntree=main.nodetree.first; ntree; ntree= ntree.id.next)
//			ntree_version_245(fd, lib, ntree);
//
//		/* fix for temporary flag changes during 245 cycle */
//		for(ima= main.image.first; ima; ima= ima.id.next) {
//			if(ima.flag & IMA_OLD_PREMUL) {
//				ima.flag &= ~IMA_OLD_PREMUL;
//				ima.flag |= IMA_DO_PREMUL;
//			}
//		}
//
//		for(tex=main.tex.first; tex; tex=tex.id.next) {
//			if(tex.iuser.flag & IMA_OLD_PREMUL) {
//				tex.iuser.flag &= ~IMA_OLD_PREMUL;
//				tex.iuser.flag |= IMA_DO_PREMUL;
//
//			}
//
//			ima= newlibadr(fd, lib, tex.ima);
//			if(ima && (tex.iuser.flag & IMA_DO_PREMUL)) {
//				ima.flag &= ~IMA_OLD_PREMUL;
//				ima.flag |= IMA_DO_PREMUL;
//			}
//		}
//	}
//
//	/* sanity check for skgen
//	 * */
//	{
//		Scene *sce;
//		for(sce=main.scene.first; sce; sce = sce.id.next)
//		{
//			if (sce.toolsettings.skgen_subdivisions[0] == sce.toolsettings.skgen_subdivisions[1] ||
//				sce.toolsettings.skgen_subdivisions[0] == sce.toolsettings.skgen_subdivisions[2] ||
//				sce.toolsettings.skgen_subdivisions[1] == sce.toolsettings.skgen_subdivisions[2])
//			{
//					sce.toolsettings.skgen_subdivisions[0] = SKGEN_SUB_CORRELATION;
//					sce.toolsettings.skgen_subdivisions[1] = SKGEN_SUB_LENGTH;
//					sce.toolsettings.skgen_subdivisions[2] = SKGEN_SUB_ANGLE;
//			}
//		}
//	}
//
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 2)) {
//		Image *ima;
//
//		/* initialize 1:1 Aspect */
//		for(ima= main.image.first; ima; ima= ima.id.next) {
//			ima.aspx = ima.aspy = 1.0f;
//		}
//
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 4)) {
//		bArmature *arm;
//		ModifierData *md;
//		Object *ob;
//
//		for(arm= main.armature.first; arm; arm= arm.id.next)
//			arm.deformflag |= ARM_DEF_B_BONE_REST;
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			for(md=ob.modifiers.first; md; md=md.next) {
//				if(md.type==eModifierType_Armature)
//					((ArmatureModifierData*)md).deformflag |= ARM_DEF_B_BONE_REST;
//			}
//		}
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 5)) {
//		/* foreground color needs to be somthing other then black */
//		Scene *sce;
//		for(sce= main.scene.first; sce; sce=sce.id.next) {
//			sce.r.fg_stamp[0] = sce.r.fg_stamp[1] = sce.r.fg_stamp[2] = 0.8f;
//			sce.r.fg_stamp[3] = 1.0f; /* dont use text alpha yet */
//			sce.r.bg_stamp[3] = 0.25f; /* make sure the background has full alpha */
//		}
//	}
//
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 6)) {
//		Scene *sce;
//		/* fix frs_sec_base */
//		for(sce= main.scene.first; sce; sce= sce.id.next) {
//			if (sce.r.frs_sec_base == 0) {
//				sce.r.frs_sec_base = 1;
//			}
//		}
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 7)) {
//		Object *ob;
//		bPoseChannel *pchan;
//		bConstraint *con;
//		bConstraintTarget *ct;
//
//		for (ob = main.object.first; ob; ob= ob.id.next) {
//			if (ob.pose) {
//				for (pchan=ob.pose.chanbase.first; pchan; pchan=pchan.next) {
//					for (con=pchan.constraints.first; con; con=con.next) {
//						if (con.type == CONSTRAINT_TYPE_PYTHON) {
//							bPythonConstraint *data= (bPythonConstraint *)con.data;
//							if (data.tar) {
//								/* version patching needs to be done */
//								ct= MEM_callocN(sizeof(bConstraintTarget), "PyConTarget");
//
//								ct.tar = data.tar;
//								strcpy(ct.subtarget, data.subtarget);
//								ct.space = con.tarspace;
//
//								BLI_addtail(&data.targets, ct);
//								data.tarnum++;
//
//								/* clear old targets to avoid problems */
//								data.tar = NULL;
//								strcpy(data.subtarget, "");
//							}
//						}
//						else if (con.type == CONSTRAINT_TYPE_LOCLIKE) {
//							bLocateLikeConstraint *data= (bLocateLikeConstraint *)con.data;
//
//							/* new headtail functionality makes Bone-Tip function obsolete */
//							if (data.flag & LOCLIKE_TIP)
//								con.headtail = 1.0f;
//						}
//					}
//				}
//			}
//
//			for (con=ob.constraints.first; con; con=con.next) {
//				if (con.type==CONSTRAINT_TYPE_PYTHON) {
//					bPythonConstraint *data= (bPythonConstraint *)con.data;
//					if (data.tar) {
//						/* version patching needs to be done */
//						ct= MEM_callocN(sizeof(bConstraintTarget), "PyConTarget");
//
//						ct.tar = data.tar;
//						strcpy(ct.subtarget, data.subtarget);
//						ct.space = con.tarspace;
//
//						BLI_addtail(&data.targets, ct);
//						data.tarnum++;
//
//						/* clear old targets to avoid problems */
//						data.tar = NULL;
//						strcpy(data.subtarget, "");
//					}
//				}
//				else if (con.type == CONSTRAINT_TYPE_LOCLIKE) {
//					bLocateLikeConstraint *data= (bLocateLikeConstraint *)con.data;
//
//					/* new headtail functionality makes Bone-Tip function obsolete */
//					if (data.flag & LOCLIKE_TIP)
//						con.headtail = 1.0f;
//				}
//			}
//
//			if(ob.soft && ob.soft.keys) {
//				SoftBody *sb = ob.soft;
//				int k;
//
//				for(k=0; k<sb.totkey; k++) {
//					if(sb.keys[k])
//						MEM_freeN(sb.keys[k]);
//				}
//
//				MEM_freeN(sb.keys);
//
//				sb.keys = NULL;
//				sb.totkey = 0;
//			}
//		}
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 8)) {
//		Scene *sce;
//		Object *ob;
//		PartEff *paf=0;
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			if(ob.soft && ob.soft.keys) {
//				SoftBody *sb = ob.soft;
//				int k;
//
//				for(k=0; k<sb.totkey; k++) {
//					if(sb.keys[k])
//						MEM_freeN(sb.keys[k]);
//				}
//
//				MEM_freeN(sb.keys);
//
//				sb.keys = NULL;
//				sb.totkey = 0;
//			}
//
//			/* convert old particles to new system */
//			if((paf = give_parteff(ob))) {
//				ParticleSystem *psys;
//				ModifierData *md;
//				ParticleSystemModifierData *psmd;
//				ParticleSettings *part;
//
//				/* create new particle system */
//				psys = MEM_callocN(sizeof(ParticleSystem), "particle_system");
//				psys.pointcache = BKE_ptcache_add();
//
//				part = psys.part = psys_new_settings("ParticleSettings", main);
//
//				/* needed for proper libdata lookup */
//				oldnewmap_insert(fd.libmap, psys.part, psys.part, 0);
//				part.id.lib= ob.id.lib;
//
//				part.id.us--;
//				part.id.flag |= (ob.id.flag & LIB_NEEDLINK);
//
//				psys.totpart=0;
//				psys.flag= PSYS_ENABLED|PSYS_CURRENT;
//
//				BLI_addtail(&ob.particlesystem, psys);
//
//				md= modifier_new(eModifierType_ParticleSystem);
//				sprintf(md.name, "ParticleSystem %i", BLI_countlist(&ob.particlesystem));
//				psmd= (ParticleSystemModifierData*) md;
//				psmd.psys=psys;
//				BLI_addtail(&ob.modifiers, md);
//
//				/* convert settings from old particle system */
//				/* general settings */
//				part.totpart = MIN2(paf.totpart, 100000);
//				part.sta = paf.sta;
//				part.end = paf.end;
//				part.lifetime = paf.lifetime;
//				part.randlife = paf.randlife;
//				psys.seed = paf.seed;
//				part.disp = paf.disp;
//				part.omat = paf.mat[0];
//				part.hair_step = paf.totkey;
//
//				part.eff_group = paf.group;
//
//				/* old system didn't interpolate between keypoints at render time */
//				part.draw_step = part.ren_step = 0;
//
//				/* physics */
//				part.normfac = paf.normfac * 25.0f;
//				part.obfac = paf.obfac;
//				part.randfac = paf.randfac * 25.0f;
//				part.dampfac = paf.damp;
//				VECCOPY(part.acc, paf.force);
//
//				/* flags */
//				if(paf.stype & PAF_VECT) {
//					if(paf.flag & PAF_STATIC) {
//						/* new hair lifetime is always 100.0f */
//						float fac = paf.lifetime / 100.0f;
//
//						part.draw_as = PART_DRAW_PATH;
//						part.type = PART_HAIR;
//						psys.recalc |= PSYS_RECALC_REDO;
//
//						part.normfac *= fac;
//						part.randfac *= fac;
//					}
//					else {
//						part.draw_as = PART_DRAW_LINE;
//						part.draw |= PART_DRAW_VEL_LENGTH;
//						part.draw_line[1] = 0.04f;
//					}
//				}
//
//				part.rotmode = PART_ROT_VEL;
//
//				part.flag |= (paf.flag & PAF_BSPLINE) ? PART_HAIR_BSPLINE : 0;
//				part.flag |= (paf.flag & PAF_TRAND) ? PART_TRAND : 0;
//				part.flag |= (paf.flag & PAF_EDISTR) ? PART_EDISTR : 0;
//				part.flag |= (paf.flag & PAF_UNBORN) ? PART_UNBORN : 0;
//				part.flag |= (paf.flag & PAF_DIED) ? PART_DIED : 0;
//				part.from |= (paf.flag & PAF_FACE) ? PART_FROM_FACE : 0;
//				part.draw |= (paf.flag & PAF_SHOWE) ? PART_DRAW_EMITTER : 0;
//
//				psys.vgroup[PSYS_VG_DENSITY] = paf.vertgroup;
//				psys.vgroup[PSYS_VG_VEL] = paf.vertgroup_v;
//				psys.vgroup[PSYS_VG_LENGTH] = paf.vertgroup_v;
//
//				/* dupliobjects */
//				if(ob.transflag & OB_DUPLIVERTS) {
//					Object *dup = main.object.first;
//
//					for(; dup; dup= dup.id.next) {
//						if(ob == newlibadr(fd, lib, dup.parent)) {
//							part.dup_ob = dup;
//							ob.transflag |= OB_DUPLIPARTS;
//							ob.transflag &= ~OB_DUPLIVERTS;
//
//							part.draw_as = PART_DRAW_OB;
//
//							/* needed for proper libdata lookup */
//							oldnewmap_insert(fd.libmap, dup, dup, 0);
//						}
//					}
//				}
//
//
//				{
//					FluidsimModifierData *fluidmd = (FluidsimModifierData *)modifiers_findByType(ob, eModifierType_Fluidsim);
//					if(fluidmd && fluidmd.fss && fluidmd.fss.type == OB_FLUIDSIM_PARTICLE)
//						part.type = PART_FLUID;
//				}
//
//				free_effects(&ob.effect);
//
//				printf("Old particle system converted to new system.\n");
//			}
//		}
//
//		for(sce= main.scene.first; sce; sce=sce.id.next) {
//			ParticleEditSettings *pset= &sce.toolsettings.particle;
//			int a;
//
//			if(pset.brush[0].size == 0) {
//				pset.flag= PE_KEEP_LENGTHS|PE_LOCK_FIRST|PE_DEFLECT_EMITTER;
//				pset.emitterdist= 0.25f;
//				pset.totrekey= 5;
//				pset.totaddkey= 5;
//				pset.brushtype= PE_BRUSH_NONE;
//
//				for(a=0; a<PE_TOT_BRUSH; a++) {
//					pset.brush[a].strength= 50;
//					pset.brush[a].size= 50;
//					pset.brush[a].step= 10;
//				}
//
//				pset.brush[PE_BRUSH_CUT].strength= 100;
//			}
//		}
//	}
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 9)) {
//		Material *ma;
//		int a;
//
//		for(ma=main.mat.first; ma; ma= ma.id.next)
//			if(ma.mode & MA_NORMAP_TANG)
//				for(a=0; a<MAX_MTEX; a++)
//					if(ma.mtex[a] && ma.mtex[a].tex)
//						ma.mtex[a].normapspace = MTEX_NSPACE_TANGENT;
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 10)) {
//		Object *ob;
//
//		/* dupliface scale */
//		for(ob= main.object.first; ob; ob= ob.id.next)
//			ob.dupfacesca = 1.0f;
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 11)) {
//		Object *ob;
//		bActionStrip *strip;
//
//		/* nla-strips - scale */
//		for (ob= main.object.first; ob; ob= ob.id.next) {
//			for (strip= ob.nlastrips.first; strip; strip= strip.next) {
//				float length, actlength, repeat;
//
//				if (strip.flag & ACTSTRIP_USESTRIDE)
//					repeat= 1.0f;
//				else
//					repeat= strip.repeat;
//
//				length = strip.end-strip.start;
//				if (length == 0.0f) length= 1.0f;
//				actlength = strip.actend-strip.actstart;
//
//				strip.scale = length / (repeat * actlength);
//				if (strip.scale == 0.0f) strip.scale= 1.0f;
//			}
//			if(ob.soft){
//				ob.soft.inpush =  ob.soft.inspring;
//				ob.soft.shearstiff = 1.0f;
//			}
//		}
//	}
//
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 14)) {
//		Scene *sce;
//		Sequence *seq;
//
//		for(sce=main.scene.first; sce; sce=sce.id.next) {
//			SEQ_BEGIN(sce.ed, seq) {
//				if (seq.blend_mode == 0)
//					seq.blend_opacity = 100.0f;
//			}
//			SEQ_END
//		}
//	}
//
//	/*fix broken group lengths in id properties*/
//	if ((main.versionfile < 245) || (main.versionfile == 245 && main.subversionfile < 15)) {
//		idproperties_fix_group_lengths(main.scene);
//		idproperties_fix_group_lengths(main.library);
//		idproperties_fix_group_lengths(main.object);
//		idproperties_fix_group_lengths(main.mesh);
//		idproperties_fix_group_lengths(main.curve);
//		idproperties_fix_group_lengths(main.mball);
//		idproperties_fix_group_lengths(main.mat);
//		idproperties_fix_group_lengths(main.tex);
//		idproperties_fix_group_lengths(main.image);
//		idproperties_fix_group_lengths(main.wave);
//		idproperties_fix_group_lengths(main.latt);
//		idproperties_fix_group_lengths(main.lamp);
//		idproperties_fix_group_lengths(main.camera);
//		idproperties_fix_group_lengths(main.ipo);
//		idproperties_fix_group_lengths(main.key);
//		idproperties_fix_group_lengths(main.world);
//		idproperties_fix_group_lengths(main.screen);
//		idproperties_fix_group_lengths(main.script);
//		idproperties_fix_group_lengths(main.vfont);
//		idproperties_fix_group_lengths(main.text);
//		idproperties_fix_group_lengths(main.sound);
//		idproperties_fix_group_lengths(main.group);
//		idproperties_fix_group_lengths(main.armature);
//		idproperties_fix_group_lengths(main.action);
//		idproperties_fix_group_lengths(main.nodetree);
//		idproperties_fix_group_lengths(main.brush);
//		idproperties_fix_group_lengths(main.particle);
//	}
//
//	/* sun/sky */
//	if(main.versionfile < 246) {
//		Object *ob;
//		bActuator *act;
//
//		/* dRot actuator change direction in 2.46 */
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			for(act= ob.actuators.first; act; act= act.next) {
//				if (act.type == ACT_OBJECT) {
//					bObjectActuator *ba= act.data;
//
//					ba.drot[0] = -ba.drot[0];
//					ba.drot[1] = -ba.drot[1];
//					ba.drot[2] = -ba.drot[2];
//				}
//			}
//		}
//	}
//
//	// convert fluids to modifier
//	if(main.versionfile < 246 || (main.versionfile == 246 && main.subversionfile < 1))
//	{
//		Object *ob;
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			if(ob.fluidsimSettings)
//			{
//				FluidsimModifierData *fluidmd = (FluidsimModifierData *)modifier_new(eModifierType_Fluidsim);
//				BLI_addhead(&ob.modifiers, (ModifierData *)fluidmd);
//
//				MEM_freeN(fluidmd.fss);
//				fluidmd.fss = MEM_dupallocN(ob.fluidsimSettings);
//				fluidmd.fss.ipo = newlibadr_us(fd, ob.id.lib, ob.fluidsimSettings.ipo);
//				MEM_freeN(ob.fluidsimSettings);
//
//				fluidmd.fss.lastgoodframe = INT_MAX;
//				fluidmd.fss.flag = 0;
//				fluidmd.fss.meshSurfNormals = 0;
//			}
//		}
//	}
//
//
//	if(main.versionfile < 246 || (main.versionfile == 246 && main.subversionfile < 1)) {
//		Mesh *me;
//
//		for(me=main.mesh.first; me; me= me.id.next)
//			alphasort_version_246(fd, lib, me);
//	}
//
//	if(main.versionfile < 246 || (main.versionfile == 246 && main.subversionfile < 1)){
//		Object *ob;
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			if(ob.pd && (ob.pd.forcefield == PFIELD_WIND))
//				ob.pd.f_noise = 0.0f;
//		}
//	}
//
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 2)){
//		Object *ob;
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			ob.gameflag |= OB_COLLISION;
//			ob.margin = 0.06f;
//		}
//	}
//
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 3)){
//		Object *ob;
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			// Starting from subversion 3, ACTOR is a separate feature.
//			// Before it was conditioning all the other dynamic flags
//			if (!(ob.gameflag & OB_ACTOR))
//				ob.gameflag &= ~(OB_GHOST|OB_DYNAMIC|OB_RIGID_BODY|OB_SOFT_BODY|OB_COLLISION_RESPONSE);
//			/* suitable default for older files */
//		}
//	}
//
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 4)){
//		Scene *sce= main.scene.first;
//		while(sce) {
//			if(sce.frame_step==0)
//				sce.frame_step= 1;
//			sce= sce.id.next;
//		}
//	}
//
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 5)) {
//		Lamp *la= main.lamp.first;
//		for(; la; la= la.id.next) {
//			la.skyblendtype= MA_RAMP_ADD;
//			la.skyblendfac= 1.0f;
//		}
//	}
//
//	/* set the curve radius interpolation to 2.47 default - easy */
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 6)) {
//		Curve *cu;
//		Nurb *nu;
//
//		for(cu= main.curve.first; cu; cu= cu.id.next) {
//			for(nu= cu.nurb.first; nu; nu= nu.next) {
//				if (nu) {
//					nu.radius_interp = 3;
//
//					/* resolu and resolv are now used differently for surfaces
//					 * rather then using the resolution to define the entire number of divisions,
//					 * use it for the number of divisions per segment
//					 */
//					if (nu.pntsv > 1) {
//						nu.resolu = MAX2( 1, (int)(((float)nu.resolu / (float)nu.pntsu)+0.5f) );
//						nu.resolv = MAX2( 1, (int)(((float)nu.resolv / (float)nu.pntsv)+0.5f) );
//					}
//				}
//			}
//		}
//	}
//	/* direction constraint actuators were always local in previous version */
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 7)) {
//		bActuator *act;
//		Object *ob;
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			for(act= ob.actuators.first; act; act= act.next) {
//				if (act.type == ACT_CONSTRAINT) {
//					bConstraintActuator *coa = act.data;
//					if (coa.type == ACT_CONST_TYPE_DIST) {
//						coa.flag |= ACT_CONST_LOCAL;
//					}
//				}
//			}
//		}
//	}
//
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 9)) {
//		Lamp *la= main.lamp.first;
//		for(; la; la= la.id.next) {
//			la.sky_exposure= 1.0f;
//		}
//	}
//
//	/* BGE message actuators needed OB prefix, very confusing */
//	if (main.versionfile < 247 || (main.versionfile == 247 && main.subversionfile < 10)) {
//		bActuator *act;
//		Object *ob;
//
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			for(act= ob.actuators.first; act; act= act.next) {
//				if (act.type == ACT_MESSAGE) {
//					bMessageActuator *msgAct = (bMessageActuator *) act.data;
//					if (strlen(msgAct.toPropName) > 2) {
//						/* strip first 2 chars, would have only worked if these were OB anyway */
//						memmove( msgAct.toPropName, msgAct.toPropName+2, sizeof(msgAct.toPropName)-2 );
//					} else {
//						msgAct.toPropName[0] = '\0';
//					}
//				}
//			}
//		}
//	}
//
//	if (main.versionfile < 248) {
//		Lamp *la;
//
//		for(la=main.lamp.first; la; la= la.id.next) {
//			if(la.atm_turbidity == 0.0) {
//				la.sun_effect_type = 0;
//				la.horizon_brightness = 1.0f;
//				la.spread = 1.0f;
//				la.sun_brightness = 1.0f;
//				la.sun_size = 1.0f;
//				la.backscattered_light = 1.0f;
//				la.atm_turbidity = 2.0f;
//				la.atm_inscattering_factor = 1.0f;
//				la.atm_extinction_factor = 1.0f;
//				la.atm_distance_factor = 1.0f;
//				la.sun_intensity = 1.0f;
//			}
//		}
//	}
//
//	if (main.versionfile < 248 || (main.versionfile == 248 && main.subversionfile < 2)) {
//		Scene *sce;
//
//		/* Note, these will need to be added for painting */
//		for (sce= main.scene.first; sce; sce= sce.id.next) {
//			sce.toolsettings.imapaint.seam_bleed = 2;
//			sce.toolsettings.imapaint.normal_angle = 80;
//
//			/* initialize skeleton generation toolsettings */
//			sce.toolsettings.skgen_resolution = 250;
//			sce.toolsettings.skgen_threshold_internal 	= 0.1f;
//			sce.toolsettings.skgen_threshold_external 	= 0.1f;
//			sce.toolsettings.skgen_angle_limit	 		= 30.0f;
//			sce.toolsettings.skgen_length_ratio			= 1.3f;
//			sce.toolsettings.skgen_length_limit			= 1.5f;
//			sce.toolsettings.skgen_correlation_limit		= 0.98f;
//			sce.toolsettings.skgen_symmetry_limit			= 0.1f;
//			sce.toolsettings.skgen_postpro = SKGEN_SMOOTH;
//			sce.toolsettings.skgen_postpro_passes = 3;
//			sce.toolsettings.skgen_options = SKGEN_FILTER_INTERNAL|SKGEN_FILTER_EXTERNAL|SKGEN_FILTER_SMART|SKGEN_SUB_CORRELATION|SKGEN_HARMONIC;
//			sce.toolsettings.skgen_subdivisions[0] = SKGEN_SUB_CORRELATION;
//			sce.toolsettings.skgen_subdivisions[1] = SKGEN_SUB_LENGTH;
//			sce.toolsettings.skgen_subdivisions[2] = SKGEN_SUB_ANGLE;
//
//
//			sce.toolsettings.skgen_retarget_angle_weight = 1.0f;
//			sce.toolsettings.skgen_retarget_length_weight = 1.0f;
//			sce.toolsettings.skgen_retarget_distance_weight = 1.0f;
//
//			/* Skeleton Sketching */
//			sce.toolsettings.bone_sketching = 0;
//			sce.toolsettings.skgen_retarget_roll = SK_RETARGET_ROLL_VIEW;
//		}
//	}
//	if (main.versionfile < 248 || (main.versionfile == 248 && main.subversionfile < 3)) {
//		bScreen *sc;
//
//		/* adjust default settings for Animation Editors */
//		for (sc= main.screen.first; sc; sc= sc.id.next) {
//			ScrArea *sa;
//
//			for (sa= sc.areabase.first; sa; sa= sa.next) {
//				SpaceLink *sl;
//
//				for (sl= sa.spacedata.first; sl; sl= sl.next) {
//					switch (sl.spacetype) {
//						case SPACE_ACTION:
//						{
//							SpaceAction *sact= (SpaceAction *)sl;
//
//							sact.mode= SACTCONT_DOPESHEET;
//							sact.autosnap= SACTSNAP_FRAME;
//						}
//							break;
//						case SPACE_IPO:
//						{
//							SpaceIpo *sipo= (SpaceIpo *)sl;
//							sipo.autosnap= SACTSNAP_FRAME;
//						}
//							break;
//						case SPACE_NLA:
//						{
//							SpaceNla *snla= (SpaceNla *)sl;
//							snla.autosnap= SACTSNAP_FRAME;
//						}
//							break;
//					}
//				}
//			}
//		}
//	}
//
//	if (main.versionfile < 248 || (main.versionfile == 248 && main.subversionfile < 3)) {
//		Object *ob;
//
//		/* Adjustments needed after Bullets update */
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			ob.damping *= 0.635f;
//			ob.rdamping = 0.1 + (0.8f * ob.rdamping);
//		}
//	}
//
//	if (main.versionfile < 248 || (main.versionfile == 248 && main.subversionfile < 4)) {
//		Scene *sce;
//		World *wrld;
//
//		/*  Dome (Fisheye) default parameters  */
//		for (sce= main.scene.first; sce; sce= sce.id.next) {
//			sce.r.domeangle = 180;
//			sce.r.domemode = 1;
//			sce.r.domeres = 4;
//			sce.r.domeresbuf = 1.0f;
//			sce.r.dometilt = 0;
//		}
//		/* DBVT culling by default */
//		for(wrld=main.world.first; wrld; wrld= wrld.id.next) {
//			wrld.mode |= WO_DBVT_CULLING;
//			wrld.occlusionRes = 128;
//		}
//	}
//
//	if (main.versionfile < 248 || (main.versionfile == 248 && main.subversionfile < 5)) {
//		Object *ob;
//		World *wrld;
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			ob.m_contactProcessingThreshold = 1.; //pad3 is used for m_contactProcessingThreshold
//			if(ob.parent) {
//				/* check if top parent has compound shape set and if yes, set this object
//				   to compound shaper as well (was the behaviour before, now it's optional) */
//				Object *parent= newlibadr(fd, lib, ob.parent);
//				while (parent && parent.parent != NULL) {
//					parent = newlibadr(fd, lib, parent.parent);
//				}
//				if(parent) {
//					if (parent.gameflag & OB_CHILD)
//						ob.gameflag |= OB_CHILD;
//				}
//			}
//		}
//		for(wrld=main.world.first; wrld; wrld= wrld.id.next) {
//			wrld.ticrate = 60;
//			wrld.maxlogicstep = 5;
//			wrld.physubstep = 1;
//			wrld.maxphystep = 5;
//		}
//	}
//
//	if (main.versionfile < 249) {
//		Scene *sce;
//		for (sce= main.scene.first; sce; sce= sce.id.next)
//			sce.r.renderer= 0;
//
//	}
//
//	// correct introduce of seed for wind force
//	if (main.versionfile < 249 && main.subversionfile < 1) {
//		Object *ob;
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//			if(ob.pd)
//				ob.pd.seed = ((unsigned int)(ceil(PIL_check_seconds_timer()))+1) % 128;
//		}
//
//	}
//
//	if (main.versionfile < 249 && main.subversionfile < 2) {
//		Scene *sce= main.scene.first;
//		Sequence *seq;
//		Editing *ed;
//
//		while(sce) {
//			ed= sce.ed;
//			if(ed) {
//				SEQP_BEGIN(ed, seq) {
//					if (seq.strip && seq.strip.proxy){
//						if (sce.r.size != 100.0) {
//							seq.strip.proxy.size
//								= sce.r.size;
//						} else {
//							seq.strip.proxy.size
//								= 25.0;
//						}
//						seq.strip.proxy.quality =90;
//					}
//				}
//				SEQ_END
//			}
//
//			sce= sce.id.next;
//		}
//
//	}
//
//	if (main.versionfile < 250) {
//		bScreen *screen;
//		Scene *scene;
//		Base *base;
//		Material *ma;
//		Camera *cam;
//		Mesh *me;
//		Scene *sce;
//		Tex *tx;
//		ParticleSettings *part;
//		Object *ob;
//		PTCacheID *pid;
//		ListBase pidlist;
//
//		for(screen= main.screen.first; screen; screen= screen.id.next) {
//			do_versions_windowmanager_2_50(screen);
//			do_versions_gpencil_2_50(main, screen);
//		}
//
//		/* old Animation System (using IPO's) needs to be converted to the new Animato system
//		 * (NOTE: conversion code in blenkernel/intern/ipo.c for now)
//		 */
//		//do_versions_ipos_to_animato(main);
//
//		/* toolsettings */
//		for(scene= main.scene.first; scene; scene= scene.id.next)
//			scene.r.audio = scene.audio;
//
//		/* shader, composit and texture node trees have id.name empty, put something in
//		 * to have them show in RNA viewer and accessible otherwise.
//		 */
//		for(ma= main.mat.first; ma; ma= ma.id.next) {
//			if(ma.nodetree && strlen(ma.nodetree.id.name)==0)
//				strcpy(ma.nodetree.id.name, "NTShader Nodetree");
//		}
//		/* and composit trees */
//		for(sce= main.scene.first; sce; sce= sce.id.next) {
//			if(sce.nodetree && strlen(sce.nodetree.id.name)==0)
//				strcpy(sce.nodetree.id.name, "NTComposit Nodetree");
//
//			/* move to cameras */
//			if(sce.r.scemode & R_PANORAMA) {
//				for(base=scene.base.first; base; base=base.next) {
//					ob= newlibadr(fd, lib, base.object);
//
//					if(ob.type == OB_CAMERA && !ob.id.lib) {
//						cam= newlibadr(fd, lib, ob.data);
//						cam.flag |= CAM_PANORAMA;
//					}
//				}
//
//				sce.r.scemode &= ~R_PANORAMA;
//			}
//		}
//		/* and texture trees */
//		for(tx= main.tex.first; tx; tx= tx.id.next) {
//			if(tx.nodetree && strlen(tx.nodetree.id.name)==0)
//				strcpy(tx.nodetree.id.name, "NTTexture Nodetree");
//		}
//
//		/* copy standard draw flag to meshes(used to be global, is not available here) */
//		for(me= main.mesh.first; me; me= me.id.next) {
//			me.drawflag= ME_DRAWEDGES|ME_DRAWFACES|ME_DRAWCREASES;
//		}
//
//		/* particle draw and render types */
//		for(part= main.particle.first; part; part= part.id.next) {
//			if(part.draw_as) {
//				if(part.draw_as == PART_DRAW_DOT) {
//					part.ren_as = PART_DRAW_HALO;
//					part.draw_as = PART_DRAW_REND;
//				}
//				else if(part.draw_as <= PART_DRAW_AXIS) {
//					part.ren_as = PART_DRAW_HALO;
//				}
//				else {
//					part.ren_as = part.draw_as;
//					part.draw_as = PART_DRAW_REND;
//				}
//			}
//			part.path_end = 1.0f;
//			part.clength = 1.0f;
//		}
//		/* set old pointcaches to have disk cache flag */
//		for(ob = main.object.first; ob; ob= ob.id.next) {
//
//			BKE_ptcache_ids_from_object(&pidlist, ob);
//
//			for(pid=pidlist.first; pid; pid=pid.next)
//				pid.cache.flag |= PTCACHE_DISK_CACHE;
//
//			BLI_freelistN(&pidlist);
//		}
//	}
//
//	if (main.versionfile < 250 || (main.versionfile == 250 && main.subversionfile < 1)) {
//	}
//
//	/* TODO: should be moved into one of the version blocks once this branch moves to trunk and we can
//	   bump the version (or sub-version.) */
//	{
//		World *wo;
//		Object *ob;
//		Material *ma;
//		Tex *tex;
//		Scene *sce;
//		ToolSettings *ts;
//		int i, a;
//
//		for(ob = main.object.first; ob; ob = ob.id.next) {
//
//			if(ob.type == OB_MESH) {
//				Mesh *me = newlibadr(fd, lib, ob.data);
//				void *olddata = ob.data;
//				ob.data = me;
//
//				if(me && me.id.lib==NULL && me.mr) { /* XXX - library meshes crash on loading most yoFrankie levels, the multires pointer gets invalid -  Campbell */
//					MultiresLevel *lvl;
//					ModifierData *md;
//					MultiresModifierData *mmd;
//					DerivedMesh *dm, *orig;
//
//					/* Load original level into the mesh */
//					lvl = me.mr.levels.first;
//					CustomData_free_layers(&me.vdata, CD_MVERT, lvl.totvert);
//					CustomData_free_layers(&me.edata, CD_MEDGE, lvl.totedge);
//					CustomData_free_layers(&me.fdata, CD_MFACE, lvl.totface);
//					me.totvert = lvl.totvert;
//					me.totedge = lvl.totedge;
//					me.totface = lvl.totface;
//					me.mvert = CustomData_add_layer(&me.vdata, CD_MVERT, CD_CALLOC, NULL, me.totvert);
//					me.medge = CustomData_add_layer(&me.edata, CD_MEDGE, CD_CALLOC, NULL, me.totedge);
//					me.mface = CustomData_add_layer(&me.fdata, CD_MFACE, CD_CALLOC, NULL, me.totface);
//					memcpy(me.mvert, me.mr.verts, sizeof(MVert) * me.totvert);
//					for(i = 0; i < me.totedge; ++i) {
//						me.medge[i].v1 = lvl.edges[i].v[0];
//						me.medge[i].v2 = lvl.edges[i].v[1];
//					}
//					for(i = 0; i < me.totface; ++i) {
//						me.mface[i].v1 = lvl.faces[i].v[0];
//						me.mface[i].v2 = lvl.faces[i].v[1];
//						me.mface[i].v3 = lvl.faces[i].v[2];
//						me.mface[i].v4 = lvl.faces[i].v[3];
//					}
//
//					/* Add a multires modifier to the object */
//					md = ob.modifiers.first;
//					while(md && modifierType_getInfo(md.type).type == eModifierTypeType_OnlyDeform)
//						md = md.next;
//					mmd = (MultiresModifierData*)modifier_new(eModifierType_Multires);
//					BLI_insertlinkbefore(&ob.modifiers, md, mmd);
//
//					multiresModifier_subdivide(mmd, ob, me.mr.level_count - 1, 1, 0);
//
//					mmd.lvl = mmd.totlvl;
//					orig = CDDM_from_mesh(me, NULL);
//					dm = multires_dm_create_from_derived(mmd, orig, me, 0, 0);
//
//					multires_load_old(dm, me.mr);
//
//					MultiresDM_mark_as_modified(dm);
//					dm.release(dm);
//					orig.release(orig);
//
//					/* Remove the old multires */
//					multires_free(me.mr);
//					me.mr = NULL;
//				}
//
//				ob.data = olddata;
//			}
//
//			if(ob.totcol && ob.matbits == NULL) {
//				int a;
//
//				ob.matbits= MEM_callocN(sizeof(char)*ob.totcol, "ob.matbits");
//				for(a=0; a<ob.totcol; a++)
//					ob.matbits[a]= ob.colbits & (1<<a);
//			}
//		}
//
//		/* texture filter */
//		for(tex = main.tex.first; tex; tex = tex.id.next) {
//			if(tex.afmax == 0)
//				tex.afmax= 8;
//		}
//
//		for(ma = main.mat.first; ma; ma = ma.id.next) {
//			if(ma.mode & MA_WIRE) {
//				ma.material_type= MA_TYPE_WIRE;
//				ma.mode &= ~MA_WIRE;
//			}
//			if(ma.mode & MA_HALO) {
//				ma.material_type= MA_TYPE_HALO;
//				ma.mode &= ~MA_HALO;
//			}
//
//			/* set new bump for unused slots */
//			for(a=0; a<MAX_MTEX; a++) {
//				if(ma.mtex[a]) {
//					if(!ma.mtex[a].tex)
//						ma.mtex[a].texflag |= MTEX_NEW_BUMP;
//					else if(((Tex*)newlibadr(fd, ma.id.lib, ma.mtex[a].tex)).type == 0)
//						ma.mtex[a].texflag |= MTEX_NEW_BUMP;
//				}
//			}
//		}
//
//		for(sce = main.scene.first; sce; sce = sce.id.next) {
//			ts= sce.toolsettings;
//			if(ts.normalsize == 0.0 || !ts.uv_selectmode || ts.vgroup_weight == 0.0) {
//				ts.normalsize= 0.1f;
//				ts.selectmode= SCE_SELECT_VERTEX;
//
//				/* autokeying - setting should be taken from the user-prefs
//				 * but the userprefs version may not have correct flags set
//				 * (i.e. will result in blank box when enabled)
//				 */
//				ts.autokey_mode= U.autokey_mode;
//				if (ts.autokey_mode == 0)
//					ts.autokey_mode= 2; /* 'add/replace' but not on */
//				ts.uv_selectmode= UV_SELECT_VERTEX;
//				ts.vgroup_weight= 1.0f;
//			}
//
//			/* Game Settings */
//			//Dome
//			sce.gm.dome.angle = sce.r.domeangle;
//			sce.gm.dome.mode = sce.r.domemode;
//			sce.gm.dome.res = sce.r.domeres;
//			sce.gm.dome.resbuf = sce.r.domeresbuf;
//			sce.gm.dome.tilt = sce.r.dometilt;
//			sce.gm.dome.warptext = sce.r.dometext;
//
//			//Stand Alone
//			sce.gm.fullscreen = sce.r.fullscreen;
//			sce.gm.xplay = sce.r.xplay;
//			sce.gm.yplay = sce.r.yplay;
//			sce.gm.freqplay = sce.r.freqplay;
//			sce.gm.depth = sce.r.depth;
//			sce.gm.attrib = sce.r.attrib;
//
//			//Stereo
//			sce.gm.xsch = sce.r.xsch;
//			sce.gm.ysch = sce.r.ysch;
//			sce.gm.stereomode = sce.r.stereomode;
//			/* reassigning stereomode NO_STEREO and DOME to a separeted flag*/
//			if (sce.gm.stereomode == 1){ //1 = STEREO_NOSTEREO
//				sce.gm.stereoflag = STEREO_NOSTEREO;
//				sce.gm.stereomode = STEREO_ANAGLYPH;
//			}
//			else if(sce.gm.stereomode == 8){ //8 = STEREO_DOME
//				sce.gm.stereoflag = STEREO_DOME;
//				sce.gm.stereomode = STEREO_ANAGLYPH;
//			}
//			else
//				sce.gm.stereoflag = STEREO_ENABLED;
//
//			//Framing
//			sce.gm.framing = sce.framing;
//			sce.gm.xplay = sce.r.xplay;
//			sce.gm.yplay = sce.r.yplay;
//			sce.gm.freqplay= sce.r.freqplay;
//			sce.gm.depth= sce.r.depth;
//
//			//Physic (previously stored in world)
//			//temporarily getting the correct world address
//			wo = newlibadr(fd, sce.id.lib, sce.world);
//			if (wo){
//				sce.gm.gravity = wo.gravity;
//				sce.gm.physicsEngine= wo.physicsEngine;
//				sce.gm.mode = wo.mode;
//				sce.gm.occlusionRes = wo.occlusionRes;
//				sce.gm.ticrate = wo.ticrate;
//				sce.gm.maxlogicstep = wo.maxlogicstep;
//				sce.gm.physubstep = wo.physubstep;
//				sce.gm.maxphystep = wo.maxphystep;
//			}
//			else{
//				sce.gm.gravity =9.8f;
//				sce.gm.physicsEngine= WOPHY_BULLET;// Bullet by default
//				sce.gm.mode = WO_DBVT_CULLING;	// DBVT culling by default
//				sce.gm.occlusionRes = 128;
//				sce.gm.ticrate = 60;
//				sce.gm.maxlogicstep = 5;
//				sce.gm.physubstep = 1;
//				sce.gm.maxphystep = 5;
//			}
//		}
//	}
//
//	/* WATCH IT!!!: pointers from libdata have not been converted yet here! */
//	/* WATCH IT 2!: Userdef struct init has to be in src/usiblender.c! */
//
//	/* don't forget to set version number in blender.c! */
//}

public static void lib_link_all(FileData fd, Main main)
{
//	oldnewmap_sort(fd);

	lib_link_windowmanager(fd, main);
	lib_link_screen(fd, main);
	lib_link_scene(fd, main);
	lib_link_object(fd, main);
//	lib_link_curve(fd, main);
//	lib_link_mball(fd, main);
//	lib_link_material(fd, main);
//	lib_link_texture(fd, main);
	lib_link_image(fd, main);
//	lib_link_ipo(fd, main);		// XXX depreceated... still needs to be maintained for version patches still
//	lib_link_key(fd, main);
	lib_link_world(fd, main);
	lib_link_lamp(fd, main);
//	lib_link_latt(fd, main);
//	lib_link_text(fd, main);
	lib_link_camera(fd, main);
//	lib_link_sound(fd, main);
	lib_link_group(fd, main);
//	lib_link_armature(fd, main);
//	lib_link_action(fd, main);
//	lib_link_vfont(fd, main);
//	lib_link_nodetree(fd, main);	/* has to be done after scene/materials, this will verify group nodes */
//	lib_link_brush(fd, main);
//	lib_link_particlesettings(fd, main);

	lib_link_mesh(fd, main);		/* as last: tpage images with users at zero */

	lib_link_library(fd, main);		/* only init users */
}


public static BHead read_userdef(BlendFileData bfd, FileData fd, BHead bhead)
{
	Link link;

	bfd.user= read_struct(fd, bhead, UserDef.class);
	bfd.user.themes.first= bfd.user.themes.last= null;
	// XXX
	bfd.user.uifonts.first= bfd.user.uifonts.last= null;
	bfd.user.uistyles.first= bfd.user.uistyles.last= null;

	bhead = blo_nextbhead(fd, bhead);

		/* read all attached data */
	while(bhead!=null && bhead.code==UtilDefines.DATA) {
		link= (Link)read_struct(fd, bhead, DNATools.getClassType(bhead.SDNAnr));
		ListBaseUtil.BLI_addtail(bfd.user.themes, link);
		bhead = blo_nextbhead(fd, bhead);
	}

	return bhead;
}

public static BlendFileData blo_read_file_internal(FileData fd)
{
        System.out.println("Starting read file internal ...");
	BHead bhead= blo_firstbhead(fd);
	BlendFileData bfd;

	bfd= new BlendFileData();
	bfd.main= new Main();
	ListBaseUtil.BLI_addtail(fd.mainlist, bfd.main);

	bfd.main.versionfile= (short)fd.fileversion;

	while(bhead!=null) {
		switch(bhead.code) {
		case UtilDefines.DATA:
		case UtilDefines.DNA1:
		case UtilDefines.TEST:
		case UtilDefines.REND:
			bhead = blo_nextbhead(fd, bhead);
			break;
		case UtilDefines.GLOB:
			bhead= read_global(bfd, fd, bhead);
			break;
		case UtilDefines.USER:
			bhead= read_userdef(bfd, fd, bhead);
			break;
		case UtilDefines.ENDB:
                        System.out.println("found block: ENDB");
			bhead = null;
			break;

		case DNA_ID.ID_LI:
			bhead = read_libblock(fd, bfd.main, bhead, DNA_ID.LIB_LOCAL, null);
			break;
		case DNA_ID.ID_ID:
				/* always adds to the most recently loaded
				 * ID_LI block, see direct_link_library.
				 * this is part of the file format definition.
				 */
			bhead = read_libblock(fd, fd.mainlist.last, bhead, DNA_ID.LIB_READ+DNA_ID.LIB_EXTERN, null);
			break;

			/* in 2.50+ files, the file identifier for screens is patched, forward compatibility */
		case (DNA_ID.ID_SCRN<<16):
			bhead.code= (DNA_ID.ID_SCR<<16);
			/* deliberate pass on to default */
		default:
			bhead = read_libblock(fd, bfd.main, bhead, DNA_ID.LIB_LOCAL, null);
		}
	}

	/* do before read_libraries, but skip undo case */
//	if(fd.memfile==NULL) (the mesh shuffle hacks don't work yet? ton)
//		do_versions(fd, NULL, bfd.main);

	read_libraries(fd, fd.mainlist);

	blo_join_main(fd.mainlist);

	lib_link_all(fd, bfd.main);
	lib_verify_nodetree(bfd.main, 1);
//	fix_relpaths_library(fd.filename, bfd.main); /* make all relative paths, relative to the open blend file */

	link_global(fd, bfd);	/* as last */

        System.out.println("Finished read file internal.");
	return bfd;
}

///* ************* APPEND LIBRARY ************** */
//
//struct bheadsort {
//	BHead *bhead;
//	void *old;
//};
//
//static int verg_bheadsort(const void *v1, const void *v2)
//{
//	const struct bheadsort *x1=v1, *x2=v2;
//
//	if( x1.old > x2.old) return 1;
//	else if( x1.old < x2.old) return -1;
//	return 0;
//}
//
//static void sort_bhead_old_map(FileData *fd)
//{
//	BHead *bhead;
//	struct bheadsort *bhs;
//	int tot= 0;
//
//	for (bhead= blo_firstbhead(fd); bhead; bhead= blo_nextbhead(fd, bhead))
//		tot++;
//
//	fd.tot_bheadmap= tot;
//	if(tot==0) return;
//
//	bhs= fd.bheadmap= MEM_mallocN(tot*sizeof(struct bheadsort), "bheadsort");
//
//	for (bhead= blo_firstbhead(fd); bhead; bhead= blo_nextbhead(fd, bhead), bhs++) {
//		bhs.bhead= bhead;
//		bhs.old= bhead.old;
//	}
//
//	qsort(fd.bheadmap, tot, sizeof(struct bheadsort), verg_bheadsort);
//
//}
//
//static BHead *find_previous_lib(FileData *fd, BHead *bhead)
//{
//	for (; bhead; bhead= blo_prevbhead(fd, bhead))
//		if (bhead.code==ID_LI)
//			break;
//
//	return bhead;
//}
//
//static BHead *find_bhead(FileData *fd, void *old)
//{
//#if 0
//	BHead *bhead;
//#endif
//	struct bheadsort *bhs, bhs_s;
//
//	if (!old)
//		return NULL;
//
//	if (fd.bheadmap==NULL)
//		sort_bhead_old_map(fd);
//
//	bhs_s.old= old;
//	bhs= bsearch(&bhs_s, fd.bheadmap, fd.tot_bheadmap, sizeof(struct bheadsort), verg_bheadsort);
//
//	if(bhs)
//		return bhs.bhead;
//
//#if 0
//	for (bhead= blo_firstbhead(fd); bhead; bhead= blo_nextbhead(fd, bhead))
//		if (bhead.old==old)
//			return bhead;
//#endif
//
//	return NULL;
//}

    public static byte[] bhead_id_name(FileData fd, BHead bhead) {
        return bhead.getName(fd.id_name_offs);
    }

//static ID *is_yet_read(FileData *fd, Main *mainvar, BHead *bhead)
//{
//	ListBase *lb;
//	char *idname= bhead_id_name(fd, bhead);
//
//	lb= wich_libbase(mainvar, GS(idname));
//
//	if(lb) {
//		ID *id= lb.first;
//		while(id) {
//			if( strcmp(id.name, idname)==0 )
//				return id;
//			id= id.next;
//		}
//	}
//	return NULL;
//}
//
//static void expand_doit(FileData *fd, Main *mainvar, void *old)
//{
//	BHead *bhead;
//	ID *id;
//
//	bhead= find_bhead(fd, old);
//	if(bhead) {
//			/* from another library? */
//		if(bhead.code==ID_ID) {
//			BHead *bheadlib= find_previous_lib(fd, bhead);
//
//			if(bheadlib) {
//				Library *lib= read_struct(fd, bheadlib, "Library");
//				Main *ptr= blo_find_main(fd, &fd.mainlist, lib.name, fd.filename);
//
//				id= is_yet_read(fd, ptr, bhead);
//
//				if(id==NULL) {
//					read_libblock(fd, ptr, bhead, LIB_READ+LIB_INDIRECT, NULL);
//					if(G.f & G_DEBUG) printf("expand_doit: other lib %s\n", lib.name);
//
//					/* for outliner dependency only */
//					ptr.curlib.parent= mainvar.curlib;
//				}
//				else {
//					/* The line below was commented by Ton (I assume), when Hos did the merge from the orange branch. rev 6568
//					 * This line is NEEDED, the case is that you have 3 blend files...
//					 * user.blend, lib.blend and lib_indirect.blend - if user.blend alredy references a "tree" from
//					 * lib_indirect.blend but lib.blend does too, linking in a Scene or Group from lib.blend can result in an
//					 * empty without the dupli group referenced. Once you save and reload the group would appier. - Campbell */
//					/* This crashes files, must look further into it */
//					/*oldnewmap_insert(fd.libmap, bhead.old, id, 1);*/
//
//					change_idid_adr_fd(fd, bhead.old, id);
//					if(G.f & G_DEBUG) printf("expand_doit: already linked: %s lib: %s\n", id.name, lib.name);
//				}
//
//				MEM_freeN(lib);
//			}
//		}
//		else {
//			id= is_yet_read(fd, mainvar, bhead);
//			if(id==NULL) {
//				read_libblock(fd, mainvar, bhead, LIB_TESTIND, NULL);
//			}
//			else {
//				/* this is actually only needed on UI call? when ID was already read before, and another append
//				   happens which invokes same ID... in that case the lookup table needs this entry */
//				oldnewmap_insert(fd.libmap, bhead.old, id, 1);
//				if(G.f & G_DEBUG) printf("expand: already read %s\n", id.name);
//			}
//		}
//	}
//}
//
//
//
//// XXX depreceated - old animation system
//static void expand_ipo(FileData *fd, Main *mainvar, Ipo *ipo)
//{
//	IpoCurve *icu;
//	for(icu= ipo.curve.first; icu; icu= icu.next) {
//		if(icu.driver)
//			expand_doit(fd, mainvar, icu.driver.ob);
//	}
//}
//
//// XXX depreceated - old animation system
//static void expand_constraint_channels(FileData *fd, Main *mainvar, ListBase *chanbase)
//{
//	bConstraintChannel *chan;
//	for (chan=chanbase.first; chan; chan=chan.next) {
//		expand_doit(fd, mainvar, chan.ipo);
//	}
//}
//
//// XXX depreceated - old animation system
//static void expand_action(FileData *fd, Main *mainvar, bAction *act)
//{
//	bActionChannel *chan;
//
//	for (chan=act.chanbase.first; chan; chan=chan.next) {
//		expand_doit(fd, mainvar, chan.ipo);
//		expand_constraint_channels(fd, mainvar, &chan.constraintChannels);
//	}
//}
//
//static void expand_keyingsets(FileData *fd, Main *mainvar, ListBase *list)
//{
//	KeyingSet *ks;
//	KS_Path *ksp;
//
//	/* expand the ID-pointers in KeyingSets's paths */
//	for (ks= list.first; ks; ks= ks.next) {
//		for (ksp= ks.paths.first; ksp; ksp= ksp.next) {
//			expand_doit(fd, mainvar, ksp.id);
//		}
//	}
//}
//
//static void expand_animdata_nlastrips(FileData *fd, Main *mainvar, ListBase *list)
//{
//	NlaStrip *strip;
//
//	for (strip= list.first; strip; strip= strip.next) {
//		/* check child strips */
//		expand_animdata_nlastrips(fd, mainvar, &strip.strips);
//
//		/* relink referenced action */
//		expand_doit(fd, mainvar, strip.act);
//	}
//}
//
//static void expand_animdata(FileData *fd, Main *mainvar, AnimData *adt)
//{
//	FCurve *fcd;
//	NlaTrack *nlt;
//
//	/* own action */
//	expand_doit(fd, mainvar, adt.action);
//	expand_doit(fd, mainvar, adt.tmpact);
//
//	/* drivers - assume that these F-Curves have driver data to be in this list... */
//	for (fcd= adt.drivers.first; fcd; fcd= fcd.next) {
//		ChannelDriver *driver= fcd.driver;
//		DriverTarget *dtar;
//
//		for (dtar= driver.targets.first; dtar; dtar= dtar.next)
//			expand_doit(fd, mainvar, dtar.id);
//	}
//
//	/* nla-data - referenced actions */
//	for (nlt= adt.nla_tracks.first; nlt; nlt= nlt.next)
//		expand_animdata_nlastrips(fd, mainvar, &nlt.strips);
//}
//
//static void expand_particlesettings(FileData *fd, Main *mainvar, ParticleSettings *part)
//{
//	expand_doit(fd, mainvar, part.dup_ob);
//	expand_doit(fd, mainvar, part.dup_group);
//	expand_doit(fd, mainvar, part.eff_group);
//	expand_doit(fd, mainvar, part.bb_ob);
//
//	if(part.adt)
//		expand_animdata(fd, mainvar, part.adt);
//}
//
//static void expand_group(FileData *fd, Main *mainvar, Group *group)
//{
//	GroupObject *go;
//
//	for(go= group.gobject.first; go; go= go.next) {
//		expand_doit(fd, mainvar, go.ob);
//	}
//}
//
//static void expand_key(FileData *fd, Main *mainvar, Key *key)
//{
//	expand_doit(fd, mainvar, key.ipo); // XXX depreceated - old animation system
//
//	if(key.adt)
//		expand_animdata(fd, mainvar, key.adt);
//}
//
//static void expand_nodetree(FileData *fd, Main *mainvar, bNodeTree *ntree)
//{
//	bNode *node;
//
//	if(ntree.adt)
//		expand_animdata(fd, mainvar, ntree.adt);
//
//	for(node= ntree.nodes.first; node; node= node.next)
//		if(node.id && node.type!=CMP_NODE_R_LAYERS)
//			expand_doit(fd, mainvar, node.id);
//
//}
//
//static void expand_texture(FileData *fd, Main *mainvar, Tex *tex)
//{
//	expand_doit(fd, mainvar, tex.ima);
//	expand_doit(fd, mainvar, tex.ipo); // XXX depreceated - old animation system
//
//	if(tex.adt)
//		expand_animdata(fd, mainvar, tex.adt);
//
//	if(tex.nodetree)
//		expand_nodetree(fd, mainvar, tex.nodetree);
//}
//
//static void expand_brush(FileData *fd, Main *mainvar, Brush *brush)
//{
//	int a;
//
//	for(a=0; a<MAX_MTEX; a++)
//		if(brush.mtex[a])
//			expand_doit(fd, mainvar, brush.mtex[a].tex);
//	expand_doit(fd, mainvar, brush.clone.image);
//}
//
//static void expand_material(FileData *fd, Main *mainvar, Material *ma)
//{
//	int a;
//
//	for(a=0; a<MAX_MTEX; a++) {
//		if(ma.mtex[a]) {
//			expand_doit(fd, mainvar, ma.mtex[a].tex);
//			expand_doit(fd, mainvar, ma.mtex[a].object);
//		}
//	}
//
//	expand_doit(fd, mainvar, ma.ipo); // XXX depreceated - old animation system
//
//	if(ma.adt)
//		expand_animdata(fd, mainvar, ma.adt);
//
//	if(ma.nodetree)
//		expand_nodetree(fd, mainvar, ma.nodetree);
//}
//
//static void expand_lamp(FileData *fd, Main *mainvar, Lamp *la)
//{
//	int a;
//
//	for(a=0; a<MAX_MTEX; a++) {
//		if(la.mtex[a]) {
//			expand_doit(fd, mainvar, la.mtex[a].tex);
//			expand_doit(fd, mainvar, la.mtex[a].object);
//		}
//	}
//
//	expand_doit(fd, mainvar, la.ipo); // XXX depreceated - old animation system
//
//	if (la.adt)
//		expand_animdata(fd, mainvar, la.adt);
//}
//
//static void expand_lattice(FileData *fd, Main *mainvar, Lattice *lt)
//{
//	expand_doit(fd, mainvar, lt.ipo); // XXX depreceated - old animation system
//	expand_doit(fd, mainvar, lt.key);
//}
//
//
//static void expand_world(FileData *fd, Main *mainvar, World *wrld)
//{
//	int a;
//
//	for(a=0; a<MAX_MTEX; a++) {
//		if(wrld.mtex[a]) {
//			expand_doit(fd, mainvar, wrld.mtex[a].tex);
//			expand_doit(fd, mainvar, wrld.mtex[a].object);
//		}
//	}
//
//	expand_doit(fd, mainvar, wrld.ipo); // XXX depreceated - old animation system
//
//	if (wrld.adt)
//		expand_animdata(fd, mainvar, wrld.adt);
//}
//
//
//static void expand_mball(FileData *fd, Main *mainvar, MetaBall *mb)
//{
//	int a;
//
//	for(a=0; a<mb.totcol; a++) {
//		expand_doit(fd, mainvar, mb.mat[a]);
//	}
//}
//
//static void expand_curve(FileData *fd, Main *mainvar, Curve *cu)
//{
//	int a;
//
//	for(a=0; a<cu.totcol; a++) {
//		expand_doit(fd, mainvar, cu.mat[a]);
//	}
//
//	expand_doit(fd, mainvar, cu.vfont);
//	expand_doit(fd, mainvar, cu.vfontb);
//	expand_doit(fd, mainvar, cu.vfonti);
//	expand_doit(fd, mainvar, cu.vfontbi);
//	expand_doit(fd, mainvar, cu.key);
//	expand_doit(fd, mainvar, cu.ipo); // XXX depreceated - old animation system
//	expand_doit(fd, mainvar, cu.bevobj);
//	expand_doit(fd, mainvar, cu.taperobj);
//	expand_doit(fd, mainvar, cu.textoncurve);
//
//	if(cu.adt)
//		expand_animdata(fd, mainvar, cu.adt);
//}
//
//static void expand_mesh(FileData *fd, Main *mainvar, Mesh *me)
//{
//	CustomDataLayer *layer;
//	MTFace *mtf;
//	TFace *tf;
//	int a, i;
//
//	for(a=0; a<me.totcol; a++) {
//		expand_doit(fd, mainvar, me.mat[a]);
//	}
//
//	expand_doit(fd, mainvar, me.key);
//	expand_doit(fd, mainvar, me.texcomesh);
//
//	if(me.tface) {
//		tf= me.tface;
//		for(i=0; i<me.totface; i++, tf++)
//			if(tf.tpage)
//				expand_doit(fd, mainvar, tf.tpage);
//	}
//
//	for(a=0; a<me.fdata.totlayer; a++) {
//		layer= &me.fdata.layers[a];
//
//		if(layer.type == CD_MTFACE) {
//			mtf= (MTFace*)layer.data;
//			for(i=0; i<me.totface; i++, mtf++)
//				if(mtf.tpage)
//					expand_doit(fd, mainvar, mtf.tpage);
//		}
//	}
//}
//
//static void expand_constraints(FileData *fd, Main *mainvar, ListBase *lb)
//{
//	bConstraint *curcon;
//
//	for (curcon=lb.first; curcon; curcon=curcon.next) {
//
//		if (curcon.ipo)
//			expand_doit(fd, mainvar, curcon.ipo); // XXX depreceated - old animation system
//
//		switch (curcon.type) {
//		case CONSTRAINT_TYPE_NULL:
//			break;
//		case CONSTRAINT_TYPE_PYTHON:
//			{
//				bPythonConstraint *data = (bPythonConstraint*)curcon.data;
//				bConstraintTarget *ct;
//
//				for (ct= data.targets.first; ct; ct= ct.next)
//					expand_doit(fd, mainvar, ct.tar);
//
//				expand_doit(fd, mainvar, data.text);
//			}
//			break;
//		case CONSTRAINT_TYPE_ACTION:
//			{
//				bActionConstraint *data = (bActionConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//				expand_doit(fd, mainvar, data.act);
//			}
//			break;
//		case CONSTRAINT_TYPE_LOCLIKE:
//			{
//				bLocateLikeConstraint *data = (bLocateLikeConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_ROTLIKE:
//			{
//				bRotateLikeConstraint *data = (bRotateLikeConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_SIZELIKE:
//			{
//				bSizeLikeConstraint *data = (bSizeLikeConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_KINEMATIC:
//			{
//				bKinematicConstraint *data = (bKinematicConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//				expand_doit(fd, mainvar, data.poletar);
//			}
//			break;
//		case CONSTRAINT_TYPE_TRACKTO:
//			{
//				bTrackToConstraint *data = (bTrackToConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_MINMAX:
//			{
//				bMinMaxConstraint *data = (bMinMaxConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_LOCKTRACK:
//			{
//				bLockTrackConstraint *data = (bLockTrackConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_FOLLOWPATH:
//			{
//				bFollowPathConstraint *data = (bFollowPathConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_STRETCHTO:
//			{
//				bStretchToConstraint *data = (bStretchToConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_RIGIDBODYJOINT:
//			{
//				bRigidBodyJointConstraint *data = (bRigidBodyJointConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_CLAMPTO:
//			{
//				bClampToConstraint *data = (bClampToConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_CHILDOF:
//			{
//				bChildOfConstraint *data = (bChildOfConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_TRANSFORM:
//			{
//				bTransformConstraint *data = (bTransformConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_DISTLIMIT:
//			{
//				bDistLimitConstraint *data = (bDistLimitConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.tar);
//			}
//			break;
//		case CONSTRAINT_TYPE_SHRINKWRAP:
//			{
//				bShrinkwrapConstraint *data = (bShrinkwrapConstraint*)curcon.data;
//				expand_doit(fd, mainvar, data.target);
//			}
//			break;
//		default:
//			break;
//		}
//	}
//}
//
//static void expand_bones(FileData *fd, Main *mainvar, Bone *bone)
//{
//	Bone *curBone;
//
//	for (curBone = bone.childbase.first; curBone; curBone=curBone.next) {
//		expand_bones(fd, mainvar, curBone);
//	}
//
//}
//
//static void expand_pose(FileData *fd, Main *mainvar, bPose *pose)
//{
//	bPoseChannel *chan;
//
//	if (!pose)
//		return;
//
//	for (chan = pose.chanbase.first; chan; chan=chan.next) {
//		expand_constraints(fd, mainvar, &chan.constraints);
//		expand_doit(fd, mainvar, chan.custom);
//	}
//}
//
//static void expand_armature(FileData *fd, Main *mainvar, bArmature *arm)
//{
//	Bone *curBone;
//
//	for (curBone = arm.bonebase.first; curBone; curBone=curBone.next) {
//		expand_bones(fd, mainvar, curBone);
//	}
//}
//
//static void expand_modifier(FileData *fd, Main *mainvar, ModifierData *md)
//{
//	if (md.type==eModifierType_Lattice) {
//		LatticeModifierData *lmd = (LatticeModifierData*) md;
//
//		expand_doit(fd, mainvar, lmd.object);
//	}
//	else if (md.type==eModifierType_Curve) {
//		CurveModifierData *cmd = (CurveModifierData*) md;
//
//		expand_doit(fd, mainvar, cmd.object);
//	}
//	else if (md.type==eModifierType_Array) {
//		ArrayModifierData *amd = (ArrayModifierData*) md;
//
//		expand_doit(fd, mainvar, amd.curve_ob);
//		expand_doit(fd, mainvar, amd.offset_ob);
//	}
//	else if (md.type==eModifierType_Mirror) {
//		MirrorModifierData *mmd = (MirrorModifierData*) md;
//
//		expand_doit(fd, mainvar, mmd.mirror_ob);
//	}
//	else if (md.type==eModifierType_Displace) {
//		DisplaceModifierData *dmd = (DisplaceModifierData*) md;
//
//		expand_doit(fd, mainvar, dmd.map_object);
//		expand_doit(fd, mainvar, dmd.texture);
//	}
//}
//
//static void expand_object(FileData *fd, Main *mainvar, Object *ob)
//{
//	ModifierData *md;
//	ParticleSystem *psys;
//	bSensor *sens;
//	bController *cont;
//	bActuator *act;
//	bActionStrip *strip;
//	PartEff *paf;
//	int a;
//
//
//	expand_doit(fd, mainvar, ob.data);
//
//	for (md=ob.modifiers.first; md; md=md.next) {
//		expand_modifier(fd, mainvar, md);
//	}
//
//	expand_pose(fd, mainvar, ob.pose);
//	expand_doit(fd, mainvar, ob.poselib);
//	expand_constraints(fd, mainvar, &ob.constraints);
//
//// XXX depreceated - old animation system (for version patching only)
//	expand_doit(fd, mainvar, ob.ipo);
//	expand_doit(fd, mainvar, ob.action);
//
//	expand_constraint_channels(fd, mainvar, &ob.constraintChannels);
//
//	for (strip=ob.nlastrips.first; strip; strip=strip.next){
//		expand_doit(fd, mainvar, strip.object);
//		expand_doit(fd, mainvar, strip.act);
//		expand_doit(fd, mainvar, strip.ipo);
//	}
//// XXX depreceated - old animation system (for version patching only)
//
//	if(ob.adt)
//		expand_animdata(fd, mainvar, ob.adt);
//
//	for(a=0; a<ob.totcol; a++) {
//		expand_doit(fd, mainvar, ob.mat[a]);
//	}
//
//	paf = give_parteff(ob);
//	if (paf && paf.group)
//		expand_doit(fd, mainvar, paf.group);
//
//	if(ob.dup_group)
//		expand_doit(fd, mainvar, ob.dup_group);
//
//	if(ob.proxy)
//		expand_doit(fd, mainvar, ob.proxy);
//	if(ob.proxy_group)
//		expand_doit(fd, mainvar, ob.proxy_group);
//
//	for(psys=ob.particlesystem.first; psys; psys=psys.next)
//		expand_doit(fd, mainvar, psys.part);
//
//	sens= ob.sensors.first;
//	while(sens) {
//		if(sens.type==SENS_TOUCH) {
//			bTouchSensor *ts= sens.data;
//			expand_doit(fd, mainvar, ts.ma);
//		}
//		else if(sens.type==SENS_MESSAGE) {
//			bMessageSensor *ms= sens.data;
//			expand_doit(fd, mainvar, ms.fromObject);
//		}
//		sens= sens.next;
//	}
//
//	cont= ob.controllers.first;
//	while(cont) {
//		if(cont.type==CONT_PYTHON) {
//			bPythonCont *pc= cont.data;
//			expand_doit(fd, mainvar, pc.text);
//		}
//		cont= cont.next;
//	}
//
//	act= ob.actuators.first;
//	while(act) {
//		if(act.type==ACT_SOUND) {
//			bSoundActuator *sa= act.data;
//			expand_doit(fd, mainvar, sa.sound);
//		}
//		else if(act.type==ACT_CAMERA) {
//			bCameraActuator *ca= act.data;
//			expand_doit(fd, mainvar, ca.ob);
//		}
//		else if(act.type==ACT_EDIT_OBJECT) {
//			bEditObjectActuator *eoa= act.data;
//			if(eoa) {
//				expand_doit(fd, mainvar, eoa.ob);
//				expand_doit(fd, mainvar, eoa.me);
//			}
//		}
//		else if(act.type==ACT_OBJECT) {
//			bObjectActuator *oa= act.data;
//			expand_doit(fd, mainvar, oa.reference);
//		}
//		else if(act.type==ACT_SCENE) {
//			bSceneActuator *sa= act.data;
//			expand_doit(fd, mainvar, sa.camera);
//			expand_doit(fd, mainvar, sa.scene);
//		}
//		else if(act.type==ACT_ACTION) {
//			bActionActuator *aa= act.data;
//			expand_doit(fd, mainvar, aa.act);
//		}
//		else if(act.type==ACT_SHAPEACTION) {
//			bActionActuator *aa= act.data;
//			expand_doit(fd, mainvar, aa.act);
//		}
//		else if(act.type==ACT_PROPERTY) {
//			bPropertyActuator *pa= act.data;
//			expand_doit(fd, mainvar, pa.ob);
//		}
//		else if(act.type==ACT_MESSAGE) {
//			bMessageActuator *ma= act.data;
//			expand_doit(fd, mainvar, ma.toObject);
//		}
//		act= act.next;
//	}
//
//	if(ob.pd && ob.pd.tex)
//		expand_doit(fd, mainvar, ob.pd.tex);
//
//}
//
//static void expand_scene(FileData *fd, Main *mainvar, Scene *sce)
//{
//	Base *base;
//	SceneRenderLayer *srl;
//
//	for(base= sce.base.first; base; base= base.next) {
//		expand_doit(fd, mainvar, base.object);
//	}
//	expand_doit(fd, mainvar, sce.camera);
//	expand_doit(fd, mainvar, sce.world);
//
//	if(sce.adt)
//		expand_animdata(fd, mainvar, sce.adt);
//	expand_keyingsets(fd, mainvar, &sce.keyingsets);
//
//	if(sce.set)
//		expand_doit(fd, mainvar, sce.set);
//
//	if(sce.nodetree)
//		expand_nodetree(fd, mainvar, sce.nodetree);
//
//	for(srl= sce.r.layers.first; srl; srl= srl.next) {
//		expand_doit(fd, mainvar, srl.mat_override);
//		expand_doit(fd, mainvar, srl.light_override);
//	}
//
//	if(sce.r.dometext)
//		expand_doit(fd, mainvar, sce.gm.dome.warptext);
//}
//
//static void expand_camera(FileData *fd, Main *mainvar, Camera *ca)
//{
//	expand_doit(fd, mainvar, ca.ipo); // XXX depreceated - old animation system
//
//	if(ca.adt)
//		expand_animdata(fd, mainvar, ca.adt);
//}
//
//static void expand_sound(FileData *fd, Main *mainvar, bSound *snd)
//{
//	expand_doit(fd, mainvar, snd.ipo); // XXX depreceated - old animation system
//}


public static void expand_main(FileData fd, Main mainvar)
{
//	ListBase *lbarray[MAX_LIBARRAY];
//	ID *id;
//	int a, doit= 1;
//
//	if(fd==0) return;
//
//	while(doit) {
//		doit= 0;
//
//		a= set_listbasepointers(mainvar, lbarray);
//		while(a--) {
//			id= lbarray[a].first;
//
//			while(id) {
//				if(id.flag & LIB_TEST) {
//
//					switch(GS(id.name)) {
//
//					case ID_OB:
//						expand_object(fd, mainvar, (Object *)id);
//						break;
//					case ID_ME:
//						expand_mesh(fd, mainvar, (Mesh *)id);
//						break;
//					case ID_CU:
//						expand_curve(fd, mainvar, (Curve *)id);
//						break;
//					case ID_MB:
//						expand_mball(fd, mainvar, (MetaBall *)id);
//						break;
//					case ID_SCE:
//						expand_scene(fd, mainvar, (Scene *)id);
//						break;
//					case ID_MA:
//						expand_material(fd, mainvar, (Material *)id);
//						break;
//					case ID_TE:
//						expand_texture(fd, mainvar, (Tex *)id);
//						break;
//					case ID_WO:
//						expand_world(fd, mainvar, (World *)id);
//						break;
//					case ID_LT:
//						expand_lattice(fd, mainvar, (Lattice *)id);
//						break;
//					case ID_LA:
//						expand_lamp(fd, mainvar,(Lamp *)id);
//						break;
//					case ID_KE:
//						expand_key(fd, mainvar, (Key *)id);
//						break;
//					case ID_CA:
//						expand_camera(fd, mainvar, (Camera *)id);
//						break;
//					case ID_SO:
//						expand_sound(fd, mainvar, (bSound *)id);
//						break;
//					case ID_AR:
//						expand_armature(fd, mainvar, (bArmature *)id);
//						break;
//					case ID_AC:
//						expand_action(fd, mainvar, (bAction *)id); // XXX depreceated - old animation system
//						break;
//					case ID_GR:
//						expand_group(fd, mainvar, (Group *)id);
//						break;
//					case ID_NT:
//						expand_nodetree(fd, mainvar, (bNodeTree *)id);
//						break;
//					case ID_BR:
//						expand_brush(fd, mainvar, (Brush *)id);
//						break;
//					case ID_IP:
//						expand_ipo(fd, mainvar, (Ipo *)id); // XXX depreceated - old animation system
//						break;
//					case ID_PA:
//						expand_particlesettings(fd, mainvar, (ParticleSettings *)id);
//					}
//
//					doit= 1;
//					id.flag -= LIB_TEST;
//
//				}
//				id= id.next;
//			}
//		}
//	}
}

//static int object_in_any_scene(Main *mainvar, Object *ob)
//{
//	Scene *sce;
//
//	for(sce= mainvar.scene.first; sce; sce= sce.id.next)
//		if(object_in_scene(ob, sce))
//			return 1;
//	return 0;
//}
//
///* when *lib set, it also does objects that were in the appended group */
//static void give_base_to_objects(Main *mainvar, Scene *sce, Library *lib, int is_group_append)
//{
//	Object *ob;
//	Base *base;
//
//	/* give all objects which are LIB_INDIRECT a base, or for a group when *lib has been set */
//	for(ob= mainvar.object.first; ob; ob= ob.id.next) {
//
//		if( ob.id.flag & LIB_INDIRECT ) {
//
//				/* IF below is quite confusing!
//				if we are appending, but this object wasnt just added allong with a group,
//				then this is alredy used indirectly in the scene somewhere else and we didnt just append it.
//
//				(ob.id.flag & LIB_APPEND_TAG)==0 means that this is a newly appended object - Campbell */
//			if (is_group_append==0 || (ob.id.flag & LIB_APPEND_TAG)==0) {
//
//				int do_it= 0;
//
//				if(ob.id.us==0)
//					do_it= 1;
//				else if(ob.id.us==1 && lib)
//					if(ob.id.lib==lib && (ob.flag & OB_FROMGROUP) && object_in_any_scene(mainvar, ob)==0)
//						do_it= 1;
//
//				if(do_it) {
//					base= MEM_callocN( sizeof(Base), "add_ext_base");
//					BLI_addtail(&(sce.base), base);
//					base.lay= ob.lay;
//					base.object= ob;
//					base.flag= ob.flag;
//					ob.id.us= 1;
//
//					ob.id.flag -= LIB_INDIRECT;
//					ob.id.flag |= LIB_EXTERN;
//				}
//			}
//		}
//	}
//}
//
//
//static void append_named_part(FileData *fd, Main *mainvar, Scene *scene, char *name, int idcode, short flag)
//{
//	Object *ob;
//	Base *base;
//	BHead *bhead;
//	ID *id;
//	int endloop=0;
//
//	bhead = blo_firstbhead(fd);
//	while(bhead && endloop==0) {
//
//		if(bhead.code==ENDB) endloop= 1;
//		else if(bhead.code==idcode) {
//			char *idname= bhead_id_name(fd, bhead);
//
//			if(strcmp(idname+2, name)==0) {
//
//				id= is_yet_read(fd, mainvar, bhead);
//				if(id==NULL) {
//					read_libblock(fd, mainvar, bhead, LIB_TESTEXT, NULL);
//				}
//				else {
//					printf("append: already linked\n");
//					oldnewmap_insert(fd.libmap, bhead.old, id, 1);
//					if(id.flag & LIB_INDIRECT) {
//						id.flag -= LIB_INDIRECT;
//						id.flag |= LIB_EXTERN;
//					}
//				}
//
//				if(idcode==ID_OB) {	/* loose object: give a base */
//					base= MEM_callocN( sizeof(Base), "app_nam_part");
//					BLI_addtail(&scene.base, base);
//
//					if(id==NULL) ob= mainvar.object.last;
//					else ob= (Object *)id;
//
//					/* XXX use context to find view3d.lay */
//					//if((flag & FILE_ACTIVELAY)) {
//					//	scene.lay;
//					//}
//					base.lay= ob.lay;
//					base.object= ob;
//					ob.id.us++;
//
//					if(flag & FILE_AUTOSELECT) {
//						base.flag |= SELECT;
//						base.object.flag = base.flag;
//						/* do NOT make base active here! screws up GUI stuff, if you want it do it on src/ level */
//					}
//				}
//				endloop= 1;
//			}
//		}
//
//		bhead = blo_nextbhead(fd, bhead);
//	}
//}

    public static void append_id_part(FileData fd, Main mainvar, ID id, ID[] id_r) {
        for (BHead bhead = blo_firstbhead(fd); bhead != null; bhead = blo_nextbhead(fd, bhead)) {
            if (bhead.code == LibraryUtil.GS(id.name)) {
                if (StringUtil.BLI_streq(id.name, 0, bhead_id_name(fd, bhead), 0)) {
                    id.flag &= ~DNA_ID.LIB_READ;
                    id.flag |= DNA_ID.LIB_TEST;
                    read_libblock(fd, mainvar, bhead, id.flag, id_r);
                    break;
                }
            } else if (bhead.code == UtilDefines.ENDB) {
                break;
            }
        }
    }

///* common routine to append/link something from a library */
//
//static Library* library_append(Main *mainvar, Scene *scene, char* file, char *dir, int idcode,
//		int totsel, FileData **fd, struct direntry* filelist, int totfile, short flag)
//{
//	Main *mainl;
//	Library *curlib;
//
//	/* make mains */
//	blo_split_main(&(*fd).mainlist, mainvar);
//
//	/* which one do we need? */
//	mainl = blo_find_main(*fd, &(*fd).mainlist, dir, G.sce);
//
//	mainl.versionfile= (*fd).fileversion;	/* needed for do_version */
//
//	curlib= mainl.curlib;
//
//	if(totsel==0) {
//		append_named_part(*fd, mainl, scene, file, idcode, flag);
//	}
//	else {
//		int a;
//		for(a=0; a<totfile; a++) {
//			if(filelist[a].flags & ACTIVE) {
//				append_named_part(*fd, mainl, scene, filelist[a].relname, idcode, flag);
//			}
//		}
//	}
//
//	/* make main consistant */
//	expand_main(*fd, mainl);
//
//	/* do this when expand found other libs */
//	read_libraries(*fd, &(*fd).mainlist);
//
//	if(flag & FILE_STRINGCODE) {
//
//		/* use the full path, this could have been read by other library even */
//		BLI_strncpy(mainl.curlib.name, mainl.curlib.filename, sizeof(mainl.curlib.name));
//
//		/* uses current .blend file as reference */
//		BLI_makestringcode(G.sce, mainl.curlib.name);
//	}
//
//	blo_join_main(&(*fd).mainlist);
//	mainvar= (*fd).mainlist.first;
//
//	lib_link_all(*fd, mainvar);
//	lib_verify_nodetree(mainvar, 0);
//	fix_relpaths_library(G.sce, mainvar); /* make all relative paths, relative to the open blend file */
//
//	/* give a base to loose objects. If group append, do it for objects too */
//	if(idcode==ID_GR) {
//		if (flag & FILE_LINK) {
//			give_base_to_objects(mainvar, scene, NULL, 0);
//		} else {
//			give_base_to_objects(mainvar, scene, curlib, 1);
//		}
//	} else {
//		give_base_to_objects(mainvar, scene, NULL, 0);
//	}
//	/* has been removed... erm, why? s..ton) */
//	/* 20040907: looks like they are give base already in append_named_part(); -Nathan L */
//	/* 20041208: put back. It only linked direct, not indirect objects (ton) */
//
//	/* patch to prevent switch_endian happens twice */
//	if((*fd).flags & FD_FLAGS_SWITCH_ENDIAN) {
//		blo_freefiledata( *fd );
//		*fd = NULL;
//	}
//
//	return curlib;
//}
//
///* this is a version of BLO_library_append needed by the BPython API, so
// * scripts can load data from .blend files -- see Blender.Library module.*/
///* append to scene */
///* this should probably be moved into the Python code anyway */
//
//void BLO_script_library_append(BlendHandle **bh, char *dir, char *name,
//		int idcode, short flag, Main *mainvar, Scene *scene, ReportList *reports)
//{
//	FileData *fd= (FileData*)(*bh);
//
//	/* try to append the requested object */
//	fd.reports= reports;
//	library_append(mainvar, scene, name, dir, idcode, 0, &fd, NULL, 0, flag );
//	if(fd) fd.reports= NULL;
//
//	/* do we need to do this? */
//	DAG_scene_sort(scene);
//
//	*bh= (BlendHandle*)fd;
//}
//
///* append to scene */
//void BLO_library_append(BlendHandle** bh, struct direntry* filelist, int totfile,
//						 char *dir, char* file, short flag, int idcode, Main *mainvar, Scene *scene, ReportList *reports)
//{
//	FileData *fd= (FileData*)(*bh);
//	Library *curlib;
//	Base *centerbase;
//	Object *ob;
//	int a, totsel=0;
//
//	/* are there files selected? */
//	for(a=0; a<totfile; a++) {
//		if(filelist[a].flags & ACTIVE) {
//			totsel++;
//		}
//	}
//
//	if(totsel==0) {
//		/* is the indicated file in the filelist? */
//		if(file[0]) {
//			for(a=0; a<totfile; a++) {
//				if( strcmp(filelist[a].relname, file)==0) break;
//			}
//			if(a==totfile) {
//				BKE_report(reports, RPT_ERROR, "Wrong indicated name");
//				return;
//			}
//		}
//		else {
//			BKE_report(reports, RPT_ERROR, "Nothing indicated");
//			return;
//		}
//	}
//	/* now we have or selected, or an indicated file */
//
//	if(flag & FILE_AUTOSELECT) scene_deselect_all(scene);
//
//	fd.reports= reports;
//	curlib = library_append(mainvar, scene, file, dir, idcode, totsel, &fd, filelist, totfile,flag );
//	if(fd) fd.reports= NULL;
//
//	*bh= (BlendHandle*)fd;
//
//	/* when not linking (appending)... */
//	if((flag & FILE_LINK)==0) {
//		if(flag & FILE_ATCURSOR) {
//			float *curs, centerloc[3], vec[3], min[3], max[3];
//			int count= 0;
//
//			INIT_MINMAX(min, max);
//
//			centerbase= (scene.base.first);
//			while(centerbase) {
//				if(centerbase.object.id.lib==curlib && centerbase.object.parent==NULL) {
//					VECCOPY(vec, centerbase.object.loc);
//					DO_MINMAX(vec, min, max);
//					count++;
//				}
//				centerbase= centerbase.next;
//			}
//			if(count) {
//				centerloc[0]= (min[0]+max[0])/2;
//				centerloc[1]= (min[1]+max[1])/2;
//				centerloc[2]= (min[2]+max[2])/2;
//				curs = scene.cursor;
//				VECSUB(centerloc,curs,centerloc);
//
//				centerbase= (scene.base.first);
//				while(centerbase) {
//					if(centerbase.object.id.lib==curlib && centerbase.object.parent==NULL) {
//						ob= centerbase.object;
//						ob.loc[0] += centerloc[0];
//						ob.loc[1] += centerloc[1];
//						ob.loc[2] += centerloc[2];
//					}
//					centerbase= centerbase.next;
//				}
//			}
//		}
//	}
//}

/* ************* READ LIBRARY ************** */

public static int mainvar_count_libread_blocks(Main mainvar) {
        ListBase[] lbarray = new ListBase[LibraryUtil.MAX_LIBARRAY];
        int tot = 0;

        int a = LibraryUtil.set_listbasepointers(mainvar, lbarray);
        while (a-- != 0) {
            for (ID id = (ID) lbarray[a].first; id != null; id = (ID) id.next) {
                if ((id.flag & DNA_ID.LIB_READ) != 0) {
                    tot++;
                }
            }
        }
        return tot;
    }

public static void read_libraries(FileData basefd, ListBase<Main> mainlist)
{
	Main mainl= mainlist.first;
	Main mainptr;
	ListBase[] lbarray = new ListBase[LibraryUtil.MAX_LIBARRAY];
	int a, doit= 1;

	while(doit!=0) {
		doit= 0;

		/* test 1: read libdata */
		mainptr= mainl.next;
		while(mainptr!=null) {
			int tot= mainvar_count_libread_blocks(mainptr);

			// printf("found LIB_READ %s\n", mainptr.curlib.name);
			if(tot!=0) {
				FileData fd= (FileData)mainptr.curlib.filedata;

				if(fd==null) {
//					ReportList reports;
//
//					printf("read library: lib %s\n", mainptr.curlib.name);
//					fd= blo_openblenderfile(mainptr.curlib.filename, &reports);
//					fd.reports= basefd.reports;
//
//					if (fd) {
//						if (fd.libmap)
//							oldnewmap_free(fd.libmap);
//
//						fd.libmap = oldnewmap_new();
//
//						mainptr.curlib.filedata= fd;
//						mainptr.versionfile= fd.fileversion;
//
//						/* subversion */
//						read_file_version(fd, mainptr);
//					}
//					else mainptr.curlib.filedata= NULL;
//
//					if (fd==NULL)
                                                System.out.printf("ERROR: can't find lib %s \n", StringUtil.toJString(mainptr.curlib.filepath,0));
//						printf("ERROR: can't find lib %s \n", mainptr.curlib.filename);
				}
				if(fd!=null) {
					doit = 1;
                                        a = LibraryUtil.set_listbasepointers(mainptr, lbarray);
                                        while (a-- != 0) {
                                            ID id = (ID) lbarray[a].first;

                                            while (id != null) {
                                                ID idn = (ID) id.next;
                                                if ((id.flag & DNA_ID.LIB_READ) != 0) {
                                                    ID[] realid = {null};
                                                    ListBaseUtil.BLI_remlink(lbarray[a], id);

                                                    append_id_part(fd, mainptr, id, realid);
                                                    if (realid[0] == null) {
                                                        System.out.printf("LIB ERROR: can't find %s\n", StringUtil.toJString(id.name,0));
                                                    }

                                                    change_idid_adr(mainlist, basefd, id, realid);
                                                }
                                                id = idn;
                                            }
                                        }

                                        expand_main(fd, mainptr);

					/* dang FileData... now new libraries need to be appended to original filedata, it is not a good replacement for the old global (ton) */
					while( fd.mainlist.first!=null ) {
						Main mp= fd.mainlist.first;
						ListBaseUtil.BLI_remlink(fd.mainlist, mp);
						ListBaseUtil.BLI_addtail(basefd.mainlist, mp);
					}
				}
			}

			mainptr= mainptr.next;
		}
	}

	/* test if there are unread libblocks */
	for(mainptr= mainl.next; mainptr!=null; mainptr= mainptr.next) {
//		a= set_listbasepointers(mainptr, lbarray);
//		while(a--) {
//			ID *id= lbarray[a].first;
//			while(id) {
//				ID *idn= id.next;
//				if(id.flag & LIB_READ) {
//					BLI_remlink(lbarray[a], id);
//
//					printf("LIB ERROR: can't find %s\n", id.name);
//					change_idid_adr(mainlist, basefd, id, NULL);
//
//					MEM_freeN(id);
//				}
//				id= idn;
//			}
//		}
	}

	/* do versions, link, and free */
	for(mainptr= mainl.next; mainptr!=null; mainptr= mainptr.next) {
//		/* some mains still have to be read, then
//		 * versionfile is still zero! */
//		if(mainptr.versionfile) {
//			if(mainptr.curlib.filedata) // can be zero... with shift+f1 append
//				do_versions(mainptr.curlib.filedata, mainptr.curlib, mainptr);
//			else
//				do_versions(basefd, NULL, mainptr);
//		}
//
//		if(mainptr.curlib.filedata)
//			lib_link_all(mainptr.curlib.filedata, mainptr);
//
//		if(mainptr.curlib.filedata) blo_freefiledata(mainptr.curlib.filedata);
//		mainptr.curlib.filedata= NULL;
	}
}


///* reading runtime */
//
//BlendFileData *blo_read_blendafterruntime(int file, char *name, int actualsize, ReportList *reports)
//{
//	BlendFileData *bfd = NULL;
//	FileData *fd = filedata_new();
//	fd.filedes = file;
//	fd.buffersize = actualsize;
//	fd.read = fd_read_from_file;
//
//	/* needed for library_append and read_libraries */
//	BLI_strncpy(fd.filename, name, sizeof(fd.filename));
//
//	fd = blo_decode_and_check(fd, reports);
//	if (!fd)
//		return NULL;
//
//	fd.reports= reports;
//	bfd= blo_read_file_internal(fd);
//	blo_freefiledata(fd);
//
//	return bfd;
//}
}