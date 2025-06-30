// StateDMI_JFrame - main GUI to control StateDMI functions

/* NoticeStart

StateDMI
StateDMI is a part of Colorado's Decision Support Systems (CDSS)
Copyright (C) 1997-2023 Colorado Department of Natural Resources

StateDMI is free software:  you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

StateDMI is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

You should have received a copy of the GNU General Public License
    along with StateDMI.  If not, see <https://www.gnu.org/licenses/>.

NoticeEnd */

package DWR.DMI.StateDMI;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.filechooser.FileFilter;
import javax.swing.ImageIcon;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.JToolBar;
import javax.swing.ListSelectionModel;
import javax.swing.SwingUtilities;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;
import javax.swing.UIManager;

import DWR.DMI.HydroBaseDMI.HydroBaseDMI;
import DWR.DMI.HydroBaseDMI.HydroBaseDataStore;
import DWR.DMI.HydroBaseDMI.HydroBase_CountyRef;
import DWR.DMI.HydroBaseDMI.HydroBase_Cropchar;
import DWR.DMI.HydroBaseDMI.HydroBase_CUBlaneyCriddle;
import DWR.DMI.HydroBaseDMI.HydroBase_CUPenmanMonteith;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_AdminNumCalculator;
import DWR.DMI.HydroBaseDMI.SelectHydroBaseJDialog;

import rti.tscommandprocessor.commands.util.Comment_Command;
import rti.tscommandprocessor.commands.util.Comment_JDialog;
import rti.tscommandprocessor.commands.util.Exit_Command;
import rti.tscommandprocessor.core.TSCommandProcessorUtil;

import RTi.GRTS.TSViewJFrame;
import RTi.DMI.DatabaseDataStore;
import RTi.GIS.GeoView.GeoViewJFrame;

import RTi.TS.TS;
import RTi.TS.TS_ListSelector_JFrame;
import RTi.TS.TS_ListSelector_Listener;

import RTi.Util.GUI.HelpAboutJDialog;
import RTi.Util.GUI.JFileChooserFactory;
import RTi.Util.GUI.FindInJListJDialog;
import RTi.Util.GUI.JGUIUtil;
import RTi.Util.GUI.JScrollWorksheet;
import RTi.Util.GUI.JWorksheet;
import RTi.Util.GUI.JWorksheet_AbstractRowTableModel;
import RTi.Util.GUI.ResponseJDialog;
import RTi.Util.GUI.ReportJFrame;
import RTi.Util.GUI.SimpleFileFilter;
import RTi.Util.GUI.SimpleJButton;
import RTi.Util.GUI.SimpleJComboBox;
import RTi.Util.GUI.SimpleJMenuItem;
import RTi.Util.GUI.SimpleJTree_Node;
import RTi.Util.GUI.TextResponseJDialog;
import RTi.Util.Help.HelpViewer;
import RTi.Util.Help.HelpViewerUrlFormatter;
import RTi.Util.IO.AbstractCommand;
import RTi.Util.IO.AnnotatedCommandJList;
import RTi.Util.IO.Command;
import RTi.Util.IO.CommandDiscoverable;
import RTi.Util.IO.CommandLogRecord;
import RTi.Util.IO.CommandLog_CellRenderer;
import RTi.Util.IO.CommandLog_TableModel;
import RTi.Util.IO.CommandPhaseType;
import RTi.Util.IO.CommandProcessor;
import RTi.Util.IO.CommandProcessorListener;
import RTi.Util.IO.CommandProcessorRequestResultsBean;
import RTi.Util.IO.CommandProgressListener;
import RTi.Util.IO.CommandStatusProvider;
import RTi.Util.IO.CommandStatusType;
import RTi.Util.IO.CommandStatusUtil;
import RTi.Util.IO.DataSetComponent;
import RTi.Util.IO.FileGenerator;
import RTi.Util.IO.HTMLViewer;
import RTi.Util.IO.IOUtil;
import RTi.Util.IO.ProcessManager;
import RTi.Util.IO.ProcessManagerJDialog;
import RTi.Util.IO.Prop;
import RTi.Util.IO.PropList;
import RTi.Util.IO.PropList_CellRenderer;
import RTi.Util.IO.PropList_TableModel;
import RTi.Util.IO.TextPrinterJob;
import RTi.Util.IO.UnknownCommand;
import RTi.Util.IO.UnknownCommandException;
import RTi.Util.Message.DiagnosticsJFrame;
import RTi.Util.Message.Message;
import RTi.Util.Message.MessageLogListener;
import RTi.Util.String.StringUtil;
import RTi.Util.Table.DataTable;
import RTi.Util.Table.DataTable_JFrame;
import RTi.Util.Table.TableColumnType;
import RTi.Util.Table.TableField;
import RTi.Util.Time.TimeInterval;
import riverside.datastore.DataStore;
import riverside.datastore.DataStoreSubstitute;
import riverside.datastore.DataStores_JFrame;
import riverside.datastore.GenericDatabaseDataStore;
import DWR.StateCU.StateCU_BlaneyCriddle_Data_JFrame;
import DWR.StateCU.StateCU_ClimateStation_JFrame;
import DWR.StateCU.StateCU_ClimateStation_Data_JFrame;
import DWR.StateCU.StateCU_CropCharacteristics_JFrame;
import DWR.StateCU.StateCU_CropCharacteristics_Data_JFrame;
import DWR.StateCU.StateCU_CropPatternTS;
import DWR.StateCU.StateCU_DataSet;
import DWR.StateCU.StateCU_DataSet_JFrame;
import DWR.StateCU.StateCU_DataSet_JTree;
import DWR.StateCU.StateCU_DataSetComponent_CellRenderer;
import DWR.StateCU.StateCU_DataSetComponent_TableModel;
import DWR.StateCU.StateCU_IrrigationPracticeTS;
import DWR.StateCU.StateCU_Location_JFrame;
import DWR.StateCU.StateCU_Location_ClimateStation_Data_JFrame;
import DWR.StateCU.StateCU_Location_Collection_Data_JFrame;
import DWR.StateCU.StateCU_Location_Data_JFrame;
import DWR.StateCU.StateCU_PenmanMonteith_Data_JFrame;
import DWR.StateCU.StateCU_Util;

import DWR.StateMod.StateMod_DataSet;
import DWR.StateMod.StateMod_DataSet_JTree;
import DWR.StateMod.StateMod_DataSet_WindowManager;
import DWR.StateMod.StateMod_DataSetComponent_CellRenderer;
import DWR.StateMod.StateMod_DataSetComponent_TableModel;
import DWR.StateMod.StateMod_DelayTable_JFrame;
import DWR.StateMod.StateMod_DelayTable_Data_JFrame;
import DWR.StateMod.StateMod_Diversion;
import DWR.StateMod.StateMod_Diversion_JFrame;
import DWR.StateMod.StateMod_Diversion_Collection_Data_JFrame;
import DWR.StateMod.StateMod_Diversion_Data_JFrame;
import DWR.StateMod.StateMod_Diversion_DelayTableAssignment_Data_JFrame;
import DWR.StateMod.StateMod_DiversionRight_Data_JFrame;
import DWR.StateMod.StateMod_InstreamFlow_JFrame;
import DWR.StateMod.StateMod_InstreamFlow_Data_JFrame;
import DWR.StateMod.StateMod_InstreamFlowRight_Data_JFrame;
import DWR.StateMod.StateMod_Network_JFrame;
import DWR.StateMod.StateMod_NodeNetwork;
import DWR.StateMod.StateMod_OperationalRight_Data_JFrame;
import DWR.StateMod.StateMod_OperationalRight_JFrame;
import DWR.StateMod.StateMod_Plan_Data_JFrame;
import DWR.StateMod.StateMod_Plan_Return_Data_JFrame;
import DWR.StateMod.StateMod_Plan_WellAugmentation_Data_JFrame;
import DWR.StateMod.StateMod_Reservoir_JFrame;
import DWR.StateMod.StateMod_ReservoirAccount_Data_JFrame;
import DWR.StateMod.StateMod_ReservoirAreaCap_Data_JFrame;
import DWR.StateMod.StateMod_ReservoirClimate_Data_JFrame;
import DWR.StateMod.StateMod_Reservoir_Collection_Data_JFrame;
import DWR.StateMod.StateMod_Reservoir_Data_JFrame;
import DWR.StateMod.StateMod_ReservoirRight_Data_JFrame;
import DWR.StateMod.StateMod_Reservoir_Return_Data_JFrame;
import DWR.StateMod.StateMod_RiverNetworkNode_JFrame;
import DWR.StateMod.StateMod_RiverNetworkNode_Data_JFrame;
import DWR.StateMod.StateMod_StreamEstimate_Data_JFrame;
import DWR.StateMod.StateMod_StreamEstimateCoefficients_Data_JFrame;
import DWR.StateMod.StateMod_StreamGage_JFrame;
import DWR.StateMod.StateMod_StreamGage_Data_JFrame;
import DWR.StateMod.StateMod_Util;
import DWR.StateMod.StateMod_Well;
import DWR.StateMod.StateMod_Well_JFrame;
import DWR.StateMod.StateMod_Well_Data_JFrame;
import DWR.StateMod.StateMod_Well_Collection_Data_JFrame;
import DWR.StateMod.StateMod_Well_DelayTableAssignment_Data_JFrame;
import DWR.StateMod.StateMod_WellRight;
import DWR.StateMod.StateMod_WellRight_Data_JFrame;

import DWR.DMI.HydroBaseDMI.HydroBase_Util;

/**
Main graphical user interface (GUI) class for StateDMI.
The interface provides menus and tools to help create files for StateCU and StateMod.
*/
@SuppressWarnings("serial")
public class StateDMI_JFrame extends JFrame
implements
ActionListener,
CommandProcessorListener,
CommandProgressListener,
ItemListener,
HelpViewerUrlFormatter,
KeyListener,
ListDataListener,
ListSelectionListener,
MessageLogListener,
MouseListener,
TreeSelectionListener,
TS_ListSelector_Listener,
WindowListener
{

/**
StateDMI session information, used to track command file open history, etc.
*/
private StateDMISession session = null;

/**
Path to resources, like graphics.
*/
private final String __RESOURCE_PATH = "/DWR/DMI/StateDMI";

/**
Indicate the application type for the StateDMI run so that menus can be set for StateCU or StateMod.
See StateDMI.APP_TYPE_*
*/
private int __appType = 0;

/**
TODO SAM 2008
Indicate whether data set features are enabled.
For now comment out because they were implemented for development and are just taking up space.
The data set displays probably need to be in a separate tab or edge panel (tree?).
*/
private boolean __datasetFeaturesEnabled = false;

/**
Label for datastores, necessary because label will be set not visible if no datastores.
*/
private JLabel __dataStore_JLabel = null;

// TODO SAM phase in file datastore at some point.
/**
Tabbed panel to keep datastores and input types separate.
*/
private JTabbedPane __dataStore_JTabbedPane = null;

/**
Available datastores.
*/
private SimpleJComboBox __dataStore_JComboBox = null;

/**
Map interface.
*/
private GeoViewJFrame __geoview_JFrame = null;

/**
Maximum number of files in recent files, taken from TSToolSession history.
*/
private final int MAX_RECENT_FILES = 20;

/**
StateMod network frame.
*/
private StateMod_Network_JFrame __network_JFrame = null;

/**
Fraction of the height for the layout.
TODO SAM 2005-01-18 need to make this dynamic if in commands mode.
*/
private final double __LAYOUT_COMPONENTS_FRACTION = .10, //.35,
		__LAYOUT_COMMANDS_FRACTION = .65; //.25;

/**
The command being edited is a new one, so it will be inserted in the command list.
*/
private final int __INSERT_COMMAND = 1;

/**
The command being edited is not a new one, so the old one in the list will be updated.
*/
private final int __UPDATE_COMMAND = 2;

/**
StateDMI session type - unknown session type (e.g., at startup or after closing another session).
*/
private final int __SESSION_UNKNOWN = 0;

/**
StateDMI session type - session is editing one data component (e.g., Diversions)
with no knowledge of the full data set.
*/
private final int __SESSION_DATA_SET_COMPONENT = 1;

/**
StateDMI session type - session is editing a full data set.
*/
private final int __SESSION_DATA_SET = 2;

/**
StateDMI session type - session is editing commands from a command file.
The data set component can be "guessed" from the commands.
*/
private final int __SESSION_COMMANDS = 3;

/**
StateDMI session type that is active.
*/
private int __sessionType = __SESSION_UNKNOWN;

/**
StateCU data set (corresponds to the response file).
*/
private StateCU_DataSet __statecuDataset = null;

/**
Data set manager (TODO SAM not needed with new interface?).
*/
private StateCU_DataSet_JFrame __statecuDatasetManager = null;

/**
Tree to display the data set components (input).
*/
private StateCU_DataSet_JTree __statecuDataset_JTree = null;

/**
StateCU data set type (see __STATECU_DATA_SET_*).
*/
private int __statecuDatasetType = StateCU_DataSet.TYPE_UNKNOWN;

/**
StateMod data set type (see __STATEMOD_DATA_SET_*).
TODO SAM 2007-06-26 Evaluate use
*/
//private int __statemod_dataset_type = StateMod_DataSet.TYPE_UNKNOWN;

/**
The selected data set component, used to enable/disable menus.
*/
private DataSetComponent __statecuSelectedComponent = null;

/**
StateMod data set (corresponds to the response file).
*/
private StateMod_DataSet __statemodDataset = null;

/**
Tree to display the data set components (input).
*/
private StateMod_DataSet_JTree __statemodDataset_JTree = null;

/**
The selected data set component, used to enable/disable menus.
*/
private DataSetComponent __statemodSelectedComponent = null;

/**
Panel for component group list.
*/
private JPanel __list_JPanel = null;

/**
Worksheet to display the list of data objects for a component group.
*/
private JWorksheet __list_JWorksheet = null;

/**
Table model for the list.
*/
@SuppressWarnings("rawtypes")
private JWorksheet_AbstractRowTableModel __list_TableModel = null;

// Commands-related.

//TODO SAM 2007-11-02 Evaluate putting in the processor
/**
Indicates whether the commands have been edited without being saved.
This will trigger some changes in the UI,
for example indicating that the commands have been modified and need to be saved (or cancel) before exit.
*/
private boolean __commandsDirty = false;

/**
The last directory selected when loading a command file.
*/
private String __Dir_LastCommandFileOpened = null;

/**
Use this to temporarily ignore item action performed events, necessary when programatically modifying the contents of combo boxes.
*/
private boolean __ignoreActionEvent = false;

// TODO SAM 2007-10-19 Evaluate whether still needed with new list model.
/**
Use this to temporarily ignore item listener events, necessary when programatically modifying the contents of combo boxes.
*/
private boolean __ignoreItemEvent = false;

/**
This is used in some cases to disable updates during bulk operations to the command list.
*/
private boolean __ignoreListSelectionEvent = false;

/**
Last command file that was read.  Don't set until selected by the user (or on the command line).
*/
private String __commandFileName = null;

/**
Panel for commands - title border is reset for messages.
*/
private JPanel __commands_JPanel;

/**
Annotated list to hold commands and display the command status.
*/
private AnnotatedCommandJList __commands_AnnotatedCommandJList;

/**
Commands JList, to support interaction such as selecting and popup menus.
This is a reference to the JList managed by AnnotatedList (and also the legacy string list).
*/
private JList<String> __commands_JList;

/**
Fixed-width font - courier for report output
*/
private String __FIXED_WIDTH_FONT = "Courier";

/**
Command font - looks better than courier
*/
private final String __COMMANDS_FONT = "Lucida Console";

/**
TODO smalers 2020-02-16 need to parameterize generics.
List model that maps the TSCommandProcessor Command data to the command JList.
*/
private StateDMI_Processor_ListModel __commands_JListModel;

/**
Buffer to hold commands manipulated by cut/copy/paste.
Note that this is maintained internally and is not the same as the operating system cut/copy/paste buffer.
*/
private List<Command> __commandsCutBuffer = new ArrayList<>();

// Results-related.

/**
Tree to display the data set results (output).
*/
// FIXME SAM 2008-11-11 Evaluate whether to use.
//private StateCU_DataSet_JTree __statecuResults_JTree = null;

/**
Tree to display the data set results (output).
*/
// FIXME SAM 2008-11-11 Evaluate whether to use.
//private StateMod_DataSet_JTree __statemodResults_JTree = null;

/**
Tabbed panel to include all results.
*/
private JTabbedPane __results_JTabbedPane;

//TODO SAM 2005-03-23 should the data sets have separate file lists?
/**
List of results output files for viewing with an editor.
This includes StateCU AND StateMod files (unlike data components, which are listed by model).
*/
private JList<String> __resultsOutputFiles_JList = null;

/**
JList data model for final time series (basically a list of filenames associated with __resultsOutputFiles_JList).
*/
private DefaultListModel<String> __resultsOutputFiles_JListModel = null;

/**
Worksheet that contains a list of problems from processing.
*/
private JWorksheet __resultsProblems_JWorksheet = null;

/**
List of results components for viewing with JWorksheets, for StateCU components.
*/
private JList<String> __resultsStateCUComponents_JList = null;

/**
JList data model for StateCU components (basically a list of component names associated with __resultsStateCUComponents_JList).
*/
private DefaultListModel<String> __resultsStateCUComponents_JListModel = null;

/**
List of results components for viewing with JWorksheets, for StateMod components.
*/
private JList<String> __resultsStateModComponents_JList = null;

/**
JList data model for StateCU components (basically a list of
component names associated with __resultsStateModComponents_JList).
*/
private DefaultListModel<String> __resultsStateModComponents_JListModel = null;

/**
List of results tables for viewing with an editor.
*/
private JList<String> __resultsTables_JList = null;

/**
Popup menu for table results.
*/
private JPopupMenu __resultsTables_JPopupMenu = null;

/**
JList data model for final time series (a list of table identifiers associated with __results_tables_JList).
*/
private DefaultListModel<String> __resultsTables_JListModel;

/**
List of time series selectors and associated component types, maintained to look up graph properties.
*/
List<TS_ListSelector_JFrame>  TS_ListSelector_JFrame_List = new ArrayList<>();
List<Integer> TS_ListSelector_JFrame_app_type_List = new ArrayList<>();
List<Integer> TS_ListSelector_JFrame_comp_type_List = new ArrayList<>();

/**
Worksheet that contains a list of processor properties.
*/
private JWorksheet __resultsProperties_JWorksheet = null;

/**
The command processor, which maintains a list of command objects, process the data, and the results.
There is only one command processor instance for a StateDMI session and it is kept current with the application.
In the future, it may be possible to have, for example, tabs for different command files, each with a StateDMI_Processor.
*/
private StateDMI_Processor __statedmiProcessor = new StateDMI_Processor();

// Status-area related.

/**
General status string to indicate that the GUI is ready for user input.
*/
private final String __STATUS_READY = "Ready";

/**
General status string to indicate that the user should wait for the GUI to finish a task.
*/
private final String __STATUS_BUSY = "Wait";

/**
General status string to indicate that command processing is being cancelled.
*/
private final String __STATUS_CANCELING = "Canceling";

/**
General status string to indicate that command processing has been cancelled.
*/
private final String __STATUS_CANCELLED = "Cancelled";

/**
Message area text field (e.g., "Processing commands...") - long and left-most.
*/
private JTextField __message_JTextField;

/**
Progress bar to show progress of running commands in processor.
*/
private JProgressBar __processor_JProgressBar;

/**
Progress bar to show progress of running a specific commands.
*/
private JProgressBar __command_JProgressBar;

/**
Status area text field (e.g., "READY", "WAIT") - small and right-most.
*/
private JTextField __status_JTextField;

// General.

/**
The initial working directory corresponding to a command file read/write or opened File.
This is used when processing the list of setWorkingDir() commands passed to command editors.
Without the initial working directory, relative changes in the working directory will result in an inaccurate initial state.
*/
private String __initialWorkingDir = "";

// Menu items that need to be modified throughout the session.

// Buttons used in the main interface.

private SimpleJButton
	__Run_AllCommands_JButton,
	__Run_SelectedCommands_JButton,
	__ClearCommands_JButton;

// The menu bar for all menus.

JMenuBar
	__JMenuBar = null;

/**
Panel for input options.
*/
private JPanel __queryInput_JPanel;

/**
Text field indicating that datastores are initializing.
*/
private JLabel __dataStoreInitializing_JLabel;

private final static int MENU_STYLE_TWO_LEVEL = 2;
private final static int MENU_STYLE_THREE_LEVEL = 3;

/**
The style for menus.
*/
private int menu_style = MENU_STYLE_THREE_LEVEL;

// Popup menu.

private JPopupMenu
	__Commands_JPopupMenu;
private JMenuItem
	__CommandsPopup_ShowCommandStatus_JMenuItem,
	__CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem,

	__CommandsPopup_Cut_JMenuItem,
	__CommandsPopup_Copy_JMenuItem,
	__CommandsPopup_Paste_JMenuItem,

	__CommandsPopup_Delete_JMenuItem,
	__CommandsPopup_FindCommandsUsingString_JMenuItem,
	__CommandsPopup_FindCommandsUsingLineNumber_JMenuItem,

	__CommandsPopup_SelectAll_JMenuItem,
	__CommandsPopup_DeselectAll_JMenuItem,

	__CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem,
	__CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem,
	__CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,
	__CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,
	__CommandsPopup_CancelCommandProcessing_JMenuItem,

	__CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem,
	__CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem;

// File menu.

private JMenu
	// Used with StateCU and StateMod.
	__File_Open_JMenu = null;
		private JMenuItem
			__File_Open_CommandFileRecent_JMenuItem[] = null;
private JMenuItem
	__File_Open_CommandFile_JMenuItem,
	__File_Open_DataSet_JMenuItem;
private JMenu
	// Used with StateCU and StateMod.
	__File_Open_DataSetComponent_JMenu;
private JMenuItem
	// Used with StateCU.
	//__File_Open_DataSetComponent_StateCU_Locations_JMenuItem,
	//__File_Open_DataSetComponent_StateCU_CropCharacteristics_JMenuItem,
	//__File_Open_DataSetComponent_StateCU_BlaneyCriddle_JMenuItem,
	//__File_Open_DataSetComponent_StateCU_ClimateStations_JMenuItem,
	// Used with StateMod...
	__File_Open_ModelNetwork_JMenuItem,
	__File_New_ModelNetwork_JMenuItem,
	// Used with StateCU and StateMod.
	__File_Open_HydroBase_JMenuItem;

private JMenu
	// Used with StateCU and StateMod.
	__File_New_JMenu,
	__File_New_DataSet_JMenu,
	// Used with StateCU.
	__File_New_DataSet_StateCU_ClimateStations_JMenu;
private JMenuItem
	// Used with StateCU.
	__File_New_DataSet_StateCU_ClimateStations_FromList_JMenuItem,
	__File_New_DataSet_StateCU_ClimateStations_FromHydroBase_JMenuItem;
private JMenu
	// Used with StateCU.
	__File_New_DataSet_StateCU_Structures_JMenu;
private JMenuItem
	__File_New_DataSet_StateCU_Structures_FromList_JMenuItem;
private JMenu
	__File_New_DataSet_StateCU_WaterSupplyLimited_JMenu,
	__File_New_DataSet_StateCU_WaterSupplyLimitedByRights_JMenu,
	__File_New_DataSet_StateCU_RiverDepletion_JMenu,
	__File_New_DataSet_StateCU_OtherUses_JMenu,
	// Used with StateMod.
	__File_New_DataSet_StateMod_Historical_JMenu,
	__File_New_DataSet_StateMod_Demands_JMenu;
private JMenu
	// Used with StateCU and StateMod.
	__File_New_DataSetComponent_JMenu,
	// Used with StateCU.
	__File_New_DataSetComponent_StateCU_Locations_JMenu;
private JMenuItem
	__File_New_DataSetComponent_StateCU_Locations_FromList_JMenuItem;
private JMenu
	__File_New_DataSetComponent_StateCU_CropCharacteristics_JMenu;
private JMenuItem
	__File_New_DataSetComponent_StateCU_CropCharacteristics_FromList_JMenuItem;
private JMenu
	__File_New_DataSetComponent_StateCU_BlaneyCriddle_JMenu;
private JMenuItem
	__File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList_JMenuItem;
private JMenu
	__File_New_DataSetComponent_StateCU_ClimateStations_JMenu;
private JMenuItem
	__File_New_DataSetComponent_StateCU_ClimateStations_FromList_JMenuItem,
	// Used with StateCU and StateMod.
	__File_New_CommandFile_JMenuItem;

private JMenu
	__File_Save_JMenu;

private JMenuItem
	__File_Save_Commands_JMenuItem,	// Enable/disable based on state.
	__File_Save_CommandsAs_JMenuItem,

	__File_Save_DataSet_JMenuItem;

	// StateCU Level 1.
	//__File_Save_StateCU_All_JMenuItem,
	//__File_Save_StateCU_Response_JMenuItem,
	//__File_Save_StateCU_Control_JMenuItem,
	//__File_Save_StateCU_CULocations_JMenuItem,
	//__File_Save_StateCU_CropCharacteristics_JMenuItem,
	//__File_Save_StateCU_BlaneyCriddleCropCoefficients_JMenuItem,
	//__File_Save_StateCU_ClimateStations_JMenuItem,
	//__File_Save_StateCU_TemperatureTSMonthly_JMenuItem,
	//__File_Save_StateCU_YearlyFrostDatesTS_JMenuItem,
	//__File_Save_StateCU_MonthlyPrecipitationTS_JMenuItem,

	// StateCU Level 2.
	//__File_Save_StateCU_CropPatternTS_JMenuItem;

private JMenu
	__File_Print_JMenu = null;
private JMenuItem
    __File_Print_Commands_JMenuItem = null;

JMenu
	__File_Properties_JMenu;
JMenuItem
	__File_Properties_HydroBase_JMenuItem,
	__File_Properties_DataSet_JMenuItem,

	__File_SetWorkingDirectory_JMenuItem,

	__File_Test_JMenuItem,

	__File_SwitchToStateCU_JMenuItem,
	__File_SwitchToStateMod_JMenuItem,
	__File_Exit_JMenuItem;

	// Edit.

//private JMenu
//	__Edit_JMenu;
private JMenuItem
	__Edit_CutCommands_JMenuItem,
	__Edit_CopyCommands_JMenuItem,
	__Edit_PasteCommands_JMenuItem,
	// --
	__Edit_DeleteCommands_JMenuItem,
	// --
	__Edit_SelectAllCommands_JMenuItem,
	__Edit_DeselectAllCommands_JMenuItem,
	// --
	__Edit_CommandWithErrorChecking_JMenuItem,
	// --
	__Edit_ConvertSelectedCommandsToComments_JMenuItem = null,
	__Edit_ConvertSelectedCommandsFromComments_JMenuItem = null;

	// View menu (StateCU).

JCheckBoxMenuItem
	__View_DataSetManager_JCheckBoxMenuItem,
	__View_Map_JCheckBoxMenuItem,
	__View_ModelNetwork_JCheckBoxMenuItem,
	__View_ThreeLevelCommandsMenu_JCheckBoxMenuItem;

private JMenuItem
	__View_CommandFileDiff_JMenuItem = null,
	__View_DataStores_JMenuItem = null;

	// The following are used by StateCU and StateMod.

private JMenu
	__Commands_JMenu;
	// Only used by StateMod because there are too many data set component groups to fit in one menu on the screen.
	//__Commands2_JMenu;

	// Commands menu for StateCU.

private JMenuItem
	__Commands_StateCU_ClimateStationsData_JMenuItem;
private JMenu
	__Commands_StateCU_ClimateStations_JMenu;
private JMenuItem
	//__Commands_StateCU_ClimateStations_TemperatureTS_JMenuItem,
	//__Commands_StateCU_ClimateStations_FrostDatesTS_JMenuItem,
	//__Commands_StateCU_ClimateStations_PrecipitationTS_JMenuItem,
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromList_JMenuItem,
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_JMenuItem,
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_JMenuItem,
	__Commands_StateCU_ClimateStations_SetClimateStation_JMenuItem,
	__Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_JMenuItem,
	__Commands_StateCU_ClimateStations_FillClimateStation_JMenuItem,
	__Commands_StateCU_ClimateStations_SortClimateStations_JMenuItem,
	__Commands_StateCU_ClimateStations_WriteClimateStationsToList_JMenuItem,
	__Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_JMenuItem;
private JMenuItem
	__Commands_StateCU_CropCharacteristicsData_JMenuItem;
private JMenu
	__Commands_StateCU_CropCharacteristics_JMenu;
private JMenuItem
	__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_JMenuItem,
	__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_JMenuItem,
	__Commands_StateCU_CropCharacteristics_SetCropCharacteristics_JMenuItem,
	__Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_JMenuItem,
	__Commands_StateCU_CropCharacteristics_SortCropCharacteristics_JMenuItem,
	__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_JMenuItem,
	__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_JMenuItem;
private JMenu
	__Commands_StateCU_BlaneyCriddle_JMenu;
private JMenuItem
	__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_JMenuItem,
	__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_JMenuItem;
private JMenu
	__Commands_StateCU_PenmanMonteith_JMenu;
private JMenuItem
	__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_JMenuItem,
	__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_JMenuItem,
	__Commands_StateCU_PenmanMonteith_SetPenmanMonteith_JMenuItem,
	__Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_JMenuItem,
	__Commands_StateCU_PenmanMonteith_SortPenmanMonteith_JMenuItem,
	__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_JMenuItem,
	__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_JMenuItem;

private JMenuItem
	__Commands_StateCU_CULocationsData_JMenuItem;

private JMenu
	__Commands_StateCU_CULocations_JMenu;
private JMenuItem
	//__Commands_StateCU_CULocations_ReadCULocationsFromList_JMenuItem,
	//__Commands_StateCU_CULocations_ReadCULocationsFromStateCU_JMenuItem,
	//__Commands_StateCU_CULocations_ReadCULocationsFromStateMod_JMenuItem,
	__Commands_StateCU_CULocations_SetCULocation_JMenuItem,
	__Commands_StateCU_CULocations_SetCULocationsFromList_JMenuItem,
	//__Commands_StateCU_CULocations_SetDiversionAggregate_JMenuItem,
	//__Commands_StateCU_CULocations_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateCU_CULocations_SetDiversionSystem_JMenuItem,
	//__Commands_StateCU_CULocations_SetDiversionSystemFromList_JMenuItem,
	//__Commands_StateCU_CULocations_SetWellAggregate_JMenuItem,
	//__Commands_StateCU_CULocations_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateCU_CULocations_SetWellSystem_JMenuItem,
	//__Commands_StateCU_CULocations_SetWellSystemFromList_JMenuItem,
	__Commands_StateCU_CULocations_SortCULocations_JMenuItem,
	__Commands_StateCU_CULocations_FillCULocationsFromList_JMenuItem,
	__Commands_StateCU_CULocations_FillCULocationsFromHydroBase_JMenuItem,
	__Commands_StateCU_CULocations_FillCULocation_JMenuItem,
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_JMenuItem,
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_JMenuItem,
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeights_JMenuItem,
	__Commands_StateCU_CULocations_FillCULocationClimateStationWeights_JMenuItem,
	__Commands_StateCU_CULocations_WriteCULocationsToList_JMenuItem,
	__Commands_StateCU_CULocations_WriteCULocationsToStateCU_JMenuItem;

private JMenu
	__Commands_StateCU_Parcels_JMenu;
private JMenuItem
	__Commands_StateCU_Parcels_ReadParcelsFromHydroBase_JMenuItem,
	__Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_JMenuItem,
	__Commands_StateCU_Parcels_SetParcel_JMenuItem,
	__Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_JMenuItem,
	__Commands_StateCU_Parcels_SetParcelGroundWaterSupply_JMenuItem,
	__Commands_StateCU_Parcels_CheckParcels_JMenuItem,
	__Commands_StateCU_Parcels_CheckIrrigatedLands_JMenuItem,
	__Commands_StateCU_Parcels_WriteParcelsToFile_JMenuItem;

private JMenu
	__Commands_StateCU_CropPatternTS_JMenu;
private JMenuItem
	//__Commands_StateCU_CropPatternTS_ReadCULocationsFromList_JMenuItem,
	//__Commands_StateCU_CropPatternTS_ReadCULocationsFromStateCU_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetDiversionAggregate_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetDiversionSystem_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetDiversionSystemFromList_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetWellAggregate_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetWellSystem_JMenuItem,
	//__Commands_StateCU_CropPatternTS_SetWellSystemFromList_JMenuItem,
	__Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_JMenuItem,
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_JMenuItem,
	//FIXME SAM 2008-12-30 Remove if not needed
	//__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_JMenuItem,
	__Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_JMenuItem,
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_JMenuItem,
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_JMenuItem,
	__Commands_StateCU_CropPatternTS_SetCropPatternTS_JMenuItem,
	__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_JMenuItem,
	__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_JMenuItem,
	__Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_JMenuItem,
	__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_JMenuItem,
	__Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_JMenuItem,
	__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_JMenuItem,
	__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_JMenuItem,
	__Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_JMenuItem,
	__Commands_StateCU_CropPatternTS_SortCropPatternTS_JMenuItem,
	__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_JMenuItem,
	__Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_JMenuItem,
	__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_JMenuItem;
	// TODO smalers 2021-01-24 - used for supplemental data?  Not sure if it was fully ever implemented.
	//__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_JMenuItem;
private JMenu
	__Commands_StateCU_IrrigationPracticeTS_JMenu;
private JMenuItem
	// setOutputPeriod() generic
	//__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromList_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromStateCU_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregate_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystem_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystemFromList_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetWellAggregate_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetWellSystem_JMenuItem,
	//__Commands_StateCU_IrrigationPracticeTS_SetWellSystemFromList_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_JMenuItem,
	// TODO SAM 2005-03-07 Comment out - use what is in HydroBase.
	//__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromDBF_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_JMenuItem,
	__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_JMenuItem,

	__Commands_StateCU_DiversionTS_JMenuItem,
	__Commands_StateCU_WellPumpingTS_JMenuItem,
	__Commands_StateCU_DiversionRights_JMenuItem;

//Commands...Datastore Processing.
private JMenu
 	__Commands_Datastore_JMenu = null;

// Commands... Output File Processing.
private JMenu
	__Commands_Output_JMenu = null;
private JMenuItem
	__Commands_Output_SplitStateModReport_JMenuItem;

// Commands... Spatial Processing.
private JMenu
	__Commands_Spatial_JMenu = null;
private JMenuItem
	__Commands_Spatial_WriteTableToGeoJSON_JMenuItem,
	__Commands_Spatial_WriteTableToShapefile_JMenuItem;

// Commands... Spreadsheet Processing.

private JMenu
	__Commands_Spreadsheet_JMenu = null;
private JMenuItem
	__Commands_Spreadsheet_NewExcelWorkbook_JMenuItem,
	__Commands_Spreadsheet_ReadExcelWorkbook_JMenuItem,
	__Commands_Spreadsheet_ReadTableFromExcel_JMenuItem,
	__Commands_Spreadsheet_ReadTableCellsFromExcel_JMenuItem,
	__Commands_Spreadsheet_ReadPropertiesFromExcel_JMenuItem,
	__Commands_Spreadsheet_SetExcelCell_JMenuItem,
	__Commands_Spreadsheet_SetExcelWorksheetViewProperties_JMenuItem,
	__Commands_Spreadsheet_WriteTableToExcel_JMenuItem,
	__Commands_Spreadsheet_WriteTableCellsToExcel_JMenuItem,
	__Commands_Spreadsheet_WriteTimeSeriesToExcel_JMenuItem,
	__Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_JMenuItem,
	__Commands_Spreadsheet_CloseExcelWorkbook_JMenuItem;

private JMenu
	__Commands_General_Comments_JMenu;
private JMenuItem
	__Commands_General_Comments_Comment_JMenuItem,
	__Commands_General_Comments_StartComment_JMenuItem,
	__Commands_General_Comments_EndComment_JMenuItem,
	__Commands_General_Comments_ReadOnlyComment_JMenuItem = null,
	__Commands_General_Comments_EnabledComment_JMenuItem = null,
	__Commands_General_Comments_ExpectedStatusFailureComment_JMenuItem = null,
	__Commands_General_Comments_ExpectedStatusWarningComment_JMenuItem = null,
	__Commands_General_Comments_RequireApplicationComment_JMenuItem = null,
	__Commands_General_Comments_RequireDatastoreComment_JMenuItem = null;

private JMenu
    __Commands_General_FileHandling_JMenu = null;
private JMenuItem
	__Commands_General_FileHandling_FTPGet_JMenuItem = null,
	__Commands_General_FileHandling_WebGet_JMenuItem = null,
	__Commands_General_FileHandling_CompareFiles_JMenuItem = null,
	__Commands_General_FileHandling_MergeListFileColumns_JMenuItem = null,
	__Commands_General_FileHandling_AppendFile_JMenuItem = null,
	__Commands_General_FileHandling_CopyFile_JMenuItem = null,
	__Commands_General_FileHandling_ListFiles_JMenuItem = null,
	__Commands_General_FileHandling_UnzipFile_JMenuItem = null,
    __Commands_General_FileHandling_RemoveFile_JMenuItem = null;

private JMenu
	__Commands_General_HydroBase_JMenu = null;
private JMenuItem
	__Commands_General_HydroBase_OpenHydroBase_JMenuItem;

private JMenu
	__Commands_General_Logging_JMenu;
private JMenuItem
	__Commands_General_Logging_StartLog_JMenuItem,
	__Commands_General_Logging_SetDebugLevel_JMenuItem,
	__Commands_General_Logging_SetWarningLevel_JMenuItem,
	__Commands_General_Logging_Message_JMenuItem;

JMenu
	__Commands_General_Running_JMenu = null;
private JMenuItem
	__Commands_General_Running_SetOutputPeriod_JMenuItem = null,
	__Commands_General_Running_SetOutputYearType_JMenuItem = null,
	__Commands_General_Running_SetProperty_JMenuItem = null,
	__Commands_General_Running_FormatDateTimeProperty_JMenuItem = null,
	__Commands_General_Running_FormatStringProperty_JMenuItem = null,
	__Commands_General_Running_RunCommands_JMenuItem = null,
	__Commands_General_Running_RunProgram_JMenuItem = null,
	__Commands_General_Running_RunPython_JMenuItem = null,
	__Commands_General_Running_RunR_JMenuItem = null,
	__Commands_General_Running_Exit_JMenuItem = null,
	__Commands_General_Running_SetWorkingDir_JMenuItem = null,
	__Commands_General_Running_WritePropertiesToFile_JMenuItem = null;

//Commands (General - Test Processing).
JMenu
    __Commands_General_TestProcessing_JMenu = null;
JMenuItem
    __Commands_General_TestProcessing_CompareFiles_JMenuItem = null,
    __Commands_General_TestProcessing_WriteProperty_JMenuItem = null,
    //-- separator ---
    __Commands_General_TestProcessing_CreateRegressionTestCommandFile_JMenuItem = null,
    __Commands_General_TestProcessing_StartRegressionTestResultsReport_JMenuItem = null;

// Commands (Table).

private JMenu
	__Commands_Table_JMenu = null;

// Create, Copy, Free Table.
private JMenu
	__Commands_TableCreate_JMenu = null;
private JMenuItem
	__Commands_TableCreate_NewTable_JMenuItem,
	__Commands_TableCreate_CopyTable_JMenuItem,
	__Commands_TableCreate_FreeTable_JMenuItem;

// Read Table
private JMenu
	__Commands_TableRead_JMenu = null;
private JMenuItem
	__Commands_TableRead_ReadTableFromDataStore_JMenuItem,
	__Commands_TableRead_ReadTableFromDBF_JMenuItem,
	__Commands_TableRead_ReadTableFromDelimitedFile_JMenuItem,
	__Commands_TableRead_ReadTableFromExcel_JMenuItem,
	__Commands_TableRead_ReadTableFromFixedFormatFile_JMenuItem,
	__Commands_TableRead_ReadTableFromJSON_JMenuItem, // not being used
	__Commands_TableRead_ReadTableFromXML_JMenuItem; // not being used

// Append, Join Tables
private JMenu
	__Commands_TableJoin_JMenu = null;
private JMenuItem
	__Commands_TableJoin_AppendTable_JMenuItem,
	__Commands_TableJoin_JoinTables_JMenuItem;

// Analyze Table
private JMenu
	__Commands_TableAnalyze_JMenu = null;
private JMenuItem
	__Commands_TableAnalyze_CompareTables_JMenuItem;

// Manipulate Table Values
private JMenu
	__Commands_TableManipulate_JMenu = null;
private JMenuItem
	__Commands_TableManipulate_InsertTableColumn_JMenuItem,
	__Commands_TableManipulate_DeleteTableColumns_JMenuItem,
	__Commands_TableManipulate_DeleteTableRows_JMenuItem,
	__Commands_TableManipulate_FormatTableString_JMenuItem,
	__Commands_TableManipulate_ManipulateTableString_JMenuItem,
	__Commands_TableManipulate_SetTableValues_JMenuItem,
	__Commands_TableManipulate_SplitTableColumn_JMenuItem,
	__Commands_TableManipulate_TableMath_JMenuItem,
	__Commands_TableManipulate_TableTimeSeriesMath_JMenuItem,
	__Commands_TableManipulate_InsertTableRow_JMenuItem,
	__Commands_TableManipulate_SortTable_JMenuItem,
	__Commands_TableManipulate_SplitTableRow_JMenuItem;

// Output Table
private JMenu
	__Commands_TableOutput_JMenu = null;
private JMenuItem
	__Commands_TableOutput_WriteTableToDataStore_JMenuItem,
	__Commands_TableOutput_WriteTableToDelimitedFile_JMenuItem,
	__Commands_TableOutput_WriteTableToExcel_JMenuItem,
	__Commands_TableOutput_WriteTableToHTML_JMenuItem;

// Running and Properties
private JMenu
	__Commands_TableRunning_JMenu = null;
private JMenuItem
	__Commands_TableRunning_SetPropertyFromTable_JMenuItem,
	__Commands_TableRunning_CopyPropertiesToTable_JMenuItem;

// Commands Menu for StateMod.

private JMenu
//__Commands_StateMod_ControlData_JMenu,
__Commands_StateMod_Response_JMenu;
private JMenuItem
__Commands_StateMod_Response_ReadResponseFromStateMod_JMenuItem,
__Commands_StateMod_Response_WriteResponseToStateMod_JMenuItem;
private JMenu
__Commands_StateMod_Control_JMenu;
private JMenuItem
__Commands_StateMod_Control_ReadControlFromStateMod_JMenuItem,
__Commands_StateMod_Control_WriteControlToStateMod_JMenuItem;
//private JMenuItem
//__Commands_StateMod_OutputRequest_JMenuItem,
//__Commands_StateMod_ReachData_JMenuItem;

// Stream Gage Data
// Stream Gage Stations
private JMenuItem
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_JMenuItem,
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_JMenuItem,
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_JMenuItem,
	__Commands_StateMod_StreamGageStations_SetStreamGageStation_JMenuItem,
	__Commands_StateMod_StreamGageStations_SortStreamGageStations_JMenuItem,
	__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_JMenuItem,
	__Commands_StateMod_StreamGageStations_ReadNetworkFromStateMod_JMenuItem,
	__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_JMenuItem,
	__Commands_StateMod_StreamGageStations_FillStreamGageStation_JMenuItem,
	__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_JMenuItem,
	__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_JMenuItem;

	//__Commands_StateMod_StreamGageHistoricalTS_JMenuItem,
	//__Commands_StateMod_StreamGageBaseTS_JMenuItem;

// Delay Table Data
// Dalay Tables Monthly
private JMenuItem
	__Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_JMenuItem,
	__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_JMenuItem;
//Dalay Tables Daily
private JMenuItem
	__Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_JMenuItem,
	__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_JMenuItem,
	__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_JMenuItem;

// Diversion Data
// Diversion Stations
private JMenuItem
	__Commands_StateMod_DiversionStations_SetOutputYearType_JMenuItem,
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_JMenuItem,
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_DiversionStations_SetDiversionAggregate_JMenuItem,
	//__Commands_StateMod_DiversionStations_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateMod_DiversionStations_SetDiversionSystem_JMenuItem,
	//__Commands_StateMod_DiversionStations_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_DiversionStations_SortDiversionStations_JMenuItem,
	__Commands_StateMod_DiversionStations_SetDiversionStation_JMenuItem,
	__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_JMenuItem,
	__Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_JMenuItem,
	__Commands_StateMod_DiversionStations_FillDiversionStation_JMenuItem,
	__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_JMenuItem,
	__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_JMenuItem,
	__Commands_StateMod_DiversionStations_WriteDiversionStationsToList_JMenuItem,
	__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_JMenuItem;
JMenu
	__Commands_StateMod_DiversionRights_JMenu;
JMenuItem
	__Commands_StateMod_DiversionRights_ReadDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionRights_ReadDiversionStationsFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionRights_SetDiversionAggregate_JMenuItem,
	__Commands_StateMod_DiversionRights_SetDiversionAggregateFromList_JMenuItem,
	__Commands_StateMod_DiversionRights_SetDiversionSystem_JMenuItem,
	__Commands_StateMod_DiversionRights_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_JMenuItem,
	__Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionRights_SetDiversionRight_JMenuItem,
	__Commands_StateMod_DiversionRights_SortDiversionRights_JMenuItem,
	__Commands_StateMod_DiversionRights_FillDiversionRight_JMenuItem,
	__Commands_StateMod_DiversionRights_WriteDiversionRightsToList_JMenuItem,
	__Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_JMenuItem;
JMenu
	__Commands_StateMod_DiversionHistoricalTSMonthly_JMenu;
JMenuItem
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregate_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregateFromList_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystem_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionRightsFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_JMenuItem,
	__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_JMenuItem;

// Diversions - Historical TS, Daily
// Diversions - Demand TS, Monthly
JMenuItem
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregate_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregateFromList_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystem_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_JMenuItem,
	__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_JMenuItem,

	__Commands_StateMod_DiversionDemandTSOverrideMonthly_JMenuItem,
	__Commands_StateMod_DiversionDemandTSAverageMonthly_JMenuItem;
// Diversions - Demand TS, Daily
private JMenuItem
	//__Commands_StateMod_IrrigationPracticeTS_JMenuItem,
	//__Commands_StateMod_ConsumptiveWaterRequirementTS_JMenuItem,
    __Commands_StateMod_Parcels_ReadParcelsFromHydroBase_JMenuItem,
    __Commands_StateMod_Parcels_ReadParcelsFromIrrigatedLands_JMenuItem,
    __Commands_StateMod_Parcels_SetParcel_JMenuItem,
    __Commands_StateMod_Parcels_SetParcelSurfaceWaterSupply_JMenuItem,
    __Commands_StateMod_Parcels_SetParcelGroundWaterSupply_JMenuItem,
    __Commands_StateMod_Parcels_CheckParcels_JMenuItem,
    __Commands_StateMod_Parcels_CheckIrrigatedLands_JMenuItem,
    __Commands_StateMod_Parcels_WriteParcelsToFile_JMenuItem;
	//__Commands_StateMod_SoilMoisture_JMenuItem;
// Precipitation Data
// Precipitation Data - TS Monthly
//private JMenuItem
//	__Commands_StateMod_PrecipitationTSMonthly_JMenuItem,
// Evaporation Data
// Evaporation Data - TS Monthly
//	__Commands_StateMod_EvaporationTSMonthly_JMenuItem;
// Reservoir Data
// Reservoir Stations
private JMenuItem
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_JMenuItem,
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_JMenuItem,
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_ReservoirStations_SetReservoirAggregate_JMenuItem,
	//__Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_JMenuItem,
	/* TODO SAM 2004-07-07 maybe enable later
	__Commands_StateMod_ReservoirStations_SetReservoirSystem_JMenuItem,
	__Commands_StateMod_ReservoirStations_SetReservoirSystemFromList_JMenuItem,
	*/
	__Commands_StateMod_ReservoirStations_SetReservoirStation_JMenuItem,
	__Commands_StateMod_ReservoirStations_SortReservoirStations_JMenuItem,
	__Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_JMenuItem,
	__Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_JMenuItem,
	__Commands_StateMod_ReservoirStations_FillReservoirStation_JMenuItem,
	__Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_JMenuItem,
	__Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_JMenuItem;
private JMenuItem
// Reservoir Rights
	__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromList_JMenuItem,
	__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_ReservoirRights_SetReservoirAggregate_JMenuItem,
	//__Commands_StateMod_ReservoirRights_SetReservoirAggregateFromList_JMenuItem,
	/* TODO SAM 2004-07-07 maybe enable later
	__Commands_StateMod_ReservoirRights_SetReservoirSystem_JMenuItem,
	__Commands_StateMod_ReservoirRights_SetReservoirSystemFromList_JMenuItem,
	*/
	__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_JMenuItem,
	__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_JMenuItem,
	__Commands_StateMod_ReservoirRights_SetReservoirRight_JMenuItem,
	__Commands_StateMod_ReservoirRights_SortReservoirRights_JMenuItem,
	__Commands_StateMod_ReservoirRights_FillReservoirRight_JMenuItem,
	__Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_JMenuItem,
	__Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_JMenuItem;

// Reservoir Return
private JMenuItem
	__Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_JMenuItem,
	__Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_JMenuItem;

//private JMenuItem
//	__Commands_StateMod_ReservoirContentAndTargetTS_JMenuItem;
// Instream Flow Data
// Instream Flow Stations
private JMenuItem
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_JMenuItem,
	__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_JMenuItem;
// Instream Flow Rights
private JMenuItem
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromList_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromStateMod_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_JMenuItem,
	__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_JMenuItem;
// Instream Flow Demand Average Monthly
private JMenuItem
	// generic setOutputYearType() here
	// Not needed (yet)...
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_JMenuItem,
	//__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowStationsFromStateMod_JMenuItem,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowRightsFromStateMod_JMenuItem,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_JMenuItem,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_JMenuItem,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_JMenuItem;

	//__Commands_StateMod_InstreamFlowDemandTS_JMenuItem;
// Well Data
// Well Stations
private JMenuItem
	__Commands_StateMod_WellStations_ReadWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellStations_ReadWellStationsFromNetwork_JMenuItem,
	__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_WellStations_SetWellAggregate_JMenuItem,
	//__Commands_StateMod_WellStations_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateMod_WellStations_SetWellSystem_JMenuItem,
	//__Commands_StateMod_WellStations_SetWellSystemFromList_JMenuItem,
	//__Commands_StateMod_WellStations_SetDiversionAggregate_JMenuItem,
	//__Commands_StateMod_WellStations_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateMod_WellStations_SetDiversionSystem_JMenuItem,
	//__Commands_StateMod_WellStations_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStation_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_JMenuItem,
	__Commands_StateMod_WellStations_ReadWellRightsFromStateMod_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_JMenuItem,
	__Commands_StateMod_WellStations_SortWellStations_JMenuItem,
	__Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_JMenuItem,
	__Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_JMenuItem,
	__Commands_StateMod_WellStations_FillWellStationsFromNetwork_JMenuItem,
	__Commands_StateMod_WellStations_FillWellStation_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_JMenuItem,
	__Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_JMenuItem,
	__Commands_StateMod_WellStations_WriteWellStationsToList_JMenuItem,
	__Commands_StateMod_WellStations_WriteWellStationsToStateMod_JMenuItem;
// Well rights
private JMenuItem
	__Commands_StateMod_WellRights_ReadWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellRights_ReadWellStationsFromNetwork_JMenuItem,
	__Commands_StateMod_WellRights_ReadWellStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_WellRights_SetWellAggregate_JMenuItem,
	//__Commands_StateMod_WellRights_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateMod_WellRights_SetWellSystem_JMenuItem,
	//__Commands_StateMod_WellRights_SetWellSystemFromList_JMenuItem,
	//__Commands_StateMod_WellRights_SetDiversionAggregate_JMenuItem,
	//__Commands_StateMod_WellRights_SetDiversionAggregateFromList_JMenuItem,
	//__Commands_StateMod_WellRights_SetDiversionSystem_JMenuItem,
	//__Commands_StateMod_WellRights_SetDiversionSystemFromList_JMenuItem,
	__Commands_StateMod_WellRights_ReadParcelsFromHydroBase_JMenuItem,
	__Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_JMenuItem,
	__Commands_StateMod_WellRights_ReadWellRightsFromStateMod_JMenuItem,
	__Commands_StateMod_WellRights_SetWellRight_JMenuItem,
	__Commands_StateMod_WellRights_FillWellRight_JMenuItem,
	__Commands_StateMod_WellRights_MergeWellRights_JMenuItem,
	__Commands_StateMod_WellRights_AggregateWellRights_JMenuItem,
	__Commands_StateMod_WellRights_SortWellRights_JMenuItem,
	__Commands_StateMod_WellRights_CheckWellRights_JMenuItem,
	__Commands_StateMod_WellRights_WriteCheckFile_JMenuItem,
	__Commands_StateMod_WellRights_WriteWellRightsToList_JMenuItem,
	__Commands_StateMod_WellRights_WriteWellRightsToStateMod_JMenuItem;
// Well historical pumping, monthly
private JMenuItem
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromStateMod_JMenuItem,
	//__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregate_JMenuItem,
	//__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregateFromList_JMenuItem,
	//__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystem_JMenuItem,
	//__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystemFromList_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellRightsFromStateMod_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_JMenuItem,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_JMenuItem;
//	__Commands_StateMod_WellHistoricalPumpingTSDaily_JMenuItem;
// Well demand, monthly
JMenuItem
	__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromStateMod_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellAggregate_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellAggregateFromList_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellSystem_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellSystemFromList_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellStation_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_JMenuItem,
	__Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_JMenuItem,

	__Commands_StateMod_WellDemandTSDaily_JMenuItem;

// Plan Data
// Plan Stations
private JMenuItem
	//__Commands_StateMod_PlanStations_ReadPlanStationsFromList_JMenuItem,
	//__Commands_StateMod_PlanStations_ReadPlanStationsFromNetwork_JMenuItem,
	__Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_JMenuItem,
	__Commands_StateMod_PlanStations_SetPlanStation_JMenuItem,
	//__Commands_StateMod_PlanStations_SetPlanStationsFromList_JMenuItem,
	//__Commands_StateMod_PlanStations_SortPlanStations_JMenuItem,
	//__Commands_StateMod_PlanStations_FillPlanStationsFromNetwork_JMenuItem,
	//__Commands_StateMod_PlanStations_FillPlanStation_JMenuItem,
	//__Commands_StateMod_PlanStations_WritePlanStationsToList_JMenuItem,
	__Commands_StateMod_PlanStations_WritePlanStationsToStateMod_JMenuItem;

// Plan (Well Augmentation)
private JMenuItem
	__Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_JMenuItem,
	__Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_JMenuItem;

//Plan Return
private JMenuItem
	__Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_JMenuItem,
	__Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_JMenuItem;

private JMenuItem __Commands_StateMod_StreamEstimateData_JMenuItem;
// Stream Estimate Data
// Stream Estimate Stations
private JMenuItem
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_ReadNetworkFromStateMod_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_JMenuItem,
	__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_JMenuItem;
// Stream Estimare coefficients
private JMenuItem
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromList_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromNetwork_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromStateMod_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_SortStreamEstimateStations_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_JMenuItem,
	__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_JMenuItem;
	//__Commands_StateMod_StreamEstimateBaseTS_JMenuItem;
// River Network Data
// Network (StateDMI)
private JMenuItem
	__Commands_StateMod_Network_ReadNetworkFromStateMod_JMenuItem,
	__Commands_StateMod_Network_AppendNetwork_JMenuItem,
	__Commands_StateMod_Network_ReadRiverNetworkFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadStreamGageStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadDiversionStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadReservoirStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadWellStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_JMenuItem,
	__Commands_StateMod_Network_CreateNetworkFromRiverNetwork_JMenuItem,
	__Commands_StateMod_Network_FillNetworkFromHydroBase_JMenuItem,
	__Commands_StateMod_Network_WriteNetworkToList_JMenuItem,
	__Commands_StateMod_Network_WriteNetworkToStateMod_JMenuItem,
	__Commands_StateMod_Network_PrintNetwork_JMenuItem;
// River Network (StateMod)
private JMenuItem
	__Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_JMenuItem,
	__Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_JMenuItem,
	__Commands_StateMod_RiverNetwork_SetRiverNetworkNode_JMenuItem,
	__Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_JMenuItem,
	__Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_JMenuItem,
	__Commands_StateMod_RiverNetwork_FillRiverNetworkNode_JMenuItem,
	__Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_JMenuItem,
	__Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_JMenuItem;
private JMenu
	__Commands_StateMod_OperationalData_JMenu,
	__Commands_StateMod_OperationalRights_JMenu;
private JMenuItem
	__Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_JMenuItem,
	__Commands_StateMod_OperationalRights_SetOperationalRight_JMenuItem,
	//__Commands_StateMod_OperationalRights_SortOperationalRights_JMenuItem,
	__Commands_StateMod_OperationalRights_CheckOperationalRights_JMenuItem,
	__Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_JMenuItem;
private JMenuItem
	__Commands_StateMod_DownstreamCallTSDaily_JMenuItem,
	__Commands_StateMod_SanJuanSedimentRecoveryPlan_JMenuItem,
	__Commands_StateMod_RioGrandeSpill_JMenuItem;
private JMenuItem
	__Commands_StateMod_SpatialData_JMenuItem;
private JMenu
	__Commands_StateMod_GeoViewProject_JMenu;

// Run...

private JMenu
	__Run_JMenu;
private JMenuItem
	__Run_AllCommandsCreateOutput_JMenuItem,
	__Run_AllCommandsIgnoreOutput_JMenuItem,
	__Run_SelectedCommandsCreateOutput_JMenuItem,
	__Run_SelectedCommandsIgnoreOutput_JMenuItem,
	__Run_CommandsFromFile_JMenuItem,
	__Run_CancelCommandProcessing_JMenuItem,
	//__Run_RunCommandFile_JMenuItem,
	__Run_RunStateCUVersion_JMenuItem,
	__Run_RunStateModVersion_JMenuItem;

	// Results menu (StateCU).

private JMenu
	__Results_JMenu;

private JMenuItem
	__Results_StateCU_ControlData_JMenuItem,
	__Results_StateCU_ClimateStationsData_JMenuItem,
	__Results_StateCU_CropCharacteristicsData_JMenuItem,
	__Results_StateCU_DelayTablesData_JMenuItem,
	__Results_StateCU_CULocationsData_JMenuItem;

	// Results Menu (StateMod).

private JMenuItem
	__Results_StateMod_RiverData_JMenuItem,
	__Results_StateMod_DelayTableData_JMenuItem,
	__Results_StateMod_DiversionData_JMenuItem,
	__Results_StateMod_PrecipitationData_JMenuItem,
	__Results_StateMod_EvaporationData_JMenuItem,
	__Results_StateMod_ReservoirData_JMenuItem,
	__Results_StateMod_InstreamFlowData_JMenuItem,
	__Results_StateMod_WellData_JMenuItem,
	__Results_StateMod_RiverNetworkData_JMenuItem,
	__Results_StateMod_OperationalData_JMenuItem;

private JMenu
	__Tools_JMenu,
	__Tools_CompareFiles_JMenu;
private JMenuItem
	__Tools_AdministrationNumberCalculator_JMenuItem,
	__Tools_CompareFiles_StateModWellRights_JMenuItem,
	__Tools_ListSurfaceWaterDiversions_JMenuItem,
	__Tools_ListWellStationRightTotals_JMenuItem,
	__Tools_HydrobaseParcelWaterSupply_JMenuItem,
	__Tools_MergeListFileColumns_JMenuItem,
	__Tools_ViewLogFile_Startup_JMenuItem,

	__Help_AboutStateDMI_JMenuItem,
	__Help_ViewDocumentation_JMenuItem = null,
	__Help_ViewDocumentation_ReleaseNotes_JMenuItem = null,
	__Help_ViewDocumentation_UserManual_JMenuItem = null,
	__Help_ViewDocumentation_CommandReference_JMenuItem = null,
	__Help_ViewDocumentation_DatastoreReference_JMenuItem = null,
	__Help_ViewDocumentation_Troubleshooting_JMenuItem = null,
	__Help_ViewTrainingMaterials_JMenuItem = null;

/**
Properties for the application, currently only containing "WorkingDir".
*/
private PropList __props;

/**
HydroBase DMI object used for all HydroBase queries (set to null if the connection is not made).
*/
private HydroBaseDMI __hbdmi = null;

/**
Region1 strings for use with StateCU.
These are initialized in editCommand() and are therefore only used when editing.
Later, need to possibly initialize based on a command.
For now default region1 to County and region2 to HUC from HydroBase.
*/
private List<String> __region1_List = null;
private List<Integer> __region2_List = null;

/**
Valid Cropchar CU methods from HydroBase.  These are used when selecting data for the StateCU CCH file.
*/
private List<String> __cropcharCuMethod_List = null;

/**
Valid BlaneyCriddle CU methods from HydroBase.  These are used when selecting data for the StateCU KBC files.
*/
private List<String> __blaneyCriddleCuMethod_List = null;

/**
Valid PenManMontieth CU methods from HydroBase.  These are used when selecting data for the StateCU KPM files.
*/
private List<String> __penmanMonteithCuMethod_List = null;

// Strings representing commands and options in the various menus and buttons,
// listed from left to right and top to bottom as they appear in the interface.

private String
	// Buttons on the interface.

	__Button_RunAllCommands_String = "Run All Commands",
	__Button_RunSelectedCommands_String = "Run Selected Commands",
	__Button_ClearCommands_String = "Clear Commands",

	// Popup menu.

	__CommandsPopup_ShowCommandStatus_String = "Show Command Status (Success/Warning/Failure)",
	__CommandsPopup_FindCommandsUsingString_String = "Find command(s) using substring...",
	__CommandsPopup_FindCommandUsingLineNumber_String = "Find command using line number...",

	// File menu.

	__File_String = "File",

	__File_Open_String = "Open",
	__File_Open_CommandFile_String = "Command File ...",
	__File_Open_DataSet_String = "Data Set (Under Development)...",
	__File_Open_DataSetComponent_String = "Data Set Component (Under Development)",
	__File_Open_DataSetComponent_StateCU_Locations_String =	"CU Locations...",
	__File_Open_DataSetComponent_StateCU_CropCharacteristics_String = "Crop Characteristics ...",
	__File_Open_DataSetComponent_StateCU_BlaneyCriddle_String =	"Blaney-Criddle Crop Coefficients ...",
	__File_Open_DataSetComponent_StateCU_ClimateStations_String = "Climate Stations ...",
	__File_Open_ModelNetwork_String = "Model Network ...",
	__File_Open_HydroBase_String = "HydroBase ...",

	MENU_File_New = "New",
	MENU_File_New_DataSet = "Data Set",
		MENU_File_New_DataSet_StateCU_ClimateStations =	"Climate Stations",
			MENU_File_New_DataSet_StateCU_ClimateStations_FromList = "From List...",
			MENU_File_New_DataSet_StateCU_ClimateStations_FromHydroBase = "From HydroBase...",
		MENU_File_New_DataSet_StateCU_Structures = "Structures",
			MENU_File_New_DataSet_StateCU_Structures_FromList = "From List...",
		MENU_File_New_DataSet_StateCU_WaterSupplyLimited = "Structures (Water Supply Limited)",
		MENU_File_New_DataSet_StateCU_WaterSupplyLimitedByWaterRights =
			"Structures (Water Supply Limited by Water Rights)",
		MENU_File_New_DataSet_StateCU_RiverDepletions =	"Structures (River Depletions)",
		MENU_File_New_DataSet_StateCU_OtherUses = "Other Uses",

	MENU_File_New_DataSet_StateMod_Historical = "Historical Data (Natural flows, calibration)...",
	MENU_File_New_DataSet_StateMod_Demands = "Demands Data Set (Simulation)...",

	MENU_File_New_DataSetComponent = "Data Set Component",
		MENU_File_New_DataSetComponent_StateCU_Locations = "CU Locations",
			MENU_File_New_DataSetComponent_StateCU_Locations_FromList = "From List...",
		MENU_File_New_DataSetComponent_StateCU_CropCharacteristics = "Crop Characteristics",
			MENU_File_New_DataSetComponent_StateCU_CropCharacteristics_FromList = "From List...",
		MENU_File_New_DataSetComponent_StateCU_BlaneyCriddle = "Blaney-Criddel Crop Coefficients",
			MENU_File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList = "From List...",
		MENU_File_New_DataSetComponent_StateCU_ClimateStations = "Climate Stations",
			MENU_File_New_DataSetComponent_StateCU_ClimateStations_FromList = "From List...",
	__File_New_CommandFile_String = "Command File",
	__File_New_NewModelNetwork_String = "Model Network ...",

	__File_Save_String = "Save",

	__File_Save_Commands_String = "Commands",
	__File_Save_CommandsAs_String = "Commands As ...",

	__File_Save_DataSet_String = "Data Set",

	__File_Print_String = "Print",
	__File_Print_Commands_String = "Commands...",

	__File_Properties_String = "Properties",
	__File_Properties_HydroBase_String = "HydroBase",
	__File_Properties_DataSet_String = "Data Set",
	//__File_SetWorkingDirectory_String = "Set Working Directory ...",
	__File_Test_String = "Test",
	__File_SwitchToStateCU_String = "Switch to StateCU",
	__File_SwitchToStateMod_String = "Switch to StateMod",
	__File_Exit_String = "Exit",

	// Edit menu.

	__Edit_CutCommands_String = "Cut Command(s)",
	__Edit_CopyCommands_String = "Copy Command(s)",
	__Edit_PasteCommands_String = "Paste Command(s) (After Selected)",

	__Edit_DeleteCommands_String = "Delete Command(s)",

	__Edit_SelectAllCommands_String = "Select All Commands",
	__Edit_DeselectAllCommands_String = "Deselect All Commands",

	__Edit_CommandWithErrorChecking_String = "Command...",
	__Edit_CommandFile_String = "Command File...",

	__Edit_ConvertSelectedCommandsToComments_String = "Convert selected commands to # comments",
	__Edit_ConvertSelectedCommandsFromComments_String = "Convert selected commands from # comments",

	// View menu.

	__View_CommandFileDiff_String = "Command File Diff",
	__View_DataStores_String = "Datastores",
	__View_DataSetManager_String = "Data Set Manager",
	__View_Map_String = "Map",
	__View_ModelNetwork_String = "Model Network",
	__View_ThreeLevelCommandsMenu_String = "Three-level Commands Menu",

	// Commands Menu.

	// Shared.

	__Commands_Shared_WriteCheckFile_String = "WriteCheckFile() ...",

	// StateCU sub-menus (see the first item for the file being edited).

	__Commands_StateCU_ClimateStationsData_String =	"Climate Stations Data",
	__Commands_StateCU_ClimateStations_String = "Climate Stations",
	__Commands_StateCU_ClimateStations_TemperatureTS_String = "Temperature TS (Monthly Average)",
	__Commands_StateCU_ClimateStations_FrostDatesTS_String = "Frost Dates TS (Yearly)",
	__Commands_StateCU_ClimateStations_PrecipitationTS_String = "Precipitation TS (Monthly)",
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromList_String =	"ReadClimateStationsFromList() ...",
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_String = "ReadClimateStationsFromStateCU() ...",
	__Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_String = "ReadClimateStationsFromHydroBase() ...",
	__Commands_StateCU_ClimateStations_SetClimateStation_String = "SetClimateStation() ...",
	__Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_String = "FillClimateStationsFromHydroBase() ...",
	__Commands_StateCU_ClimateStations_FillClimateStation_String = "FillClimateStation() ...",
	__Commands_StateCU_ClimateStations_SortClimateStations_String = "SortClimateStations() ...",
	__Commands_StateCU_ClimateStations_WriteClimateStationsToList_String = "WriteClimateStationsToList() ...",
	__Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_String = "WriteClimateStationsToStateCU() ...",
	__Commands_StateCU_ClimateStations_CheckClimateStations_String = "CheckClimateStations() ...",

	__Commands_StateCU_CropCharacteristicsData_String = "Crop Characteristics/Coefficients Data",
	__Commands_StateCU_CropCharacteristics_String =	"Crop Characteristics",
	__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_String = "ReadCropCharacteristicsFromStateCU() ...",
	__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_String = "ReadCropCharacteristicsFromHydroBase() ...",
	__Commands_StateCU_CropCharacteristics_SetCropCharacteristics_String = "SetCropCharacteristics() ...",
	__Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_String = "TranslateCropCharacteristics() ...",
	__Commands_StateCU_CropCharacteristics_SortCropCharacteristics_String = "SortCropCharacteristics() ...",
	__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_String = "WriteCropCharacteristicsToList() ...",
	__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_String = "WriteCropCharacteristicsToStateCU() ...",
	__Commands_StateCU_CropCharacteristics_CheckCropCharacteristics_String = "CheckCropCharacteristics() ...",

	__Commands_StateCU_BlaneyCriddle_String = "Blaney-Criddle Crop Coefficients",
	__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_String = "ReadBlaneyCriddleFromStateCU() ...",
	__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_String = "ReadBlaneyCriddleFromHydroBase() ...",
	__Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_String = "SetBlaneyCriddle() ...",
	__Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_String = "TranslateBlaneyCriddle() ...",
	__Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_String = "SortBlaneyCriddle() ...",
	__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_String = "WriteBlaneyCriddleToList() ...",
	__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_String = "WriteBlaneyCriddleToStateCU() ...",
	__Commands_StateCU_BlaneyCriddle_CheckBlaneyCriddle_String = "CheckBlaneyCriddle() ...",

	__Commands_StateCU_PenmanMonteith_String = "Penman-Monteith Crop Coefficients",
	__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_String = "ReadPenmanMonteithFromStateCU() ...",
	__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_String = "ReadPenmanMonteithFromHydroBase() ...",
	__Commands_StateCU_PenmanMonteith_SetPenmanMonteith_String = "SetPenmanMonteith() ...",
	__Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_String = "TranslatePenmanMonteith() ...",
	__Commands_StateCU_PenmanMonteith_SortPenmanMonteith_String = "SortPenmanMonteith() ...",
	__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_String = "WritePenmanMonteithToList() ...",
	__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_String = "WritePenmanMonteithToStateCU() ...",
	__Commands_StateCU_PenmanMonteith_CheckPenmanMonteith_String = "CheckPenmanMonteith() ...",

	// TODO SAM 2010-02-04 Not currently used (but was at one time)
	//__Commands_StateCU_DelayTablesData_String = "Delay Tables Data",
	//__Commands_StateCU_DelayTables_String = "Delay Tables",
	//__Commands_StateCU_DelayTables_ReadDelayTablesFromStateMod_String = "ReadDelayTablesFromStateMod() ...",
	//__Commands_StateCU_DelayTables_WriteDelayTablesToList_String = "WriteStateCUDelayTablesToList() ...",
	//__Commands_StateCU_DelayTables_WriteDelayTablesToStateCU_String = "WriteDelayTablesToStateCU() ...",
	//__Commands_StateCU_DelayTables_CheckDelayTables_String = "CheckDelayTables() ...",

	__Commands_StateCU_CULocationsData_String = "CU Locations Data",
	__Commands_StateCU_CULocations_String = "CU Locations",
	__Commands_StateCU_CULocations_ReadCULocationsFromList_String = "ReadCULocationsFromList() ...",
	__Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String = "ReadCULocationsFromStateCU() ...",
	__Commands_StateCU_CULocations_ReadCULocationsFromStateMod_String = "ReadCULocationsFromStateMod() ...",
	__Commands_StateCU_CULocations_SetCULocation_String = "SetCULocation() ...",
	__Commands_StateCU_CULocations_SetCULocationsFromList_String = "SetCULocationsFromList() ...",
	__Commands_StateCU_CULocations_SetDiversionAggregate_String = "SetDiversionAggregate() ...",
	__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String = "SetDiversionAggregateFromList() ...",
	__Commands_StateCU_CULocations_SetDiversionSystem_String = "SetDiversionSystem() ...",
	__Commands_StateCU_CULocations_SetDiversionSystemFromList_String = "SetDiversionSystemFromList() ...",
	__Commands_StateCU_CULocations_SetWellAggregate_String = "SetWellAggregate() ...",
	__Commands_StateCU_CULocations_SetWellAggregateFromList_String = "SetWellAggregateFromList() ...",
	__Commands_StateCU_CULocations_SetWellSystem_String = "SetWellSystem() ...",
	__Commands_StateCU_CULocations_SetWellSystemFromList_String = "SetWellSystemFromList() ...",
	__Commands_StateCU_CULocations_SortCULocations_String = "SortCULocations() ...",
	__Commands_StateCU_CULocations_FillCULocation_String = "FillCULocation() ...",
	__Commands_StateCU_CULocations_FillCULocationsFromList_String = "FillCULocationsFromList() ...",
	__Commands_StateCU_CULocations_FillCULocationsFromHydroBase_String = "FillCULocationsFromHydroBase() ...",
	// --
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_String = "SetCULocationClimateStationWeightsFromList() ...",
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_String = "[Legacy] SetCULocationClimateStationWeightsFromHydroBase() ...",
	__Commands_StateCU_CULocations_SetCULocationClimateStationWeights_String = "SetCULocationClimateStationWeights() ...",
	__Commands_StateCU_CULocations_FillCULocationClimateStationWeights_String = "FillCULocationClimateStationWeights() ...",
	// --
	__Commands_StateCU_CULocations_WriteCULocationsToList_String = "WriteCULocationsToList() ...",
	__Commands_StateCU_CULocations_WriteCULocationsToStateCU_String = "WriteCULocationsToStateCU() ...",
	__Commands_StateCU_CULocations_CheckCULocations_String = "CheckCULocations() ...",

	// Parcels.

	__Commands_StateCU_Parcels_String = "Parcels",
	__Commands_StateCU_Parcels_ReadParcelsFromHydroBase_String = "ReadParcelsFromHydroBase() ...",
	__Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_String = "ReadParcelsFromIrrigatedLands() ...",
	__Commands_StateCU_Parcels_SetParcel_String = "SetParcel() ...",
	__Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_String = "SetParcelSurfaceWaterSupply() ...",
	__Commands_StateCU_Parcels_SetParcelGroundWaterSupply_String = "SetParcelGroundWaterSupply() ...",
	__Commands_StateCU_Parcels_CheckParcels_String = "CheckParcels() ...",
	__Commands_StateCU_Parcels_CheckIrrigatedLands_String = "CheckIrrigatedLands() ...",
	__Commands_StateCU_Parcels_WriteParcelsToFile_String = "WriteParcelsToFile() ...",

	// CDS - crop pattern time series.

	__Commands_StateCU_CropPatternTS_String = "Crop Pattern TS (Yearly)",
		// Also has a SetOutputPeriod() here.
		// Also has a SetOutputAnnualAverage() here.
	__Commands_StateCU_CropPatternTS_ReadCULocationsFromList_String = __Commands_StateCU_CULocations_ReadCULocationsFromList_String,
	__Commands_StateCU_CropPatternTS_ReadCULocationsFromStateCU_String = __Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String,
	__Commands_StateCU_CropPatternTS_SetDiversionAggregate_String = __Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateCU_CropPatternTS_SetDiversionAggregateFromList_String = __Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateCU_CropPatternTS_SetDiversionSystem_String = __Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateCU_CropPatternTS_SetDiversionSystemFromList_String = __Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateCU_CropPatternTS_SetWellAggregate_String = __Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateCU_CropPatternTS_SetWellAggregateFromList_String = __Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateCU_CropPatternTS_SetWellSystem_String = __Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateCU_CropPatternTS_SetWellSystemFromList_String = __Commands_StateCU_CULocations_SetWellSystemFromList_String,
	__Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_String = "CreateCropPatternTSForCULocations() ...",
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_String = "ReadCropPatternTSFromStateCU() ...",
	// FIXME SAM 2008-12-30 Remove if not needed.
	//__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_String = "OLD: ReadCropPatternTSFromDBF() ...",
	__Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_String = "SetCropPatternTSFromList() ...",
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_String = "ReadCropPatternTSFromHydroBase() ...",
	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_String = "ReadCropPatternTSFromParcels() ...",
	__Commands_StateCU_CropPatternTS_SetCropPatternTS_String = "SetCropPatternTS() ...",
	__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_String = "TranslateCropPatternTS() ...",
	__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_String = "RemoveCropPatternTS() ...",
	// FIXME SAM 2008-12-30 Remove if not needed.
	//__Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_String = "OLD: ReadAgStatsTSFromDateValue() ...",
	__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_String = "FillCropPatternTSConstant() ...",
	__Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_String = "FillCropPatternTSRepeat() ...",
	__Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_String = "FillCropPatternTSInterpolate() ...",
	// FIXME SAM 2008-12-30 Remove if not needed.
	//__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_String = "OLD: FillCropPatternTSProrateAgStats() ...",
	__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_String = "[Legacy] FillCropPatternTSUsingWellRights() ...",
	__Commands_StateCU_CropPatternTS_SortCropPatternTS_String = "SortCropPatternTS() ...",
	__Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_String = "WriteCropPatternTSToStateCU() ...",
	__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_String = "WriteCropPatternTSToDateValue() ...",
	// TODO smalers 2021-01-24 - used for supplemental data?  Not sure if it was fully ever implemented.
	//__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_String = "WriteCropPatternParcelsToFile() ...",
	__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_String = "CompareCropPatternTSFiles() ...",
	__Commands_StateCU_CropPatternTS_CheckCropPatternTS_String = "CheckCropPatternTS() ...",

	__Commands_StateCU_IrrigationPracticeTS_String = "Irrigation Practice TS (Yearly)",
		// Also has a setOutputPeriod() here.
		// Also has a setOutputAnnualAverage() here.
	__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromList_String = __Commands_StateCU_CULocations_ReadCULocationsFromList_String,
	__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromStateCU_String = __Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String,
	__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregate_String = __Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregateFromList_String = __Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystem_String = __Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystemFromList_String = __Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateCU_IrrigationPracticeTS_SetWellAggregate_String = __Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateCU_IrrigationPracticeTS_SetWellAggregateFromList_String = __Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateCU_IrrigationPracticeTS_SetWellSystem_String = __Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateCU_IrrigationPracticeTS_SetWellSystemFromList_String = __Commands_StateCU_CULocations_SetWellSystemFromList_String,
	__Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_String = "CreateIrrigationPracticeTSForCULocations() ...",
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_String = "ReadIrrigationPracticeTSFromStateCU() ...",
	// TODO SAM 2005-03-07 Disable and only read from HydroBase.
	//__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromDBF_String =
	//	__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_String,
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_String = "ReadIrrigationPracticeTSFromHydroBase() ...",
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_String = "ReadIrrigationPracticeTSFromList() ...",
	__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_String = "ReadIrrigationPracticeTSFromParcels() ...",
	__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_String = "1: " + __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_String,
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_String = "2: SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage() ...",
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_String = "SetIrrigationPracticeTSPumpingMaxUsingWellRights() ...",
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_String = "SetIrrigationPracticeTSSprinklerAcreageFromList() ...",
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_String = "SetIrrigationPracticeTS() ...",
	__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_String = "SetIrrigationPracticeTSFromList() ...",
	__Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_String =	"1: ReadWellRightsFromStateMod() ...",
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_String =	"2: FillIrrigationPracticeTSAcreageUsingWellRights() ...",
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_String = "FillIrrigationPracticeTSInterpolate() ...",
	__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_String = "FillIrrigationPracticeTSRepeat() ...",
	__Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_String = "SortIrrigationPracticeTS() ...",
	__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_String = "WriteIrrigationPracticeTSToDateValue() ...",
	__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_String = "WriteIrrigationPracticeTSToStateCU() ...",
	__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_String = "CompareIrrigationPracticeTSFiles() ...",
	__Commands_StateCU_IrrigationPracticeTS_CheckIrrigationPracticeTS_String = "CheckIrrigationPracticeTS() ...",

	// Reuse StateMod.
	//__Commands_StateCU_DiversionTS_String = "Diversion TS (Monthly)",
	//__Commands_StateCU_WellPumpingTS_String = "Well Pumping TS (Monthly)",
	//__Commands_StateCU_DiversionRights_String = "Diversion Rights",
	__Commands_StateCU_DelayTableAssignment_String = "Delay Table Assignment",
	__Commands_StateCU_DelayTableAssignment_ReadCULocationsFromStateCU_String = __Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String,
	__Commands_StateCU_DelayTableAssignment_SetCULocationDelayTableAssignmentsFromStateMod_String = "SetCULocationDelayTableAssignmentsFromStateMod() ...",
	__Commands_StateCU_DelayTableAssignment_WriteCULocationDelayTableAssignmentsToList_String = "WriteCULocationDelayTableAssignmentsToList() ...",
	__Commands_StateCU_DelayTableAssignment_WriteCULocationDelayTableAssignmentsToStateCU_String = "WriteCULocationDelayTableAssignmentsToStateCU() ...",
	__Commands_StateCU_DelayTableAssignment_CheckCULocationDelayTableAssignments_String = "CheckCULocationDelayTableAssignments() ...",

	// Datastore Commands.
	__Commands_Datastore_String = "Datastore Processing",

	// Output File Processing Commands.

	__Commands_Output_String = "Output File Processing",
	__Commands_Output_SplitStateModReport_String = "SplitStateModReport()... <split StateMod report file>",

	// Spatial Commands.

	__Commands_Spatial_String = "Spatial Processing",
	__Commands_Spatial_WriteTableToGeoJSON_String = "WriteTableToGeoJSON()... <write table to a GeoJSON file>",
	__Commands_Spatial_WriteTableToShapefile_String = "WriteTableToShapefile()... <write table to a Shapefile>",

	// Spreadsheet Commands.

	__Commands_Spreadsheet_String = "Spreadsheet Processing",
	__Commands_Spreadsheet_NewExcelWorkbook_String = "NewExcelWorkbook()... <create a new Excel workbook file>",
	__Commands_Spreadsheet_ReadExcelWorkbook_String = "ReadExcelWorkbook()... <read an Excel workbook file>",
	__Commands_Spreadsheet_ReadTableFromExcel_String = "ReadTableFromExcel()... <read a table from an Excel file>",
	__Commands_Spreadsheet_ReadTableCellsFromExcel_String = "ReadTableCellsFromExcel()... <read a table's cells from an Excel file>",
	__Commands_Spreadsheet_ReadPropertiesFromExcel_String = "ReadPropertiesFromExcel()... <read processor properties from an Excel file>",
	__Commands_Spreadsheet_SetExcelCell_String = "SetExcelCell()... <set single Excel value and formatting>",
	__Commands_Spreadsheet_SetExcelWorksheetViewProperties_String = "SetExcelWorksheetViewProperties()... <set Excel view properties>",
	__Commands_Spreadsheet_WriteTableToExcel_String = "WriteTableToExcel()... <write a table to an Excel file>",
	__Commands_Spreadsheet_WriteTableCellsToExcel_String = "WriteTableCellsToExcel()... <write a table's cells to an Excel file>",
	__Commands_Spreadsheet_WriteTimeSeriesToExcel_String = "WriteTimeSeriesToExcel()... <write 1+ time series to an Excel file>",
	__Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String = "WriteTimeSeriesToExcelBlock()... <write 1+ time series to an Excel file as data block(s)>",
	__Commands_Spreadsheet_CloseExcelWorkbook_String = "CloseExcelWorkbook()... <close and optionally write an Excel file>",

	// General commands.

	__Commands_General_Comments_String = "General - Comments",
	__Commands_General_Comments_Comment_String = "# comment(s) ...",
	__Commands_General_Comments_StartComment_String = "/* <start comment block>",
	__Commands_General_Comments_EndComment_String = "*/ <end comment block>",
    __Commands_General_Comments_ReadOnlyComment_String = "#@readOnly <insert read-only comment>",
    __Commands_General_Comments_EnabledComment_String = "#@enabled False <used to disable command file for testing>",
    __Commands_General_Comments_ExpectedStatusFailureComment_String = "#@expectedStatus Failure <used to test commands>",
    __Commands_General_Comments_ExpectedStatusWarningComment_String = "#@expectedStatus Warning <used to test commands>",
    __Commands_General_Comments_RequireApplicationComment_String = "#@require application ... <check application version dependency>",
    __Commands_General_Comments_RequireDatastoreComment_String = "#@require datastore ... <check datastore version dependency>",

	__Commands_General_FileHandling_String = "General - File Handling",
	__Commands_General_FileHandling_FTPGet_String = "FTPGet()... <get file(s) using FTP>",
	__Commands_General_FileHandling_WebGet_String = "WebGet()... <get file(s) from the web>",
	__Commands_General_FileHandling_MergeListFileColumns_String = "MergeListFileColumns() ...",
    __Commands_General_FileHandling_RemoveFile_String = "RemoveFile()... <remove file(s)>",
    __Commands_General_FileHandling_AppendFile_String = "AppendFile()... <append file(s)>",
    __Commands_General_FileHandling_CopyFile_String = "CopyFile()... <copy file(s)>",
    __Commands_General_FileHandling_ListFiles_String = "ListFiles()... <list file(s) to a table>",
    __Commands_General_FileHandling_UnzipFile_String = "UnzipFile()... <unzip file>",

	__Commands_General_HydroBase_String = "General - HydroBase",
	__Commands_General_HydroBase_OpenHydroBase_String = "OpenHydroBase() ...",

	__Commands_General_Logging_String = "General - Logging and Messaging",
	__Commands_General_Logging_StartLog_String = "StartLog() ...",
	__Commands_General_Logging_SetDebugLevel_String = "SetDebugLevel() ...",
	__Commands_General_Logging_SetWarningLevel_String = "SetWarningLevel() ...",
	__Commands_General_Logging_Message_String = "Message()... <print a message>",

	__Commands_General_Running_String = "General - Running and Properties",
	__Commands_General_Running_SetProperty_String = "SetProperty()... <set processor property>",
	__Commands_General_Running_FormatDateTimeProperty_String = "FormatDateTimeProperty()... <format date/time property as string property>",
	__Commands_General_Running_FormatStringProperty_String = "FormatStringProperty()... <format a string property>",
	// This menu is reused in different menus.
	__Commands_General_Running_SetOutputPeriod_String = "SetOutputPeriod() ...",
	// This menu is reused in different menus.
	__Commands_General_Running_SetOutputYearType_String = "SetOutputYearType() ...",
	__Commands_General_Running_RunCommands_String = "RunCommands()... <run a command file>",
	__Commands_General_Running_RunProgram_String = "RunProgram()... <run external program>",
    __Commands_General_Running_RunPython_String = "RunPython()... <run a Python script>",
    __Commands_General_Running_RunR_String = "RunR()... <run an R script>",
	__Commands_General_Running_Exit_String = "Exit() ",
	__Commands_General_Running_SetWorkingDir_String = "SetWorkingDir() ...",
	__Commands_General_Running_WritePropertiesToFile_String = "WritePropertiesToFile()... <write processor properties to file>",

	__Commands_General_TestProcessing_String = "General - Test Processing",
	__Commands_General_TestProcessing_StartRegressionTestResultsReport_String = "StartRegressionTestResultsReport()... <for test results>",
	__Commands_General_TestProcessing_CompareFiles_String = "CompareFiles()... <compare files, to test software>",
	__Commands_General_TestProcessing_WriteProperty_String = "WriteProperty()... <write processor property, to test software>",
	__Commands_General_TestProcessing_CreateRegressionTestCommandFile_String = "CreateRegressionTestCommandFile()... <to test software>";

	// Table Commands.

	private String

	__Commands_Table_String = "Commands (Table)",

	// Create, Copy, Free Table
	__Commands_TableCreate_String = "Create, Copy, Free Table",
	__Commands_TableCreate_NewTable_String = "NewTable()... <create a new empty table>",
	__Commands_TableCreate_CopyTable_String = "CopyTable()... <create a new table as a full/partial copy of another>",
	__Commands_TableCreate_FreeTable_String = "FreeTable()... <free a table (will not be available to later commands)>",

	// Read Table
	__Commands_TableRead_String = "Read Table",
	__Commands_TableRead_ReadTableFromDataStore_String = "ReadTableFromDataStore()... <read a table from a database datastore>",
	__Commands_TableRead_ReadTableFromDBF_String = "ReadTableFromDBF()... <read a table from a dBASE file>",
	__Commands_TableRead_ReadTableFromDelimitedFile_String = "ReadTableFromDelimitedFile()... <read a table from a delimited file>",
	__Commands_TableRead_ReadTableFromExcel_String = "ReadTableFromExcel()... <read a table from an Excel file>",
	__Commands_TableRead_ReadTableFromFixedFormatFile_String = "ReadTableFromFixedFormatFile()... <read a table from a fixed format file>",
	__Commands_TableRead_ReadTableFromJSON_String = "ReadTableFromJSON()... <read a table from a JSON file>", //not being used
	__Commands_TableRead_ReadTableFromXML_String = "ReadTableFromXML()... <read a table from an XML file>", //not being used

	// Append, Join Tables
	__Commands_TableJoin_String = "Append, Join Tables",
	__Commands_TableJoin_AppendTable_String = "AppendTable()... <append a table's rows to another table>",
	__Commands_TableJoin_JoinTables_String = "JoinTables()... <join a table's rows to another table by matching column value(s)>",

	// Manipulate Table Values
	__Commands_TableManipulate_String = "Manipulate Table Values",
	__Commands_TableManipulate_InsertTableColumn_String = "InsertTableColumn()... <insert table column>",
	__Commands_TableManipulate_DeleteTableColumns_String = "DeleteTableColumns()... <delete table column(s)>",
	__Commands_TableManipulate_DeleteTableRows_String = "DeleteTableRows()... <delete table row(s)>",
	__Commands_TableManipulate_FormatTableDateTime_String = "FormatTableDateTime()... <format table date/time column into output column>",
	__Commands_TableManipulate_FormatTableString_String = "FormatTableString()... <format table columns into a string column>",
	__Commands_TableManipulate_ManipulateTableString_String = "ManipulateTableString()... <perform simple manipulation on table strings>",
	__Commands_TableManipulate_SetTableValues_String = "SetTableValues()... <set table cell values>",
	__Commands_TableManipulate_SplitTableColumn_String = "SplitTableColumn()... <split a column into multiple columns>",
	__Commands_TableManipulate_TableMath_String = "TableMath()... <perform simple math on table columns>",
	__Commands_TableManipulate_TableTimeSeriesMath_String = "TableTimeSeriesMath()... <perform simple math on table columns and time series>",
	__Commands_TableManipulate_InsertTableRow_String = "InsertTableRow()... <insert table row(s)>",
	__Commands_TableManipulate_SortTable_String = "SortTable()... <sort a table's rows>",
	__Commands_TableManipulate_SplitTableRow_String = "SplitTableRow()... <split a row into multiple rows>",

	// Analyze Tables
	__Commands_TableAnalyze_String = "Analyze Tables",
	__Commands_TableAnalyze_CompareTables_String = "CompareTables()... <compare two tables (indicate differences)>",

	// Output Table
	__Commands_TableOutput_String = "Output Table",
	__Commands_TableOutput_WriteTableToDataStore_String = "WriteTableToDataStore()... <write a table to a database datastore>", // not being used
	__Commands_TableOutput_WriteTableToDelimitedFile_String = "WriteTableToDelimitedFile()... <write a table to a delimited file>",
	__Commands_TableOutput_WriteTableToExcel_String = "WriteTableToExcel()... <write a table to an Excel file>",
	__Commands_TableOutput_WriteTableToHTML_String = "WriteTableToHTML()... <write a table to an HTML file>",

	// Running and Properties
	__Commands_TableRunning_String = "Running and Properties",
	__Commands_TableRunning_SetPropertyFromTable_String = "SetPropertyFromTable()... <set a processor property from a table>",
	__Commands_TableRunning_CopyPropertiesToTable_String = "CopyPropertiesToTable()... <copy processor properties to a table>";

	// StateMod sub-menus (see the first item for the file being edited).

	private String

	__Commands_StateMod_ControlData_String = "Control Data",
	__Commands_StateMod_Response_String = "Response",
	__Commands_StateMod_Response_ReadResponseFromStateMod_String = "ReadResponseFromStateMod() ...",
	__Commands_StateMod_Response_WriteResponseToStateMod_String = "WriteResponseToStateMod() ...",

	__Commands_StateMod_Control_String = "Control",
	__Commands_StateMod_Control_ReadControlFromStateMod_String = "ReadControlFromStateMod() ...",
	__Commands_StateMod_Control_WriteControlToStateMod_String = "WriteControlToStateMod() ...",
	__Commands_StateMod_OutputRequest_String = "Output Request",
	__Commands_StateMod_ReachData_String = "Reach Data",

	__Commands_StateMod_ConsumptiveUseData_String = "Consumptive Use Data",
	__Commands_StateMod_StateCUStructure_String = "StateCU Structures (for AWC)",
	__Commands_StateMod_Parcels_String = "Parcels",
	__Commands_StateMod_Parcels_ReadParcelsFromHydroBase_String = "ReadParcelsFromHydroBase()...",
	__Commands_StateMod_Parcels_ReadParcelsFromIrrigatedLands_String = "ReadParcelsFromIrrigatedLands()...",
	__Commands_StateMod_Parcels_SetParcel_String = "SetParcel()...",
	__Commands_StateMod_Parcels_SetParcelSurfaceWaterSupply_String = "SetParcelSurfaceWaterSupply()...",
	__Commands_StateMod_Parcels_SetParcelGroundWaterSupply_String = "SetParcelGroundWaterSupply()...",
	__Commands_StateMod_Parcels_CheckParcels_String = "CheckParcels()...",
	__Commands_StateMod_Parcels_CheckIrrigatedLands_String = "CheckIrrigatedLands()...",
	__Commands_StateMod_Parcels_WriteParcelsToFile_String = "WriteParcelsToFile()...",
	__Commands_StateMod_IrrigationPracticeTS_String = "Irrigation Practice TS (Yearly)",
	__Commands_StateMod_ConsumptiveWaterRequirementTS_String = "Consumptive Water Requirement (Monthly, Daily)",

	__Commands_StateMod_StreamGageData_String = "Stream Gage Data",

	__Commands_StateMod_StreamGageStations_String =	"Stream Gage Stations",
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_String =
		"ReadStreamGageStationsFromList() ...",
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_String =
		"ReadStreamGageStationsFromNetwork() ...",
	__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_String =
		"ReadStreamGageStationsFromStateMod() ...",
	__Commands_StateMod_StreamGageStations_SetStreamGageStation_String = "SetStreamGageStation() ...",
	__Commands_StateMod_StreamGageStations_SortStreamGageStations_String = "SortStreamGageStations() ...",
	__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_String =
		"FillStreamGageStationsFromHydroBase() ...",
	__Commands_StateMod_StreamGageStations_ReadNetworkFromStateMod_String =
		"1: ReadNetworkFromStateMod() ...",
	__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_String =
		"2: FillStreamGageStationsFromNetwork() ...",
	__Commands_StateMod_StreamGageStations_FillStreamGageStation_String = "FillStreamGageStation() ...",
	__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_String =
		"WriteStreamGageStationsToList() ...",
	__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_String =
		"WriteStreamGageStationsToStateMod() ...",
	__Commands_StateMod_StreamGageStations_CheckStreamGageStations_String = "CheckStreamGageStations()...",

	__Commands_StateMod_StreamGageHistoricalTS_String = "Stream Historical TS (Monthly, Daily)",
	__Commands_StateMod_StreamGageBaseTS_String = "Stream Natural Flow TS (Monthly, Daily)",

	__Commands_StateMod_DelayTableData_String = "Delay Table Data",
	__Commands_StateMod_DelayTablesMonthly_String = "Delay Tables (Monthly)",
	__Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_String =
		"ReadDelayTablesMonthlyFromStateMod() ...",
	__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_String =
		"WriteDelayTablesMonthlyToList() ...",
	__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_String =
		"WriteDelayTablesMonthlyToStateMod() ...",
	__Commands_StateMod_DelayTablesDaily_String = "Delay Tables (Daily)",
	__Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_String = "ReadDelayTablesDailyFromStateMod() ...",
	__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_String = "WriteDelayTablesDailyToList() ...",
	__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_String = "WriteDelayTablesDailyToStateMod() ...",

	__Commands_StateMod_DiversionData_String = "Diversion Data",
	__Commands_StateMod_DiversionStations_String = "Diversion Stations",
	__Commands_StateMod_DiversionStations_SetOutputYearType_String = "SetOutputYearType() ...",
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String =
		"ReadDiversionStationsFromList() ...",
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_String =
		"ReadDiversionStationsFromNetwork() ...",
	__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String =
		"ReadDiversionStationsFromStateMod() ...",
	__Commands_StateMod_DiversionStations_SetDiversionAggregate_String =
		__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateMod_DiversionStations_SetDiversionAggregateFromList_String =
		__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateMod_DiversionStations_SetDiversionSystem_String =
		__Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateMod_DiversionStations_SetDiversionSystemFromList_String =
		__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_DiversionStations_SortDiversionStations_String = "SortDiversionStations() ...",
	__Commands_StateMod_DiversionStations_SetDiversionStation_String = "SetDiversionStation() ...",
	__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_String =
		"SetDiversionStationsFromList() ...",
	__Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_String =
		"FillDiversionStationsFromHydroBase() ...",
	__Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_String =
		"FillDiversionStationsFromNetwork() ...",
	__Commands_StateMod_DiversionStations_FillDiversionStation_String = "FillDiversionStation() ...",
	__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_String =
		"SetDiversionStationDelayTablesFromNetwork() ...",
	__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_String =
		"SetDiversionStationDelayTablesFromRTN() ...",
	__Commands_StateMod_DiversionStations_WriteDiversionStationsToList_String = "WriteDiversionStationsToList() ...",
	__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_String =
		"WriteDiversionStationsToStateMod() ...",
	__Commands_StateMod_DiversionStations_CheckDiversionStations_String = "CheckDiversionStations() ...",

	__Commands_StateMod_DiversionRights_String = "Diversion Rights",
	__Commands_StateMod_DiversionRights_ReadDiversionStationsFromList_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String,
	__Commands_StateMod_DiversionRights_ReadDiversionStationsFromStateMod_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
	__Commands_StateMod_DiversionRights_SetDiversionAggregate_String =
		__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateMod_DiversionRights_SetDiversionAggregateFromList_String =
		__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateMod_DiversionRights_SetDiversionSystem_String =
		__Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateMod_DiversionRights_SetDiversionSystemFromList_String =
		__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_String =
		"ReadDiversionRightsFromHydroBase() ...",
	__Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_String =
		"ReadDiversionRightsFromStateMod() ...",
	__Commands_StateMod_DiversionRights_SetDiversionRight_String = "SetDiversionRight() ...",
	__Commands_StateMod_DiversionRights_SortDiversionRights_String = "SortDiversionRights() ...",
	__Commands_StateMod_DiversionRights_FillDiversionRight_String = "FillDiversionRight() ...",
	__Commands_StateMod_DiversionRights_WriteDiversionRightsToList_String = "WriteDiversionRightsToList() ...",
	__Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_String = "WriteDiversionRightsToStateMod() ...",
	__Commands_StateMod_DiversionRights_CheckDiversionRights_String = "CheckDiversionRights() ...",

	__Commands_StateMod_DiversionHistoricalTSMonthly_String = "Diversion Historical TS (Monthly)",
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromList_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromStateMod_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregate_String =
		__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregateFromList_String =
		__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystem_String =
		__Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystemFromList_String =
		__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_String =
		"ReadDiversionHistoricalTSMonthlyFromHydroBase() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String =
		"ReadDiversionHistoricalTSMonthlyFromStateMod() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_String =
		"SetDiversionHistoricalTSMonthly() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_String =
		"SetDiversionHistoricalTSMonthlyConstant() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_String =
		"FillDiversionHistoricalTSMonthlyAverage() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_String =
		"FillDiversionHistoricalTSMonthlyConstant() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_String = "1: ReadPatternFile() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_String =
		"2: FillDiversionHistoricalTSMonthlyPattern() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionRightsFromStateMod_String =
		"1: ReadDiversionRightsFromStateMod() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_String =
		"2: LimitDiversionHistoricalTSMonthlyToRights() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_String =
		"WriteDiversionHistoricalTSMonthlyToStateMod() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_String =
		"SetDiversionStationCapacitiesFromTS() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_String =
		__Commands_StateMod_DiversionStations_SetDiversionStation_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_String =
		__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_String =
		"SortDiversionHistoricalTSMonthly() ...",
	__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_String =
		__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_String,
	__Commands_StateMod_DiversionHistoricalTSMonthly_CheckDiversionHistoricalTSMonthly_String =
		"CheckDiversionHistoricalTSMonthly() ...",

	__Commands_StateMod_DiversionHistoricalTSDaily_String = "Diversion Historical TS (Daily)",

	__Commands_StateMod_DiversionDemandTSMonthly_String = "Diversion Demand TS (Monthly)",
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromList_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String,
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromStateMod_String =
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregate_String =
		__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregateFromList_String =
		__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystem_String =
		__Commands_StateCU_CULocations_SetDiversionSystem_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystemFromList_String =
		__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_String =
		"SetDiversionMultiStruct()...",
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_String =
		"SetDiversionMultiStructFromList()...",
	__Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String =
		"1: ReadIrrigationWaterRequirementTSMonthlyFromStateCU() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String =
		"2: ReadDiversionHistoricalTSMonthlyFromStateMod() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_String =
		"[Legacy] 3: CalculateDiversionStationEfficiencies() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_String=
		__Commands_StateMod_DiversionStations_SetDiversionStation_String,
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_String=
		__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_String,
	__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_String =
		__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_String,
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_String =
		"CalculateDiversionDemandTSMonthly() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_String =
		"CalculateDiversionDemandTSMonthlyAsMax() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_String =
		"ReadDiversionDemandTSMonthlyFromStateMod() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_String =
		"FillDiversionDemandTSMonthlyAverage() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_String =
		"FillDiversionDemandTSMonthlyConstant() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_String = "1: ReadPatternFile() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_String =
		"2: FillDiversionDemandTSMonthlyPattern() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_String =
		"LimitDiversionDemandTSMonthlyToRights() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_String =
		"SetDiversionDemandTSMonthly() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_String =
		"SetDiversionDemandTSMonthlyConstant() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_String =
		"SortDiversionDemandTSMonthly() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_String =
		"WriteDiversionDemandTSMonthlyToStateMod() ...",
	__Commands_StateMod_DiversionDemandTSMonthly_CheckDiversionDemandTSMonthly_String =
		"CheckDiversionDemandTSMonthly() ...",

	__Commands_StateMod_DiversionDemandTSOverrideMonthly_String = "Diversion Demand TS Override (Monthly)",

	__Commands_StateMod_DiversionDemandTSAverageMonthly_String = "Diversion Demand TS (Average Monthly)",

	__Commands_StateMod_DiversionDemandTSDaily_String = "Diversion Demand TS (Daily)",

	__Commands_StateMod_PrecipitationData_String ="Precipitation Data",
	__Commands_StateMod_PrecipitationTSMonthly_String =	"Precipitation TS (Monthly, Yearly)",

	__Commands_StateMod_EvaporationData_String = "Evaporation Data",
	__Commands_StateMod_EvaporationTSMonthly_String = "Evaporation TS (Monthly, Yearly)",

	__Commands_StateMod_ReservoirData_String = "Reservoir Data",
	__Commands_StateMod_ReservoirStations_String = "Reservoir Stations",
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_String =
		"ReadReservoirStationsFromList() ...",
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_String =
		"ReadReservoirStationsFromNetwork() ...",
	__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_String =
		"ReadReservoirStationsFromStateMod() ...",
	__Commands_StateMod_ReservoirStations_SetReservoirAggregate_String = "SetReservoirAggregate() ...",
	__Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_String =
		"SetReservoirAggregateFromList() ...",
/* TODO SAM 2004-07-02 - need to evaluate how to aggregate reservoirs.
	__Commands_StateMod_ReservoirStations_SetReservoirSystem_String =
		__Commands_StateCU_CULocations_SetReservoirSystem_String,
	__Commands_StateMod_ReservoirStations_SetReservoirSystemFromList_String =
		__Commands_StateCU_CULocations_SetReservoirSystemFromList_String,
*/
	__Commands_StateMod_ReservoirStations_SetReservoirStation_String = "SetReservoirStation() ...",
	__Commands_StateMod_ReservoirStations_SortReservoirStations_String =
		"SortReservoirStations() ...",
	__Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_String =
		"FillReservoirStationsFromHydroBase() ...",
	__Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_String =
		"FillReservoirStationsFromNetwork() ...",
	__Commands_StateMod_ReservoirStations_FillReservoirStation_String = "FillReservoirStation() ...",
	__Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_String =
		"WriteReservoirStationsToList() ...",
	__Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_String =
		"WriteReservoirStationsToStateMod() ...",
	__Commands_StateMod_ReservoirStations_CheckReservoirStations_String = "CheckReservoirStations() ...",

	__Commands_StateMod_ReservoirRights_String = "Reservoir Rights",
	__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromList_String =
		__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_String,
	__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromStateMod_String =
		__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_String,
	__Commands_StateMod_ReservoirRights_SetReservoirAggregate_String =
		__Commands_StateMod_ReservoirStations_SetReservoirAggregate_String,
	__Commands_StateMod_ReservoirRights_SetReservoirAggregateFromList_String =
		__Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_String,
	/* TODO SAM 2004-07-07 maybe support later.
	__Commands_StateMod_ReservoirRights_SetReservoirSystem_String =
		__Commands_StateCU_CULocations_SetReservoirSystem_String,
	__Commands_StateMod_ReservoirRights_SetReservoirSystemFromList_String =
		__Commands_StateCU_CULocations_SetReservoirSystemFromList_String,
	*/
	__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_String =
		"ReadReservoirRightsFromHydroBase() ...",
	__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_String =
		"ReadReservoirRightsFromStateMod() ...",
	__Commands_StateMod_ReservoirRights_SetReservoirRight_String = "SetReservoirRight() ...",
	__Commands_StateMod_ReservoirRights_SortReservoirRights_String = "SortReservoirRights() ...",
	__Commands_StateMod_ReservoirRights_FillReservoirRight_String = "FillReservoirRight() ...",
	__Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_String = "WriteReservoirRightsToList() ...",
	__Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_String = "WriteReservoirRightsToStateMod() ...",
	__Commands_StateMod_ReservoirRights_CheckReservoirRights_String = "CheckReservoirRights() ...",

	__Commands_StateMod_ReservoirReturn_String = "Reservoir Return",
	__Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_String = "ReadReservoirReturnFromStateMod() ...",
	__Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_String = "WriteReservoirReturnToStateMod() ...",

	__Commands_StateMod_ReservoirContentAndTargetTS_String = "Reservoir Content, Target TS (Monthly, Daily)",

	__Commands_StateMod_InstreamFlowData_String = "Instream Flow Data",
	__Commands_StateMod_InstreamFlowStations_String = "Instream Flow Stations",
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_String =
		"ReadInstreamFlowStationsFromList() ...",
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_String =
		"ReadInstreamFlowStationsFromNetwork() ...",
	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String =
		"ReadInstreamFlowStationsFromStateMod() ...",
	__Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_String = "SetInstreamFlowStation() ...",
	__Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_String = "SortInstreamFlowStations() ...",
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_String =
		"FillInstreamFlowStationsFromHydroBase() ...",
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_String =
		"FillInstreamFlowStationsFromNetwork() ...",
	__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_String = "FillInstreamFlowStation() ...",
	__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_String =
		"WriteInstreamFlowStationsToList() ...",
	__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_String =
		"WriteInstreamFlowStationsToStateMod() ...",
	__Commands_StateMod_InstreamFlowStations_CheckInstreamFlowStations_String =
		"CheckInstreamFlowStations() ...",

	__Commands_StateMod_InstreamFlowRights_String = "Instream Flow Rights",
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromList_String =
		__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_String,
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromStateMod_String =
		__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String,
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_String =
		"ReadInstreamFlowRightsFromHydroBase() ...",
	__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_String =
		"ReadInstreamFlowRightsFromStateMod() ...",
	__Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_String = "SetInstreamFlowRight() ...",
	__Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_String = "SortInstreamFlowRights() ...",
	__Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_String = "FillInstreamFlowRight() ...",
	__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_String = "WriteInstreamFlowRightsToList() ...",
	__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_String =
		"WriteInstreamFlowRightsToStateMod() ...",
	__Commands_StateMod_InstreamFlowRights_CheckInstreamFlowRights_String = "CheckInstreamFlowRights() ...",

	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_String =
		"Instream Flow Demand TS (Average Monthly)",
	// Not needed (yet).
	//__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowStationsFromStateMod_String =
	//	__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_String =
		"ReadInstreamFlowDemandTSAverageMonthlyFromStateMod() ...",
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowRightsFromStateMod_String =
		"1: " + __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_String,
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_String =
		"2: SetInstreamFlowDemandTSAverageMonthlyFromRights() ...",
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_String =
		"SetInstreamFlowDemandTSAverageMonthlyConstant() ...",
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_String =
		"WriteInstreamFlowDemandTSAverageMonthlyToStateMod() ...",
	__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_CheckInstreamFlowDemandTSAverageMonthly_String =
		"CheckInstreamFlowDemandTSAverageMonthly() ...",

	__Commands_StateMod_InstreamFlowDemandTS_String = "Instream Flow Demand (Monthly, Daily)",

	__Commands_StateMod_WellData_String = "Well Data",
	__Commands_StateMod_WellStations_String = "Well Stations",
	__Commands_StateMod_WellStations_ReadWellStationsFromList_String = "ReadWellStationsFromList() ...",
	__Commands_StateMod_WellStations_ReadWellStationsFromNetwork_String = "ReadWellStationsFromNetwork() ...",
	__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String = "ReadWellStationsFromStateMod() ...",
	__Commands_StateMod_WellStations_SetWellAggregate_String =
		__Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateMod_WellStations_SetWellAggregateFromList_String =
		__Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateMod_WellStations_SetWellSystem_String =
		__Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateMod_WellStations_SetWellSystemFromList_String =
		__Commands_StateCU_CULocations_SetWellSystemFromList_String,
	//__Commands_StateMod_WellStations_SetDiversionAggregate_String =
	//	__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	//__Commands_StateMod_WellStations_SetDiversionAggregateFromList_String =
	//	__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	//__Commands_StateMod_WellStations_SetDiversionSystem_String =
	//	__Commands_StateCU_CULocations_SetDiversionSystem_String,
	//__Commands_StateMod_WellStations_SetDiversionSystemFromList_String =
	//	__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_WellStations_SetWellStation_String = "SetWellStation() ...",
	__Commands_StateMod_WellStations_SetWellStationsFromList_String = "SetWellStationsFromList() ...",
	__Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_String =
		"1: " + __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_String,
	__Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_String =
		"2: SetWellStationAreaToCropPatternTS() ...",
	__Commands_StateMod_WellStations_ReadWellRightsFromStateMod_String =
		"1: ReadWellRightsFromStateMod() ...",  // Defined below so put literal here
	__Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_String =
		"2: SetWellStationCapacityToWellRights() ...",
	__Commands_StateMod_WellStations_SortWellStations_String = "SortWellStations() ...",
	__Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_String =
		"1: " + __Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
	__Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_String =
		"2: FillWellStationsFromDiversionStations() ...",
	__Commands_StateMod_WellStations_FillWellStationsFromNetwork_String =
		"FillWellStationsFromNetwork() ...",
	__Commands_StateMod_WellStations_FillWellStation_String = "FillWellStation() ...",
	__Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_String =
		"SetWellStationDelayTablesFromNetwork() ...",
	__Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_String =
		"SetWellStationDelayTablesFromRTN() ...",
	__Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_String =
		"SetWellStationDepletionTablesFromRTN() ...",
	__Commands_StateMod_WellStations_WriteWellStationsToList_String = "WriteWellStationsToList() ...",
	__Commands_StateMod_WellStations_WriteWellStationsToStateMod_String = "WriteWellStationsToStateMod() ...",
	__Commands_StateMod_WellStations_CheckWellStations_String = "CheckWellStations() ...",

	__Commands_StateMod_WellRights_String = "Well Rights",
	__Commands_StateMod_WellRights_ReadWellStationsFromList_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromList_String,
	__Commands_StateMod_WellRights_ReadWellStationsFromNetwork_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromNetwork_String,
	__Commands_StateMod_WellRights_ReadWellStationsFromStateMod_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,
	__Commands_StateMod_WellRights_SetWellAggregate_String =
		__Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateMod_WellRights_SetWellAggregateFromList_String =
		__Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateMod_WellRights_SetWellSystem_String =
		__Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateMod_WellRights_SetWellSystemFromList_String =
		__Commands_StateCU_CULocations_SetWellSystemFromList_String,
	//__Commands_StateMod_WellRights_SetDiversionAggregate_String =
	//	__Commands_StateCU_CULocations_SetDiversionAggregate_String,
	//__Commands_StateMod_WellRights_SetDiversionAggregateFromList_String =
	//	__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
	//__Commands_StateMod_WellRights_SetDiversionSystem_String =
	//	__Commands_StateCU_CULocations_SetDiversionSystem_String,
	//__Commands_StateMod_WellRights_SetDiversionSystemFromList_String =
	//	__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
	__Commands_StateMod_WellRights_ReadParcelsFromHydroBase_String = "ReadParcelsFromHydroBase() ...",
	__Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_String = "ReadWellRightsFromHydroBase() ...",
	__Commands_StateMod_WellRights_ReadWellRightsFromStateMod_String = "ReadWellRightsFromStateMod() ...",
	__Commands_StateMod_WellRights_SetWellRight_String = "SetWellRight() ...",
	__Commands_StateMod_WellRights_FillWellRight_String = "FillWellRight() ...",
	__Commands_StateMod_WellRights_MergeWellRights_String = "MergeWellRights() ...",
	__Commands_StateMod_WellRights_AggregateWellRights_String = "AggregateWellRights() ...",
	__Commands_StateMod_WellRights_SortWellRights_String = "SortWellRights() ...",
	__Commands_StateMod_WellRights_WriteWellRightsToList_String = "WriteWellRightsToList() ...",
	__Commands_StateMod_WellRights_WriteWellRightsToStateMod_String = "WriteWellRightsToStateMod() ...",
	__Commands_StateMod_WellRights_CheckWellRights_String = "CheckWellRights() ...",
	__Commands_StateMod_WellRights_WriteCheckFile_String = __Commands_Shared_WriteCheckFile_String,

	__Commands_StateMod_WellHistoricalPumpingTSMonthly_String = "Well Historical Pumping TS (Monthly)",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromList_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromList_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromStateMod_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregate_String =
		__Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregateFromList_String =
		__Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystem_String =
		__Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystemFromList_String =
		__Commands_StateCU_CULocations_SetWellSystemFromList_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_String =
		"ReadWellHistoricalPumpingTSMonthlyFromStateCU() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String =
		"ReadWellHistoricalPumpingTSMonthlyFromStateMod() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_String =
		"SetWellHistoricalPumpingTSMonthly() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_String =
		"SetWellHistoricalPumpingTSMonthlyConstant() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_String =
		"FillWellHistoricalPumpingTSMonthlyAverage() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_String =
		"FillWellHistoricalPumpingTSMonthlyConstant() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_String = "1: ReadPatternFile() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_String =
		"2: FillWellHistoricalPumpingTSMonthlyPattern() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellRightsFromStateMod_String =
		"1: ReadWellRightsFromStateMod() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_String =
		"2: LimitWellHistoricalPumpingTSMonthlyToRights() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_String =
		"WriteWellHistoricalPumpingTSMonthlyToStateMod() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_String =
		"SetWellStationCapacitiesFromTS() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_String =
		__Commands_StateMod_WellStations_SetWellStation_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_String =
		__Commands_StateMod_WellStations_SetWellStationsFromList_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_String =
		"SortWellHistoricalPumpingTSMonthly() ...",
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_String =
		__Commands_StateMod_WellStations_WriteWellStationsToStateMod_String,
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_CheckWellHistoricalPumpingTSMonthly_String =
		"CheckWellHistoricalPumpingTSMonthly() ...",

	__Commands_StateMod_WellHistoricalPumpingTSDaily_String = "Well Historical Pumping TS (Daily)",

	__Commands_StateMod_WellDemandTSMonthly_String = "Well Demand TS (Monthly)",
	__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromList_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromList_String,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromStateMod_String =
		__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,
	__Commands_StateMod_WellDemandTSMonthly_SetWellAggregate_String =
		__Commands_StateCU_CULocations_SetWellAggregate_String,
	__Commands_StateMod_WellDemandTSMonthly_SetWellAggregateFromList_String =
		__Commands_StateCU_CULocations_SetWellAggregateFromList_String,
	__Commands_StateMod_WellDemandTSMonthly_SetWellSystem_String =
		__Commands_StateCU_CULocations_SetWellSystem_String,
	__Commands_StateMod_WellDemandTSMonthly_SetWellSystemFromList_String =
		__Commands_StateCU_CULocations_SetWellSystemFromList_String,
	__Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_String =
		"ReadWellDemandTSMonthlyFromStateMod() ...",
	__Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String =
		"1: ReadIrrigationWaterRequirementTSMonthlyFromStateCU() ...",
	__Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String =
		"2: ReadWellHistoricalPumpingTSMonthlyFromStateMod() ...",
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_String =
		"3: CalculateWellStationEfficiencies() ...",
	__Commands_StateMod_WellDemandTSMonthly_SetWellStation_String=
		__Commands_StateMod_WellStations_SetWellStation_String,
	__Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_String=
		__Commands_StateMod_WellStations_SetWellStationsFromList_String,
	__Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_String =
		__Commands_StateMod_WellStations_WriteWellStationsToStateMod_String,
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_String =
		"CalculateWellDemandTSMonthly() ...",
	__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_String =
		"CalculateWellDemandTSMonthlyAsMax() ...",
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_String =
		"FillWellDemandTSMonthlyAverage() ...",
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_String =
		"FillWellDemandTSMonthlyConstant() ...",
	__Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_String = "1: ReadPatternFile() ...",
	__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_String =
		"2: FillWellDemandTSMonthlyPattern() ...",
	__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_String = "SetWellDemandTSMonthly() ...",
	__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_String = "SetWellDemandTSMonthlyConstant() ...",
	__Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_String = "ReadWellRightsFromStateMod() ...",
	__Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_String = "LimitWellDemandTSMonthlyToRights() ...",
	__Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_String = "SortWellDemandTSMonthly() ...",
	__Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_String =
		"WriteWellDemandTSMonthlyToStateMod() ...",
	__Commands_StateMod_WellDemandTSMonthly_CheckWellDemandTSMonthly_String =
		"CheckWellDemandTSMonthly() ...",

	__Commands_StateMod_WellDemandTSDaily_String = "Well Demand TS (Daily)",

	__Commands_StateMod_PlanData_String = "Plan Data",
	__Commands_StateMod_PlanStations_String = "Plan Stations",
	__Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_String = "ReadPlanStationsFromStateMod() ...",
	__Commands_StateMod_PlanStations_SetPlanStation_String = "SetPlanStation() ...",
	__Commands_StateMod_PlanStations_WritePlanStationsToStateMod_String = "WritePlanStationsToStateMod() ...",

	__Commands_StateMod_PlanWellAugmentation_String = "Plan Well Augmentation Data",
	__Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_String = "ReadPlanWellAugmentationFromStateMod() ...",
	__Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_String = "WritePlanWellAugmentationToStateMod() ...",

	__Commands_StateMod_PlanReturn_String = "Plan Return",
	__Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_String = "ReadPlanReturnFromStateMod() ...",
	__Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_String = "WritePlanReturnToStateMod() ...",

	__Commands_StateMod_StreamEstimateData_String = "Stream Estimate Data",
	__Commands_StateMod_StreamEstimateStations_String = "Stream Estimate Stations",
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_String =
		"ReadStreamEstimateStationsFromList() ...",
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_String =
		"ReadStreamEstimateStationsFromNetwork() ...",
	__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_String =
		"ReadStreamEstimateStationsFromStateMod() ...",
	__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_String =
		"SetStreamEstimateStation() ...",
	__Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_String =
		"SortStreamEstimateStations() ...",
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_String =
		"FillStreamEstimateStationsFromHydroBase() ...",
	__Commands_StateMod_StreamEstimateStations_ReadNetworkFromStateMod_String =
		"1: ReadNetworkFromStateMod() ...",
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_String =
		"2: FillStreamEstimateStationsFromNetwork() ...",
	__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_String = "FillStreamEstimateStation() ...",
	__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_String =
		"WriteStreamEstimateStationsToList() ...",
	__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_String =
		"WriteStreamEstimateStationsToStateMod() ...",
	__Commands_StateMod_StreamEstimateStations_CheckStreamEstimateStations_String =
		"CheckStreamEstimateStations() ...",

	__Commands_StateMod_StreamEstimateCoefficients_String = "Stream Estimate Coefficients",
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_String =
		"ReadStreamEstimateCoefficientsFromStateMod() ...",
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromList_String =
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_String,
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromNetwork_String =
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_String,
	__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromStateMod_String =
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_String,
	__Commands_StateMod_StreamEstimateCoefficients_SortStreamEstimateStations_String =
		__Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_String,
	__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_String =
		"SetStreamEstimateCoefficientsPFGage() ...",
	__Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_String =
		"CalculateStreamEstimateCoefficients() ...",
	__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_String =
		"SetStreamEstimateCoefficients() ...",
	__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_String =
		"WriteStreamEstimateCoefficientsToList() ...",
	__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_String =
		"WriteStreamEstimateCoefficientsToStateMod() ...",
	__Commands_StateMod_StreamEstimateCoefficients_CheckStreamEstimateCoefficients_String =
		"CheckStreamEstimateCoefficients() ...",

	__Commands_StateMod_StreamEstimateBaseTS_String = "Stream Estimate Natural Flow TS (Monthly, Daily)",

	__Commands_StateMod_RiverNetworkData_String = "River Network Data",
	__Commands_StateMod_Network_String = "Network (used by StateDMI, StateMod GUI)",
	__Commands_StateMod_Network_ReadNetworkFromStateMod_String = "ReadNetworkFromStateMod() ...",
	__Commands_StateMod_Network_AppendNetwork_String = "AppendNetwork() ...",
	__Commands_StateMod_Network_ReadRiverNetworkFromStateMod_String = "1: ReadRiverNetworkFromStateMod() ...",
	__Commands_StateMod_Network_ReadStreamGageStationsFromStateMod_String =
		"2: " + __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_String,
	__Commands_StateMod_Network_ReadDiversionStationsFromStateMod_String =
		"3: " + __Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
	__Commands_StateMod_Network_ReadReservoirStationsFromStateMod_String =
		"4: " + __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_String,
	__Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_String =
		"5: " + __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String,
	__Commands_StateMod_Network_ReadWellStationsFromStateMod_String =
		"6: " + __Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,
	__Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_String =
		"7: " + __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_String,
	__Commands_StateMod_Network_CreateNetworkFromRiverNetwork_String =
		"8: CreateNetworkFromRiverNetwork() ...",
	__Commands_StateMod_Network_FillNetworkFromHydroBase_String = "FillNetworkFromHydroBase() ...",
	__Commands_StateMod_Network_WriteNetworkToList_String = "WriteNetworkToList() ...",
	__Commands_StateMod_Network_WriteNetworkToStateMod_String = "WriteNetworkToStateMod() ...",
	__Commands_StateMod_Network_PrintNetwork_String = "PrintNetwork() ...",

	__Commands_StateMod_RiverNetwork_String = "River Network (used by StateMod)",
	__Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_String = "ReadNetworkFromStateMod() ...",
	__Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_String = "CreateRiverNetworkFromNetwork() ...",
	__Commands_StateMod_RiverNetwork_SetRiverNetworkNode_String = "SetRiverNetworkNode() ...",
	__Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_String = "FillRiverNetworkFromHydroBase() ...",
	__Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_String = "FillRiverNetworkFromNetwork() ...",
	__Commands_StateMod_RiverNetwork_FillRiverNetworkNode_String = "FillRiverNetworkNode() ...",
	__Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_String = "WriteRiverNetworkToList() ...",
	__Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_String = "WriteRiverNetworkToStateMod() ...",
	__Commands_StateMod_RiverNetwork_CheckRiverNetwork_String = "CheckRiverNetwork() ...",

	__Commands_StateMod_OperationalData_String = "Operational Data",
	__Commands_StateMod_OperationalRights_String = "Operational Rights",
	__Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_String =
		"ReadOperationalRightsFromStateMod() ...",
	__Commands_StateMod_OperationalRights_SetOperationalRight_String = "SetOperationalRight() ...",
	//__Commands_StateMod_OperationalRights_SortOperationalRights_String = "SortOperationalRights() ...",
	__Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_String = "WriteOperationalRightsToStateMod() ...",
	__Commands_StateMod_OperationalRights_CheckOperationalRights_String = "CheckOperationalRights() ...",

	__Commands_StateMod_DownstreamCallTSDaily_String = "Downstream Call TS (Daily)",
	__Commands_StateMod_SanJuanSedimentRecoveryPlan_String = "San Juan Sediment Recovery Plan",
	__Commands_StateMod_RioGrandeSpill_String = "Rio Grande Spill",

	__Commands_StateMod_SpatialData_String = "Spatial Data",
	__Commands_StateMod_GeoViewProject_String = "GeoView Project",

	// General commands same as for StateCU.

	// Run menu.

	__Run_AllCommandsCreateOutput_String = "All Commands (create all output)",
	__Run_AllCommandsIgnoreOutput_String = "All Commands (ignore output commands)",
	__Run_SelectedCommandsCreateOutput_String = "Selected Commands (create all output)",
	__Run_SelectedCommandsIgnoreOutput_String = "Selected Commands (ignore output commands)",
	__Run_CancelCommandProcessing_String = "Cancel Command Processing",
	__Run_CommandsFromFile_String = "Run Command File",
	__Run_RunStateCUVersion_String = "Run StateCU -version",
	__Run_RunStateModVersion_String = "Run StateMod -version",

	// Results menu (StateCU)...

	MENU_Results_StateCU_ControlData = "Control Data",
	MENU_Results_StateCU_ClimateStationsData = "Climate Stations Data",
	MENU_Results_StateCU_CropCharacteristicsData = "Crop Characteristics/Coefficients Data",
	MENU_Results_StateCU_DelayTablesData = "Delay Tables Data",
	MENU_Results_StateCU_CULocationsData = "CU Locations Data",

	// Results menu (StateMod)...

	MENU_Results_StateMod_RiverData = "River Data",
	MENU_Results_StateMod_DelayTableData = "Delay Table Data",
	MENU_Results_StateMod_DiversionData = "Diversion Data",
	MENU_Results_StateMod_PrecipitationData = "Precipitation Data",
	MENU_Results_StateMod_EvaporationData = "Evaporation Data",
	MENU_Results_StateMod_ReservoirData = "Reservoir Data",
	MENU_Results_StateMod_InstreamFlowData = "Instream Flow Data",
	MENU_Results_StateMod_WellData = "Well Data",
	MENU_Results_StateMod_RiverNetworkData = "River Network Data",
	MENU_Results_StateMod_OperationalData = "Operational Data",

	// Tools menu.

	__Tools_String = "Tools",
	__Tools_AdministrationNumberCalculator_String = "Administration Number Calculator...",
	__Tools_CompareFiles_String = "Compare Files",
	__Tools_CompareFiles_StateModWellRights_String = "StateMod Well Rights",
	__Tools_ListSurfaceWaterDiversions_String = "List Surface Water Diversions",
	__Tools_ListWellStationRightTotals_String = "List Well Station Right Totals",
	__Tools_HydrobaseParcelWaterSupply_String = "HydroBase - Parcel Water Supply...",
	__Tools_ViewLogFile_Startup_String = "Diagnostics - View Log File (Startup)...",
	// Currently Diagnostics are added dynamically.

	// Help menu.

	__Help_AboutStateDMI_String = "About StateDMI",
	__Help_ViewDocumentation_String = "View Documentation (PDF)",
	__Help_ViewDocumentation_ReleaseNotes_String = "View Documentation - Release Notes",
	__Help_ViewDocumentation_UserManual_String = "View Documentation - User Manual",
	__Help_ViewDocumentation_CommandReference_String = "View Documentation - Command Reference",
	__Help_ViewDocumentation_DatastoreReference_String = "View Documentation - Datastore Reference",
	__Help_ViewDocumentation_Troubleshooting_String = "View Documentation - Troubleshooting",
	//__Help_ViewTrainingMaterials_String = "View Training Materials",

	// Results at bottom of window.

	__Results_Table_Properties_String = "Table properties...",

	// Commands list pop-up menu (may be selectively added to/removed from the popup menu).

	MENU_Popup_Edit_WithErrorChecks = "Edit Command...",

	MENU_Popup_Cut = "Cut",
	MENU_Popup_Copy = "Copy",
	MENU_Popup_Paste = "Paste (After Selected)",

	MENU_Popup_Delete = "Delete",

	__CommandsPopup_SelectAll_String = "Select All",
	__CommandsPopup_DeselectAll_String = "Deselect All";

private JToolBar __toolBar = null;
private SimpleJButton
	__toolBarNewButton = null,
	__toolBarOpenButton = null,
	__toolBarSaveButton = null;

/**
StateDMIMain GUI constructor.  Create the main graphical user interface.
@param app_type the application type from the StateDMI class (APP_TYPE_XXX).
*/
public StateDMI_JFrame ( StateDMISession session, int app_type ) {
	String rtn = "StateDMI_JFrame.constructor";
	__appType = app_type;

	// Let the message package know that the application is the top level.

	Message.setTopLevel (this);

	// Session to track command file history and other user session properties.
	this.session = session;

	String directory = System.getProperty ("user.dir") + System.getProperty("file.separator");
	IOUtil.setProgramWorkingDir(directory);
	JGUIUtil.setLastFileDialogDirectory(directory);
	__props = new PropList("StateDMI_JFrame");
	__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
	__initialWorkingDir = __props.getValue ( "WorkingDir" );

	ui_InitGUI();

	// Open startup datastores, displaying dialog if SystemLogin or SystemPassword property is "prompt".
	// TODO SAM 2010-09-03 migrate more input types to datastores.
	try {
		Message.printStatus(2, rtn, "Opening datastores from StateDMI UI...");
	    StateDMI.openDataStoresAtStartup(session,__statedmiProcessor,false);
	}
	catch ( Exception e ) {
	    Message.printStatus ( 1, rtn, "Error opening datastores (" + e + ")." );
	}

	// Select HydroBase database.  Force a login if the database connection cannot be made:
	// - this will override any startup datastores opened above

	uiAction_OpenHydroBase();

	// Default the working directory to the directory where the application started.

	Message.printStatus (1, rtn, "Ready");

	// Populate the datastore choices in the UI.

	ui_DataStoreList_Populate ();

	ui_UpdateStatus(true);
}

/**
Process action events from the menus and buttons.
@param event ActionEvent to process.
*/
public void actionPerformed ( ActionEvent event ) {
	String action = event.getActionCommand();
	String command = action;	// To keep StateDMI and TSTool code the same.
	Object o = event.getSource ();
	String routine = "StateDMI_JFrame.actionPerformed";

	if ( ui_GetIgnoreActionEvent() ) {
		// Used when programatically modifying components and don't want an event to be handled.
		return;
	}

	// List the actions in order of the main GUI menus.
	// Popup menus are duplicates of main menu actions and are mixed throughout.
	// If an action takes more than a few lines of code, break out into a separate method.

	// File menu.

	if ( (o == __File_Open_CommandFile_JMenuItem) || (o == __toolBarOpenButton) ) {
		uiAction_OpenCommandFile ( null, true );
	}
	else if ( command.toUpperCase().endsWith(".STATEDMI")) {
    	// StateDMI command file in recent files, treat as open.
    	uiAction_OpenCommandFile ( command, false );
    }
	else if ( o == __File_Open_ModelNetwork_JMenuItem ) {
		uiAction_OpenModelNetwork ();
	}
	else if ( o == __File_New_ModelNetwork_JMenuItem ) {
		uiAction_OpenNewModelNetwork ();
	}
	else if ( o == __File_Open_HydroBase_JMenuItem ) {
		uiAction_OpenHydroBase ();
	}

	else if ( o == __File_Open_DataSet_JMenuItem ) {
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			uiAction_OpenStateCUDataSet ();
		}
		else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
			uiAction_OpenStateModDataSet ();
		}
	}

	// File menu, StateCU climate.

	else if ( o == __File_New_DataSet_StateCU_ClimateStations_FromList_JMenuItem ){
		uiAction_ReadStateCUClimateStationsFromList ();
	}
	else if (o==__File_New_DataSet_StateCU_Structures_FromList_JMenuItem ) {
		__statecuDatasetType = StateCU_DataSet.TYPE_STRUCTURES;
		uiAction_ReadStateCUStructuresFromList ();
	}
	else if((o == __File_New_CommandFile_JMenuItem) || (o == __toolBarNewButton) ) {
		uiAction_NewCommandFile ();
	}
	else if((o == __File_Save_Commands_JMenuItem) || (o == __toolBarSaveButton) ) {
		if (__commandFileName != null) {
			// Write without prompting for the command file name.
			uiAction_WriteCommandFile ( __commandFileName, false );
		}
		else {
			// Prompt for the command file name.
			uiAction_WriteCommandFile (__commandFileName, true );
		}
	}
	else if ( o == __File_Save_CommandsAs_JMenuItem ) {
		uiAction_WriteCommandFile ( __commandFileName, true );
	}
	else if ( o == __File_Save_DataSet_JMenuItem ) {
		uiAction_WriteDataSet ( null, true );
	}
    else if (command.equals(__File_Print_Commands_String) ) {
        // Get all commands as strings for printing.
        try {
            new TextPrinterJob ( commandList_GetCommandStrings(true), "StateDMI Commands",
                null, // Printer name.
                "na-letter", // Paper size.
                null, // Paper source.
                "Landscape", // Page orientation.
                .75, // Left margin.
                .75, // Right.
                .6, // Top.
                .6, // Bottom.
                0, // Lines per page - let called code determine.
                null, // Header.
                null, // Footer.
                true, // Show line count.
                true, // Show page count.
                null, // Print all pages.
                false, // Double-sided.
                null, // Print file.
                true ); // Show print configuration dialog.
        }
        catch ( Exception e ) {
            Message.printWarning ( 1, routine, "Error printing commands (" + e + ").");
            Message.printWarning ( 3, routine, e );
        }
    }
    else if ( o == __File_Properties_HydroBase_JMenuItem ) {
		// Simple text display of HydroBase properties.
		PropList reportProp = new PropList ("HydroBase Properties");
		reportProp.set ( "TotalWidth", "600" );
		reportProp.set ( "TotalHeight", "300" );
		reportProp.set ( "DisplayFont", "Courier" );
		reportProp.set ( "DisplaySize", "11" );
		reportProp.set ( "PrintFont", "Courier" );
		reportProp.set ( "PrintSize", "7" );
		reportProp.set ( "Title", "HydroBase Properties" );
		reportProp.setUsingObject ( "ParentUIComponent", this );
		List<String> v = null;
		if ( __hbdmi == null ) {
			v = new ArrayList();
			v.add ( "StateDMI HydroBase Properties" );
			v.add ( "" );
			v.add ( "No HydroBase database is available." );
		}
		else {
			v = __hbdmi.getDatabaseProperties();
		}
		//reportProp.set ( "URL", "http://granby.riverside.com" );
		// Does not work...
		//reportProp.set ( "URL", "\\CDSS\\develop\\Apps\\" +
		//"TSTool\\doc\\UserManual\\05.06.07\\html\\tstool.html" );
		// Does not seem to work...
		//reportProp.set ( "URL",
		//"http://hbserver/manuals/tstool_test/tstool.html" );
		new ReportJFrame ( v, reportProp );
	}
    else if ( o == __File_Properties_DataSet_JMenuItem ) {
		// Simple text display of data set properties, including last command file that was read.
		uiAction_ShowDataSetProperties ();
	}
    else if ( o == __File_SetWorkingDirectory_JMenuItem ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle(
		"Set the Working Directory (normally only use if a command file was not opened or saved)");
		fc.setFileSelectionMode (JFileChooser.DIRECTORIES_ONLY );
		if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
			return;
		}
		String directory = fc.getSelectedFile().getPath();
		IOUtil.setProgramWorkingDir(directory);
		JGUIUtil.setLastFileDialogDirectory(directory);
		// Reset to make sure the ending delimiter is removed.
		__props.set ("WorkingDir", IOUtil.getProgramWorkingDir() );
		__initialWorkingDir = __props.getValue ( "WorkingDir" );
	}
	else if ( o == __File_Test_JMenuItem ) {
		uiAction_Test ();
	}
	else if ( o == __File_SwitchToStateCU_JMenuItem ) {
		uiAction_SwitchAppType ( StateDMI.APP_TYPE_STATECU );
	}
	else if ( o == __File_SwitchToStateMod_JMenuItem ) {
		uiAction_SwitchAppType ( StateDMI.APP_TYPE_STATEMOD );
	}
	else if ( o == __File_Exit_JMenuItem ) {
		uiAction_CloseClicked();
	}

	// Edit menu.

	else if (action.equals(__CommandsPopup_ShowCommandStatus_String) ) {
		uiAction_ShowCommandStatus();
	}
	else if (action.equals (__Edit_CutCommands_String) || action.equals (MENU_Popup_Cut)) {
		// Cut the commands and save to the buffer.
		uiAction_CopyFromCommandListToCutBuffer( true );
	}
	else if (action.equals (__Edit_CopyCommands_String) || action.equals (MENU_Popup_Copy)) {
		// Copy commands to the buffer.
		uiAction_CopyFromCommandListToCutBuffer( false );
	}
	else if (action.equals (__Edit_PasteCommands_String) ||	action.equals (MENU_Popup_Paste)) {
		// Copy the commands buffer to the command list.
		uiAction_PasteFromCutBufferToCommandList();
	}
	else if ( o == __ClearCommands_JButton || action.equals (__Edit_DeleteCommands_String) ||
		action.equals (MENU_Popup_Delete)) {
		// The commands WILL NOT remain in the cut buffer.
		// Now clear the list of selected commands.
		commandList_RemoveCommandsBasedOnUI();
	}
	else if (action.equals (__Edit_CommandFile_String)) {
		// Edit the command file in Notepad.
		JFileChooser fc = JFileChooserFactory.createJFileChooser( JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle("Edit Command File");
		if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
			return;
		}
		String path = fc.getSelectedFile().getPath();

		try {
			String [] command_array = new String[2];
			command_array[0] = "notepad";
			command_array[1] = path;
			ProcessManager p = new ProcessManager ( command_array );
			p.run();
		} catch (Exception e2) {
			Message.printWarning (1, routine, "Unable to edit filename \"" + path + "\"");
		}
	}
	else if (action.equals (__Edit_CommandWithErrorChecking_String) ||
		action.equals (MENU_Popup_Edit_WithErrorChecks)) {
		// Edit the first selected command, unless a comment, in which case all are edited.
		uiAction_EditCommand ();
	}
	else if (action.equals (__Edit_SelectAllCommands_String) ||
		action.equals (__CommandsPopup_SelectAll_String)) {
		// Select all the commands in the list.
		uiAction_SelectAllCommands ();
	}
	else if (action.equals (__Edit_DeselectAllCommands_String) ||
		action.equals (__CommandsPopup_DeselectAll_String)) {
		// Deselect all the commands in the list.
		uiAction_DeselectAllCommands ();
	}
	else if (action.equals(__Edit_ConvertSelectedCommandsToComments_String) ) {
		uiAction_ConvertCommandsToComments ( true );
	}
	else if (action.equals(__Edit_ConvertSelectedCommandsFromComments_String) ) {
		uiAction_ConvertCommandsToComments ( false );
	}

	// View menu.

    if ( command.equals(__View_CommandFileDiff_String) ) {
        // Show visual diff of current command file and saved version.
        uiAction_ViewCommandFileDiff();
    }
	else if ( command.equals(__View_DataStores_String) ) {
        // Show the datastores.
        uiAction_ShowDataStores();
    }
    else if ( o == __View_ThreeLevelCommandsMenu_JCheckBoxMenuItem ) {
		// This method will trigger a refresh of the menus.
    	// TODO SAM 2007-06-25 Need to rework to have a "redrawMenus" method.
    	uiAction_SwitchAppType ( getAppType() );
	}

	// StateCU Commands menu.

	// StateCU climate stations commands.

	else if ( o == __Commands_StateCU_ClimateStations_ReadClimateStationsFromList_JMenuItem){
		// Read CU Climate Stations from a list file.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_ReadClimateStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_JMenuItem){
		// Read CU Climate Stations from a StateCU CLI file.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_JMenuItem){
		// Read CU Climate Stations from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_ClimateStations_SetClimateStation_JMenuItem){
		// Set CU Climate Station.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_SetClimateStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_JMenuItem){
		// Fill CU Climate Stations from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_ClimateStations_FillClimateStation_JMenuItem){
		// Fill CU Climate Stations.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_FillClimateStation_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_ClimateStations_SortClimateStations_JMenuItem){
		// Sort CU Climate Stations.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_SortClimateStations_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_ClimateStations_WriteClimateStationsToList_JMenuItem){
		// Write CU Climate Stations to CLI file.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_WriteClimateStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_JMenuItem){
		// Write CU Climate Stations to CLI file.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_ClimateStations_CheckClimateStations_String) ){
		// Check CU Climate Stations.
		commandList_EditCommand ( __Commands_StateCU_ClimateStations_CheckClimateStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_ClimateStations_TemperatureTS_String) ){
		// Display information about using TSTool.
		new ResponseJDialog ( this, "StateCU Temperature Time Series",
		"StateCU temperature time series files are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n" +
		"The climate stations file can be used as a list for input to other software.\n",
			ResponseJDialog.OK);
	}
	else if ( action.equals(__Commands_StateCU_ClimateStations_FrostDatesTS_String)){
		// Display information about using TSTool.
		new ResponseJDialog ( this, "StateCU Frost Dates Time Series",
		"StateCU frost date time series files are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n" +
		"The climate stations file can be used as a list for input to other software.\n",
			ResponseJDialog.OK);
	}
	else if ( action.equals(__Commands_StateCU_ClimateStations_PrecipitationTS_String)){
		// Display information about using TSTool.
		new ResponseJDialog ( this, "StateCU Precipitation Time Series",
		"StateCU precipitation time series files are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n" +
		"The climate stations file can be used as a list for input to other software.\n",
			ResponseJDialog.OK);
	}

	// StateCU CCH commands.

	else if ( o == __Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_JMenuItem) {
		// Read CU Locations from a StateCU CCH file.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_JMenuItem) {
		// Read CU crop characteristics from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_SetCropCharacteristics_JMenuItem) {
		// Set CUCropCharacteristics values using user edits.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_SetCropCharacteristics_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_JMenuItem) {
		// Translate CUCropCharacteristics crop types.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_SortCropCharacteristics_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_SortCropCharacteristics_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_JMenuItem) {
		// Write CU crop characteristics to a CCH file.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_JMenuItem) {
		// Write CU crop characteristics to a CCH file.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_CropCharacteristics_CheckCropCharacteristics_String)) {
		// Write CU crop characteristics to a CCH file.
		commandList_EditCommand ( __Commands_StateCU_CropCharacteristics_CheckCropCharacteristics_String,
		null, __INSERT_COMMAND);
	}

	// StateCU Blaney-Criddle (KBC) commands.

	else if ( o == __Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_JMenuItem ) {
		// Read CU Blaney Criddle from KBC file.
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_JMenuItem) {
		// Read CU Blaney Criddle from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_JMenuItem) {
		commandList_EditCommand (
		__Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_String, null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_BlaneyCriddle_CheckBlaneyCriddle_String) ) {
		commandList_EditCommand ( __Commands_StateCU_BlaneyCriddle_CheckBlaneyCriddle_String,
		null, __INSERT_COMMAND);
	}

	// StateCU Penman-Monteith (KPM) commands.

	else if ( o == __Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_JMenuItem ) {
		// Read CU Penman-Monteith from KPM file.
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_JMenuItem) {
		// Read CU Penman-Monteith from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_SetPenmanMonteith_JMenuItem) {
		commandList_EditCommand (
		__Commands_StateCU_PenmanMonteith_SetPenmanMonteith_String, null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_SortPenmanMonteith_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_SortPenmanMonteith_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_PenmanMonteith_CheckPenmanMonteith_String) ) {
		commandList_EditCommand ( __Commands_StateCU_PenmanMonteith_CheckPenmanMonteith_String,
		null, __INSERT_COMMAND);
	}

	// StateCU CU Locations (STR) commands.

	// Compare string because several menus use the same action command.
	else if ( action.equals( __Commands_StateCU_CULocations_ReadCULocationsFromList_String)){
		// Read CU Locations from a list file.
		commandList_EditCommand ( __Commands_StateCU_CULocations_ReadCULocationsFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare string because several menus use the same action command.
	else if ( action.equals( __Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String)) {
		// Read CU Locations from a StateCU STR file.
		commandList_EditCommand ( __Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	// Compare string because several menus use the same action command.
	else if ( action.equals( __Commands_StateCU_CULocations_ReadCULocationsFromStateMod_String)){
		// Read CU Locations from a StateMod DDS or WES file.
		commandList_EditCommand ( __Commands_StateCU_CULocations_ReadCULocationsFromStateMod_String,
		null, __INSERT_COMMAND );
	}
	else if ( o == __Commands_StateCU_CULocations_SetCULocation_JMenuItem) {
		// Set CULocation values using user edits.
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetCULocation_String, null,
		__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CULocations_SetCULocationsFromList_JMenuItem) {
		// Set CULocation values from a list.
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetCULocationsFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetDiversionAggregateFromList_String)) {
		commandList_EditCommand (__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateCU string is used, the value of the string is
	// the same for all instances where it is used...
	else if ( action.equals( __Commands_StateCU_CULocations_SetDiversionAggregate_String)) {
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetDiversionAggregate_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals ( __Commands_StateCU_CULocations_SetDiversionSystemFromList_String)) {
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetDiversionSystemFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals ( __Commands_StateCU_CULocations_SetDiversionSystem_String)) {
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetDiversionSystem_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	// Even though the StateMod string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_String)) {
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateMod string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_String)) {
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	else if ( action.equals( __Commands_StateMod_ReservoirStations_SetReservoirAggregate_String)) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_SetReservoirAggregate_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	else if ( action.equals(__Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_String)) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetDiversionAggregate_String)) {
		commandList_EditCommand (__Commands_StateCU_CULocations_SetDiversionAggregate_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetWellAggregateFromList_String)){
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetWellAggregateFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetWellAggregate_String)){
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetWellAggregate_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus (put before shorter string to avoid conflict).
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetWellSystemFromList_String)) {
		commandList_EditCommand (__Commands_StateCU_CULocations_SetWellSystemFromList_String,
		null, __INSERT_COMMAND);
	}
	// Compare strings because the same command is available in several menus.
	// Even though the StateCU string is used, the value of the string is the same for all instances where it is used.
	else if ( action.equals( __Commands_StateCU_CULocations_SetWellSystem_String)) {
		commandList_EditCommand (__Commands_StateCU_CULocations_SetWellSystem_String,
		null, __INSERT_COMMAND);
	}
	else if(o == __Commands_StateCU_CULocations_SortCULocations_JMenuItem) {
		// Sort CULocations using the ID.
		commandList_EditCommand ( __Commands_StateCU_CULocations_SortCULocations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CULocations_FillCULocationsFromList_JMenuItem ) {
		// Fill CULocation data using available data from List.
		commandList_EditCommand ( __Commands_StateCU_CULocations_FillCULocationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CULocations_FillCULocationsFromHydroBase_JMenuItem) {
		// Fill CULocation data using available data from HydroBase.
		commandList_EditCommand (__Commands_StateCU_CULocations_FillCULocationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CULocations_FillCULocation_JMenuItem) {
		// Set CULocation values using user edits.
		commandList_EditCommand (__Commands_StateCU_CULocations_FillCULocation_String, null,
		__INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_JMenuItem) {
		// Set CULocation climate station weights from a list file.
		commandList_EditCommand (
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_String, null,
		__INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_JMenuItem) {
		// Set CULocation climate station weights from HydroBase.
		commandList_EditCommand (
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_String, null,
		__INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CULocations_SetCULocationClimateStationWeights_JMenuItem) {
		// Set CULocation climate station weights.
		commandList_EditCommand ( __Commands_StateCU_CULocations_SetCULocationClimateStationWeights_String,
		null, __INSERT_COMMAND );
	}
	else if (o == __Commands_StateCU_CULocations_FillCULocationClimateStationWeights_JMenuItem) {
		// Fill CULocation climate station weights.
		commandList_EditCommand (__Commands_StateCU_CULocations_FillCULocationClimateStationWeights_String,
		null, __INSERT_COMMAND );
	}
	else if ( o == __Commands_StateCU_CULocations_WriteCULocationsToList_JMenuItem) {
		// Write CULocations out to an STR file.
		commandList_EditCommand ( __Commands_StateCU_CULocations_WriteCULocationsToList_String,
			null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_CULocations_WriteCULocationsToStateCU_JMenuItem) {
		// Write CULocations out to an STR file.
		commandList_EditCommand ( __Commands_StateCU_CULocations_WriteCULocationsToStateCU_String,
			null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_CULocations_CheckCULocations_String)) {
		// Check CULocations.
		commandList_EditCommand ( __Commands_StateCU_CULocations_CheckCULocations_String,
			null, __INSERT_COMMAND);
	}

    // StateCU Parcels (experimental - as input to CDS and IPY).

	else if ( action.equals( __Commands_StateCU_Parcels_ReadParcelsFromHydroBase_String) ) {
		// Read parcels associated with CU Locations from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_Parcels_ReadParcelsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_String) ) {
		// Read parcels associated with CU Locations from irrigated lands table.
		commandList_EditCommand ( __Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_SetParcel_String) ) {
		// Set/remove parcel data.
		commandList_EditCommand ( __Commands_StateCU_Parcels_SetParcel_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_String) ) {
		// Set/remove parcel surface water supply data.
		commandList_EditCommand ( __Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_SetParcelGroundWaterSupply_String) ) {
		// Set/remove parcel groundwater supply data.
		commandList_EditCommand ( __Commands_StateCU_Parcels_SetParcelGroundWaterSupply_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_CheckParcels_String) ) {
		// Check parcels.
		commandList_EditCommand ( __Commands_StateCU_Parcels_CheckParcels_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_CheckIrrigatedLands_String) ) {
		// Check parcels.
		commandList_EditCommand ( __Commands_StateCU_Parcels_CheckIrrigatedLands_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateCU_Parcels_WriteParcelsToFile_String) ) {
		// Write parcels associated with CU Locations to a file.
		commandList_EditCommand ( __Commands_StateCU_Parcels_WriteParcelsToFile_String,
		null, __INSERT_COMMAND);
	}

	// StateCU CDS commands.

	else if (o == __Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_JMenuItem){
		// Create crop pattern TS data for each location.
		commandList_EditCommand ( __Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_JMenuItem){
		// Read CU crop patterns from a StateCU CDS file.
		commandList_EditCommand ( __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	/* FIXME SAM 2008-12-30 Remove if not needed.
	else if (o == __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_JMenuItem) {
		// Read CU crop patterns from a DBF file.
		commandList_EditCommand ( __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_String,
		null, __INSERT_COMMAND);
	}
	*/
	else if (o == __Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_JMenuItem) {
		// Set CU crop patterns from a list.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_JMenuItem) {
		// Read CU crop patterns from HydroBase.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_JMenuItem) {
		// Read CU crop patterns from Parcels.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_String,
		null, __INSERT_COMMAND);
	}
	else if(o==__Commands_StateCU_CropPatternTS_SetCropPatternTS_JMenuItem){
		// Set the crop pattern.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_SetCropPatternTS_String,
		null, __INSERT_COMMAND);
	}
	else if (o ==__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_JMenuItem){
		// Translate crop pattern data.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_String,
		null, __INSERT_COMMAND);
	}
	else if (o ==__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_JMenuItem){
		// Remove crop pattern data.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_String,
		null, __INSERT_COMMAND);
	}
	/* FIXME SAM 2008-12-30 Remove if not needed.
	else if (o == __Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_JMenuItem){
		// Read county crop statistics from DateValue.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_String,
		null, __INSERT_COMMAND);
	}
	*/
	else if (o ==__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_JMenuItem){
		// Fill CU crop patterns by interpolating.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_JMenuItem){
		// Fill CU crop patterns by interpolating.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_String,
		null, __INSERT_COMMAND);
	}
	/* FIXME SAM 2008-12-30 Remove if not needed.
	else if (o ==__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_JMenuItem){
		// Fill CU crop patterns by prorating AgStats.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_String,
		null, __INSERT_COMMAND);
	}
	*/
	else if (o ==__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_JMenuItem){
		// Fill CU crop patterns by using water rights.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_JMenuItem) {
		// Fill CU crop patterns by repeating the value.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_SortCropPatternTS_JMenuItem) {
		// Sort CU crop patterns.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_SortCropPatternTS_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_JMenuItem) {
		// Write CU crop patterns to a StateCU CDS file.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if (o ==__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_JMenuItem) {
		// Write CU crop patterns to a DateValue time series file.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_String,
		null, __INSERT_COMMAND);
	}
	// TODO smalers 2021-01-24 - used for supplemental data?  Not sure if it was fully ever implemented.
    /*
	else if (o ==__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_JMenuItem) {
		// Write CU crop pattern parcel data to file.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_String,
		null, __INSERT_COMMAND);
	}
	*/
	else if ( action.equals(__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_String)) {
		// Compare crop pattern time series files.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_CropPatternTS_CheckCropPatternTS_String)) {
		// Check CU crop pattern time series.
		commandList_EditCommand (__Commands_StateCU_CropPatternTS_CheckCropPatternTS_String,
		null, __INSERT_COMMAND);
	}

	// StateCU Irrigation Practice commands.

	else if (o == __Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_JMenuItem) {
		// Create Irrigation practice time series for CU Locations.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_JMenuItem) {
		// Read CU irrigation practice time series from the TSP file.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	/* TODO 2005-03-07 Unneeded with new commands?
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromDBF_JMenuItem)
		{
		// Read crop pattern TS from a DBF (needed to deal with well data).
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_readCropPatternTSFromDBF_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromHydroBase_JMenuItem) {
		// Read CU crop patterns from HydroBase (needed to deal with well data).
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	*/
	/*
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSGroundwaterAreaFromHydroBase_JMenuItem) {
		// Read groundwater (well-irrigated parcel) area from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSGroundwaterAreaFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSSprinklerAreaFromHydroBase_JMenuItem){
		// Read sprinkler parcels and area from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSSprinklerAreaFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	*/
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_JMenuItem) {
		// Read IPY area from HydroBase.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_JMenuItem) {
		// Read IPY area from List.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_JMenuItem) {
		// Read IPY area from Parcels.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_JMenuItem) {
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_JMenuItem){
		// Set irrigation practice time series.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_JMenuItem) {
		// Set irrigation practice time series.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_JMenuItem) {
		// Fill irrigation practice time series.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_JMenuItem) {
		// Fill irrigation practice time series.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_JMenuItem) {
		// Fill irrigation practice time series.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_JMenuItem) {
		// Read crop pattern time series from a StateCU file.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_JMenuItem ) {
		// Write irrigation practice time series to a DateValue time series file.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_String,
		null, __INSERT_COMMAND);
	}
	else if (o == __Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_JMenuItem) {
		// Write irrigation practice time series to a StateCU file.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_String)) {
		// Compare irrigation practice time series files.
		commandList_EditCommand (__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_String,
		null, __INSERT_COMMAND);
	}
	else if (action.equals(__Commands_StateCU_IrrigationPracticeTS_CheckIrrigationPracticeTS_String)) {
		// Check irrigation practice time series to a StateCU file.
		commandList_EditCommand ( __Commands_StateCU_IrrigationPracticeTS_CheckIrrigationPracticeTS_String,
		null, __INSERT_COMMAND);
	}

	// StateCU Diversion TS... - handled with StateMod.

	// StateCU Well Pumping TS... - handled with StateMod.

	// StateCU Diversion rights... - handled with StateMod.

	// General Commands (same for both models).

    //else if (command.equals(__Commands_General_CheckingResults_OpenCheckFile_String) ) {
    //    commandList_EditCommand ( __Commands_General_CheckingResults_OpenCheckFile_String, null, __INSERT_COMMAND );
    //}
	else if (command.equals(__Commands_General_Comments_Comment_String) ) {
		commandList_EditCommand ( __Commands_General_Comments_Comment_String, null, __INSERT_COMMAND );
	}
    else if (command.equals(__Commands_General_Comments_ReadOnlyComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@readOnly",true) );
        commandList_EditCommand ( __Commands_General_Comments_ReadOnlyComment_String, comments, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_General_Comments_EnabledComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@enabled False",true) );
        commandList_EditCommand ( __Commands_General_Comments_EnabledComment_String, comments, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_General_Comments_ExpectedStatusFailureComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@expectedStatus Failure",true) );
        commandList_EditCommand ( __Commands_General_Comments_ExpectedStatusFailureComment_String, comments, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_General_Comments_ExpectedStatusWarningComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@expectedStatus Warning",true) );
        commandList_EditCommand ( __Commands_General_Comments_ExpectedStatusWarningComment_String, comments, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_General_Comments_RequireApplicationComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@require application StateDMI >= X.YY.ZZ",true) );
        commandList_EditCommand ( __Commands_General_Comments_RequireApplicationComment_String, comments, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_General_Comments_RequireDatastoreComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much verbage.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@require datastore HydroBase >= YYYYMMDD",true) );
        commandList_EditCommand ( __Commands_General_Comments_RequireDatastoreComment_String, comments, __INSERT_COMMAND );
    }
	else if (command.equals(__Commands_General_Comments_StartComment_String) ) {
		commandList_EditCommand ( __Commands_General_Comments_StartComment_String, null, __INSERT_COMMAND );
	}
	else if (command.equals(__Commands_General_Comments_EndComment_String) ) {
		commandList_EditCommand ( __Commands_General_Comments_EndComment_String,	null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_Logging_StartLog_String) ) {
		commandList_EditCommand ( __Commands_General_Logging_StartLog_String, null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_Logging_SetDebugLevel_String) ) {
		commandList_EditCommand ( __Commands_General_Logging_SetDebugLevel_String, null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_Logging_SetWarningLevel_String) ) {
		commandList_EditCommand ( __Commands_General_Logging_SetWarningLevel_String, null, __INSERT_COMMAND );
	}
	else if (command.equals(__Commands_General_Logging_Message_String) ) {
		commandList_EditCommand(__Commands_General_Logging_Message_String, null, __INSERT_COMMAND);
	}
	else if (command.equals( __Commands_General_Running_SetWorkingDir_String) ) {
		commandList_EditCommand ( __Commands_General_Running_SetWorkingDir_String, null, __INSERT_COMMAND );
	}
	else if (command.equals(__Commands_General_Running_Exit_String) ) {
		commandList_EditCommand ( __Commands_General_Running_Exit_String, null, __INSERT_COMMAND );
	}
	/*
    else if (command.equals( __Commands_General_FileHandling_FTPGet_String)) {
        commandList_EditCommand ( __Commands_General_FileHandling_FTPGet_String, null, __INSERT_COMMAND );
    }
    */
	else if ( action.equals( __Commands_General_FileHandling_MergeListFileColumns_String) ) {
		commandList_EditCommand (__Commands_General_FileHandling_MergeListFileColumns_String, null,__INSERT_COMMAND);
	}
    else if (command.equals( __Commands_General_FileHandling_RemoveFile_String)){
        commandList_EditCommand ( __Commands_General_FileHandling_RemoveFile_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_General_FileHandling_FTPGet_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_FTPGet_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_FileHandling_WebGet_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_WebGet_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_FileHandling_AppendFile_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_AppendFile_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_FileHandling_CopyFile_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_CopyFile_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_FileHandling_ListFiles_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_ListFiles_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_FileHandling_UnzipFile_String ) ) {
    	commandList_EditCommand( __Commands_General_FileHandling_UnzipFile_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_Running_FormatDateTimeProperty_String)){
    	commandList_EditCommand(__Commands_General_Running_FormatDateTimeProperty_String, null, __INSERT_COMMAND);
    }
    else if (command.equals( __Commands_General_Running_FormatStringProperty_String)){
    	commandList_EditCommand(__Commands_General_Running_FormatStringProperty_String, null, __INSERT_COMMAND);
    }
	else if ( action.equals( __Commands_General_HydroBase_OpenHydroBase_String) ) {
		commandList_EditCommand (__Commands_General_HydroBase_OpenHydroBase_String, null,__INSERT_COMMAND);
	}
    else if (command.equals( __Commands_General_Running_Exit_String) ) {
        commandList_EditCommand ( __Commands_General_Running_Exit_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_General_Running_SetProperty_String) ) {
        commandList_EditCommand ( __Commands_General_Running_SetProperty_String, null, __INSERT_COMMAND );
    }
	else if (command.equals( __Commands_General_Running_RunCommands_String) ) {
		commandList_EditCommand ( __Commands_General_Running_RunCommands_String, null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_Running_RunProgram_String) ) {
		commandList_EditCommand ( __Commands_General_Running_RunProgram_String, null, __INSERT_COMMAND );
	}
    else if (command.equals( __Commands_General_Running_RunPython_String) ) {
        commandList_EditCommand ( __Commands_General_Running_RunPython_String, null, __INSERT_COMMAND );
    }
	else if (command.equals( __Commands_General_Running_RunR_String) ) {
		commandList_EditCommand ( __Commands_General_Running_RunR_String, null, __INSERT_COMMAND );
	}
	else if ( action.equals( __Commands_General_Running_SetOutputPeriod_String) ) {
		commandList_EditCommand (__Commands_General_Running_SetOutputPeriod_String, null,__INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_General_Running_SetOutputYearType_String) ) {
		commandList_EditCommand (__Commands_General_Running_SetOutputYearType_String, null,__INSERT_COMMAND);
	}
	else if (command.equals( __Commands_General_Running_WritePropertiesToFile_String)){
        commandList_EditCommand ( __Commands_General_Running_WritePropertiesToFile_String, null, __INSERT_COMMAND );
    }
	else if (command.equals( __Commands_General_TestProcessing_WriteProperty_String)){
		commandList_EditCommand ( __Commands_General_TestProcessing_WriteProperty_String, null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_TestProcessing_CreateRegressionTestCommandFile_String) ) {
		commandList_EditCommand ( __Commands_General_TestProcessing_CreateRegressionTestCommandFile_String, null, __INSERT_COMMAND );
	}
	else if (command.equals( __Commands_General_TestProcessing_CompareFiles_String)){
		commandList_EditCommand ( __Commands_General_TestProcessing_CompareFiles_String, null, __INSERT_COMMAND );
	}
    else if (command.equals( __Commands_General_TestProcessing_StartRegressionTestResultsReport_String) ) {
        commandList_EditCommand ( __Commands_General_TestProcessing_StartRegressionTestResultsReport_String, null, __INSERT_COMMAND );
    }

	// Output File Processing Commands.

    else if (command.equals(__Commands_Output_SplitStateModReport_String ) ) {
    	commandList_EditCommand(__Commands_Output_SplitStateModReport_String, null, __INSERT_COMMAND );
    }

	// Spatial Commands.

    else if (command.equals(__Commands_Spatial_WriteTableToGeoJSON_String ) ) {
    	commandList_EditCommand(__Commands_Spatial_WriteTableToGeoJSON_String, null, __INSERT_COMMAND );
    }
    else if (command.equals(__Commands_Spatial_WriteTableToShapefile_String ) ) {
    	commandList_EditCommand(__Commands_Spatial_WriteTableToShapefile_String, null, __INSERT_COMMAND );
    }

	// Spreadsheet Commands.

    else if (command.equals( __Commands_Spreadsheet_NewExcelWorkbook_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_NewExcelWorkbook_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_ReadExcelWorkbook_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_ReadExcelWorkbook_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_ReadTableFromExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_ReadTableFromExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_ReadTableCellsFromExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_ReadTableCellsFromExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_ReadPropertiesFromExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_ReadPropertiesFromExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_SetExcelCell_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_SetExcelCell_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_SetExcelWorksheetViewProperties_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_SetExcelWorksheetViewProperties_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_WriteTableToExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_WriteTableToExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_WriteTableCellsToExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_WriteTableCellsToExcel_String, null, __INSERT_COMMAND );
    }
    /*else if (command.equals( __Commands_Spreadsheet_WriteTimeSeriesToExcel_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_WriteTimeSeriesToExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String, null, __INSERT_COMMAND );
    }*/
    else if (command.equals( __Commands_Spreadsheet_CloseExcelWorkbook_String) ) {
        commandList_EditCommand ( __Commands_Spreadsheet_CloseExcelWorkbook_String, null, __INSERT_COMMAND );
    }

	// Table Commands / Create, Copy, Free Table.

    else if (command.equals( __Commands_TableCreate_NewTable_String) ) {
        commandList_EditCommand ( __Commands_TableCreate_NewTable_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableCreate_CopyTable_String) ) {
        commandList_EditCommand ( __Commands_TableCreate_CopyTable_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableCreate_FreeTable_String) ) {
        commandList_EditCommand ( __Commands_TableCreate_FreeTable_String, null, __INSERT_COMMAND );
    }

	// Table Commands / Read Table.

    else if (command.equals( __Commands_TableRead_ReadTableFromDataStore_String) ) {
    	commandList_EditCommand( __Commands_TableRead_ReadTableFromDataStore_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRead_ReadTableFromDelimitedFile_String) ) {
        commandList_EditCommand ( __Commands_TableRead_ReadTableFromDelimitedFile_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRead_ReadTableFromDBF_String) ) {
        commandList_EditCommand ( __Commands_TableRead_ReadTableFromDBF_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRead_ReadTableFromExcel_String) ) {
    	commandList_EditCommand( __Commands_TableRead_ReadTableFromExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRead_ReadTableFromFixedFormatFile_String) ) {
        commandList_EditCommand ( __Commands_TableRead_ReadTableFromFixedFormatFile_String, null, __INSERT_COMMAND );
    }

    /*else if (command.equals( __Commands_TableRead_ReadTableFromJSON_String) ) {
        commandList_EditCommand ( __Commands_TableRead_ReadTableFromJSON_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRead_ReadTableFromXML_String) ) {
        commandList_EditCommand ( __Commands_TableRead_ReadTableFromXML_String, null, __INSERT_COMMAND );
    }*/

	// Table Commands / Append/Join Tables.

    else if (command.equals( __Commands_TableJoin_AppendTable_String) ) {
        commandList_EditCommand ( __Commands_TableJoin_AppendTable_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableJoin_JoinTables_String) ) {
        commandList_EditCommand ( __Commands_TableJoin_JoinTables_String, null, __INSERT_COMMAND );
    }

	// Table Commands / Manipulate Table Values.

    else if (command.equals( __Commands_TableManipulate_FormatTableDateTime_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_FormatTableDateTime_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_FormatTableString_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_FormatTableString_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_ManipulateTableString_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_ManipulateTableString_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_InsertTableColumn_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_InsertTableColumn_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_DeleteTableColumns_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_DeleteTableColumns_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_DeleteTableRows_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_DeleteTableRows_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_InsertTableRow_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_InsertTableRow_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_SetTableValues_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_SetTableValues_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_SplitTableColumn_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_SplitTableColumn_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_SplitTableRow_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_SplitTableRow_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_TableMath_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_TableMath_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableManipulate_SortTable_String) ) {
        commandList_EditCommand ( __Commands_TableManipulate_SortTable_String, null, __INSERT_COMMAND );
    }

	// Table Commands / Analyze Tables.

    else if (command.equals( __Commands_TableAnalyze_CompareTables_String) ) {
        commandList_EditCommand ( __Commands_TableAnalyze_CompareTables_String, null, __INSERT_COMMAND );
    }

	// Table Commands / Output Table.

    else if (command.equals( __Commands_TableOutput_WriteTableToDelimitedFile_String) ) {
        commandList_EditCommand ( __Commands_TableOutput_WriteTableToDelimitedFile_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableOutput_WriteTableToExcel_String) ) {
    	commandList_EditCommand( __Commands_TableOutput_WriteTableToExcel_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableOutput_WriteTableToHTML_String) ) {
        commandList_EditCommand ( __Commands_TableOutput_WriteTableToHTML_String, null, __INSERT_COMMAND );
    }
    /*else if (command.equals( __Commands_TableOutput_WriteTableToDataStore_String) ) {
    	commandList_EditCommand ( __Commands_TableOutput_WriteTableToDataStore_String, null, __INSERT_COMMAND);
    }*/

	// Table Commands / Running and Properties.

    else if (command.equals( __Commands_TableRunning_SetPropertyFromTable_String) ) {
        commandList_EditCommand ( __Commands_TableRunning_SetPropertyFromTable_String, null, __INSERT_COMMAND );
    }
    else if (command.equals( __Commands_TableRunning_CopyPropertiesToTable_String) ) {
        commandList_EditCommand ( __Commands_TableRunning_CopyPropertiesToTable_String, null, __INSERT_COMMAND );
    }

	// StateMod Commands.

	// StateMod control - response file.

	else if ( o == __Commands_StateMod_Response_ReadResponseFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Response_ReadResponseFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Response_WriteResponseToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Response_WriteResponseToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod control - control file.

	else if ( o == __Commands_StateMod_Control_ReadControlFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Control_ReadControlFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Control_WriteControlToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Control_WriteControlToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod control - output request file.

	else if ( action.equals(__Commands_StateMod_OutputRequest_String) ){
		new ResponseJDialog ( this, "StateMod Output Request File",
			"The output request file is not created with StateDMI.\n" +
			"Instead, use an editor or other software - see the StateMod documentation for format information.",
			ResponseJDialog.OK);
	}

	// StateMod control - reach data file.

	else if ( action.equals(__Commands_StateMod_ReachData_String) ){
		new ResponseJDialog ( this, "StateMod Reach Data File",
			"The reach data file is not created with StateDMI.\n" +
			"Instead, use an editor or other software - see the StateMod documentation for format information.",
			ResponseJDialog.OK);
	}

	// StateCU files for StateMod.

	else if ( action.equals( __Commands_StateMod_StateCUStructure_String) ){
		new ResponseJDialog ( this,	"StateCU Structure File (for AWC)",
		"The StateCU Structure (CU Location) file contains available water content (AWC) data for each structure.\n" +
		"Use the StateCU commands to create this file.",
		ResponseJDialog.OK);
	}
	else if ( action.equals( __Commands_StateMod_IrrigationPracticeTS_String) ){
		new ResponseJDialog ( this,	"StateMod Irrigation Practice Time Series (from StateCU)",
		"Irrigation practice time series are used with variable efficiency analysis.\n" +
		"Irrigation practice time series are created by StateDMI StateCU commands.\n" +
		"Typically, the irrigation practice from a StateCU data set" +
		" is copied to the StateMod data set.\n",
		ResponseJDialog.OK);
	}
	else if ( action.equals( __Commands_StateMod_ConsumptiveWaterRequirementTS_String)){
		new ResponseJDialog ( this,	"StateMod Consumptive Water Requirement Time Series (from StateCU)",
		"Consumptive water requirement time series (monthly and daily)"+
		" are used with variable efficiency analysis.\n" +
		"The irrigation water requirement (IWR) file from StateCU is often specified for CWR\n",
		ResponseJDialog.OK);
	}

	// StateMod Stream Gage Commands.

	else if ( o == __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_JMenuItem) ||
		( o == __Commands_StateMod_Network_ReadStreamGageStationsFromStateMod_JMenuItem ) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_String,
			null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_SetStreamGageStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_SetStreamGageStation_String,
			null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_StreamGageStations_SortStreamGageStations_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_SortStreamGageStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_FillStreamGageStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_FillStreamGageStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_StreamGageStations_CheckStreamGageStations_String) ){
		commandList_EditCommand ( __Commands_StateMod_StreamGageStations_CheckStreamGageStations_String,
		null, __INSERT_COMMAND);
	}

	// Stream gage historical monthly time series.

	else if ( action.equals(__Commands_StateMod_StreamGageHistoricalTS_String) ) {
		new ResponseJDialog ( this, "StateMod Stream Historical Time Series",
		"Stream gage historical time series are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n" +
		"The stream gage stations file can be used as a list for input to other software.",
		ResponseJDialog.OK);
	}

	// Stream gage natural flow time series.

	else if ( action.equals (__Commands_StateMod_StreamGageBaseTS_String) ) {
		new ResponseJDialog ( this, "StateMod Stream Gage Natural Flow Time Series",
		"Stream gage natural flow time series are not created with StateDMI.\n" +
		"Instead, use the StateMod baseflow module, TSTool, a spreadsheet, or other software.\n" +
		"The stream gage stations file can be used as a list for input to other software.",
		ResponseJDialog.OK);
	}

	// StateMod Delay Table Commands.

	else if ( o == __Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_JMenuItem ) {
		// Read StateMod Delay tables from StateMod DLY file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_JMenuItem ) {
		// Read StateMod Delay tables from StateMod DLY file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_JMenuItem ) {
		// Write Delay tables to list file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_JMenuItem ) {
		// Write Delay tables to list file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_JMenuItem ) {
		// Write Delay tables to StateMod DLY file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_JMenuItem ) {
		// Write Delay tables to StateMod DLD file.
		commandList_EditCommand ( __Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Diversion Commands.

	else if ( o == __Commands_StateMod_DiversionStations_SetOutputYearType_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SetOutputYearType_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_DiversionRights_ReadDiversionStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromList_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	// Multiple menu items initiate the same action.
	else if ( (o == __Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_DiversionRights_ReadDiversionStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_Network_ReadDiversionStationsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,
			null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_SortDiversionStations_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SortDiversionStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_SetDiversionStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SetDiversionStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_SetDiversionStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SetDiversionStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_FillDiversionStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_FillDiversionStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_WriteDiversionStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_WriteDiversionStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_DiversionStations_CheckDiversionStations_String)){
		commandList_EditCommand ( __Commands_StateMod_DiversionStations_CheckDiversionStations_String,
		null, __INSERT_COMMAND);
	}

	// Diversion rights.

	else if ( o == __Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_JMenuItem ||
		o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionRightsFromStateMod_JMenuItem ){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_SetDiversionRight_JMenuItem)	{
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_SetDiversionRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_SortDiversionRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_SortDiversionRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_FillDiversionRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_FillDiversionRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_WriteDiversionRightsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_WriteDiversionRightsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_DiversionRights_CheckDiversionRights_String)){
		commandList_EditCommand ( __Commands_StateMod_DiversionRights_CheckDiversionRights_String,
		null, __INSERT_COMMAND);
	}

	// Diversion historical time series (monthly).
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_DiversionHistoricalTSMonthly_CheckDiversionHistoricalTSMonthly_String)){
		commandList_EditCommand ( __Commands_StateMod_DiversionHistoricalTSMonthly_CheckDiversionHistoricalTSMonthly_String,
		null, __INSERT_COMMAND);
	}

	// Historical diversion ts (daily).

	else if ( action.equals (__Commands_StateMod_DiversionHistoricalTSDaily_String) ) {
		new ResponseJDialog ( this, "StateMod Diversion Historical Time Series (Daily)",
		"Daily historical diversion time series are not created with StateDMI.\n" +
		"Instead, StateMod's estimation features, TSTool, a spreadsheet, or other software.\n" +
		"The diversion stations file can be used as a list for input to other software.",
			ResponseJDialog.OK);
	}

	// Diversion demand time series (monthly)...=

	// other commands are handled with stations.
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_DiversionDemandTSMonthly_CheckDiversionDemandTSMonthly_String)){
		commandList_EditCommand ( __Commands_StateMod_DiversionDemandTSMonthly_CheckDiversionDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}

	// Daily diversion demand.

	else if ( action.equals (__Commands_StateMod_DiversionDemandTSDaily_String) ) {
		new ResponseJDialog ( this, "StateMod Diversion Demand Time Series (Daily)",
		"Daily diversion demand time series are not created with StateDMI.\n" +
		"Instead, StateMod's estimation features, TSTool, a spreadsheet, or other software.\n" +
		"The diversion stations file can be used as a list for input to other software.",
			ResponseJDialog.OK);
	}

	// Diversion demand override.

	else if ( action.equals( __Commands_StateMod_DiversionDemandTSOverrideMonthly_String) ||
		action.equals( __Commands_StateMod_DiversionDemandTSAverageMonthly_String)){
		new ResponseJDialog ( this,	"StateMod Diversion Demand Override Time Series",
		"Diversion demand override time series are used to override the"
		+ " normal monthly demand time series.\n" +
		"The override time series file is not created with StateDMI commands.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n\n" +
		"Similarly, diversion demand average monthly time series are "+
		"used when normal monthly demand time series are not available.\n" +
		"The average time series file is not created with StateDMI commands.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n",
		ResponseJDialog.OK);
	}

	// StateMod Precipitation commands.

	else if ( action.equals( __Commands_StateMod_PrecipitationTSMonthly_String) ) {
		new ResponseJDialog ( this,	"StateMod Precipitation Time Series",
		"Precipitation time series are used with reservoir " +
		"stations to estimate net evaporation.\n" +
		"Precipitation time series are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n",
		ResponseJDialog.OK);
	}

	// StateMod Evaporation commands.

	else if ( action.equals( __Commands_StateMod_EvaporationTSMonthly_String) ) {
		new ResponseJDialog ( this,	"StateMod Evaporation Time Series",
		"Evaporation time series are used with reservoir stations to estimate net evaporation.\n" +
		"Evaporation time series are not created with StateDMI.\n" +
		"Instead, use TSTool, a spreadsheet, or other software.\n",
		ResponseJDialog.OK);
	}

	// StateMod Reservoir Commands.

	else if ( (o == __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_ReservoirRights_ReadReservoirStationsFromList_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_ReservoirRights_ReadReservoirStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_Network_ReadReservoirStationsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_SetReservoirStation_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_ReservoirStations_SetReservoirStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_SortReservoirStations_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_SortReservoirStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_FillReservoirStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_FillReservoirStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_ReservoirStations_CheckReservoirStations_String) ){
		commandList_EditCommand ( __Commands_StateMod_ReservoirStations_CheckReservoirStations_String,
		null, __INSERT_COMMAND);
	}

	// Reservoir rights.

	else if ( o == __Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_SetReservoirRight_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_SetReservoirRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_SortReservoirRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_SortReservoirRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_FillReservoirRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_FillReservoirRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_ReservoirRights_CheckReservoirRights_String)){
		commandList_EditCommand ( __Commands_StateMod_ReservoirRights_CheckReservoirRights_String,
		null, __INSERT_COMMAND);
	}

	// Reservoir return commands.

	else if ( o == __Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Reservoir content and target time series commands.

	else if ( action.equals( __Commands_StateMod_ReservoirContentAndTargetTS_String) ){
		new ResponseJDialog ( this,	"StateMod Reservoir Content Time Series",
		"Reservoir content and target time series are not created with StateDMI.\n"
		+ "Instead, use TSTool, a spreadsheet, or other software.\n" +
		"The reservoir stations list can be used as input to other software\n",
		ResponseJDialog.OK);
	}

	// Instream flow station Commands.

	else if ( (o == __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromList_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromStateMod_JMenuItem) ||
		//(o ==__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_InstreamFlowStations_CheckInstreamFlowStations_String)){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowStations_CheckInstreamFlowStations_String,
		null, __INSERT_COMMAND);
	}

	// StateMod instream flow rights.

	else if ( o == __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowRightsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_JMenuItem) {
		commandList_EditCommand (__Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_JMenuItem)	{
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_InstreamFlowRights_CheckInstreamFlowRights_String)){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowRights_CheckInstreamFlowRights_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Instream Flow demand TS (average monthly) commands.

	// SetOutputYearType() handled generically.
	// ReadInstreamFlowStationsFromStateMod() handled elsewhere.
	// ReadInstreamFlowRightsFromStateMod() handled elsewhere.
	else if ( o == __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_JMenuItem ) {
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_CheckInstreamFlowDemandTSAverageMonthly_String)){
		commandList_EditCommand ( __Commands_StateMod_InstreamFlowDemandTSAverageMonthly_CheckInstreamFlowDemandTSAverageMonthly_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Instream Flow demand TS (monthly, daily) commands.

	else if ( action.equals( __Commands_StateMod_InstreamFlowDemandTS_String) ) {
		new ResponseJDialog ( this,	"StateMod Instream Flow Demand Time Series",
		"Instream flow demand (monthly, daily) time series are not created with StateDMI.\n"
		+ "Instead, use TSTool, a spreadsheet, or other software.\n",
			ResponseJDialog.OK);
	}

	// StateMod Well Station Commands.

	else if ( (o == __Commands_StateMod_WellStations_ReadWellStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_WellRights_ReadWellStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromList_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadWellStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_WellStations_ReadWellStationsFromNetwork_JMenuItem) ||
		(o == __Commands_StateMod_WellRights_ReadWellStationsFromNetwork_JMenuItem) ){
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadWellStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_WellStations_ReadWellStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_WellRights_ReadWellStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_Network_ReadWellStationsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_WellStations_ReadWellRightsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellRightsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadWellRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SortWellStations_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SortWellStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_FillWellStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_FillWellStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_FillWellStation_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_WellStations_FillWellStation_String,
		null,__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_WriteWellStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_WriteWellStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellStations_WriteWellStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellStations_WriteWellStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_WellStations_CheckWellStations_String)){
		commandList_EditCommand ( __Commands_StateMod_WellStations_CheckWellStations_String,
		null, __INSERT_COMMAND);
	}

	// StateMod parcel commands.

	else if ( o == __Commands_StateMod_WellRights_ReadParcelsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_ReadParcelsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Well right commands.

	else if ( o == __Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_ReadWellRightsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_ReadWellRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_SetWellRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_SetWellRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_FillWellRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_FillWellRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_MergeWellRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_WellRights_MergeWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_AggregateWellRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_WellRights_AggregateWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_SortWellRights_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_WellRights_SortWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_CheckWellRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_CheckWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_WriteWellRightsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_WriteWellRightsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellRights_WriteWellRightsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellRights_WriteWellRightsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_WellRights_CheckWellRights_String)){
		commandList_EditCommand ( __Commands_StateMod_WellRights_CheckWellRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_Shared_WriteCheckFile_String) ){
		commandList_EditCommand ( __Commands_Shared_WriteCheckFile_String, null, __INSERT_COMMAND);
	}

	// StateMod well pumping time series (monthly).

	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_WellHistoricalPumpingTSMonthly_CheckWellHistoricalPumpingTSMonthly_String)){
		commandList_EditCommand ( __Commands_StateMod_WellHistoricalPumpingTSMonthly_CheckWellHistoricalPumpingTSMonthly_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Well pumping time series (daily).

	else if ( action.equals( __Commands_StateMod_WellHistoricalPumpingTSDaily_String) ) {
		new ResponseJDialog ( this, "StateMod Well Historical Pumping Time Series (Daily)",
		"Well historical pumping time series (daily) are not created with StateDMI.\n"
		+ "Instead, use TSTool, a spreadsheet, or other software.\n", ResponseJDialog.OK);
	}

	// StateMod Well demand time series (monthly).

	// Other commands are handled with stations.
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_SetWellStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_SetWellStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_WellDemandTSMonthly_CheckWellDemandTSMonthly_String)){
		commandList_EditCommand ( __Commands_StateMod_WellDemandTSMonthly_CheckWellDemandTSMonthly_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Well demand time series (daily).

	else if ( action.equals( __Commands_StateMod_WellDemandTSDaily_String) ) {
		new ResponseJDialog ( this, "StateMod Well Demand Time Series (Daily)",
		"Well demand time series (daily) are not created with StateDMI.\n"
		+ "Instead, use TSTool, a spreadsheet, or other software.\n", ResponseJDialog.OK);
	}

	// Plan station commands.

	else if ( o == __Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_PlanStations_SetPlanStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanStations_SetPlanStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_PlanStations_WritePlanStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanStations_WritePlanStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// Plan Well Augmentation commands.

	else if ( o == __Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// Plan return commands.

	else if ( o == __Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Stream Estimate Commands.

	// Stream estimate stations.

	else if ( (o == __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_JMenuItem) ||
		(o == __Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromList_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_JMenuItem) ||
		(o == __Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromNetwork_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_JMenuItem) ||
		(o == __Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromStateMod_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o ==__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( (o == __Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_JMenuItem) ||
		(o == __Commands_StateMod_StreamEstimateCoefficients_SortStreamEstimateStations_JMenuItem) ) {
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_String,
		null,__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_String,
		null,__INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_StreamEstimateStations_CheckStreamEstimateStations_String)){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateStations_CheckStreamEstimateStations_String,
		null, __INSERT_COMMAND);
	}

	// StateMod Stream estimate coefficients.

	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_JMenuItem) {
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals(__Commands_StateMod_StreamEstimateCoefficients_CheckStreamEstimateCoefficients_String)){
		commandList_EditCommand ( __Commands_StateMod_StreamEstimateCoefficients_CheckStreamEstimateCoefficients_String,
		null, __INSERT_COMMAND);
	}

	// StateMod stream estimate time series commands.

	else if ( action.equals( __Commands_StateMod_StreamEstimateBaseTS_String) ) {
		new ResponseJDialog ( this,	"StateMod Stream Estimate Natural Flow Time Series",
		"Stream estimate natural flow time series are not created with StateDMI.\n" +
		"Instead, use the StateMod baseflow module, TSTool, a spreadsheet, or other software.\n" +
		"The stream estimate stations file can be used as a list for input to other software.",
			ResponseJDialog.OK);
	}

	// StateMod Network (output NET) commands.

	else if ( o == __Commands_StateMod_Network_ReadNetworkFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadNetworkFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_AppendNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_AppendNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadRiverNetworkFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadRiverNetworkFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadDiversionStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadDiversionStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadReservoirStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadReservoirStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadWellStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadWellStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_CreateNetworkFromRiverNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_CreateNetworkFromRiverNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_FillNetworkFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_FillNetworkFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_WriteNetworkToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_WriteNetworkToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_WriteNetworkToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_WriteNetworkToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_Network_PrintNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_Network_PrintNetwork_String,
		null, __INSERT_COMMAND);
	}

	// StateMod River Network (output RIN) commands.

	else if ( o == __Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_JMenuItem ||
		o == __Commands_StateMod_StreamGageStations_ReadNetworkFromStateMod_JMenuItem ||
		o == __Commands_StateMod_StreamEstimateStations_ReadNetworkFromStateMod_JMenuItem){
		commandList_EditCommand (__Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_SetRiverNetworkNode_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_SetRiverNetworkNode_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_FillRiverNetworkNode_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_FillRiverNetworkNode_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( action.equals( __Commands_StateMod_RiverNetwork_CheckRiverNetwork_String)){
		commandList_EditCommand ( __Commands_StateMod_RiverNetwork_CheckRiverNetwork_String,
		null, __INSERT_COMMAND);
	}

	// StateMod operational rights commands.

	else if ( o == __Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_OperationalRights_SetOperationalRight_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_OperationalRights_SetOperationalRight_String,
		null, __INSERT_COMMAND);
	}
	else if ( o == __Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_JMenuItem){
		commandList_EditCommand ( __Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_String,
		null, __INSERT_COMMAND);
	}

	// StateMod San Juan Sediment Recovery plan commands.

	else if ( action.equals( __Commands_StateMod_DownstreamCallTSDaily_String) ) {
		new ResponseJDialog ( this, "StateMod Downstream Call TS (Daily)",
		"StateDMI does not currently process downstream call time series (daily) data.\n" +
		"Instead, use an editor, TSTool, spreadsheet or other software.",
		ResponseJDialog.OK);
	}

	// StateMod San Juan Sediment Recovery plan commands.

	else if ( action.equals( __Commands_StateMod_SanJuanSedimentRecoveryPlan_String) ) {
		new ResponseJDialog ( this, "StateMod San Juan Sediment Recovery Plan",
		"StateDMI does not currently process San Juan Sediment Recovery Plan data.\n" +
		"Instead, use an editor or other software.",
		ResponseJDialog.OK);
	}

	// StateMod Rio Grande Spill commands.

	else if ( action.equals( __Commands_StateMod_RioGrandeSpill_String) ) {
		new ResponseJDialog ( this, "StateMod Rio Grande Spill",
		"StateDMI does not currently process Rio Grande spill data.\n" +
		"Instead, use an editor or other software.",
		ResponseJDialog.OK);
	}

	// StateMod spatial data.

	else if ( action.equals( __Commands_StateMod_GeoViewProject_String) ) {
		new ResponseJDialog ( this, "GeoView Project",
		"StateDMI does not currently process the GeoView project file,\n" +
		"which is used to configure the map interface for the StateMod GUI.\n" +
		"Instead, use an editor or other software.",
		ResponseJDialog.OK);
	}

	// Popup menu.

	else if ( o == __CommandsPopup_FindCommandsUsingString_JMenuItem ) {
		new FindInJListJDialog(this,__commands_JList,"Find Command(s)");
		ui_CheckGUIState();
	}
	else if ( o == __CommandsPopup_FindCommandsUsingLineNumber_JMenuItem ) {
		// Display a dialog to ask for the line number.
		String line = new TextResponseJDialog ( this, "Find line number.",
		"Enter the line number to find and press OK.\n" +
		"If found, the line will be selected and all others will be deselected.\n",
		ResponseJDialog.OK | ResponseJDialog.CANCEL ).response();
		if ( StringUtil.isInteger(line) ) {
			int iline = StringUtil.atoi ( line );
			if ( iline <= 0 ) {
				// Adjust so following code will work.
				iline = 1;
			}
			if ( iline <= __commands_JListModel.size() ) {
				__commands_JList.clearSelection();
				__commands_JList.setSelectedIndex ( iline - 1 );
				// Make sure that the line is visible.
				__commands_JList.ensureIndexIsVisible(iline -1);
			}
		}
		ui_CheckGUIState();
	}

	// Run menu.

    else if ( action.equals(__Run_AllCommandsCreateOutput_String) ) {
		// Use a string comparison because the action can be initiated
		// from different buttons and menus but the action command is the same.
		// Process time series and create all output from write* commands.
		uiAction_RunCommands ( true, true );
	}
    else if ( action.equals(__Run_AllCommandsIgnoreOutput_String) ) {
		// Use a string comparison because the action can be initiated
		// from different buttons and menus but the action command is the same.
		// Process time series but ignore write* commands.
		uiAction_RunCommands ( true, false );
	}
    else if ( action.equals(__Run_SelectedCommandsCreateOutput_String) ) {
		// Use a string comparison because the action can be initiated
		// from different buttons and menus but the action command is the same.
		// Process selected commands and create all output from write* commands.
		uiAction_RunCommands ( false, true );
	}
    else if ( action.equals(__Run_SelectedCommandsIgnoreOutput_String) ) {
		// Use a string comparison because the action can be initiated
		// from different buttons and menus but the action command is the same.
		// Process selected commands but ignore write* commands.
		uiAction_RunCommands ( false, false );
	}
	else if ( o == __Run_CommandsFromFile_JMenuItem ) {
		/* TODO SAM - add later.
		// Run an external command file with results NOT shown in the GUI.
		JFileChooser fc = new JFileChooser();
		fc.setDialogTitle("Select Command File - will be run externally");
		if ( __last_directory_selected != null) {
			fc.setCurrentDirectory(new File(__last_directory_selected));
		}
		if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
			String directory = fc.getSelectedFile().getParent();
			String filename = fc.getName(fc.getSelectedFile());

			if (filename == null || filename.equals("")) {
				return;
			}
			if (directory != null) {
				__last_directory_selected = directory;
			}

			String fs = System.getProperty ("file.separator");
			String path = directory + fs + filename;
			if (path != null) {
				try {
					_StateDMI_Processor.processCommands (path );
				} catch (Exception e2) {
					Message.printWarning (1, routine, "Error processing commands in file \"" + path + "\"");
				}
			}
		}
		*/
	}
	else if (action.equals(__Run_CancelCommandProcessing_String) ) {
		// Cancel the current processor.  This may take awhile to occur.
		__statedmiProcessor.setCancelProcessingRequested ( true );
		ui_UpdateStatusTextFields ( 1, routine, null, "Processing is bing cancelled...", __STATUS_CANCELING );
		ui_UpdateStatus ( true );
	}
	else if ( o == __Run_RunStateCUVersion_JMenuItem ) {
		// Run StateCU -version
		String [] command_array = new String[2];
		command_array[0] = "statemod";
		command_array[1] = "-version";
		ProcessManager pm = new ProcessManager ( command_array );
		new ProcessManagerJDialog ( this, "StateMod Version", pm );
	}
	else if ( o == __Run_RunStateModVersion_JMenuItem ) {
		// Run StateMod -version.
		String [] command_array = new String[2];
		command_array[0] = "statemod";
		command_array[1] = "-version";
		ProcessManager pm = new ProcessManager ( command_array );
		new ProcessManagerJDialog ( this, "StateMod Version", pm );
	}

	// Results menu (StateCU).

	// TODO - how to handle control data?
	else if ( o == __Results_StateCU_ClimateStationsData_JMenuItem ) {
		results_ShowStateCUClimateStationData ();
	}
	else if ( o == __Results_StateCU_CropCharacteristicsData_JMenuItem ) {
		results_ShowStateCUCropCharacteristicsData ();
	}
	else if ( o == __Results_StateCU_DelayTablesData_JMenuItem ) {
		results_ShowStateCUDelayTableData();
	}
	else if ( o == __Results_StateCU_CULocationsData_JMenuItem ) {
		results_ShowStateCULocationData();
	}

	// Results menu (StateMod).

	// TODO - how to handle control data?
	else if ( o == __Results_StateMod_RiverData_JMenuItem ) {
		results_ShowStateModStreamGageData ();
	}
	else if ( o == __Results_StateMod_DelayTableData_JMenuItem ) {
		results_ShowStateModDelayTableData ();
	}
	else if ( o == __Results_StateMod_DiversionData_JMenuItem ) {
		results_ShowStateModDiversionData ();
	}
	else if ( o == __Results_StateMod_InstreamFlowData_JMenuItem ) {
		results_ShowStateModInstreamFlowData ();
	}
	else if ( o == __Results_StateMod_PrecipitationData_JMenuItem ) {
		results_ShowStateModPrecipitationData ();
	}
	else if ( o == __Results_StateMod_EvaporationData_JMenuItem ) {
		results_ShowStateModEvaporationData ();
	}
	else if ( o == __Results_StateMod_ReservoirData_JMenuItem ) {
		results_ShowStateModReservoirData ();
	}
	else if ( o == __Results_StateMod_WellData_JMenuItem ) {
		results_ShowStateModWellData ();
	}
	else if ( o == __Results_StateMod_RiverNetworkData_JMenuItem ) {
		results_ShowStateModRiverNetworkData ();
	}
	else if ( o == __Results_StateMod_OperationalData_JMenuItem ) {
		results_ShowStateModOperationalData ();
	}
	// TODO
	//else if ( o == __Results_StateMod_SanJuanData_JMenuItem ) {
		//results_ShowStateModSanJuanData ();
	//}

	// Tools menu.

	else if ( o == __Tools_AdministrationNumberCalculator_JMenuItem ) {
		new HydroBase_GUI_AdminNumCalculator(__statedmiProcessor.getHydroBaseDMIConnection(), this);
	}
	else if ( o == __Tools_CompareFiles_StateModWellRights_JMenuItem ) {
		// Select 2 files.
		JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle("Select 1st StateMod Well Rights File");
		fc.addChoosableFileFilter( new SimpleFileFilter("wer", "StateMod Well Rights File") );
		if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
			return;
		}
		JGUIUtil.setLastFileDialogDirectory(fc.getSelectedFile().getParent() );
		String path1 = fc.getSelectedFile().getPath();

		fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle("Select 2nd StateMod Well Rights File");
		fc.addChoosableFileFilter( new SimpleFileFilter("wer", "StateMod Well Rights File") );
		if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
			return;
		}
		JGUIUtil.setLastFileDialogDirectory( fc.getSelectedFile().getParent() );
		String path2 = fc.getSelectedFile().getPath();

		try {
			List v = StateMod_Util.compareFiles ( path1, path2, StateMod_DataSet.COMP_WELL_RIGHTS );
			PropList reportProp = new PropList ("Well Rights");
			reportProp.set ( "TotalWidth", "600" );
			reportProp.set ( "TotalHeight", "300" );
			reportProp.set ( "DisplayFont", "Courier" );
			reportProp.set ( "DisplaySize", "11" );
			reportProp.set ( "PrintFont", "Courier" );
			reportProp.set ( "PrintSize", "7" );
			reportProp.set ("Title", "Well Rights File Comparison");
			reportProp.setUsingObject ( "ParentUIComponent", this );
			new ReportJFrame ( v, reportProp );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Unable to compare files." );
			Message.printWarning ( 2, routine, e );
		}
	}
	else if ( o == __Tools_ListSurfaceWaterDiversions_JMenuItem ) {
		// Loop through the diversion stations and, if not listed in the well stations, print a message to the log file.
		String id;
		StateMod_Diversion div;
		List div_List = __statedmiProcessor.getStateModDiversionStationList();
		int size = div_List.size();
		List well_List = __statedmiProcessor.getStateModWellStationList();
		for ( int i = 0; i < size; i++ ) {
			div = (StateMod_Diversion)div_List.get(i);
			id = div.getID();
			if ( StateMod_Util.indexOf(well_List,id)< 0) {
				Message.printStatus ( 2, routine, "Surface supply only diversion:  " + id + " " + div.getName() );
			}
		}
	}
	else if ( o == __Tools_ListWellStationRightTotals_JMenuItem ) {
		uiAction_Tool_ListWellStationRightTotals ();
	}
	else if ( o == __Tools_HydrobaseParcelWaterSupply_JMenuItem ) {
		new HydroBase_GUI_IrrigatedAcresTool ( __statedmiProcessor.getHydroBaseDMIConnection(),
			__statedmiProcessor.getStateModDiversionStationList(), __statedmiProcessor.getStateModWellStationList() );
	}
	else if ( o == __Tools_ViewLogFile_Startup_JMenuItem ) {
		// View the startup log file.
		String logFile = session.getUserLogFile();
		// Show in a simple viewer.
		PropList reportProp = new PropList ("Startup Log File");
		reportProp.set ( "TotalWidth", "800" );
		reportProp.set ( "TotalHeight", "600" );
		reportProp.set ( "DisplayFont", "Courier" );
		reportProp.set ( "DisplaySize", "11" );
		reportProp.set ( "PrintFont", "Courier" );
		reportProp.set ( "PrintSize", "7" );
		reportProp.set ( "Title", "Startup Log File" );
		reportProp.setUsingObject ( "ParentUIComponent", this );
		try {
			List<String> logLines = IOUtil.fileToStringList(logFile);
			new ReportJFrame ( logLines, reportProp );
		}
		catch ( Exception e ) {
			Message.printWarning(1, routine, "Error viewing startup log file (" + e + ")." );
		}
	}

	// Help menu.

	else if ( o == __Help_AboutStateDMI_JMenuItem ) {
		String helpString =
		IOUtil.getProgramName() + " " + IOUtil.getProgramVersion() + "\n\n" +
		"Creates dataset files for StateCU and StateMod.\n\n" +
	    "StateDMI is a part of Colorado's Decision Support Systems (CDSS)\n" +
	    "Copyright (C) 1997-2023 Colorado Department of Natural Resources\n" +
	    " \n" +
	    "StateDMI is free software:  you can redistribute it and/or modify\n" +
	    "    it under the terms of the GNU General Public License as published by\n" +
	    "    the Free Software Foundation, either version 3 of the License, or\n" +
	    "    (at your option) any later version.\n" +
	    " \n" +
	    "StateDMI is distributed in the hope that it will be useful,\n" +
	    "    but WITHOUT ANY WARRANTY; without even the implied warranty of\n" +
	    "    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n" +
	    "    GNU General Public License for more details.\n" +
	    " \n" +
	    "You should have received a copy of the GNU General Public License\n" +
	    "    along with StateDMI.  If not, see <https://www.gnu.org/licenses/>.\n" +
	    " \n" +
		"Developed by the Open Water Foundation\n" +
		"\n" +
		"Funded by:\n" +
		"Colorado Division of Water Resources\n" +
		"Colorado Water Conservation Board\n" +
		"\n" +
		"Send comments to\n" +
		"DNR_OpenCDSS@state.co.us\n" +
		"steve.malers@openwaterfoundation.org";
		new HelpAboutJDialog (this, "About StateDMI", helpString, true );
	}
	else if ( command.equals ( __Help_ViewDocumentation_String ) ||
	    command.equals(__Help_ViewDocumentation_ReleaseNotes_String) ||
        command.equals(__Help_ViewDocumentation_UserManual_String) ||
        command.equals(__Help_ViewDocumentation_CommandReference_String) ||
        command.equals(__Help_ViewDocumentation_DatastoreReference_String) ||
        command.equals(__Help_ViewDocumentation_Troubleshooting_String) ) {
        uiAction_ViewDocumentation ( command );
    }
    //else if ( command.equals ( __Help_ViewTrainingMaterials_String )) {
    //    uiAction_ViewTrainingMaterials ();
    //}

	// Check the GUI state and disable buttons, etc., depending on the selections that are made
	// (for example this enables the paste menus when commands are copied).

	ui_UpdateStatus ( true );
}

/**
Add a TS_ListSelector_JFrame to the list that is being managed.
This is necessary because the information about the selector must be saved so that it can be used later when creating graphs.
The generic selector has no way to save specific data set component information.
*/
private void addTS_ListSelector_JFrame ( TS_ListSelector_JFrame selector, int app_type, int comp_type ) {
	// Add to the list being maintained.
	TS_ListSelector_JFrame_List.add ( selector );
	TS_ListSelector_JFrame_app_type_List.add ( new Integer(app_type) );
	TS_ListSelector_JFrame_comp_type_List.add ( new Integer(comp_type) );
	// Listen for selector events.
	selector.addTSListSelectorListener ( this );
}

/**
Indicate that a command has been cancelled.  The success/failure of the command is not indicated (see CommandStatusProvider).
@param icommand The command index (0+).
@param ncommand The total number of commands to process
@param command The reference to the command that has been cancelled,
either the one that has just been processed, or potentially the next one, depending on when the cancel was requested.
@param percent_complete If >= 0, the value can be used to indicate progress
running a list of commands (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its own determination
(e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandCanceled ( int icommand, int ncommand, Command command,
		float percent_complete, String message ) {
	String routine = getClass().getSimpleName() + ".commandCancelled";

	// Last refresh the results with what is available.
	//String command_string = command.toString();
	ui_UpdateStatusTextFields ( 1, routine,	null, "Canceled command processing.",
			//"Cancelled: " + command_string,
				__STATUS_CANCELLED );
	uiAction_RunCommands_ShowResults();
}

/**
Indicate that a command has completed.  The success/failure of the command is not indicated (see CommandStatusProvider).
@param icommand The command index (0+).
@param ncommand The total number of commands to process
@param command The reference to the command that is starting to run,
provided to allow future interaction with the command.
@param percent_complete If >= 0, the value can be used to indicate progress
running a list of commands (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its own determination
(e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandCompleted ( int icommand, int ncommand, Command command,
		float percent_complete, String message ) {
	String routine = "StateDMI_JFrame.commandCompleted";
	// Update the progress bar to indicate progress (1 to number of commands... completed).
	__processor_JProgressBar.setValue ( icommand + 1 );
	// For debugging.
	//Message.printStatus(2,getClass().getName()+".commandCompleted", "Setting processor progress bar to " + (icommand + 1));
	__command_JProgressBar.setValue ( __command_JProgressBar.getMaximum() );

	if ( ((icommand + 1) == ncommand) || command instanceof Exit_Command ) {
		// Last command has completed (or Exit()) so refresh the results.
		// Only need to do if threaded because otherwise will handle synchronously in the uiAction_RunCommands() method.
		String command_string = command.toString();
		ui_UpdateStatusTextFields ( 1, routine, null, "Processed: " + command_string, __STATUS_READY );
		if ( ui_Property_RunCommandProcessorInThread() ) {
			uiAction_RunCommands_ShowResults ();
		}
	}
}

/**
Determine whether commands are equal.  To allow for multi-line commands,
each command is stored in a list (but typically only the first String is used.
@param original_command Original command as a list of String or Command.
@param edited_command Edited command as a list of String or Command.
*/
private boolean commandList_CommandsAreEqual(List original_command, List edited_command) {
	if ( (original_command == null) && (edited_command != null) ) {
		return false;
	}
	else if ( (original_command != null) && (edited_command == null) ) {
		return false;
	}
	else if ( (original_command == null) && (edited_command == null) ) {
		// Should never occur?
		return true;
	}
	int original_size = original_command.size();
	int edited_size = edited_command.size();
	if ( original_size != edited_size ) {
		return false;
	}
	Object original_Object, edited_Object;
	String original_String = null, edited_String = null;
	for ( int i = 0; i < original_size; i++ ) {
		original_Object = original_command.get(i);
		edited_Object = edited_command.get(i);
		if ( original_Object instanceof String ) {
			original_String = (String)original_Object;
		}
		else if ( original_Object instanceof Command ) {
			original_String = ((Command)original_Object).toString();
		}
		if ( edited_Object instanceof String ) {
			edited_String = (String)edited_Object;
		}
		else if ( edited_Object instanceof Command ) {
			edited_String = ((Command)edited_Object).toString();
		}
		// Must be an exact match.
		if ( (original_String == null) && (edited_String != null) ) {
			return false;
		}
		else if ((original_String != null) && (edited_String == null)) {
			return false;
		}
		else if ((original_String == null) && (edited_String == null)) {
			continue;
		}
		else if ( !original_String.equals(edited_String) ) {
			return false;
		}
	}
	// Must be the same.
	return true;
}

/**
Edit a command in the command list.
@param action the string containing the event's action value.  This is checked for new commands.
When editing existing commands, command_List will contain a list of Command class instances.
Normally only the first command will be edited as a single-line command.
However, multiple # comment lines can be selected and edited at once.
@param command_List If an update, this contains the current Command instances to edit.
If a new command, this is null and the action string will be consulted to construct the appropriate command.
The only time that multiple commands will be edited are when they are in a {# delimited comment block).
@param mode the action to take when editing the command
(__INSERT_COMMAND for a new command or __UPDATE_COMMAND for an existing command).
*/
private void commandList_EditCommand ( String action, List<Command> command_List, int mode ) {
	String routine = getClass().getSimpleName() + ".editCommand";
	int dl = 1;		// Debug level.

    // Make absolutely sure that warning level 1 messages are shown to the user in a dialog.
    // This may have been turned off in command processing.
    // Should not need this if set properly in the command processor.
    //Message.setPropValue ( "ShowWarningDialog=true" );

	// Indicate whether the commands are a block of # comments.
	// If so then need to use a special editor rather than typical one-line editors.
	boolean is_comment_block = false;
	if ( mode == __UPDATE_COMMAND ) {
		is_comment_block = commandList_IsCommentBlock ( __statedmiProcessor,
			command_List,
			true,	// All must be comments.
			true );	// Comments must be contiguous.
	}
	else {
		// New command, so look for comment actions.
		if ( action.equals(__Commands_General_Comments_Comment_String) ||
	        action.equals(__Commands_General_Comments_ReadOnlyComment_String) ||
	        action.equals(__Commands_General_Comments_EnabledComment_String) ||
	        action.equals(__Commands_General_Comments_ExpectedStatusFailureComment_String) ||
	        action.equals(__Commands_General_Comments_ExpectedStatusWarningComment_String) ||
	        action.equals(__Commands_General_Comments_RequireApplicationComment_String) ||
	        action.equals(__Commands_General_Comments_RequireDatastoreComment_String) ) {
			is_comment_block = true;
		}
	}
	if ( is_comment_block ) {
		Message.printStatus(2, routine, "Command is a comment block.");
	}

	try {
        // Main try to help with troubleshooting, especially during transition to new command structure.

		// First make sure we have a Command object to edit.
		// If an old-style command then it will be stored in a GenericCommand.
		// The Command object is inserted in the processor in any case,
		// to take advantage of processor information (such as being able to get the time series identifiers from previous commands.
		// If a new command is being inserted and a cancel occurs, the command will simply be removed from the list.
		// If an existing command is being updated and a cancel occurs, the changes need to be ignored.

		Command command_to_edit_original = null;	// Command being edited (original).
		Command command_to_edit = null;	// Command being edited (clone).
		if ( mode == __UPDATE_COMMAND ) {
			// Get the command from the processor.
			if ( is_comment_block ) {
				// Use the string-based editor dialog and then convert each comment line into a command.
				// Don't do anything to the command list yet.
			}
			else {
				// Get the original command.
				command_to_edit_original = command_List.get(0);
				// Clone it so that the edit occurs on the copy.
				command_to_edit = (Command)command_to_edit_original.clone();
				Message.printStatus(2, routine, "Cloned command to edit: \"" + command_to_edit + "\"" );
				// Remove the original command.
				int pos = commandList_IndexOf ( command_to_edit_original );
				commandList_RemoveCommand ( command_to_edit_original );
				// Insert the copy during the edit.
				commandList_InsertCommandAt ( command_to_edit, pos );
				Message.printStatus(2, routine, "Will edit the copy and restore to the original if the edit is cancelled.");
			}
		}
		else if ( mode == __INSERT_COMMAND ) {
			if ( is_comment_block ) {
				// Don't do anything here.  New comments will be inserted in code below.
			}
			else {
				// New command so create a command as a place-holder for editing (filled out during the editing).
				// Get everything before the ) in the command and then re-add the ").
				// TODO SAM 2007-08-31 Why is this done?
				// Need to handle:
				//	1) Traditional commands foo(), may have leading "1: " or "[Legacy] 1:" that needs to be stripped.
				//	2) Comments # blocks
				//  3) Don't allow edit of /* */ comments - just insert/delete
				// TODO smalers 2020-12-05 actions traditionally have () at end but may have some that don't have.
				String command_string = ui_StripMenuSequencePrefix(StringUtil.getToken(action,")",0,0)+ ")");
				if ( Message.isDebugOn ) {
					Message.printDebug ( dl, routine,
						"Using command factory to create new command for \"" + command_string + "\"" );
				}

				command_to_edit = commandList_NewCommand( command_string, true );
				Message.printStatus(2, routine, "Created new command to insert:  \"" + command_to_edit + "\"" );

				// Add it to the processor at the insert point of the edit (before the first selected command.

				commandList_InsertCommandBasedOnUI ( command_to_edit );
				Message.printStatus(2, routine, "Inserted command for editing.");
			}
		}

		// Second, edit the command, whether an update or an insert.

		boolean edit_completed = false;
		List<String> new_comments = new ArrayList<>();	// Used if comments are edited.
		if ( is_comment_block ) {
			// Edit using the old-style editor.
			edit_completed = commandList_EditCommandOldStyleComments ( mode, action, command_List, new_comments );
		}
		else {
		    // Editing a single one-line command.
	        try {
	   			// Edit with the new style editors.
	   			Message.printStatus(2, routine, "Editing Command with new-style editor.");
	   			edit_completed = commandList_EditCommandNewStyle ( command_to_edit );
	        }
	        catch ( Exception e ) {
	            Message.printWarning (1 , routine, "Unexpected error editing command - refer to log and report to software support." );
	            Message.printWarning( 3, routine, e );
	            edit_completed = false;
	        }
		}

		// Third, make sure that the edits are to be saved.
		// If not, restore the original copy (if an update) or discard the command (if a new insert).
	    // If the command implements CommandDiscoverable, try to make the discovery run.

		if ( edit_completed ) {
			if ( mode == __INSERT_COMMAND ) {
				if ( is_comment_block ) {
					// Insert the comments at the insert point.
					commandList_InsertCommentsBasedOnUI ( new_comments );
				}
				else {
					// The command has already been inserted in the list.
					Message.printStatus(2, routine, "After insert, command is:  \"" + command_to_edit + "\"" );
	                if ( command_to_edit instanceof CommandDiscoverable ) {
	                    commandList_EditCommand_RunDiscovery ( command_to_edit );
	                }
	                // Connect the command to the UI to handle progress when the command is run.
	            	// TODO SAM 2009-03-23 Evaluate whether to define and interface rather than rely on AbstractCommand here.
	            	if ( command_to_edit instanceof AbstractCommand ) {
	            		((AbstractCommand)command_to_edit).addCommandProgressListener ( this );
	            	}
				}
				commandList_SetDirty(true);
			}
			else if ( mode == __UPDATE_COMMAND ) {
				// The command was updated.
				if ( is_comment_block ) {
					// Remove the commands that were selected and insert the new ones.
					commandList_ReplaceComments ( command_List, new_comments );
					if ( !commandList_CommandsAreEqual(command_List,new_comments)) {
						commandList_SetDirty(true);
					}
				}
				else {
					// The contents of the command will have been modified so there is no need to do anything more.
					Message.printStatus(2, routine, "After edit, command is:  \"" + command_to_edit + "\"" );
					if ( !command_to_edit_original.toString().equals(command_to_edit.toString())) {
						commandList_SetDirty(true);
					}
	                if ( command_to_edit instanceof CommandDiscoverable ) {
	                    commandList_EditCommand_RunDiscovery ( command_to_edit );
	                }
				}
			}
		}
		else {
	        // The edit was canceled.  If it was a new command being inserted, remove the command from the processor.
			if ( mode == __INSERT_COMMAND ) {
				if ( is_comment_block ) {
					// No comments were inserted at start of edit.  No need to do anything.
				}
				else {
					// A temporary new command was inserted so remove it.
					commandList_RemoveCommand(command_to_edit);
					Message.printStatus(2, routine, "Edit was cancelled.  Removing from command list." );
				}
			}
			else if ( mode == __UPDATE_COMMAND ) {
				if ( is_comment_block ) {
					// The original comments will remain.  No need to do anything.
				}
				else {
					// Else was an update so restore the original command.
				    Message.printStatus(2, routine, "Edit was cancelled.  Restoring pre-edit command." );
					int pos = commandList_IndexOf(command_to_edit);
					commandList_RemoveCommand(command_to_edit);
					commandList_InsertCommandAt(command_to_edit_original, pos);
				}
			}
		}

		// TODO SAM 2007-12-07 Evaluate whether to refresh the command list status?

	    ui_ShowCurrentCommandListStatus();
	}
	catch ( Exception e2 ) {
		// TODO SAM 2005-05-18 Evaluate handling of unexpected error.
		Message.printWarning(1, routine, "Unexpected error editing command (" + e2 + ")." );
		Message.printWarning ( 3, routine, e2 );
	}
}

/**
Run discovery on the command.
This will, for example, make available a list of time series to be requested with the ObjectListProvider.getObjectList() method.
*/
private void commandList_EditCommand_RunDiscovery ( Command command_to_edit ) {
    String routine = getClass().getSimpleName() + ".commandList_EditCommand_RunDiscovery";
    // Run the discovery.
    Message.printStatus(2, routine, "Running discovery mode on command:  \"" + command_to_edit + "\"" );
    try {
        ((CommandDiscoverable)command_to_edit).runCommandDiscovery(__statedmiProcessor.indexOf(command_to_edit));
        // Redraw the status area.
        ui_ShowCurrentCommandListStatus();
    }
    catch ( Exception e ) {
        // For now ignore because edit-time input may not be complete.
        String message = "Unable to make discover run - may be OK if partial data.";
        Message.printStatus(2, routine, message);
    }
}

/**
Edit a new-style command, which has a custom editor.
@param Command command_to_edit The command to edit.
*/
private boolean commandList_EditCommandNewStyle ( Command command_to_edit ) {
	return command_to_edit.editCommand(this);
}

/**
Edit comments using an old-style editor.
@param mode Mode of editing, whether updating or inserting.
@param action If not null, then the comments are new (insert).
@param command_List Comments being edited as a list of GenericCommand, as passed from the legacy code.
@param new_comments The new comments as a list of String, to be inserted into the command list.
@return true if the command edits were committed, false if canceled.
*/
private boolean commandList_EditCommandOldStyleComments (
		int mode, String action, List<Command> command_List, List new_comments ) {
	//else if ( action.equals(__Commands_General_Comment_String) ||
	//	command.startsWith("#") ) {
	List<String> cv = new ArrayList<>();
	int size = 0;
	if ( command_List != null ) {
		size = command_List.size();
	}
	Command command = null;
	for ( int i = 0; i < size; i++ ) {
		command = command_List.get(i);
		cv.add( command.toString() );
	}
	List edited_cv = new Comment_JDialog ( this, cv ).getText();
	if ( edited_cv == null ) {
		return false;
	}
	else {
		// Transfer to the list that was passed in.
		int size2 = edited_cv.size();
		for ( int i = 0; i < size2; i++ ) {
			new_comments.add ( edited_cv.get(i) );
		}
		return true;
	}
}

/**
Get the list of commands to process, as a list of Command, guaranteed to be non-null but may be zero length.
@return the commands as a list of Command.
@param get_all If false, return those that are selected
unless none are selected, in which case all are returned.
If true, all are returned, regardless of which are selected.
*/
private List<Command> commandList_GetCommands ( boolean get_all ) {
	if ( __commands_JListModel.size() == 0 ) {
		return new ArrayList<Command>();
	}

	int [] selected = ui_GetCommandJList().getSelectedIndices();
	int selected_size = 0;
	if ( selected != null ) {
		selected_size = selected.length;
	}

	if ( (selected_size == 0) || get_all ) {
		// Nothing selected or want to get all, get all.
		selected_size = __commands_JListModel.size();
		List<Command> itemList = new ArrayList<>(selected_size);
		for ( int i = 0; i < selected_size; i++ ) {
			itemList.add ( (Command)__commands_JListModel.get(i) );
		}
		return itemList;
	}
	else {
		// Else something selected so get them.
		List<Command> itemList = new ArrayList<>(selected_size);
		for ( int i = 0; i < selected_size; i++ ) {
			itemList.add ( (Command)__commands_JListModel.get(selected[i]) );
		}
		return itemList;
	}
}

/**
Get the list of commands to process.
If any are selected, only they will be returned.  If none are selected, all will be returned.
@return the commands as a list of Command.
*/
private List<Command> commandList_GetCommandsBasedOnUI ( ) {
	return commandList_GetCommands ( false );
}

/**
Get the list of commands to process, as a list of String.
@return the commands as a list of String.
@param getAll If false, return those that are selected unless none are selected, in which case all are returned.
If true, all are returned, regardless of which are selected.
*/
private List<String> commandList_GetCommandStrings ( boolean getAll ) {
	// Get the Command list, will not be non-null.
    List<Command> commands = commandList_GetCommands ( getAll );
	// Convert to String instances.
	int size = commands.size();
	List<String> strings = new ArrayList<>(size);
	for ( int i = 0; i < size; i++ ) {
		strings.add ( "" + commands.get(i) );
	}
	return strings;
}

/**
Return the number of commands with failure as max severity.
*/
private int commandList_GetFailureCount() {
	int size = __commands_JListModel.size();
	CommandStatusProvider command;
	int failure_count = 0;
	for ( int i = 0; i < size; i++ ) {
		command = (CommandStatusProvider)__commands_JListModel.get(i);
		if ( CommandStatusUtil.getHighestSeverity(command).equals(CommandStatusType.FAILURE) ) {
			++failure_count;
		}
	}
	return failure_count;
}

/**
Return the number of commands with warnings as maximum severity.
*/
private int commandList_GetWarningCount() {
	int size = __commands_JListModel.size();
	CommandStatusProvider command;
	int failure_count = 0;
	for ( int i = 0; i < size; i++ ) {
		command = (CommandStatusProvider)__commands_JListModel.get(i);
		if ( CommandStatusUtil.getHighestSeverity(command).equals(CommandStatusType.WARNING) ) {
			++failure_count;
		}
	}
	return failure_count;
}

/**
Return the index position of the command from the command list.
Currently this assumes that there is a one to one correspondence between items in the list and commands in the processor.
@param command The Command instance to determine the position in the command list.
*/
private int commandList_IndexOf ( Command command ) {
	return __statedmiProcessor.indexOf(command);
}

/**
Insert a command at the indicated position.
@param command The Command to insert.
@param pos The index in the command list at which to insert.
*/
private void commandList_InsertCommandAt ( Command command, int pos ) {
	__statedmiProcessor.insertCommandAt( command, pos );
	__commands_JList.ensureIndexIsVisible ( pos );
	// Since an insert, mark the commands list as dirty.
	//commandList_SetDirty(true);
	ui_UpdateStatus ( false );
}

/**
Insert a new command into the command list, utilizing the selected commands in the displayed list to determine the insert position.
If any commands are selected in the GUI, the insert will occur before the selection.
If none are selected, the insert will occur at the end of the list.
For example this can occur in the following cases:
<ol>
<li>	The user is interacting with the command list via command menus.</li>
<li>	Time series identifiers are being transferred to the commands area from the query results list.</li>
</ol>
The GUI should call this method WHENEVER a command is being inserted and is coded to respond to changes in the data model.
@param inserted_command The command to insert.
*/
private void commandList_InsertCommandBasedOnUI ( Command inserted_command ) {
	String routine = getClass().getSimpleName() + ".insertCommand";

	// Get the selected indices from the commands.
	int selectedIndices[] = ui_GetCommandJList().getSelectedIndices();
	int selectedSize = selectedIndices.length;

	int insert_pos = 0;
	if (selectedSize > 0) {
		// Insert before the first selected item.
		insert_pos = selectedIndices[0];
		__commands_JListModel.insertElementAt (	inserted_command, insert_pos );
		Message.printStatus(2, routine, "Inserting command \"" +
				inserted_command + "\" at [" + insert_pos + "]" );
	}
	else {
		// Insert at end of commands list.
		__commands_JListModel.addElement ( inserted_command );
		insert_pos = __commands_JListModel.size() - 1;
	}
	// Make sure that the list scrolls to the position that has been updated.
	if ( insert_pos >= 0 ) {
		__commands_JList.ensureIndexIsVisible ( insert_pos );
	}
	// Since an insert, mark the commands list as dirty.
	//commandList_SetDirty(true);
}

/**
Insert comments into the command list,
utilizing the selected commands in the displayed list to determine the insert position.
@param new_comments The comments to insert, as a list of String.
*/
private void commandList_InsertCommentsBasedOnUI ( List<String> new_comments ) {
	String routine = getClass().getSimpleName() + ".commandList_InsertCommentsBasedOnUI";

	// Get the selected indices from the commands.
	int selectedIndices[] = ui_GetCommandJList().getSelectedIndices();
	int selectedSize = selectedIndices.length;

	int size = new_comments.size();

	int insert_pos = 0;
	Command inserted_command = null;	// New comment line as Command.
	for ( int i = 0; i < size; i++ ) {
		inserted_command = commandList_NewCommand (	new_comments.get(i), true );
		if (selectedSize > 0) {
			// Insert before the first selected item...
			int insert_pos0 = selectedIndices[0];
			insert_pos = insert_pos0 + i;
			__commands_JListModel.insertElementAt (	inserted_command, insert_pos );
			Message.printStatus(2, routine, "Inserting comment \"" +
				inserted_command + "\" at [" + insert_pos + "]" );
		}
		else {
			// Insert at end of commands list.
			__commands_JListModel.addElement ( inserted_command );
			insert_pos = __commands_JListModel.size() - 1;
		}
	}
	// Make sure that the list scrolls to the position that has been updated.
	if ( insert_pos >= 0 ) {
		__commands_JList.ensureIndexIsVisible ( insert_pos );
	}
	// Since an insert, mark the commands list as dirty.
	//commandList_SetDirty(true);
}

/**
Determine whether a list of commands is a comment block consisting of multiple # comments.
@param processor The TSCommandProcessor that is processing the results, used to check for positions of commands.
@param commands list of Command instances to check.
@param allMustBeComments If true then all must be comment lines
for true to be returned.  If false, then only one must be a comment.
This allows a warning to be printed that only a block of ALL comments can be edited at once.
@param must_be_contigous If true, then the comments must be contiguous for true to be returned.
The GUI code should check this and disallow comment edits if not contiguous.
*/
private boolean commandList_IsCommentBlock ( StateDMI_Processor processor,
		List commands, boolean allMustBeComments, boolean mustBeContiguous ) {
	int size_commands = commands.size();
	boolean is_comment_block = true;
	boolean is_contiguous = true;
	// Loop through the commands to check.
	Command command = null;
	int comment_count = 0;
	int pos_prev = -1;
	for ( int i = 0; i < size_commands; i++ ) {
		command = (Command)commands.get(i);
		if ( command instanceof Comment_Command ) {
			++comment_count;
		}
		// Get the index position in the commands processor and check for contiguousness.
		int pos = processor.indexOf(command);
		if ( (i > 0) && (pos != (pos_prev + 1)) ) {
			is_contiguous = false;
		}
		// Save the position for the next check for contiguity.
		pos_prev = pos;
	}
	if ( mustBeContiguous && !is_contiguous ) {
		is_comment_block = false;
	}
	if ( allMustBeComments && (comment_count != size_commands) ) {
		is_comment_block = false;
	}
	return is_comment_block;
}

/**
Create a new Command instance given a command string.
This may be called when loading commands from a file or adding new commands while editing.
@param commandString Command as a string, to parse and create a Command instance.
@param createUnknownCommandIfNotRecognized Indicate if a generic command should be created if not recognized.
For now this should generally be true, until all commands are recognized by the TSCommandFactory.
*/
private Command commandList_NewCommand ( String commandString, boolean createUnknownCommandIfNotRecognized ) {
	int dl = 1;
	String routine = getClass().getSimpleName() + ".newCommand";
	if ( Message.isDebugOn ) {
		Message.printDebug ( dl, routine,
		"Using command factory to create a new command for \"" + commandString + "\"" );
	}
	Command c = null;
	try {
		StateDMICommandFactory cf = new StateDMICommandFactory();
		c = cf.newCommand(commandString);
		Message.printStatus ( 2, routine, "Created command from factory for \"" + commandString + "\"");
	}
	catch ( UnknownCommandException e ) {
		// Processor does not know the command so create a GenericCommand.
		c = new UnknownCommand();
		Message.printStatus ( 2, routine, "Created unknown command for \"" + commandString + "\"");
	}
	// TODO SAM 2007-08-31 This is essentially validation.
	// Need to evaluate for old-style commands, impacts on error-handling.
	// New is command from the processor.
	try {
		c.initializeCommand ( commandString, __statedmiProcessor, true ); // Full initialization.
		if ( Message.isDebugOn ) {
			Message.printDebug ( dl, routine, "Initialized command for \"" + commandString + "\"" );
		}
	}
	catch ( Exception e ) {
		// Absorb the warning and make the user try to deal with it in the editor dialog.  They can always cancel out.

		// TODO SAM 2005-05-09 Need to handle parse error.  Should the editor come up with limited information?
		Message.printWarning ( 3, routine,
		"Unexpected error initializing command \"" + commandString + "\"." );
		Message.printWarning ( 3, routine, e );
	}
	return c;
}

/**
Remove all commands in the list.  The delete is done independent of what is selected in the UI.
If UI selects are relevant, use cmmandList_ClearBasedOnUI.
*/
private void commandList_RemoveAllCommands () {
	// Do this so that the status only needs to be updated once.
	Message.printStatus(2,"commandList_RemoveAllCommands", "Calling list model removeAllElements.");
	__commands_JListModel.removeAllElements();
	commandList_SetDirty ( true );
	ui_UpdateStatus ( false );
}

/**
Remove the indicated command from the command list.
@param command The Command instance to remove from the command list.
*/
private void commandList_RemoveCommand ( Command command ) {
	int pos = commandList_IndexOf ( command );
	__commands_JListModel.removeElementAt(pos);
	//commandList_SetDirty(true);
	ui_UpdateStatus ( false );
}

/*
Remove selected command list, using the data model.
If any items are selected, then only those are selected.
If none are selected, then all are cleared, asking the user to confirm.
Items from the command list (or all if none are selected).
Save what was cleared in the __command_cut_buffer list so that it can be used with Paste.
*/
private void commandList_RemoveCommandsBasedOnUI () {
	int size = 0;
	int [] selected_indices = ui_GetCommandJList().getSelectedIndices();
	if ( selected_indices != null ) {
		size = selected_indices.length;
	}
	// Uncomment for troubleshooting.
	//String routine = getClass().getName() + ".commandList_RemoveCommandsBasedOnUI";
	//Message.printStatus ( 2, routine, "There are " + size +
	//		" commands selected for remove.  If zero all will be removed." );
	if ( (size == __commands_JListModel.size()) || (size == 0) ) {
		int x = new ResponseJDialog ( this, "Delete Commands?",
			"Are you sure you want to delete ALL the commands?",
			ResponseJDialog.YES|ResponseJDialog.NO).response();
		if ( x == ResponseJDialog.NO ) {
			return;
		}
	}
	if ( size == 0 ) {
		// Nothing selected so remove all.
		__commands_JListModel.removeAllElements();
	}
	else {
	    // Need to remove from back of selected_indices so that removing
		// elements will not affect the index of items before that index.
		// At some point need to add an undo feature.
		JGUIUtil.setWaitCursor ( this, true );
		ui_SetIgnoreItemEvent ( true );
		ui_SetIgnoreListSelectionEvent ( true );
		for ( int i = (size - 1); i >= 0; i-- ) {
			__commands_JListModel.removeElementAt (	selected_indices[i] );
		}
		ui_SetIgnoreItemEvent ( false );
		ui_SetIgnoreListSelectionEvent ( false );
		selected_indices = null;
		JGUIUtil.setWaitCursor ( this, false );
	}
	commandList_SetDirty ( true );
	results_Clear();
	ui_UpdateStatus ( true );
}

/**
Replace a command with another.  This is used, for example, when converting commands to/from comments.
@param old_command Old command to remove.
@param new_command New command to insert in its place.
*/
private void commandList_ReplaceCommand ( Command old_command, Command new_command ) {
	// Probably could get the index passed in from list operations but
	// do the lookup through the data model to be more independent.
	int pos_old = __statedmiProcessor.indexOf(old_command);
	if ( pos_old < 0 ) {
		// Can't find the old command so return.
		return;
	}
	// Remove the old command.
	__statedmiProcessor.removeCommandAt ( pos_old );
	// Insert the new command at the same position.  Handle the case that it is now at the end of the list.
	if ( pos_old < __statedmiProcessor.size() ) {
		// Have enough elements to add at the requested position.
		__statedmiProcessor.insertCommandAt( new_command, pos_old );
	}
	else {
		// Add at the end.
		__statedmiProcessor.addCommand ( new_command );
	}
	// Refresh the GUI.
	//commandList_SetDirty ( true );
	ui_UpdateStatus ( false );
}

/**
Replace a contiguous block of # comments with another block.
@param old_comments list of old comments (as Command) to remove.
@param new_comments list of new comments (as String) to insert in its place.
*/
private void commandList_ReplaceComments ( List old_comments, List new_comments ) {
	//String routine = getClass().getName() + ".commandList_ReplaceComments";
	// Probably could get the index passed in from list operations but
	// do the lookup through the data model to be more independent.
	int pos_old = __statedmiProcessor.indexOf((Command)old_comments.get(0));
	if ( pos_old < 0 ) {
		// Can't find the old command so return.
		return;
	}
	// Remove the old commands.  They will shift so OK to keep removing at the single index.
	int size = old_comments.size();
	for ( int i = 0; i < size; i++ ) {
		__statedmiProcessor.removeCommandAt ( pos_old );
	}
	// Insert the new commands at the same position.  Handle the case that it is now at the end of the list.
	int size_new = new_comments.size();
	if ( pos_old < __statedmiProcessor.size() ) {
		// Have enough elements to add at the requested position.
		for ( int i = 0; i < size_new; i++ ) {
			Command new_command = commandList_NewCommand ( (String)new_comments.get(i), true );
			//Message.printStatus ( 2, routine, "Inserting " + new_command + " at " + (pos_old + 1));
			__statedmiProcessor.insertCommandAt( new_command, (pos_old + i) );
		}
	}
	else {
		// Add at the end.
		for ( int i = 0; i < size_new; i++ ) {
			Command new_command = commandList_NewCommand ( (String)new_comments.get(i), true );
			//Message.printStatus ( 2, routine, "Adding " + new_command + " at end" );
			__statedmiProcessor.addCommand ( new_command );
		}
	}
	// Refresh the GUI.
	//commandList_SetDirty ( true );
	ui_UpdateStatus ( false );
}

/**
Select the command and optionally position the view at the command.
@param iline Command position (0+).
@param ensure_visible If true, the list will be scrolled to the selected item.
This may be undesirable if selecting many items.
*/
private void commandList_SelectCommand ( int iline, boolean ensure_visible ) {
	__commands_JList.setSelectedIndex ( iline );
	if ( ensure_visible ) {
		// Position the list to make the selected item visible.
		__commands_JList.ensureIndexIsVisible(iline);
	}
	ui_UpdateStatus ( false);
}

/**
Set the command file name.  This also will refresh any interface components
that display the command file name.  It DOES NOT cause the commands to be reloaded - it is a simple setter.
@param commandFileName Name of current command file (can be null).
*/
private void commandList_SetCommandFileName ( String commandFileName ) {
	// Set the file name used in the TSTool UI.
	__commandFileName = commandFileName;
	// Also set the initial working directory for the processor as the parent folder of the command file.
	if ( commandFileName != null ) {
		File file = new File ( commandFileName );
		commandProcessor_SetInitialWorkingDir ( file.getParent() );
	}
	// Update the title bar.
	ui_UpdateStatus ( false );
}

/**
Indicate whether the commands have been modified.  The application title is also updated to indicate this.
@param dirty Specify as true if the commands have been modified in some way.
*/
private void commandList_SetDirty ( boolean dirty ) {
	__commandsDirty = dirty;
	ui_UpdateStatus ( false );
	// TODO SAM 2007-08-31 Evaluate whether processor should have "dirty" property.
}

// All of the following methods perform and interaction with the command processor,
// beyond basic command list insert/delete/update.

/**
Return the command processor instance that is being used.
This method should be called to avoid direct interaction with the processor data member.
@return the TSCommandProcessor instance that is being used.
*/
private StateDMI_Processor commandProcessor_GetCommandProcessor () {
    return __statedmiProcessor;
}

/**
Get the command processor table results for a table identifier.
Typically this corresponds to a user selecting the time series from the results list, for further display.
@param tableId identifier for table to display
@return The matching table or null if not available from the processor.
*/
private DataTable commandProcessor_GetTable ( String tableId ) {
    String message, routine = getClass().getSimpleName() + ".commandProcessor_GetTable";
    if ( __statedmiProcessor == null ) {
        return null;
    }
    PropList request_params = new PropList ( "" );
    request_params.set ( "TableID", tableId );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = __statedmiProcessor.processRequest( "GetTable", request_params);
    }
    catch ( Exception e ) {
        message = "Error requesting GetTable(TableID=\"" + tableId + "\") from processor.";
        Message.printWarning(2, routine, message );
        Message.printWarning ( 3, routine, e );
    }
    PropList bean_PropList = bean.getResultsPropList();
    Object o_table = bean_PropList.getContents ( "Table" );
    DataTable table = null;
    if ( o_table == null ) {
        message = "Null table returned from processor for GetTable(TableID=\"" + tableId + "\").";
        Message.printWarning ( 2, routine, message );
    }
    else {
        table = (DataTable)o_table;
    }
    return table;
}

/**
Get the command processor table results list.
@return The table results list or null if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<DataTable> commandProcessor_GetTableResultsList() {
    String routine = getClass().getSimpleName() + ".commandProcessorGetTableResultsList";
    Object o = null;
    try {
        o = __statedmiProcessor.getPropContents ( "TableResultsList" );
    }
    catch ( Exception e ) {
        String message = "Error requesting TableResultsList from processor.";
        Message.printWarning(2, routine, message );
    }
    if ( o == null ) {
        return null;
    }
    else {
        return (List<DataTable>)o;
    }
}

/**
Get the working directory for a command (e.g., for editing).
*/
private String commandProcessor_GetWorkingDirForCommand ( Command command ) {
	return TSCommandProcessorUtil.getWorkingDirForCommand( __statedmiProcessor, command );
}

/**
Read and load a command file into the processor.
@param path Absolute path to the command file to read.
@return the number of lines that are automatically changed during the read (1 if the size is different after read).
@exception IOException if there is an error reading the command file.
*/
private int commandProcessor_ReadCommandFile ( String path )
throws IOException {
	String routine = getClass().getSimpleName() + ".commandProcessor_ReadCommandFile";
    // Set the command file for use with output.
	__statedmiProcessor.readCommandFile ( path,
		true,	// Create UnknownCommand instances for unrecognized commands.
		false );// Do not append to the current processor contents.
    // Refresh the GUI list to show the status done in call to this method.

	// TODO SAM 2008-05-11 Evaluate whether to move this to the readCommandFile() method.
	// If any lines in the file are different from the commands, mark the file as dirty.
	// Changes may automatically occur during the load because of automated updates to commands.
	BufferedReader in = new BufferedReader ( new InputStreamReader(IOUtil.getInputStream ( path )) );
	List<String> strings = new ArrayList<String>();
	String line;
	while ( true ) {
	    line = in.readLine();
	    if ( line == null ) {
	        break;
	    }
	    strings.add ( line );
	}
	in.close();
	int size_orig = strings.size();
	if ( size_orig != __statedmiProcessor.size() ) {
	    Message.printStatus( 2, routine, "Command list was modified during load (different length)." );
	    commandList_SetDirty ( true );
	    return 1;
	}
	// Go through all the commands.
	Command command = null;
	CommandStatusProvider csp = null;
	int numAutoChanges = 0;
	for ( int i = 0; i < size_orig; i++ ) {
	    line = strings.get(i);
	    command = __statedmiProcessor.get(i);
	    if ( !line.equals(command.toString()) ) {
	        Message.printStatus( 2, routine, "Command " + (i + 1) +
	            " was automatically updated during load (usually due to software update)." );
	        commandList_SetDirty ( true );
	        ++numAutoChanges;
	        if ( command instanceof CommandStatusProvider ) {
	            csp = (CommandStatusProvider)command;
	            // FIXME SAM 2008-05-11 This message gets clobbered by re-initialization before running.
	            // Add a message that the command was updated during load.
	            csp.getCommandStatus().addToLog ( CommandPhaseType.INITIALIZATION,
	                new CommandLogRecord(CommandStatusType.UNKNOWN,
	                    "Command was automatically updated during load (usually due to software update).",
	                    "Should not need to do anything." ) );
	        }
	    }
	}
	return numAutoChanges;
}

/**
Run the commands through the processor.
Currently this supplies the list of Command instances to run because the user can select the commands in the interface.
In the future the command processor may put together the list without being passed from the GUI.
@param commands List of commands to run.
@param createOutput whether to create output (slower) or skip those commands.
*/
private void commandProcessor_RunCommandsThreaded ( List commands, boolean createOutput ) {
	String routine = getClass().getSimpleName() + ".commandProcessor_RunCommandsThreaded";

	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "CommandList", commands );
	request_params.setUsingObject ( "InitialWorkingDir", ui_GetInitialWorkingDir() );
	request_params.setUsingObject ( "CreateOutput", new Boolean(createOutput) );
	try {
		StateDMI_Processor_ThreadRunner runner =
		new StateDMI_Processor_ThreadRunner ( __statedmiProcessor, request_params );
		Message.printStatus ( 2, routine, "Running commands in separate thread.");
		Thread thread = new Thread ( runner );
		thread.start();
		// Do one update of the GUI to reflect the GUI running.
		// This will disable run buttons, etc. until the current run is done.
		ui_CheckGUIState ();
		// At this point the GUI will get updated if any notification fires from the processor.
	}
	catch ( Exception e ) {
		String message = "Error running command processor in thread.";
		Message.printWarning(2, routine, message );
		Message.printWarning (3,routine, e);
	}
}

/**
Run the commands through the processor.
Currently this supplies the list of Command instances to run because the user can select the commands in the interface.
In the future the command processor may put together the list without being passed from the GUI.
*/
private void commandProcessor_RunCommands_OLD ( List commands, boolean create_output ) {
	String routine = getClass().getSimpleName() + ".commandProcessorRunCommandsThreaded";

	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "CommandList", commands );
	request_params.setUsingObject ( "InitialWorkingDir", getInitialWorkingDir() );
	request_params.setUsingObject ( "CreateOutput", new Boolean(create_output) );
	try {
		StateDMI_Processor_ThreadRunner runner =
		new StateDMI_Processor_ThreadRunner ( __statedmiProcessor, request_params );
		Message.printStatus ( 2, routine, "Running commands in separate thread.");
		Thread thread = new Thread ( runner );
		thread.start();
		// At this point the GUI will get updated if any notification fires from the processor.
	}
	catch ( Exception e ) {
		String message = "Error running command processor in thread.";
		Message.printWarning(2, routine, message );
		Message.printWarning (3,routine, e);
	}
}

/**
Set the command processor HydroBase instance that is opened via the GUI.
@param hbdmi Open HydroBaseDMI instance.
The input name is blank since it is the default HydroBaseDMI.
*/
private void commandProcessor_SetHydroBaseDMI( HydroBaseDMI hbdmi ) {
	// Call the overloaded method that takes a processor as a parameter.
	commandProcessor_SetHydroBaseDMI( __statedmiProcessor, hbdmi );
}

/**
Set the command processor HydroBase instance that is opened via the GUI.
This version is generally called by the overloaded version and when processing an external command file.
@param processor The command processor to set the HydroBase DMI instance.
@param hbdmi Open HydroBaseDMI instance.
The input name is blank since it is the default HydroBaseDMI.
*/
private void commandProcessor_SetHydroBaseDMI( CommandProcessor processor, HydroBaseDMI hbdmi ) {
	String message, routine = getClass().getSimpleName() + ".setCommandProcessorHydroBaseDMI";
	if ( hbdmi == null ) {
		return;
	}
	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "HydroBaseDMI", hbdmi );
	try {
		processor.processRequest( "SetHydroBaseDMI", request_params );
	}
	catch ( Exception e ) {
		message = "Error requesting SetHydroBaseDMI(HydroBaseDMI=\"" + hbdmi + " from processor.";
		Message.printWarning(2, routine, message );
	}
}

// FIXME SAM 2007-10-19 Check to see that code is enabled in processor.
/**
Set the command processor initial working directory.
@param dir Initial working directory.
*/
private void commandProcessor_SetInitialWorkingDir ( String InitialWorkingDir ) {
	try {
		__statedmiProcessor.setPropContents( "InitialWorkingDir", InitialWorkingDir );
	}
	catch ( Exception e ) {
		String routine = getClass().getName() + ".commandProcessor_setInitialWorkingDir";
		String message = "Error setting InitialWorkingDir(\"" + InitialWorkingDir + "\") in processor.";
		Message.printWarning(2, routine, message );
	}
}

/**
Indicate the progress that is occurring within a command.
This may be a chained call from a CommandProcessor that implements CommandListener to listen to a command.
This level of monitoring is useful if more than one progress indicator is present in an application UI.
@param istep The number of steps being executed in a command (0+).
@param nstep The total number of steps to process within a command.
@param command The reference to the command that is starting to run,
provided to allow future interaction with the command.
@param percent_complete If >= 0, the value can be used to indicate progress running a single command (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its own determination (e.g., ((istep + 1)/nstep)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandProgress ( int istep, int nstep, Command command, float percent_complete, String message ) {
	if ( istep == 0 ) {
		// Initialize the limits of the command progress bar.
		__command_JProgressBar.setMinimum ( 0 );
		__command_JProgressBar.setMaximum ( nstep );
	}
	// Set the current value.
	__command_JProgressBar.setValue ( istep + 1 );
}

/**
Indicate that a command has started running.
@param icommand The command index (0+).
@param ncommand The total number of commands to process
@param command The reference to the command that is starting to run,
provided to allow future interaction with the command.
@param percent_complete If >= 0, the value can be used to indicate progress running a list of commands (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its own determination (e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandStarted ( int icommand, int ncommand, Command command, float percent_complete, String message ) {
	// commandCompleted updates the progress bar after each command.
	// For this method, only reset the bounds of the progress bar and clear if the first command.
	String routine = "StateDMI_JFrme.commandStarted";
	String command_string = command.toString();
	//int max_length = ?;
	//if ( command_string)
	ui_UpdateStatusTextFields ( 1, routine, null, "Processing " + (icommand + 1) + " \"" + command_string + "\"", __STATUS_BUSY );
	if ( icommand == 0 ) {
		__processor_JProgressBar.setMinimum ( 0 );
		__processor_JProgressBar.setMaximum ( ncommand );
		__processor_JProgressBar.setValue ( 0 );
		//Message.printStatus(2, getClass().getName()+".commandStarted", "Setting processor progress bar limits to 0 to " + ncommand );
	}
	// Always set the value for the command progress so that it shows up // as zero.
	// The commandProgres() method will do a better job of setting the limits and current status for a specific command.
	__command_JProgressBar.setMinimum ( 0 );
	__command_JProgressBar.setMaximum ( 100 );
	__command_JProgressBar.setValue ( 0 );
}

/**
Required by ListDataListener.
Receive notification when the contents of the commands list have changed.
*/
public void contentsChanged ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
Update the list in the data set area to be consistent with the current data set component.
*/
private void dataSet_UpdateList() {
	String routine = getClass().getSimpleName() + ".dataSet_UpdateList";
	// Create a new table model and renderer for the selected data object.
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		try {
			__list_TableModel = new StateCU_DataSetComponent_TableModel(
			__statecuDataset, __statecuSelectedComponent );
		StateCU_DataSetComponent_CellRenderer cr =
			new StateCU_DataSetComponent_CellRenderer (
			(StateCU_DataSetComponent_TableModel)__list_TableModel);
		__list_JWorksheet.setCellRenderer ( cr );
		__list_JWorksheet.setModel ( __list_TableModel );
		__list_JWorksheet.setColumnWidths ( cr.getColumnWidths() );
		// Get the component group because the list is always related to the group.
		DataSetComponent component_group =
			((StateCU_DataSetComponent_TableModel)__list_TableModel).getComponentGroup();
		// TODO - might need better labels.
		String list_source = component_group.getListSource();
		__list_JPanel.setBorder(
			BorderFactory.createTitledBorder (
			BorderFactory.createLineBorder(Color.black),
			"List of " + component_group.getComponentName() +
			" (from " + list_source + ")" ) );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine,
			"Error displaying list for data set component:  " +
			__statecuSelectedComponent.getComponentName() );
			Message.printWarning ( 2, routine, e );
		}
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		try {
		__list_TableModel = new StateMod_DataSetComponent_TableModel(
			__statemodDataset, __statemodSelectedComponent );
		StateMod_DataSetComponent_CellRenderer cr =
			new StateMod_DataSetComponent_CellRenderer (
			(StateMod_DataSetComponent_TableModel)__list_TableModel);
		__list_JWorksheet.setCellRenderer ( cr );
		__list_JWorksheet.setModel ( __list_TableModel );
		__list_JWorksheet.setColumnWidths ( cr.getColumnWidths() );
		// Get the component group because the list is always related to the group.
		DataSetComponent component_group =
			((StateMod_DataSetComponent_TableModel)	__list_TableModel).getComponentGroup();
		// TODO - might need better labels.
		String list_source = component_group.getListSource();
		__list_JPanel.setBorder(
			BorderFactory.createTitledBorder (
			BorderFactory.createLineBorder(Color.black),
			"List of " + component_group.getComponentName() +
			" (from " + list_source + ")" ) );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error displaying list for data set component:  " +
			__statemodSelectedComponent.getComponentName() );
			Message.printWarning ( 2, routine, e );
		}
	}
}

/**
 * Format a URL to display help for a topic.
 * The document root is taken from TSTool configuration properties and otherwise the URL pattern follows the standard created for the documentation.
 * @param group a group (category) to organize items.
 * For example, the group might be "command".
 * @param item the specific item for the URL.
 * For example, the item might be a command name.
 */
public String formatHelpViewerUrl ( String group, String item ) {
	return formatHelpViewerUrl ( group, item, null );
}

//TODO smalers 2018-08-28 in the future may need a lookup file to ensure portability
//of documentation across software versions but for now assume the organization.
/**
 * Format a URL to display help for a topic.
 * The document root is taken from StateDMI configuration properties and otherwise the URL pattern follows the standard created for the documentation.
 * Candidate URLs are formed using the software version and general "latest" version,
 * and the first URL that returns content is returned so it can be used in the help viewer.
 * @param group a group (category) to organize items. For example, the group might be "command".
 * @param item the specific item for the URL. For example, the item might be a command name.
 * @param rootUrl root URL to try, useful for plugins that provide documentation in an alternative location
 * than the defaults for an application, pass as null to ignore
 * (e.g., "https://software.openwaterfoundation.org/tstool-zabbix-plugin/latest/doc-user").
 * If the plugin's documentation matches TSTool's conventions (group=literal command' and item=the CommandName)
 * the latest plugin documentation should be found by appending "command-ref/CommandName/" to the root URL.
 * However, this does not find the documentation that matches the plugin version,
 * which requires a plugin-specific URL formatter that implements logic similar to this method.
 */
public String formatHelpViewerUrl ( String group, String item, String rootUrl ) {
	String routine = getClass().getSimpleName() + ".formatHelpViewerUrl";
	// The location of the documentation is relative to root URI on the web:
    // - two locations are allowed to help transition from OWF to OpenCDSS location
	// - use the first found URL
    String docRootUri = StateDMI.getPropValue ( "StateDMI.UserDocumentationUri" );
    String docRootUri2 = StateDMI.getPropValue ( "StateDMI.UserDocumentationUri2" );
    List<String> docRootUriList= new ArrayList<>(2);
   	String version = IOUtil.getProgramVersion();
   	int pos = version.indexOf(" ");
   	if ( pos > 0 ) {
   		version = version.substring(0, pos);
   	}
    if ( docRootUri != null ) {
    	// First replace "latest" with the software version so that specific version is shown.
    	String docRootUriVersion = docRootUri.replace("latest", version);
    	docRootUriList.add(docRootUriVersion);
    	if ( !docRootUriVersion.equals(docRootUri) ) {
    		// Also add the URL with "latest".
    		docRootUriList.add(docRootUri);
    	}
    }
    if ( docRootUri2 != null ) {
    	// First replace "latest" with the software version so that specific version is shown.
    	String docRootUri2Version = docRootUri2.replace("latest", version);
    	docRootUriList.add(docRootUri2Version);
    	if ( !docRootUri2Version.equals(docRootUri2) ) {
    		// Add the URL with "latest".
    		docRootUriList.add(docRootUri2);
    	}
    }
    if ( (docRootUri == null) || docRootUri.isEmpty() ) {
    	Message.printWarning(2, "",
    		"Unable to determine documentation for group \"" + group + "\" and item \"" +
    		item + "\" - no StateDMI.UserDocumenationUri configuration property defined." );
    }
    else {
    	int failCount = 0;
    	int [] responseCode = new int[docRootUriList.size()];
    	int i = -1;
    	for ( String uri : docRootUriList ) {
    		Message.printStatus(2, routine, "URI is " + uri );
    		// Initialize response code to -1 which means unchecked.
    		++i;
    		responseCode[i] = -1;
	    	// Make sure the URI has a slash at end.
    		if ( (uri != null) && !uri.isEmpty() ) {
		    	String docUri = "";
		    	if ( !uri.endsWith("/") ) {
		    		uri += "/";
		    	}
		    	// Specific documentation requests from the UI.
		    	docUri = null;
			    if ( item.equals(__Help_ViewDocumentation_ReleaseNotes_String) ) {
			        docUri = uri + "appendix-release-notes/release-notes/";
			    }
			    else if ( item.equals(__Help_ViewDocumentation_UserManual_String) ) {
			        docUri = uri; // Go to the main documentation.
			    }
			    else if ( item.equals(__Help_ViewDocumentation_CommandReference_String) ) {
			        docUri = uri + "command-ref/overview/";
			    }
			    else if ( item.equals(__Help_ViewDocumentation_DatastoreReference_String) ) {
			        docUri = uri + "datastore-ref/overview/";
			    }
			    else if ( item.equals(__Help_ViewDocumentation_Troubleshooting_String) ) {
			        docUri = uri + "troubleshooting/troubleshooting/";
			    }
			    // Generic requests by group.
			    else if ( group.equalsIgnoreCase("command") ) {
			    	docUri = uri + "command-ref/" + item + "/" + item + "/";
			    }
			    if ( docUri != null ) {
			    	// Now display using the default application for the file extension.
			    	Message.printStatus(2, routine, "Opening documentation \"" + docUri + "\"" );
			    	// The Desktop.browse() method will always open, even if the page does not exist,
			    	// and it won't return the HTTP error code in this case.
			    	// Therefore, do a check to see if the URI is available before opening in a browser.
			    	URL url = null;
			    	try {
			    		url = new URL(docUri);
			    		HttpURLConnection huc = (HttpURLConnection)url.openConnection();
			    		huc.connect();
			    		responseCode[i] = huc.getResponseCode();
			    	}
			    	catch ( MalformedURLException e ) {
			    		Message.printWarning(2, "", "Unable to display documentation at \"" + docUri + "\" - malformed URL." );
			    	}
			    	catch ( IOException e ) {
			    		Message.printWarning(2, "", "Unable to display documentation at \"" + docUri + "\" - IOException (" + e + ")." );
			    	}
			    	catch ( Exception e ) {
			    		Message.printWarning(2, "", "Unable to display documentation at \"" + docUri + "\" - Exception (" + e + ")." );
			    	}
			    	finally {
			    		// Any cleanup?
			    	}
			    	if ( responseCode[i] == 200 ) {
			    		// Looks like a valid URI to display.
			    		return docUri.toString();
			    	}
			    	else {
			    		++failCount;
			    	}
			    }
			    else {
			    	// URL could not be determined.
			    	++failCount;
			    }
    		}
    	}
        if ( failCount == docRootUriList.size() ) {
        	// Log the a message - show a visible dialog in calling code.
        	Message.printWarning(2, "",
        		"Unable to determine documentation for group \"" + group + "\" and item \"" +
        		item + "\" - all URIs that were tried return error code." );
        }
    }
	return null;
}

protected int getAppType() {
	return __appType;
}

/**
Get the commands above a command insert position.  Only the requested commands are returned.
Use this, for example, to get the setWorkingDir() commands above the insert position for a readXXX() command,
so the working directory can be defined and used in the readXXX_Dialog.
The returned list can be processed by the StateDMI_Processor() constructor.
@return List of commands above the insert point that match the commands in the needed_commands_List.
This will always return a non-null list, even if no commands are in the list.
@param needed_commands_List list of commands that need to be processed (e.g., "setWorkingDir").
Only the main command name should be defined.
@param get_all if false, only the first found item above the insert point is returned.
If true, all matching commands above the point are returned in the order from top to bottom.
*/
/* TODO smalers 2020-02-16 no longer used?
public List<String> getCommandsAboveInsertPosition ( List<String> needed_commands_List, boolean get_all ) {
	// Determine the insert position, which will be the first selected command (or the end of the list if none are selected).
	int selectedsize = 0;
	int [] selected_indices = ui_GetCommandJList().getSelectedIndices();
	if ( selected_indices != null ) {
		selectedsize = selected_indices.length;
	}
	int insert_pos = 0;
	if ( selectedsize == 0 ) {
		// The insert position is the end of the list (same as size).
		insert_pos = __commands_JListModel.size();
	}
	else {
		// The insert position is the first selected item.
		insert_pos = selected_indices[0];
	}
	// Now search backwards matching commands for each of the requested commands.
	int size = 0;
	if ( needed_commands_List != null ) {
		size = needed_commands_List.size();
	}
	String command;
	List<String> found_commands = new ArrayList<>();
	// Now loop up through the command list.
	for ( int ic = (insert_pos - 1); ic >= 0; ic-- ) {
		for ( int i = 0; i < size; i++ ) {
			command = needed_commands_List.get(i);
			//((String)_command_List.getItem(ic)).trim() );
			if ( command.regionMatches(true,0,((String)__commands_JListModel.get(ic)).trim(),0,command.length() ) ) {
				found_commands.add ( (String)__commands_JListModel.get(ic) );
				//Message.printStatus ( 1, "", "Adding command \"" + __commands_JListModel.get(ic) + "\"" );
				if ( !get_all ) {
					// Don't need to search any more.
					break;
				}
			}
		}
	}
	// Reverse the commands so they are listed in the order of the list.
	size = found_commands.size();
	if ( size <= 1 ) {
		return found_commands;
	}
	List<String> found_commands_sorted = new ArrayList<>(size);
	for ( int i = size - 1; i >= 0; i-- ) {
		found_commands_sorted.add ( found_commands.get(i));
	}
	return found_commands_sorted;
}
*/

/**
Get the commands above the first selected row in the final list.
If nothing is selected, return all the items.
@return final list items above first selected item or all if nothing selected.
Return empty non-null list if first item is selected.
*/
public List<Command> getCommandsAboveSelected () {
	if ( __commands_JListModel.size() == 0) {
		return new ArrayList<Command>();
	}

	int selectedIndices[] = ui_GetCommandJList().getSelectedIndices();
	int selectedSize = selectedIndices.length;

	if ( selectedSize == 0 ) {
		// Return all.
		List<Command> v = new ArrayList<>();
		int size = __commands_JListModel.size();
		for (int i = 0; i < size; i++) {
			v.add ( (Command)__commands_JListModel.get(i));
		}
		return v;
	}
	if ( selectedIndices[0] == 0 ) {
		// Nothing above.
		selectedIndices = null;
		return new ArrayList<Command>();
	}
	else {
		// Return above first selected.
		List<Command> v = new ArrayList<>(selectedIndices[0] + 1);
		for (int i = 0; i < selectedIndices[0]; i++) {
			v.add ((Command)__commands_JListModel.get(i));
		}
		selectedIndices = null;
		return v;
	}
}

/**
Return the command file name.  This is used by the processor when creating the check file.
@return the command file name.
*/
public String getCommandFileName () {
	return __commandFileName;
}

/**
Return the commands menu style, which defines the organization of the commands menu.
*/
private int getCommandsMenuStyle () {
	int menu_style = MENU_STYLE_THREE_LEVEL;
	if ( !__View_ThreeLevelCommandsMenu_JCheckBoxMenuItem.isSelected() ) {
		menu_style = MENU_STYLE_TWO_LEVEL;
	}
	return menu_style;
}

/**
Return the initial working directory, which will be the software startup home,
or the location of the command file read/write (a directory).
This directory is suitable for initializing a workflow processing run.
@return the initial working directory, which should always be non-null.
*/
private String getInitialWorkingDir () {
	return __initialWorkingDir;
}

// TODO SAM 2004-04-12 - need to make part of the data set at some point.
/**
Return the StateMod_NodeNetwork that is currently opened.
@return the StateMod_NodeNetwork that is currently opened, or null if not available.
*/
public StateMod_NodeNetwork getModelNetwork () {
	if ( __network_JFrame == null ) {
		return null;
	}
	return __network_JFrame.getNetwork();
}

/**
Get the StateDMI session type as a String, suitable for output.
@return the current StateDMI session type.
*/
private String getSessionTypeName () {
	if ( __sessionType == __SESSION_DATA_SET_COMPONENT ) {
		return "Data Set Component";
	}
	else if ( __sessionType == __SESSION_DATA_SET ) {
		return "Data Set";
	}
	else if ( __sessionType == __SESSION_COMMANDS ) {
		return "Commands";
	}
	else {
		return "Unknown";
	}
}

/**
Handle actions from the message log viewer.
In particular, when a command is selected and the user wants to go to the command in the interface.
@param tag Tag that identifies the command.  This is of the format:
<pre>
<command,count>
</pre>
where "command" is the command number (1+) and "count" is an optional count of warnings for the command.
*/
public void goToMessageTag ( String tag ) {
	String command_line = "";
	if ( tag.indexOf(",") >= 0 ) {
		String first_token = StringUtil.getToken(tag,",",0,0);
		if ( first_token.equalsIgnoreCase("ProcessCommands") ) {
			// Get the command number from the second token.
			command_line = StringUtil.getToken(tag,",",0,1);
		}
		else {
			// Get the command number from the first token.
			command_line = StringUtil.getToken(tag,",",0,0);
		}
	}
	else {
		// Get the command number from the only tag.
		if ( StringUtil.isInteger(tag) ) {
			command_line = tag;
		}
	}
	if ( StringUtil.isInteger(command_line) ) {
		int iline = StringUtil.atoi(command_line);
		if ( (iline >= 0) && (iline < __commands_JListModel.size()) ) {
			// Clear previous selections.
			__commands_JList.clearSelection();
			// Select the current tag.
			ui_SelectCommand ( iline );
			// Position the list.
			__commands_JList.ensureIndexIsVisible(iline);
		}
	}
	else if ( command_line.equalsIgnoreCase("EndChecks") ) {
		// Go to last command.
		int iline = __commands_JListModel.size();
		// Clear previous selections.
		__commands_JList.clearSelection();
		// Select the current tag.
		ui_SelectCommand ( iline );
		// Position the list.
		__commands_JList.ensureIndexIsVisible(iline);
	}
}

/**
Required by ListDataListener.
Receive notification when the contents of the commands list have changed due to commands being added.
*/
public void intervalAdded ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
Required by ListDataListener.
Receive notification when the contents of the commands list have changed due to commands being removed.
*/
public void intervalRemoved ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
Handle ItemEvent events.
@param e ItemEvent to handle.
*/
public void itemStateChanged ( ItemEvent evt ) {
	Object o = evt.getSource();

	if (ui_GetIgnoreItemEvent()) {
		return;
	}

	else if ( (o == __dataStore_JComboBox) && (evt.getStateChange() == ItemEvent.SELECTED) ) {
        // New datastore selected.
        uiAction_DataStoreChoiceClicked();
    }
	else if ( o == __View_DataSetManager_JCheckBoxMenuItem ) {
		// TODO
		if ( __statecuDatasetManager == null ) {
			// Create it.
			__statecuDatasetManager =
			new StateCU_DataSet_JFrame ( this, __statecuDataset, "StateCU Data Set", true );
			__statecuDatasetManager.addWindowListener ( this );
		}
		else {
			// Just set it visible (need to make sure its contents are refreshed based on the current GUI state).
			__statecuDatasetManager.setVisible( __View_DataSetManager_JCheckBoxMenuItem.getState() );
		}
	}
    else if ( o == __View_Map_JCheckBoxMenuItem ) {
		if ( __View_Map_JCheckBoxMenuItem.isSelected() ) {
			// User wants the map to be displayed.
			uiAction_OpenGeoView ( true );
		}
		else {
			// Map is deselected.  Just set the map frame to no visible.
			if ( __geoview_JFrame != null ) {
				__geoview_JFrame.setVisible ( false );
			}
		}
	}
	else if ( o == __View_ModelNetwork_JCheckBoxMenuItem ) {
		if ( __View_ModelNetwork_JCheckBoxMenuItem.isSelected() ) {
			if (__network_JFrame == null) {
				// Network has not previously been read so prompt for a file.
				uiAction_OpenModelNetwork ();
			}
			else {
				__network_JFrame.setVisible(true);
			}
		}
		else {
			// Just make the network invisible.
			if ( __network_JFrame != null ) {
				__network_JFrame.setVisible(false);
			}
		}
	}
	ui_UpdateStatus ( true );
}

/**
Handle key pressed events.
Most actions are handled in keyReleased() to avoid multiple key press events from causing problems.
*/
public void keyPressed(KeyEvent e) {
}

/**
Handle key released events.
*/
public void keyReleased(KeyEvent event) {
	int code = event.getKeyCode();
	if ( code == KeyEvent.VK_DELETE ) {
		// Clear a command.
		if ( event.getSource() == __commands_JList ) {
			commandList_RemoveCommandsBasedOnUI();
		}
	}
	else if ( code == KeyEvent.VK_ENTER ) {
		if ( event.getSource() == __commands_JList ) {
			// Same as the Edit...Command event.
			uiAction_EditCommand ();
		}
	}
}

public void keyTyped(KeyEvent e) {
}

/**
Handle mouse clicked events.  If multiple clicks in the commands area, then edit the selected command.
*/
public void mouseClicked ( MouseEvent event ) {
	Object source = event.getSource();
	if ( source == __commands_JList ) {
		if ( event.getClickCount() == 2 ) {
			// Same as editing with error checks.
			// Edit the first selected item, unless a comment, in which case all are edited.
			uiAction_EditCommand ();
		}
	}
}

/**
Handle mouse entered event.  Nothing is done.
*/
public void mouseEntered(MouseEvent event) {
}

/**
Handle mouse exited event.  Nothing is done.
*/
public void mouseExited(MouseEvent event) {
}

/**
Handle mouse pressed event.
*/
public void mousePressed(MouseEvent event) {
	int mods = event.getModifiers();
	Component c = event.getComponent();
    // Popup for commands.
	if ( (c == ui_GetCommandJList()) && (__commands_JListModel.size() > 0) &&
		((mods & MouseEvent.BUTTON3_MASK) != 0) ) {
		Point pt = JGUIUtil.computeOptimalPosition ( event.getPoint(), c, __Commands_JPopupMenu );
		__Commands_JPopupMenu.show ( c, pt.x, pt.y );
	}
    // Popup for table results list, right click since left click automatically shows table.
    else if ( (c == __resultsTables_JList) && (__resultsTables_JListModel.size() > 0) //) {//&&
        && ((mods & MouseEvent.BUTTON3_MASK) == MouseEvent.BUTTON3_MASK) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, __resultsTables_JPopupMenu );
        __resultsTables_JPopupMenu.show ( c, pt.x, pt.y );
    }
}

/**
Handle mouse released event.  Nothing is done.
*/
public void mouseReleased(MouseEvent event) {
}

/**
 * Used for batch processing of a command file.
 * Checks for existence of the input file and returns if no file is found.
 * Otherwise, all commands are stored in a list and the runCommands method is run.
 * RunCommands will run all the commands and write any output.  Returns true if successful and false otherwise.
 *
 * @param File
 * @return boolean
 */
/* FIXME SAM 2007-10-22 Make this agree with TSTool.
protected boolean runCommandsFromFile(File  inFile) {
	// Store the commands from the file into a list and initialize the rest of the environment to run the commands.
	// FIXME SAM 2007-10-22 Fix consistent with TSTool.
	//boolean fileExists = storeCommandsFromFile(inFile);
	boolean fileExists = false;
	if(!(fileExists))
		return false;
	// Run commands in batch mode.
	// Both parameters are true since we want to run all commands
	// and write all output that is referenced with write() commands in the command file.
	uiAction_RunCommands(true, true);
	// FIXME SAM Need to make work like TSTool.
	return true;
}
*/

/**
Clear the results area because a new processor run is about to start.
*/
private void results_Clear() {
	ui_SetIgnoreActionEvent (true);
	// Clear the list of output files.
	results_OutputFiles_Clear();
	// Clear tables.
	results_Tables_Clear();
	// Clear the list of output components.
	results_StateCUComponents_Clear();
	results_StateModComponents_Clear();
	ui_SetIgnoreActionEvent( false);
}

/**
Copy a time series list and add a total, for displays.
Only the list is copied, but not the data in the time series.
@param tslist a list of time series to process, of consistent interval.
@param app_type Application type.
@param comp_type Component type, used to determine the units and other information for the total time series.
@param dataset_location the location to use for the total time series.
@param dataset_datasource the data source to use for the total time series.
@param dataset_location the description to use for the total time series.
@exception Exception if an error occurs creating the total time series.
*/
private <T extends TS> List<T> results_CopyTSListAndAddTotal ( List<T> tslist, int app_type, int comp_type,
	String dataset_location, String dataset_datasource, String dataset_description )
throws Exception {
	int vsize = tslist.size();
	List<T> v = new ArrayList<T> ( vsize );
	for ( int i = 0; i < vsize; i++ ) {
		v.add ( tslist.get(i) );
	}
	if ( app_type == StateDMI.APP_TYPE_STATEMOD ) {
		Message.printStatus ( 2, "", "Adding total time series...vsize=" + v.size());
		try {
			v.add ( StateMod_Util.createTotalTS ( tslist,
				dataset_location, dataset_datasource, dataset_description, comp_type ) );
			Message.printStatus ( 2, "", "Added total time series...vsize=" + v.size());
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, "", "Unable to add total time series (" + e + ").");
		}
	}
	return v;
}

/**
Display time series results.
@param tslist list of TS to display.
@param initial_view "Graph", "Table", or "Summary", for the initial view of the time series.
@param app_type Application type for the component.
@param comp_type Component type for the time series.
*/
private void results_DisplayTimeSeries ( List tslist, String initial_view, int app_type, int comp_type ) {
	String routine = getClass().getSimpleName() + ".results_DisplayTimeSeries";
	try {
		PropList graphprops = new PropList ( "TSView" );
		// Default properties.
		graphprops.set ( "InitialView", initial_view );
		// Parent window to center the graph.
		graphprops.setUsingObject ( "TSViewParentUIComponent", this );
		// Set the total size of the graph window.
		graphprops.set ( "TotalWidth", "600" );
		graphprops.set ( "TotalHeight", "400" );
		// Set the total size of the summary window.
		graphprops.set ( "Summary.TotalWidth", "1000" );
		graphprops.set ( "Summary.TotalHeight", "600" );
		graphprops.set ( "GraphType=Line" );
		// Title.
		if ( (app_type == StateDMI.APP_TYPE_STATECU) && (comp_type >= 0)  ) {
			graphprops.set ( "TitleString", StateCU_Util.lookupTimeSeriesGraphTitle(comp_type));
			graphprops.set ( "TSViewTitleString", StateCU_Util.lookupTimeSeriesGraphTitle(comp_type));
		}
		else if((app_type == StateDMI.APP_TYPE_STATEMOD) && (comp_type >= 0) ) {
			graphprops.set ( "TitleString", StateMod_Util.lookupTimeSeriesGraphTitle(comp_type));
			graphprops.set ( "TSViewTitleString", StateMod_Util.lookupTimeSeriesGraphTitle(comp_type));
		}
		else {
			// Default...
			graphprops.set ( "TitleString", "Time Series" );
		}
		// Summary properties for secondary displays (copy from summary output).
		graphprops.set ( "DisplayFont", "Courier" );
		graphprops.set ( "DisplaySize", "8" );
		graphprops.set ( "PrintFont", "Courier" );
		graphprops.set ( "PrintSize", "7" );
		graphprops.set ( "PageLength", "100" );
		new TSViewJFrame ( tslist, graphprops );
		// For garbage collection...
		tslist = null;
	}
	catch ( Exception e ) {
		String message = "Error displaying time series.";
		Message.printWarning ( 1, routine, message );
		Message.printWarning ( 3, routine, e );
	}
}

// TODO SAM 2009-05-08 Evaluate sorting the files - maybe need to put in a worksheet so they can be sorted.
/**
Add the specified output file to the list of output files that can be selected for viewing.
Only files that exist are added.  Files are added in the order of processing.
@param file Output file generated by the processor.
*/
private void results_OutputFiles_AddOutputFile ( File file ) {
	String filePathString = null;
    try {
        filePathString = file.getCanonicalPath();
    }
    catch ( IOException e ) {
        // Should not happen.
        return;
    }
    if ( !IOUtil.fileExists(filePathString)) {
        // File does not exist so don't show in the list of output files.
        return;
    }
    if ( JGUIUtil.indexOf(__resultsOutputFiles_JList, filePathString, false, true) < 0 ) {
        __resultsOutputFiles_JListModel.addElement( filePathString );
    }
}

/**
Clear the list of output files.  This is normally called before the commands are run.
*/
private void results_OutputFiles_Clear() {
	__resultsOutputFiles_JListModel.removeAllElements();
    ui_UpdateStatus ( false );
}

/**
Display the StateCU climate stations data.
*/
private void results_ShowStateCUClimateStationData () {
	new StateCU_ClimateStation_JFrame ( "Climate Stations",	__statecuDataset, false );
}

/**
Display the StateCU crop characteristics data.
*/
private void results_ShowStateCUCropCharacteristicsData () {
	new StateCU_CropCharacteristics_JFrame ( __statecuDataset, false );
}

/**
Show the StateCU map layers that are referenced in an existing data set.
Set the properties on the layers to reasonable defaults.
*/
/* TODO SAM 2007-06-26 Evaluate why not called.
private void results_ShowStateCUDataSetMapLayers ()
{	String routine = "StateDMI_JFrame.showStateCUDataSetMapLayers";
	if ( __statecu_dataset == null ) {
		return;
	}
	// First clear the map.

	if ( __geoview_JFrame != null ) {
		__geoview_JFrame.getGeoViewJPanel().removeAllLayerViews();
	}
	else {
		// Create the map.
		openGeoView ( true );
	}

	// Add basins.

	String filepath;
	String warning = "";
	GeoLayerView layer_view = null;
	DataSetComponent comp = __statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_GIS_STATE );
	if ( (__geoview_JFrame != null) && (comp != null) && !comp.getDataFileName().equals("") ) {
		filepath = __statecu_dataset.getDataFilePath ( comp.getDataFileName() );
		if ( !StringUtil.endsWithIgnoreCase(filepath,".shp") ) {
			filepath += ".shp";
		}
		Message.printStatus ( 1, routine, "Adding map layer \"" + filepath + "\"" );
		try {
			layer_view = new GeoLayerView ( filepath, new PropList("LayerView"),
			__geoview_JFrame.getGeoViewJPanel().getGeoView().getNumLayerViews() + 1 );
			// Set default attributes on the layer.
			if ( layer_view.getLayer().getShapeType() == GeoLayer.LINE ) {
				layer_view.getSymbol().setOutlineColor( GRColor.black);
			}
			else {
				// Assume polygon.
				layer_view.getSymbol().setColor( new GRColor(255,240,190) );
				layer_view.getSymbol().setOutlineColor( GRColor.black);
			}
			layer_view.getLegend().setText ( "State" );
			__geoview_JFrame.getGeoViewJPanel().addLayerView ( layer_view );
		}
		catch ( Exception e ) {
			Message.printWarning ( 2, routine, e );
			warning += "\nError adding map layer \""+filepath+"\"";
		}
	}
	else {
		Message.printStatus ( 1, routine, "No map layer available for states" );
	}

	// Add divisions.

	comp = __statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_GIS_DIVISIONS );
	if ( (__geoview_JFrame != null) && (comp != null) && !comp.getDataFileName().equals("") ) {
		filepath = __statecu_dataset.getDataFilePath ( comp.getDataFileName() );
		if ( !StringUtil.endsWithIgnoreCase(filepath,".shp") ) {
			filepath += ".shp";
		}
		Message.printStatus ( 1, routine, "Adding map layer \"" + filepath + "\"" );
		try {
			layer_view = new GeoLayerView ( filepath, new PropList("LayerView"),
			__geoview_JFrame.getGeoViewJPanel().getGeoView().getNumLayerViews() + 1 );
			if ( layer_view.getLayer().getShapeType() == GeoLayer.LINE ) {
				layer_view.getSymbol().setColor( GRColor.black);
			}
			else {
				// Assume polygon.
				layer_view.getSymbol().setColor( new GRColor(255,240,190) );
				layer_view.getSymbol().setOutlineColor( GRColor.black);
			}
			layer_view.getLegend().setText ( "Divisions" );
			__geoview_JFrame.getGeoViewJPanel().addLayerView ( layer_view );
		}
		catch ( Exception e ) {
			warning += "\nError adding map layer \""+filepath+"\"";
		}
	}
	else {
		Message.printStatus ( 1, routine, "No map layer available for districts" );
	}

	// Add rivers.

	comp = __statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_GIS_RIVERS );
	if ( (__geoview_JFrame != null) && (comp != null) && !comp.getDataFileName().equals("") ) {
		filepath = __statecu_dataset.getDataFilePath ( comp.getDataFileName() );
		if ( !StringUtil.endsWithIgnoreCase(filepath,".shp") ) {
			filepath += ".shp";
		}
		Message.printStatus ( 1, routine, "Adding map layer \"" + filepath + "\"" );
		try {
			layer_view = new GeoLayerView ( filepath, new PropList("LayerView"),
			__geoview_JFrame.getGeoViewJPanel().getGeoView().getNumLayerViews() + 1 );
			layer_view.getSymbol().setColor(new GRColor(0,188,253));
			layer_view.getLegend().setText ( "Rivers" );
			__geoview_JFrame.getGeoViewJPanel().addLayerView ( layer_view );
		}
		catch ( Exception e ) {
			warning += "\nError adding map layer \""+filepath+"\"";
			Message.printWarning ( 2, routine, e );
		}
	}
	else {
		Message.printStatus ( 1, routine, "No map layer available for rivers" );
	}

	// Add climate stations.

	comp = __statecu_dataset.getComponentForComponentType (	StateCU_DataSet.COMP_GIS_CLIMATE_STATIONS );
	if ( (__geoview_JFrame != null) && (comp != null) && !comp.getDataFileName().equals("") ) {
		filepath = __statecu_dataset.getDataFilePath ( comp.getDataFileName() );
		if ( !StringUtil.endsWithIgnoreCase(filepath,".shp") ) {
			filepath += ".shp";
		}
		Message.printStatus ( 1, routine, "Adding map layer \"" + filepath + "\"" );
		try {
			layer_view = new GeoLayerView ( filepath, new PropList("LayerView"),
			__geoview_JFrame.getGeoViewJPanel().getGeoView().getNumLayerViews() + 1 );
			layer_view.getSymbol().setColor(new GRColor(0,0,0));
			layer_view.getSymbol().setStyle( GRSymbol.SYM_FCIR);
			layer_view.getSymbol().setSize(6.0);
			layer_view.getLegend().setText ( "Climate Stations" );
			__geoview_JFrame.getGeoViewJPanel().addLayerView ( layer_view );
		}
		catch ( Exception e ) {
			warning += "\nError adding map layer \""+filepath+"\"";
		}
	}
	else {
		Message.printStatus ( 1, routine, "No map layer available for climate stations." );
	}

	// Add structures.

	if ( (__statecu_dataset_type != StateCU_DataSet.TYPE_CLIMATE_STATIONS) &&
		(__statecu_dataset_type != StateCU_DataSet.TYPE_OTHER_USES) ) {
	comp = __statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_GIS_STRUCTURES);
	if ( (__geoview_JFrame != null) && (comp != null) ) {
		filepath = __statecu_dataset.getDataFilePath ( comp.getDataFileName() );
		if ( !StringUtil.endsWithIgnoreCase(filepath,".shp") ) {
			filepath += ".shp";
		}
		Message.printStatus ( 1, routine, "Adding map layer \"" + filepath + "\"" );
		try {
			layer_view = new GeoLayerView ( filepath, new PropList("LayerView"),
			__geoview_JFrame.getGeoViewJPanel().getGeoView().getNumLayerViews() + 1 );
			layer_view.getSymbol().setColor(new GRColor(0,255,0));
			layer_view.getSymbol().setStyle( GRSymbol.SYM_FSQ);
			layer_view.getSymbol().setSize(4.0);
			layer_view.getLegend().setText ( "Structures" );
			__geoview_JFrame.getGeoViewJPanel().addLayerView ( layer_view );
		}
		catch ( Exception e ) {
			warning += "\nError adding map layer \""+filepath+"\"";
		}
	}
	else {
		Message.printStatus ( 1, routine, "No map layer available for structures." );
	}
	}

	if ( warning.length() > 0 ) {
		Message.printWarning ( 1, routine, "Error adding map layers:\n" + warning );
	}
}
*/

/**
Display the StateCU delay table data.
*/
private void results_ShowStateCUDelayTableData () {
	DataSetComponent comp = __statecuDataset.getComponentForComponentType (
		StateCU_DataSet.COMP_DELAY_TABLES_MONTHLY);
	if ( comp != null ) {
		List data = (List)comp.getData();
		if ( data != null ) {
			new StateMod_DelayTable_JFrame ( data, true, false );
		}
	}
}

/**
Display the StateCU location data.
*/
private void results_ShowStateCULocationData() {
	new StateCU_Location_JFrame ( true, __statecuDataset, null, false );
}

/**
Display the StateCU locations (this is currently a demo of a combination plot).
*/
/* TODO SAM 2007-06-26 Evaluate why not used.
private void results_ShowStateCULocationsSAM () {
	// Create a list of TS and PropList for a TSProduct.
	PropList props = new PropList ( "CU Locations" );
	Vector tslist = new Vector();

	props.set ( "TotalWidth=600" );
	props.set ( "TotalHeight=800" );
	props.set ( "InitialView=Graph" );

	// Need the CU Location to get the identifier to look up.
	// TODO- when data objects are linked don't need to look up here.
	DataSetComponent culoc_comp = __statecu_dataset.getComponentForComponentType (
		StateCU_DataSet.COMP_CU_LOCATIONS);
	StateCU_Location culoc = null;
	if ( culoc_comp != null ) {
		Vector data = (Vector)culoc_comp.getData();
		if ( data != null ) {
			// TODO - just a test.
			int size = data.size();
			for ( int i = 0; i < size; i++ ) {
				culoc = (StateCU_Location)data.elementAt(i);
				if ( culoc == null ) {
					continue;
				}
				if ( culoc.getID().equals("430819") ) {
					// Pick this one because it has more than one crop.
					break;
				}
			}
		}
	}
	if ( culoc == null ) {
		return;
	}
	Message.printStatus ( 1, "", "Displaying CU Location " + culoc.getID() );

	// Start with the climate data.

	int sub = 1;
	props.set ( "SubProduct " + sub + ".GraphType=Bar" );
	props.set ( "SubProduct " + sub + ".MainTitleString=Precipitation Stations" );
	props.set ( "SubProduct " + sub + ".MainTitleFontSize=10" );
	DataSetComponent comp = __statecu_dataset.getComponentForComponentType (
		StateCU_DataSet.COMP_PRECIPITATION_TS_MONTHLY);
	int ncli = culoc.getNumClimateStations();
	String stationid;
	int pos;
	TS ts;
	if ( (comp != null) && (ncli > 0) ) {
		Vector data = (Vector)comp.getData();
		if ( data != null ) {
			for ( int i = 0; i < ncli; i++ ) {
				stationid = culoc.getClimateStationID(i);
				Message.printStatus ( 1, "", "Displaying CU Location station " + stationid );
				pos = TSUtil.indexOf ( data, stationid, "Location", 1 );
				if ( pos >= 0 ) {
					ts = (TS)data.elementAt(pos);
					props.set ( "Data " + sub + "." + (i + 1) + ".TSID=" + ts.getIdentifierString() );
					tslist.addElement ( ts );
				}
				else {
					props.set ( "Data " + sub + "." + (i + 1) + ".TSID=?" );
					tslist.addElement ( null );
				}
			}
		}
	}
	++sub;
	props.set ( "SubProduct " + sub + ".GraphType=Line" );
	props.set ( "SubProduct " + sub + ".MainTitleString=Temperature Stations" );
	props.set ( "SubProduct " + sub + ".MainTitleFontSize=10" );
	comp =	__statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_TEMPERATURE_TS_MONTHLY_AVERAGE );
	if ( (comp != null) && (ncli > 0) ) {
		Vector data = (Vector)comp.getData();
		if ( data != null ) {
			for ( int i = 0; i < ncli; i++ ) {
				stationid = culoc.getClimateStationID(i);
				pos = TSUtil.indexOf ( data, stationid, "Location", 1 );
				if ( pos >= 0 ) {
					ts = (TS)data.elementAt(pos);
					// TODO - need a true data type to let the TSProduct know what to do.
					ts.getIdentifier().setType("Temp");
					props.set ( "Data " + sub + "." + (i + 1) + ".TSID=" + ts.getIdentifierString() );
					tslist.addElement ( ts );
				}
				else {
					props.set ( "Data " + sub + "." + (i + 1) + ".TSID=?" );
					tslist.addElement ( null );
				}
			}
		}
	}

	// Next add Crops.

	++sub;
	props.set ( "SubProduct " + sub + ".GraphType=Line" );
	props.set ( "SubProduct " + sub + ".MainTitleString=Crop Acres and Acres by Irrigation Method" );
	props.set ( "SubProduct " + sub + ".MainTitleFontSize=10" );
	comp =	__statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY );
	int idata = 1;
	if ( comp != null ) {
		Vector data = (Vector)comp.getData();
		if ( data != null ) {
			// Find CU location's data...
			pos = StateCU_Util.indexOf ( data, culoc.getID() );
			if ( pos >= 0 ) {
				StateCU_CropPatternTS cropts = (StateCU_CropPatternTS)data.elementAt(pos);
				Vector crops = cropts.getCropNames();
				int ncrops = crops.size();
				for ( int i = 0; i < ncrops; i++ ) {
					ts = cropts.getCropPatternTS ( (String)crops.elementAt(i) );
					if ( ts != null ) {
						props.set ( "Data " + sub + "." + (idata++) + ".TSID=" + ts.getIdentifierString() );
						tslist.addElement ( ts );
					}
					else {
						props.set ( "Data " + sub + "." + (idata++) + ".TSID=?" );
						tslist.addElement ( null );
					}
				}
			}
		}
	}
	comp = __statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY );
	if ( comp != null ) {
		Vector data = (Vector)comp.getData();
		if ( data != null ) {
			// Find CU location's data.
			pos = StateCU_Util.indexOf ( data, culoc.getID() );
			if ( pos >= 0 ) {
				StateCU_IrrigationPracticeTS ipyts = (StateCU_IrrigationPracticeTS)data.elementAt(pos);
				ts = ipyts.getSacreTS();
				if ( ts != null ) {
					props.set ( "Data " + sub + "." + (idata++) + ".TSID=" + ts.getIdentifierString() );
					tslist.addElement ( ts );
				}
				else {
					props.set ( "Data " + sub + "." + (idata++) + ".TSID=?" );
					tslist.addElement ( null );
				}
				ts = ipyts.getGacreTS();
				if ( ts != null ) {
					props.set ( "Data " + sub + "." + (idata++) + ".TSID=" + ts.getIdentifierString() );
					tslist.addElement ( ts );
				}
				else {
					props.set ( "Data " + sub +	"." + (idata++) + ".TSID=?" );
					tslist.addElement ( null );
				}
				ts = ipyts.getTacreTS();
				if ( ts != null ) {
					props.set ( "Data " + sub + "." + (idata++) + ".TSID=" + ts.getIdentifierString() );
					tslist.addElement ( ts );
				}
				else {
					props.set ( "Data " + sub +	"." + (idata++) + ".TSID=?" );
					tslist.addElement ( null );
				}
			}
		}
	}

	// Next add irrigation practice efficiencies, and pumping.

	// Finally add diversions.

	++sub;
	props.set ( "SubProduct " + sub + ".GraphType=Line" );
	props.set ( "SubProduct " + sub + ".MainTitleString=Historical Diversions" );
	props.set ( "SubProduct " + sub + ".MainTitleFontSize=10" );
	comp =	__statecu_dataset.getComponentForComponentType ( StateCU_DataSet.COMP_DIVERSION_TS_MONTHLY );
	if ( comp != null ) {
		Vector data = (Vector)comp.getData();
		if ( data != null ) {
			pos = TSUtil.indexOf ( data, culoc.getID(), "Location", 1 );
			if ( pos >= 0 ) {
				ts = (TS)data.elementAt(pos);
				props.set ( "Data " + sub + ".1.TSID=" + ts.getIdentifierString() );
				tslist.addElement ( ts );
			}
			else {
				props.set ( "Data " + sub + ".1.TSID=?" );
				tslist.addElement ( null );
			}
		}
	}

	// Now create the graph.

	try {
		TSProduct tsproduct = new TSProduct ( props, null );
		tsproduct.setTSList ( tslist );
		new TSViewJFrame ( tsproduct );
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, "", "Unable to display results." );
		Message.printWarning ( 2, "", e );
	}
}
*/

/**
Display the StateCU monthly precipitation time series data.
TODO - perhaps need a way to select a subset to view.  Maybe figure out what is selected in the results tree?
*/
/* TODO SAM 2007-06-26 Evaluate why not called.
private void results_ShowStateCUMonthlyPrecipitationTS () {
	DataSetComponent comp = __statecu_dataset.getComponentForComponentType (
		StateCU_DataSet.COMP_PRECIPITATION_TS_MONTHLY);
	if ( comp != null ) {
		Vector tslist = (Vector)comp.getData();
		if ( tslist != null ) {
			PropList graphprops = new PropList ( "ts" );
			graphprops.set ( "TotalWidth", "600" );
			graphprops.set ( "TotalHeight", "400" );
			graphprops.set ( "Title", "Precipitation Time Series" );
			graphprops.set ( "GraphType", "Bar" );
			graphprops.set ( "DisplayFont", "Courier" );
			graphprops.set ( "DisplaySize", "11" );
			graphprops.set ( "PrintFont", "Courier" );
			graphprops.set ( "PrintSize", "7" );
			graphprops.set ( "PageLength", "100" );
			graphprops.set ( "InitialView", "Graph" );
			try {
				new TSViewJFrame ( tslist, graphprops );
			}
			catch ( Exception e ) {
				Message.printWarning ( 1, "showStateCUMonthlyPrecipitationTS", "Error displaying data." );
			}
		}
	}
}
*/

/**
Display the StateCU monthly temperature time series data.
TODO - perhaps need a way to select a subset to view. Maybe figure out what is selected in the results tree?
*/
/* TODO SAM 2007-06-26 Evaluate why not enabled.
private void results_ShowStateCUTemperatureTSMonthly () {
	DataSetComponent comp = __statecu_dataset.getComponentForComponentType (
		StateCU_DataSet.COMP_TEMPERATURE_TS_MONTHLY_AVERAGE);
	if ( comp != null ) {
		Vector tslist = (Vector)comp.getData();
		if ( tslist != null ) {
			PropList graphprops = new PropList ( "ts" );
			graphprops.set ( "TotalWidth", "600" );
			graphprops.set ( "TotalHeight", "400" );
			graphprops.set ( "Title", "Monthly Average Temperature Time Series" );
			graphprops.set ( "DisplayFont", "Courier" );
			graphprops.set ( "DisplaySize", "11" );
			graphprops.set ( "PrintFont", "Courier" );
			graphprops.set ( "PrintSize", "7" );
			graphprops.set ( "PageLength", "100" );
			graphprops.set ( "InitialView", "Graph" );
			try {
				new TSViewJFrame ( tslist, graphprops );
			}
			catch ( Exception e ) {
				Message.printWarning ( 1, "showStateCUTemperatureTSMonthly", "Error displaying data." );
			}
		}
	}
}
*/

/**
Display the StateMod delay table data.
*/
private void results_ShowStateModDelayTableData () {
	new StateMod_DelayTable_JFrame( __statemodDataset, null, true, false );
}

/**
Display the StateMod diversion data.
*/
private void results_ShowStateModDiversionData () {
	new StateMod_Diversion_JFrame ( __statemodDataset, null, false );
}

/**
Display the StateMod evaporation data.
*/
private void results_ShowStateModEvaporationData () {
	// TODO - Not usually that many so show all.
	// Need a threshold count to force select of subset?
	String routine = "StateDMI_JFrame.showStateModEvaporationData";
	DataSetComponent comp2 = __statemodDataset.getComponentForComponentType (
		StateMod_DataSet.COMP_EVAPORATION_TS_MONTHLY);
	List tslist = null;
	if ( comp2 != null ) {
		tslist = (List)comp2.getData();
	}
	PropList props = new PropList ( "Evaporation" );
	props.set ( "Title=Evaporation" );
	props.set ( "InitialView=Graph" );
	props.set ( "GraphType=Bar" );
	try {
		new TSViewJFrame ( tslist, props );
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, routine, "Error displaying data." );
	}
}

/**
Display the StateMod instream flow data.
*/
private void results_ShowStateModInstreamFlowData () {
	new StateMod_InstreamFlow_JFrame ( __statemodDataset, null, false );
}

/**
Display the StateMod river gage station data.
*/
private void results_ShowStateModStreamGageData () {
	new StateMod_StreamGage_JFrame ( __statemodDataset, (StateMod_DataSet_WindowManager)null, false );
}

/**
Display the StateMod network data.
*/
private void results_ShowStateModRiverNetworkData () {
	new StateMod_RiverNetworkNode_JFrame ( __statemodDataset, (StateMod_DataSet_WindowManager)null, false );
}

/**
Display the StateMod operational data.
*/
private void results_ShowStateModOperationalData () {
	new StateMod_OperationalRight_JFrame ( __statemodDataset, (StateMod_DataSet_WindowManager)null, false );
}

/**
Display the StateMod precipitation data.
*/
private void results_ShowStateModPrecipitationData () {
	// TODO - Not usually that many so show all.
	// Need a threshold count to force select of subset?
	String routine = "StateDMI_JFrame.showStateModPrecipitationData";
	DataSetComponent comp2 = __statemodDataset.getComponentForComponentType (
		StateMod_DataSet.COMP_PRECIPITATION_TS_MONTHLY);
	List tslist = null;
	if ( comp2 != null ) {
		tslist = (List)comp2.getData();
	}
	PropList props = new PropList ( "Precipitation" );
	props.set ( "Title=Precipitation" );
	props.set ( "InitialView=Graph" );
	props.set ( "GraphType=Bar" );
	try {
		new TSViewJFrame ( tslist, props );
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, routine, "Error displaying data." );
	}
}

/**
Display the StateMod reservoir data.
*/
private void results_ShowStateModReservoirData () {
	new StateMod_Reservoir_JFrame ( __statemodDataset, null, false);
}

/**
Display the StateMod well data.
*/
private void results_ShowStateModWellData () {
	new StateMod_Well_JFrame ( __statemodDataset, null, false );
}

/**
Add the specified component name to the list of components that can be selected for viewing.
@param table Table generated by the processor.
*/
private void results_StateCUComponents_AddComponents ( String componentName ) {
    if ( JGUIUtil.indexOf(__resultsStateCUComponents_JList, componentName, false, true) < 0 ) {
    	// Not already in the list so add it.
         __resultsStateCUComponents_JListModel.addElement( componentName );
    }
}

/**
Clear the list of StateCU components.  This is normally called before the commands are run.
*/
private void results_StateCUComponents_Clear() {
	__resultsStateCUComponents_JListModel.removeAllElements();
    ui_UpdateStatus ( false );
}

/**
Add the specified component name to the list of components that can be selected for viewing.
@param table Table generated by the processor.
*/
private void results_StateModComponents_AddComponents ( String componentName ) {
    if ( JGUIUtil.indexOf(__resultsStateModComponents_JList, componentName, false, true) < 0 ) {
         __resultsStateModComponents_JListModel.addElement( componentName );
    }
}

/**
Clear the list of StateMod components.  This is normally called before the commands are run.
*/
private void results_StateModComponents_Clear() {
	__resultsStateModComponents_JListModel.removeAllElements();
    ui_UpdateStatus ( false );
}

/**
Add the specified table to the list of tables that can be selected for viewing.
@param tableid table identifier for table generated by the processor.
*/
private void results_Tables_AddTable ( String tableid ) {
    __resultsTables_JListModel.addElement( tableid );
}

/**
Clear the list of results tables.  This is normally called immediately before the commands are run.
*/
private void results_Tables_Clear() {
    __resultsTables_JListModel.removeAllElements();
}

/**
Handle TS_ListSelector_JFrame events.
@param selector TS_ListSelector_JFrame instance from which the time series were selected.
@param tslist The list of TS that were selected.
@param action Action string that indicates which button was pressed on the selector ("Summary", "Table", or "Graph").
*/
public void timeSeriesSelected ( TS_ListSelector_JFrame selector, List<TS> tslist, String action ) {
	// Determine the component type for the time series.
	int vsize = TS_ListSelector_JFrame_List.size();
	TS_ListSelector_JFrame selector_saved;
	for ( int i = 0; i < vsize; i++ ) {
		selector_saved = TS_ListSelector_JFrame_List.get(i);
		if ( selector_saved == selector ) {
			// Display the time series.
			results_DisplayTimeSeries ( tslist, action,
			TS_ListSelector_JFrame_app_type_List.get(i).intValue(),
			TS_ListSelector_JFrame_comp_type_List.get(i).intValue() );
			return;
		}
	}
}

/**
Check to make sure necessary input is available for dialogs, including lists of available region1 and region2 for StateCu.
*/
private void ui_CheckDialogInput () {
	if ( __region1_List == null ) {
		// Get the counties from HydroBase.
		__region1_List = new ArrayList<>();
		if ( __hbdmi != null ) {
			List<HydroBase_CountyRef> v = __hbdmi.getCountyRef();
			int size = 0;
			if ( v != null ) {
				size = v.size();
			}
			HydroBase_CountyRef county = null;
			for ( int i = 0; i < size; i++ ) {
				county = v.get(i);
				__region1_List.add ( county.getCounty() );
			}
		}
	}
	if ( __region2_List == null ) {
		// Get the HUC from HydroBase.
		__region2_List = new ArrayList<>();
		if ( __hbdmi != null ) {
			__region2_List = __hbdmi.getHUC();
		}
	}
	if ( __cropcharCuMethod_List == null ) {
		// Get the Cropchar CU methods from HydroBase.
		__cropcharCuMethod_List = new ArrayList<>();
		if ( __hbdmi != null ) {
			List<HydroBase_Cropchar> v = __hbdmi.getCropcharCUMethod();
			int size = 0;
			if ( v != null ) {
				size = v.size();
			}
			HydroBase_Cropchar cropchar = null;
			for ( int i = 0; i < size; i++ ) {
				cropchar = v.get(i);
				__cropcharCuMethod_List.add ( cropchar.getMethod_desc() );
			}
		}
	}
	if ( __blaneyCriddleCuMethod_List == null ) {
		// Get the CU methods from HydroBase.
		__blaneyCriddleCuMethod_List = new ArrayList<>();
		if ( __hbdmi != null ) {
			List<HydroBase_CUBlaneyCriddle> v = __hbdmi.getBlaneyCriddleCUMethod();
			int size = 0;
			if ( v != null ) {
				size = v.size();
			}
			HydroBase_CUBlaneyCriddle cubc = null;
			for ( int i = 0; i < size; i++ ) {
				cubc = v.get(i);
				__blaneyCriddleCuMethod_List.add ( cubc.getMethod_desc() );
			}
		}
	}
	if ( __penmanMonteithCuMethod_List == null ) {
		// Get the CU methods from HydroBase.
		__penmanMonteithCuMethod_List = new ArrayList<>();
		if ( __hbdmi != null ) {
			List<HydroBase_CUPenmanMonteith> v = __hbdmi.getPenmanMonteithCUMethod();
			int size = 0;
			if ( v != null ) {
				size = v.size();
			}
			HydroBase_CUPenmanMonteith cupm = null;
			for ( int i = 0; i < size; i++ ) {
				cupm = v.get(i);
				__penmanMonteithCuMethod_List.add ( cupm.getMethod_desc() );
			}
		}
	}
}

/**
Checks the current state of the GUI and updates components as necessary.
For example, if nothing is selected in the list, the Edit...Commands menus are disabled.
Use the JGUIUtil.setEnabled() method to simplify checks.
It checks for null items (nulls may be present during development and during application startup).
*/
private void ui_CheckGUIState() {
	//Message.printStatus(2, "ui_CheckGUIState", "Starting");
	// First figure out if something in the list is selected.
	int command_list_size = 0;
	int selected_commands_size = 0;
	if ( __commands_JListModel != null ) {
		command_list_size = __commands_JListModel.size();
		selected_commands_size = JGUIUtil.selectedSize ( ui_GetCommandJList() );
	}

	int dataStoreListSize = 0;
	if ( __statedmiProcessor != null ) {
	    dataStoreListSize = __statedmiProcessor.getDataStores().size();
	}

	// Check the menus in the order of the GUI.  Check the popup menus as appropriate with other menus.

	// File menu.

	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		// Enable/disable the main menus.
		if ( __statecuDatasetType == StateCU_DataSet.TYPE_UNKNOWN ) {
			JGUIUtil.setEnabled ( __File_Save_JMenu, false );
		}
		else {
			// Allow a save if the data set is dirty or we have never saved the data set file.
			if ( (__statecuDataset.getDataSetFileName().equals("")) || __statecuDataset.isDirty() ||
				__commandsDirty ){
				JGUIUtil.setEnabled ( __File_Save_JMenu, true );
			}
			else {
				JGUIUtil.setEnabled ( __File_Save_JMenu, false);
			}
		}
		JGUIUtil.setEnabled ( __File_SwitchToStateCU_JMenuItem, false );
		JGUIUtil.setEnabled ( __File_SwitchToStateMod_JMenuItem, true );
		if ( (__statecuDataset == null) || !__statecuDataset.isDirty() ) {
			/* TODO SAM 2004-02-27 - need to decide what to do.
			JGUIUtil.setEnabled ( __File_Save_AllData_JMenuItem, false );
			*/
		}
		else {
		}
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		// Allow a save if the data set is dirty or we have never saved the data set file.
		if ( (__statemodDataset != null) && ((__statemodDataset.getDataSetFileName().equals("")) ||
				__statemodDataset.isDirty()) ||	__commandsDirty ){
			JGUIUtil.setEnabled ( __File_Save_JMenu, true );
		}
		else {
			JGUIUtil.setEnabled ( __File_Save_JMenu, false);
		}
		JGUIUtil.setEnabled ( __File_SwitchToStateCU_JMenuItem, true );
		JGUIUtil.setEnabled ( __File_SwitchToStateMod_JMenuItem, false);
	}

	// Always able to open a new command file.

	JGUIUtil.setEnabled ( __File_New_CommandFile_JMenuItem, true );

	// If the list is not empty, enable the save menus.

	boolean enabled = false;
	if ( command_list_size > 0 ) {
		if ( __commandsDirty ) {
			JGUIUtil.setEnabled ( __File_Save_Commands_JMenuItem, true );
		}
		else {
			// No need to save.
			JGUIUtil.setEnabled ( __File_Save_Commands_JMenuItem, false );
		}
		JGUIUtil.setEnabled (__File_Save_CommandsAs_JMenuItem,true);
		enabled = true;
	}
	else {
		JGUIUtil.setEnabled ( __File_Save_Commands_JMenuItem,false);
		JGUIUtil.setEnabled ( __File_Save_CommandsAs_JMenuItem, false );
	}
	JGUIUtil.setEnabled ( __File_Save_JMenu, enabled );
	JGUIUtil.setEnabled ( __File_Print_Commands_JMenuItem, true );

	if ( __hbdmi == null ) {
		JGUIUtil.setEnabled ( __File_Properties_HydroBase_JMenuItem, false );
	}
	else {
		JGUIUtil.setEnabled ( __File_Properties_HydroBase_JMenuItem, true );
	}

	// Edit menu.

	if ( selected_commands_size > 0 ) {
		JGUIUtil.setEnabled ( __Edit_CutCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Cut_JMenuItem, true );
		JGUIUtil.setEnabled ( __Edit_CopyCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Copy_JMenuItem, true );
		JGUIUtil.setEnabled ( __Edit_DeleteCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Delete_JMenuItem, true );

		JGUIUtil.setEnabled ( __Edit_CommandWithErrorChecking_JMenuItem, true );
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsToComments_JMenuItem,true);
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsFromComments_JMenuItem,true);
	}
	else {
		JGUIUtil.setEnabled ( __Edit_CutCommands_JMenuItem, false );
		JGUIUtil.setEnabled ( __CommandsPopup_Cut_JMenuItem, false );
		JGUIUtil.setEnabled ( __Edit_CopyCommands_JMenuItem, false );
		JGUIUtil.setEnabled ( __CommandsPopup_Copy_JMenuItem, false );
		JGUIUtil.setEnabled ( __Edit_DeleteCommands_JMenuItem, false );
		JGUIUtil.setEnabled ( __CommandsPopup_Delete_JMenuItem, false );

		JGUIUtil.setEnabled ( __Edit_CommandWithErrorChecking_JMenuItem, false );
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsToComments_JMenuItem,false);
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsFromComments_JMenuItem,false);
	}
	if ( __commandsCutBuffer.size() > 0 ) {
		// Paste button should be enabled.
		JGUIUtil.setEnabled ( __Edit_PasteCommands_JMenuItem, true );
		JGUIUtil.setEnabled ( __CommandsPopup_Paste_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Edit_PasteCommands_JMenuItem, false );
		JGUIUtil.setEnabled ( __CommandsPopup_Paste_JMenuItem, false );
	}
	if ( selected_commands_size > 0 ) {
		JGUIUtil.setEnabled ( __Edit_CutCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Cut_JMenuItem,true);
		JGUIUtil.setEnabled ( __Edit_CopyCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Copy_JMenuItem,true);
		JGUIUtil.setEnabled ( __Edit_DeleteCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_Delete_JMenuItem,true);
		JGUIUtil.setEnabled ( __Edit_SelectAllCommands_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_SelectAll_JMenuItem,true);

		JGUIUtil.setEnabled (__Edit_CommandWithErrorChecking_JMenuItem, true);

		JGUIUtil.setEnabled ( __CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem, true);

		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsToComments_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem, true);
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsFromComments_JMenuItem,true);
		JGUIUtil.setEnabled ( __CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem, true);
	}
	else {
		JGUIUtil.setEnabled ( __Edit_CutCommands_JMenuItem,false);
		JGUIUtil.setEnabled ( __CommandsPopup_Cut_JMenuItem,false);
		JGUIUtil.setEnabled ( __Edit_CopyCommands_JMenuItem,false);
		JGUIUtil.setEnabled ( __CommandsPopup_Copy_JMenuItem,false);
		JGUIUtil.setEnabled ( __Edit_DeleteCommands_JMenuItem,false);
		JGUIUtil.setEnabled ( __CommandsPopup_Delete_JMenuItem,false);

		JGUIUtil.setEnabled ( __Edit_CommandWithErrorChecking_JMenuItem, false );

		JGUIUtil.setEnabled ( __CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem, false);

		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsToComments_JMenuItem,false);
		JGUIUtil.setEnabled ( __CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem, false);
		JGUIUtil.setEnabled ( __Edit_ConvertSelectedCommandsFromComments_JMenuItem,false);
		JGUIUtil.setEnabled ( __CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem, false);
	}

	if ( (selected_commands_size >= 0) && (selected_commands_size != command_list_size) ) {
		// Less than all are selected so allow all to be selected.
		JGUIUtil.setEnabled ( __Edit_SelectAllCommands_JMenuItem,true);
		JGUIUtil.setEnabled (__CommandsPopup_SelectAll_JMenuItem,true);
	}
	else {
		JGUIUtil.setEnabled ( __Edit_SelectAllCommands_JMenuItem,false);
		JGUIUtil.setEnabled (__CommandsPopup_SelectAll_JMenuItem,false);
	}
	if ( selected_commands_size > 0 ) {
		// Some commands are selected so allow to deselect all.
		JGUIUtil.setEnabled (__Edit_DeselectAllCommands_JMenuItem,true);
		JGUIUtil.setEnabled(__CommandsPopup_DeselectAll_JMenuItem,true);
	}
	else {
		JGUIUtil.setEnabled(__Edit_DeselectAllCommands_JMenuItem,false);
		JGUIUtil.setEnabled(__CommandsPopup_DeselectAll_JMenuItem,false);
	}

	// View menu.

	if ( dataStoreListSize > 0 ) {
	    JGUIUtil.setEnabled ( __View_DataStores_JMenuItem, true );
	}
	else {
	    JGUIUtil.setEnabled ( __View_DataStores_JMenuItem, false );
	}
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		if ( __statecuDataset == null ) {
			JGUIUtil.setEnabled ( __View_DataSetManager_JCheckBoxMenuItem, false );
		}
		else {
			JGUIUtil.setEnabled ( __View_DataSetManager_JCheckBoxMenuItem, true );
		}
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		if ( __statemodDataset == null ) {
			JGUIUtil.setEnabled ( __View_DataSetManager_JCheckBoxMenuItem, false );
		}
		else {
			JGUIUtil.setEnabled ( __View_DataSetManager_JCheckBoxMenuItem, true );
		}
	}

	// Commands menu.

	// TODO - are there any cases where commands would not be enabled?
	JGUIUtil.setEnabled ( __Commands_JMenu, true );
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		ui_CheckGUIState_CommandsMenu_StateCU ();
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		ui_CheckGUIState_CommandsMenu_StateMod ();
	}

	// Run menu.

	ui_CheckGUIState_RunMenu ( command_list_size, selected_commands_size );

	// Results menu.

	// If the data set type is not known, disable the Get Data, Data, and
	// File...Save menus (check more specifically below).

	if ( (__appType == StateDMI.APP_TYPE_STATECU) && (__statecuDataset != null) ) {
		JGUIUtil.setEnabled ( __Results_JMenu, true );
		ui_CheckGUIState_ResultsMenu_StateCU ();
	}
	else if ((__appType == StateDMI.APP_TYPE_STATEMOD) && (__statemodDataset != null) ) {
		JGUIUtil.setEnabled ( __Results_JMenu, true );
		ui_CheckGUIState_ResultsMenu_StateMod ();
	}
	else {
		JGUIUtil.setEnabled ( __Results_JMenu, false );
	}

	// TODO - Disable menus until features are enabled.

	// Not sure if this will ever make sense.

	JGUIUtil.setEnabled ( __File_Open_DataSetComponent_JMenu, false );

	// Need to enable when there is time, especially for commands.

	JGUIUtil.setEnabled ( __File_New_JMenu, true);
	JGUIUtil.setEnabled ( __File_New_DataSet_JMenu, false);
	JGUIUtil.setEnabled ( __File_New_DataSetComponent_JMenu, false);

	// Not currently supported.

	JGUIUtil.setEnabled ( __File_Save_DataSet_JMenuItem, false );

	// StateCU.

	// Disable for now since the list file works.  Don't have a HUC list in memory.

	JGUIUtil.setEnabled (
		__Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_JMenuItem, false );

	// Disable menus whose commands have not been enabled.

	// StateMod..

	//JGUIUtil.setEnabled (__Commands_StateMod_SanJuanData_JMenuItem, false );
	//JGUIUtil.setEnabled (__Commands_StateMod_SanJuanSedimentRecoveryPlan_JMenu, false );
	JGUIUtil.setEnabled (__Commands_StateMod_SpatialData_JMenuItem, false );
	JGUIUtil.setEnabled ( __Commands_StateMod_GeoViewProject_JMenu, false );
}

/**
Check the GUI state for the StateMod Commands menu.  Each Commands sub-menu item is checked.
*/
private void ui_CheckGUIState_CommandsMenu_StateCU () {
	int selected_component_type = StateCU_DataSet.COMP_UNKNOWN;
	int selected_component_group_type=StateCU_DataSet.COMP_UNKNOWN;

	// True indicates that a commands file has been opened directly.
	boolean show_all_commands = false;
	if ( (__statecuDatasetType == StateCU_DataSet.TYPE_UNKNOWN) && (__statecuDataset == null) ) { // &&
		//(__commands_file_name != null) () {
		// User is editing commands directly without a data set.
		show_all_commands = true;
	}
	// Else rely on the data set type to enable/disable menus.

	// Get the selected component and selected component group.

	if ( __statecuSelectedComponent != null ) {
		selected_component_type = __statecuSelectedComponent.getComponentType();
		if ( !__statecuSelectedComponent.isGroup() ) {
			DataSetComponent cucomp = __statecuSelectedComponent.getParentComponent();
			if ( cucomp != null ) {
				selected_component_group_type =	cucomp.getComponentType();
			}
		}
	}

	// Climate stations.

	if ( show_all_commands ||
		(selected_component_type == StateCU_DataSet.COMP_CLIMATE_STATIONS_GROUP) ||
		(selected_component_group_type == StateCU_DataSet.COMP_CLIMATE_STATIONS_GROUP) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_ClimateStationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled (__Commands_StateCU_ClimateStationsData_JMenuItem, false );
	}
	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CLIMATE_STATIONS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_CLIMATE_STATIONS) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_ClimateStations_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_ClimateStations_JMenu, false );
	}

	// Crop characteristics menus.

	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CROP_CHARACTERISTICS_GROUP) ||
		(selected_component_group_type == StateCU_DataSet.COMP_CROP_CHARACTERISTICS_GROUP) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_CropCharacteristicsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_CropCharacteristicsData_JMenuItem, false );
	}
	if ( show_all_commands || (selected_component_group_type ==
		StateCU_DataSet.COMP_CROP_CHARACTERISTICS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_CROP_CHARACTERISTICS) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_CropCharacteristics_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_CropCharacteristics_JMenu, false );
	}
	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CROP_CHARACTERISTICS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_BLANEY_CRIDDLE) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_BlaneyCriddle_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_BlaneyCriddle_JMenu, false );
	}
	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CROP_CHARACTERISTICS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_PENMAN_MONTEITH) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_PenmanMonteith_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_PenmanMonteith_JMenu, false );
	}

	// CU Locations menus.

	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_CULocationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_CULocationsData_JMenuItem, false );
	}
	if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
		(selected_component_type == StateCU_DataSet.COMP_CU_LOCATIONS) ) {
		JGUIUtil.setEnabled ( __Commands_StateCU_CULocations_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_CULocations_JMenu, false );
	}

	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_STRUCTURES) ) {
		if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
			(selected_component_type == StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY) ){
			JGUIUtil.setEnabled ( __Commands_StateCU_CropPatternTS_JMenu, true );
		}
		else {
			JGUIUtil.setEnabled ( __Commands_StateCU_CropPatternTS_JMenu, false );
		}
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_CropPatternTS_JMenu, false );
	}

	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED) ) {
		if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
			(selected_component_type == StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY) ) {
			JGUIUtil.setEnabled ( __Commands_StateCU_IrrigationPracticeTS_JMenu, true );
		}
		else {
			JGUIUtil.setEnabled ( __Commands_StateCU_IrrigationPracticeTS_JMenu, false );
		}
		if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
			(selected_component_type == StateCU_DataSet.COMP_DIVERSION_TS_MONTHLY) ) {
			JGUIUtil.setEnabled ( __Commands_StateCU_DiversionTS_JMenuItem, true );
		}
		else {
			JGUIUtil.setEnabled ( __Commands_StateCU_DiversionTS_JMenuItem, false );
		}
		if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
			(selected_component_type == StateCU_DataSet.COMP_WELL_PUMPING_TS_MONTHLY) ) {
			JGUIUtil.setEnabled ( __Commands_StateCU_WellPumpingTS_JMenuItem, true );
		}
		else {
			JGUIUtil.setEnabled ( __Commands_StateCU_WellPumpingTS_JMenuItem, false );
		}
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_IrrigationPracticeTS_JMenu, false );
		JGUIUtil.setEnabled ( __Commands_StateCU_DiversionTS_JMenuItem, false );
		JGUIUtil.setEnabled ( __Commands_StateCU_WellPumpingTS_JMenuItem, false );
	}

	if ( show_all_commands || (__statecuDatasetType >=
		StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED_BY_WATER_RIGHTS) ) {
		if ( show_all_commands || (selected_component_group_type == StateCU_DataSet.COMP_CU_LOCATIONS_GROUP) ||
			(selected_component_type == StateCU_DataSet.COMP_DIVERSION_RIGHTS) ) {
			JGUIUtil.setEnabled ( __Commands_StateCU_DiversionRights_JMenuItem, true );
		}
		else {
			JGUIUtil.setEnabled ( __Commands_StateCU_DiversionRights_JMenuItem, false );
		}
	}
	else {
		JGUIUtil.setEnabled ( __Commands_StateCU_DiversionRights_JMenuItem, false );
	}

	if ( show_all_commands || (__statecuDataset != null) ) {
		JGUIUtil.setEnabled ( __Commands_General_Logging_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Commands_General_Logging_JMenu, false );
	}
}

/**
Check the GUI state for the StateMod Commands menu.  Each Commands sub-menu item is checked.
*/
private void ui_CheckGUIState_CommandsMenu_StateMod () {
	// TODO 2004-06-13 SAM - need to enable this similar to StateCU.

	boolean showAllCommands = true;
	if ( showAllCommands || (__statemodDataset != null) ) {
		showAllCommands = true;
	}
	else {
		showAllCommands = false;
	}
	//JGUIUtil.setEnabled ( __Commands_General_CheckingResults_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_Comments_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_FileHandling_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_HydroBase_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_Logging_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_Running_JMenu, showAllCommands );
	JGUIUtil.setEnabled ( __Commands_General_TestProcessing_JMenu, showAllCommands );
}

/**
Check the GUI state for the Results menu.  Each Results sub-menu item is checked.
*/
private void ui_CheckGUIState_ResultsMenu_StateCU () {
	// Control data (always disabled for now).

	JGUIUtil.setEnabled ( __Results_StateCU_ControlData_JMenuItem, false );

	// Climate stations data.

	boolean hasdata = false;
	if ( __statecuDataset.componentHasData(	StateCU_DataSet.COMP_CLIMATE_STATIONS) ) {
		hasdata = true;
	}
	if ( __statecuDataset.componentHasData(	StateCU_DataSet.COMP_TEMPERATURE_TS_MONTHLY_AVERAGE)){
		hasdata = true;
	}
	if ( __statecuDataset.componentHasData(	StateCU_DataSet.COMP_FROST_DATES_TS_YEARLY)){
		hasdata = true;
	}
	if ( __statecuDataset.componentHasData(	StateCU_DataSet.COMP_PRECIPITATION_TS_MONTHLY)){
		hasdata = true;
	}
	if ( hasdata ) {
		JGUIUtil.setEnabled ( __Results_StateCU_ClimateStationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Results_StateCU_ClimateStationsData_JMenuItem, false );
	}

	// Crop characteristics.

	hasdata = false;
	if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_CROP_CHARACTERISTICS) ) {
		hasdata = true;
	}
	if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_BLANEY_CRIDDLE) ) {
		hasdata = true;
	}
	if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_PENMAN_MONTEITH) ) {
		hasdata = true;
	}
	if ( hasdata ) {
		JGUIUtil.setEnabled ( __Results_StateCU_CropCharacteristicsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Results_StateCU_CropCharacteristicsData_JMenuItem, false );
	}

	// CU Locations.

	hasdata = false;
	if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_CU_LOCATIONS) ) {
		hasdata = true;
	}
	if ( __statecuDatasetType >= StateCU_DataSet.TYPE_STRUCTURES ) {
		if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY)){
			hasdata = true;
		}
	}
	if ( __statecuDatasetType >= StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED ) {
		if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY)){
			hasdata = true;
		}
	}
	if ( __statecuDatasetType >= StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED_BY_WATER_RIGHTS ) {
		if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_DIVERSION_TS_MONTHLY)){
			hasdata = true;
		}
		if ( __statecuDataset.componentHasData( StateCU_DataSet.COMP_DIVERSION_RIGHTS)){
			hasdata = true;
		}
	}

	if ( hasdata ) {
		JGUIUtil.setEnabled ( __Results_StateCU_CULocationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( __Results_StateCU_CULocationsData_JMenuItem, false );
	}
}

/**
Check the GUI state for the Results menu.  Each Results sub-menu item is checked.
*/
private void ui_CheckGUIState_ResultsMenu_StateMod () {
	// Enable the menu if output files are available.

	/* FIXME SAM 2009-02-24 Evaluate use.
	List results_files = __statedmiProcessor.getResultsFileList();
	if ( (results_files != null) && (results_files.size() > 0) ) {
		JGUIUtil.setEnabled ( __Results_JMenu, true );
	}
	else {
		JGUIUtil.setEnabled ( __Results_JMenu, false );
	}
	*/

	/* TODO SAM 2004-10-04 need to decide how to handle components.

	// Control data (always disabled for now).

	JGUIUtil.setEnabled ( __Results_StateCU_ControlData_JMenuItem, false );

	// Climate stations data.

	boolean hasdata = false;
	if ( __statecu_dataset.componentHasData(StateCU_DataSet.COMP_CLIMATE_STATIONS) ) {
		hasdata = true;
	}
	if ( __statecu_dataset.componentHasData(StateCU_DataSet.COMP_TEMPERATURE_TS_MONTHLY_AVERAGE)){
		hasdata = true;
	}
	if ( __statecu_dataset.componentHasData(StateCU_DataSet.COMP_FROST_DATES_TS_YEARLY)){
		hasdata = true;
	}
	if ( __statecu_dataset.componentHasData(StateCU_DataSet.COMP_PRECIPITATION_TS_MONTHLY)){
		hasdata = true;
	}
	if ( hasdata ) {
		JGUIUtil.setEnabled (__Results_StateCU_ClimateStationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled (__Results_StateCU_ClimateStationsData_JMenuItem, false );
	}

	// Crop characteristics.

	hasdata = false;
	if (__statecu_dataset.componentHasData(StateCU_DataSet.COMP_CROP_CHARACTERISTICS) ) {
		hasdata = true;
	}
	if (__statecu_dataset.componentHasData(StateCU_DataSet.COMP_BLANEY_CRIDDLE) ) {
		hasdata = true;
	}
	if (__statecu_dataset.componentHasData(StateCU_DataSet.COMP_PENMAN_MONTEITH) ) {
		hasdata = true;
	}
	if ( hasdata ) {
		JGUIUtil.setEnabled (__Results_StateCU_CropCharacteristicsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled (__Results_StateCU_CropCharacteristicsData_JMenuItem, false );
	}

	// CU Locations.

	hasdata = false;
	if (__statecu_dataset.componentHasData(StateCU_DataSet.COMP_CU_LOCATIONS) ) {
		hasdata = true;
	}
	if ( __statecu_dataset_type >= StateCU_DataSet.TYPE_STRUCTURES ) {
		if (__statecu_dataset.componentHasData(	StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY)){
			hasdata = true;
		}
	}
	if (__statecu_dataset_type >=StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED ) {
		if (__statecu_dataset.componentHasData(	StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY)){
			hasdata = true;
		}
	}
	if (__statecu_dataset_type >=StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED_BY_WATER_RIGHTS ) {
		if (__statecu_dataset.componentHasData(	StateCU_DataSet.COMP_DIVERSION_TS_MONTHLY)){
			hasdata = true;
		}
		if (__statecu_dataset.componentHasData(	StateCU_DataSet.COMP_DIVERSION_RIGHTS)){
			hasdata = true;
		}
	}
	if ( hasdata ) {
		JGUIUtil.setEnabled (__Results_StateCU_CULocationsData_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled (__Results_StateCU_CULocationsData_JMenuItem, false );
	}
*/
}

/**
Check the GUI state for the Run menu, enabling/disabling menus as appropriate.
@param command_list_size The size of the command list (0+).
@param selected_commands_size The number of commands that are selected.
*/
private void ui_CheckGUIState_RunMenu ( int command_list_size, int selected_commands_size ) {
	// If the final processor is running, allow it to be cancelled and only allow one to run at a time.
	// If commands are available to run, the run menus are enabled above so don't interfere with that.

	// "enable_run" indicates if run menus should be enabled, based on whether a run is already started.

	boolean enable_run = false;

	if ( (__statedmiProcessor != null) && __statedmiProcessor.getIsRunning() ) {
		// Running, so allow cancel but not another run.
		enable_run = false;
		JGUIUtil.setEnabled (__Run_CancelCommandProcessing_JMenuItem, true);
		JGUIUtil.setEnabled (__CommandsPopup_CancelCommandProcessing_JMenuItem,true);

	}
	else {
		// Not running, so disable cancel, but do allow run if there are commands (see below).
		enable_run = true;
		JGUIUtil.setEnabled (__Run_CancelCommandProcessing_JMenuItem, false);
		JGUIUtil.setEnabled (__CommandsPopup_CancelCommandProcessing_JMenuItem,false );
	}
	// Check the run flag below with combinations of commands, to set the state.
	if ( enable_run && (command_list_size > 0) ) {
		JGUIUtil.setEnabled (__Run_AllCommandsCreateOutput_JMenuItem, true);
		JGUIUtil.setEnabled (__CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem, true );
		JGUIUtil.setEnabled (__Run_AllCommandsIgnoreOutput_JMenuItem, true);
		JGUIUtil.setEnabled (__CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem,	true );
		JGUIUtil.setEnabled ( __Run_AllCommands_JButton, true);
	}
	if ( !enable_run || (command_list_size == 0) ) {
		JGUIUtil.setEnabled (__Run_AllCommandsCreateOutput_JMenuItem, false);
		JGUIUtil.setEnabled (__CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem,false );
		JGUIUtil.setEnabled (__Run_AllCommandsIgnoreOutput_JMenuItem, false);
		JGUIUtil.setEnabled (__CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem,	false );
		JGUIUtil.setEnabled ( __Run_AllCommands_JButton, false );
	}
	if ( enable_run && (selected_commands_size > 0) ) {
		JGUIUtil.setEnabled (__Run_SelectedCommandsCreateOutput_JMenuItem, true);
		JGUIUtil.setEnabled (__CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,true );
		JGUIUtil.setEnabled (__Run_SelectedCommandsIgnoreOutput_JMenuItem, true);
		JGUIUtil.setEnabled (__CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,true );
		JGUIUtil.setEnabled ( __Run_SelectedCommands_JButton, true );
	}
	if ( !enable_run || (selected_commands_size == 0) ) {
		JGUIUtil.setEnabled (__Run_SelectedCommandsCreateOutput_JMenuItem, false);
		JGUIUtil.setEnabled (__CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,false );
		JGUIUtil.setEnabled (__Run_SelectedCommandsIgnoreOutput_JMenuItem, false);
		JGUIUtil.setEnabled (__CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,false );
		JGUIUtil.setEnabled ( __Run_SelectedCommands_JButton, false );
	}
	if ( command_list_size == 0 ) {
		JGUIUtil.setEnabled ( __ClearCommands_JButton, false );
	}
	else {
		JGUIUtil.setEnabled ( __ClearCommands_JButton, true );
	}
}

/**
Populate the datastore list from available processor datastores.
*/
private void ui_DataStoreList_Populate () {
    __dataStore_JComboBox.removeAll();
    List<String> dataStoreNameList = new ArrayList<String>();
    dataStoreNameList.add ( "" ); // Blank when picking input type and name separately.
    // Get all enabled datastores, even those not active - the View ... Datastores menu can be used to show errors.
    List<DataStore> dataStoreList = __statedmiProcessor.getDataStores();
    for ( DataStore dataStore : dataStoreList ) {
        if ( dataStore.getClass().getName().endsWith(".NrcsAwdbDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisDailyDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisGroundwaterDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisInstantaneousDataStore") ) {
            // For now disable in the main browser since no interactive browsing ability has been implemented.
            // FIXME SAM 2012-10-26 For USGS enable when USGS site service is enabled.
            // FIXME SAM 2012-12-18 Enable with filter panel is developed specific to web services.
            continue;
        }
        else if ( dataStore.getClass().getName().endsWith(".GenericDatabaseDataStore") ) {
            // Only populate if configured for time series.
            GenericDatabaseDataStore ds = (GenericDatabaseDataStore)dataStore;
            if ( !ds.hasTimeSeriesInterface(true) ) {
                continue;
            }
        }
        String name = dataStore.getName();
        if ( dataStore.getStatus() != 0 ) {
        	// Show the user but make sure they know there is a problem so they avoid selecting.
        	name = name + " (ERROR)";
        }
        dataStoreNameList.add ( name );
    }
    __dataStore_JComboBox.setData(dataStoreNameList);
    // Select the blank.
    __dataStore_JComboBox.select("");
}

/**
Display the StateCU results in a record-based table.
@param componentName The name of the component to display.
*/
private void ui_DisplayResultsStateCUComponentTable ( String componentName ) {
	String routine = getClass().getSimpleName() + ".ui_DisplayResultsStateCUComponentTable";
	// List these in the order of the component groups.

	if ( (componentName == null) || (componentName.length() == 0) ) {
		return;
	}

	// Properties for the time series selector.

	PropList tsselector_props = new PropList ( "TSSelector" );
	tsselector_props.add ( "ActionButtons=Graph,Table,Summary" );
	tsselector_props.add ( "Width=1100" );
	tsselector_props.add ( "Height=500" );
	tsselector_props.setUsingObject ( "ParentUIComponent", this );

	try {
	StateCU_DataSet statecu_dataset = new StateCU_DataSet ();

	boolean editable = false;

	String titleString = IOUtil.getProgramName() + " - " + componentName;

	int app_type = StateDMI.APP_TYPE_STATECU;

	if (componentName.equals(statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CLIMATE_STATIONS))) {
		new StateCU_ClimateStation_Data_JFrame(this,
			__statedmiProcessor.getStateCUClimateStationList(),titleString, editable);
	}

	// Climate station time series are not handled by StateDMI.

	else if (componentName.equals(statecu_dataset.lookupComponentName(
		StateCU_DataSet.COMP_CROP_CHARACTERISTICS))) {
		new StateCU_CropCharacteristics_Data_JFrame(this,
			__statedmiProcessor.getStateCUCropCharacteristicsList(),titleString, editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_BLANEY_CRIDDLE))) {
		new StateCU_BlaneyCriddle_Data_JFrame(this,
			__statedmiProcessor.getStateCUBlaneyCriddleList(),titleString, editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_PENMAN_MONTEITH))) {
		new StateCU_PenmanMonteith_Data_JFrame(this, __statedmiProcessor.getStateCUPenmanMonteithList(),titleString, editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CU_LOCATIONS))) {
		new StateCU_Location_Data_JFrame(this, __statedmiProcessor.getStateCULocationList(),
			titleString, editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(
		StateCU_DataSet.COMP_CU_LOCATION_CLIMATE_STATIONS))) {
		new StateCU_Location_ClimateStation_Data_JFrame(this,
			__statedmiProcessor.getStateCULocationList(),titleString + " Climate Stations", editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(
		StateCU_DataSet.COMP_CU_LOCATION_COLLECTIONS))) {
		new StateCU_Location_Collection_Data_JFrame(this,
			__statedmiProcessor.getStateCULocationList(), titleString, editable);
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(
		StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			StateCU_CropPatternTS.toTSList(
			__statedmiProcessor.getStateCUCropPatternTSList(),
			true,		// Should totals for each location be added?
			true,		// Should a total for the entire data set be added?
			"DataSet",	// Base identifier for totals.
			"StateDMI"),	// Data source for totals.
			tsselector_props );
		// Manage the selector to process its actions.
		addTS_ListSelector_JFrame ( selector, app_type, StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY );
	}

	else if (componentName.equals(statecu_dataset.lookupComponentName(
		StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			StateCU_IrrigationPracticeTS.toTSList(
			__statedmiProcessor.getStateCUIrrigationPracticeTSList(),
			true,		// Should a total for the entire data set be added?
			"DataSet",	// Base identifier for totals.
			"StateDMI"),	// Data source for totals.
			tsselector_props );
		// Manage the selector to process its actions.
		addTS_ListSelector_JFrame ( selector, app_type, StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY );
	}

	// Intervening files are not handled by StateDMI.

	}
	catch ( Exception e ) {
		Message.printWarning ( 1, routine, "Error displaying results for \"" + componentName + "\" (" + e + ")." );
		Message.printWarning ( 2, routine, e );
	}
}

/**
Display the StateMod component results in a record-based table.
@param componentName The name of the component to display.
*/
private void ui_DisplayResultsStateModComponentTable ( String componentName ) {
	String routine = getClass().getSimpleName() + ".ui_DisplayResultsStateModComponentTable";
	// List these in the order of the component groups.

	if ( (componentName == null) || (componentName.length() == 0) ) {
		return;
	}

	// Properties for the time series selector.

	// TODO smalers 2019-06-30 Need to pass JFrame to something to center on StateDMI.
	PropList tsselector_props = new PropList ( "TSSelector" );
	tsselector_props.add ( "ActionButtons=Graph,Table,Summary" );
	tsselector_props.add ( "Width=1100" );
	tsselector_props.add ( "Height=500" );
	tsselector_props.setUsingObject ( "ParentUIComponent", this );

	try {
	StateMod_DataSet statemod_dataset = new StateMod_DataSet ();

	boolean editable = false;

	String titleString = IOUtil.getProgramName() + " - " + componentName;

	int app_type = StateDMI.APP_TYPE_STATEMOD;

	if (componentName.equals(statemod_dataset.lookupComponentName(
		StateMod_DataSet.COMP_STREAMGAGE_STATIONS))) {
		new StateMod_StreamGage_Data_JFrame( this,
			__statedmiProcessor.getStateModStreamGageStationList(), titleString, editable );
	}

	// Stream gage time series are not handled by StateDMI so use TSTool or other software to display.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DELAY_TABLES_MONTHLY))) {
		new StateMod_DelayTable_Data_JFrame( this,
			__statedmiProcessor.getStateModDelayTableList(TimeInterval.MONTH),
			titleString, true, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DELAY_TABLES_DAILY))) {
		new StateMod_DelayTable_Data_JFrame( this,
			__statedmiProcessor.getStateModDelayTableList(TimeInterval.DAY),
			titleString, false, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_STATIONS))) {
		new StateMod_Diversion_Data_JFrame( this,
			__statedmiProcessor.getStateModDiversionStationList(), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DIVERSION_STATION_DELAY_TABLES))){
		new StateMod_Diversion_DelayTableAssignment_Data_JFrame( this,
			__statedmiProcessor.getStateModDiversionStationList(),titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DIVERSION_STATION_COLLECTIONS))){
		new StateMod_Diversion_Collection_Data_JFrame( this,
			__statedmiProcessor.getStateModDiversionStationList(),titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DIVERSION_RIGHTS))) {
		new StateMod_DiversionRight_Data_JFrame(this,
			__statedmiProcessor.getStateModDiversionRightList(), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DIVERSION_TS_MONTHLY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModDiversionHistoricalTSMonthlyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_DIVERSION_TS_MONTHLY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_DIVERSION_TS_MONTHLY );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DIVERSION_TS_DAILY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModDiversionHistoricalTSDailyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_DIVERSION_TS_DAILY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_DIVERSION_TS_DAILY );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DEMAND_TS_MONTHLY))) {
		// TODO SAM 2005-03-29 This does not include a total time series.  Need to enable.
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModDiversionDemandTSMonthlyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_DEMAND_TS_MONTHLY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_DEMAND_TS_MONTHLY );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_DEMAND_TS_DAILY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModDiversionDemandTSDailyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_DEMAND_TS_DAILY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_DEMAND_TS_DAILY );
	}

	// The remaining diversion files are not currently handled by StateDMI.

	// Precipitation time series are not currently handled by StateDMI.

	// Evaporation time series are not currently handled by StateDMI.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_STATIONS))) {
		new StateMod_Reservoir_Data_JFrame( this,
			__statedmiProcessor.getStateModReservoirStationList(), titleString, editable);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_STATION_ACCOUNTS))){
		new StateMod_ReservoirAccount_Data_JFrame( this,
			StateMod_ReservoirAccount_Data_JFrame.createDataList(
			__statedmiProcessor.getStateModReservoirStationList()), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName(
		StateMod_DataSet.COMP_RESERVOIR_STATION_PRECIP_STATIONS))){
		boolean isPrecip = true; // Precipitation stations.
		new StateMod_ReservoirClimate_Data_JFrame( this,
			StateMod_ReservoirClimate_Data_JFrame.createDataList(
				__statedmiProcessor.getStateModReservoirStationList(),isPrecip), titleString, editable, true );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_STATION_EVAP_STATIONS))){
		boolean isPrecip = false; // Evaporation stations.
		new StateMod_ReservoirClimate_Data_JFrame( this,
			StateMod_ReservoirClimate_Data_JFrame.createDataList(
				__statedmiProcessor.getStateModReservoirStationList(),isPrecip), titleString, editable, false );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_STATION_CURVE))){
		new StateMod_ReservoirAreaCap_Data_JFrame( this,
			StateMod_ReservoirAreaCap_Data_JFrame.createDataList(
				__statedmiProcessor.getStateModReservoirStationList()), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_STATION_COLLECTIONS))){
		new StateMod_Reservoir_Collection_Data_JFrame( this,
			__statedmiProcessor.getStateModReservoirStationList(), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_RIGHTS))) {
		new StateMod_ReservoirRight_Data_JFrame(this,
			__statedmiProcessor.getStateModReservoirRightList(), titleString, editable);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_RESERVOIR_RETURN))) {
		new StateMod_Reservoir_Return_Data_JFrame( this,
			__statedmiProcessor.getStateModReservoirReturnList(), titleString, editable );
	}

	// Reservoir time series are not currently handled by StateDMI.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_INSTREAM_STATIONS))) {
		new StateMod_InstreamFlow_Data_JFrame( this,
			__statedmiProcessor.getStateModInstreamFlowStationList(), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_INSTREAM_RIGHTS))) {
		new StateMod_InstreamFlowRight_Data_JFrame( this,
			__statedmiProcessor.getStateModInstreamFlowRightList(), titleString, editable  );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_INSTREAM_DEMAND_TS_AVERAGE_MONTHLY))) {
		// Do not include a total since not consumptive.
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			__statedmiProcessor.getStateModInstreamFlowDemandTSAverageMonthlyList(),
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type,
			StateMod_DataSet.COMP_INSTREAM_DEMAND_TS_AVERAGE_MONTHLY );
	}

	// The remaining instream flow demand time series files are not handled by StateDMI.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_STATIONS))) {
		new StateMod_Well_Data_JFrame( this,
			__statedmiProcessor.getStateModWellStationList(), titleString, editable );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_STATION_DELAY_TABLES))){
		new StateMod_Well_DelayTableAssignment_Data_JFrame( this,
			__statedmiProcessor.getStateModWellStationList(), titleString, editable, false);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_STATION_DEPLETION_TABLES))){
		new StateMod_Well_DelayTableAssignment_Data_JFrame( this,
			__statedmiProcessor.getStateModWellStationList(), titleString, editable, true);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_STATION_COLLECTIONS))){
		new StateMod_Well_Collection_Data_JFrame( this,
			__statedmiProcessor.getStateModWellStationList(), titleString, editable);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_RIGHTS))) {
		new StateMod_WellRight_Data_JFrame( this,
			__statedmiProcessor.getStateModWellRightList(), titleString, editable);
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_WELL_PUMPING_TS_MONTHLY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModWellHistoricalPumpingTSMonthlyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_WELL_PUMPING_TS_MONTHLY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_WELL_PUMPING_TS_MONTHLY );
	}

	else if (componentName.equals(
		statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_DEMAND_TS_MONTHLY))) {
		TS_ListSelector_JFrame selector = new TS_ListSelector_JFrame (
			results_CopyTSListAndAddTotal (
				__statedmiProcessor.getStateModWellDemandTSMonthlyList(),
				StateDMI.APP_TYPE_STATEMOD,
				StateMod_DataSet.COMP_WELL_DEMAND_TS_MONTHLY,
				"DataSet",
				"StateDMI",
				"" ),	// Use default description.
			tsselector_props );
		addTS_ListSelector_JFrame ( selector, app_type, StateMod_DataSet.COMP_WELL_DEMAND_TS_MONTHLY );
	}

	// Other well time series are currently not handled by StateDMI.

	if (componentName.equals(statemod_dataset.lookupComponentName(
		StateMod_DataSet.COMP_STREAMESTIMATE_STATIONS))) {
		new StateMod_StreamEstimate_Data_JFrame( this,
			__statedmiProcessor.getStateModStreamEstimateStationList(), titleString, editable );
	}

	if (componentName.equals(statemod_dataset.lookupComponentName(
		StateMod_DataSet.COMP_STREAMESTIMATE_COEFFICIENTS))) {
		new StateMod_StreamEstimateCoefficients_Data_JFrame( this,
			__statedmiProcessor.getStateModStreamEstimateCoefficientsList(), titleString, editable );
	}

	// Plan stations.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_PLANS))) {
		new StateMod_Plan_Data_JFrame( this,
			__statedmiProcessor.getStateModPlanStationList(), titleString, editable );
	}

	// Plan well augmentation.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_PLAN_WELL_AUGMENTATION))) {
		new StateMod_Plan_WellAugmentation_Data_JFrame( this,
			__statedmiProcessor.getStateModPlanWellAugmentationList(), titleString, editable );
	}

	// Plan return.

	else if (componentName.equals(
		statemod_dataset.lookupComponentName( StateMod_DataSet.COMP_PLAN_RETURN))) {
		new StateMod_Plan_Return_Data_JFrame( this,
			__statedmiProcessor.getStateModPlanReturnList(), titleString, editable );
	}

	// Stream estimate time series are not handled by StateDMI so use TSTool or other software to display.

	if (componentName.equals(statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RIVER_NETWORK))) {
		new StateMod_RiverNetworkNode_Data_JFrame( this,
			__statedmiProcessor.getStateModRiverNetworkNodeList(), titleString);
	}

	// Operational rights (list the first card).

	if (componentName.equals(statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_OPERATION_RIGHTS))) {
		new StateMod_OperationalRight_Data_JFrame( this,
			__statedmiProcessor.getStateModOperationalRightList(), titleString, editable);
	}

	// The remaining files are currently not handled by StateDMI.

	}
	catch ( Exception e ) {
		Message.printWarning ( 1, routine, "Error displaying results for \"" + componentName + "\" (" + e + ")." );
		Message.printWarning ( 3, routine, e );
	}
}

/**
Return the command list component.  Do it this way because the command component may evolve.
*/
private JList ui_GetCommandJList() {
    return __commands_AnnotatedCommandJList.getJList();
}

/**
Return the directory for the last "File...Open Command File".
*/
private String ui_GetDir_LastCommandFileOpened() {
    String routine = getClass().getSimpleName() + ".ui_GetDir_LastCommandFileOpened";
	if ( __Dir_LastCommandFileOpened != null ) {
	    Message.printStatus ( 2, routine,
	        "Returning last (non null) command file directory: " + __Dir_LastCommandFileOpened );
	    return __Dir_LastCommandFileOpened;
	}

	// Try to get the generic dialog selection location.
	__Dir_LastCommandFileOpened = JGUIUtil.getLastFileDialogDirectory();
    if ( __Dir_LastCommandFileOpened != null ) {
        Message.printStatus ( 2, routine,
            "Returning last command file directory from last dialog selection: " + __Dir_LastCommandFileOpened );
        return __Dir_LastCommandFileOpened;
    }
	// This will check user.dir.
	__Dir_LastCommandFileOpened = IOUtil.getProgramWorkingDir ();
	Message.printStatus ( 2, routine,
        "Returning last command file directory from working directory: " + __Dir_LastCommandFileOpened );
	return __Dir_LastCommandFileOpened;
}

/**
Return whether ActionEvents should be ignored.
*/
private boolean ui_GetIgnoreActionEvent() {
	return __ignoreActionEvent;
}

/**
Return whether ItemEvents should be ignored.
*/
private boolean ui_GetIgnoreItemEvent() {
	return __ignoreItemEvent;
}

/**
Return whether ListSelectionEvents should be ignored.
*/
private boolean ui_GetIgnoreListSelectionEvent() {
	return __ignoreListSelectionEvent;
}

//FIXME SAM 2007-11-01 Need to use /tmp etc for a startup home if not specified so the software install home is not used.
/**
Return the initial working directory, which will be the software startup home, or the location of new command files.
This directory is suitable for initializing a workflow processing run.
@return the initial working directory, which should always be non-null.
*/
private String ui_GetInitialWorkingDir () {
	return __initialWorkingDir;
}

/**
Get a PropList with properties needed for an old-style editor.
Mainly this is the WorkingDir property, with a value determined from the initial working directory
and subsequent setWorkingDir() commands prior to the command being edited.
This is needed because old style editors get the information from a PropList that is passed to the editor.
@param command_to_edit Command that is being edited.
@return the PropList containing a valid WorkingDir value, accurate at for the context
of the command being edited.
*/
private PropList ui_GetPropertiesForOldStyleEditor ( Command command_to_edit ) {
	PropList props = new PropList ( "" );
	props.set ( "WorkingDir", commandProcessor_GetWorkingDirForCommand ( command_to_edit ) );
	return props;
}

/**
Initialize GUI components including menus and the main interfaces.
*/
private void ui_InitGUI () {
	String routine = getClass().getSimpleName() + ".ui_InitGUI";
	int initial_height = 900, initial_width = 1000;
	int y;

	JGUIUtil.setIcon(this, JGUIUtil.getIconImage());

	try {
		UIManager.setLookAndFeel( "com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
	}
	catch (Exception e) {
		Message.printStatus ( 2, routine, e.toString() );
	}

	// Set the help viewer handler, which is used to format a URL for command help.
	HelpViewer.getInstance().setUrlFormatter(this);

	JGUIUtil.setIcon(this, JGUIUtil.getIconImage());

	JPanel query_JPanel = new JPanel();
    query_JPanel.setLayout(new BorderLayout());
    getContentPane().add("North", query_JPanel);

	// Objects used throughout the GUI layout.
	int buffer = 3;
	Insets insetsNLNR = new Insets(0,buffer,0,buffer);
	Insets insetsNNNR = new Insets(0,0,0,buffer);
	Insets insetsNLNN = new Insets(0,buffer,0,0);
	//Insets insetsNLBR = new Insets(0,buffer,buffer,buffer);
	//Insets insetsTLNR = new Insets(buffer,buffer,0,buffer);
	Insets insetsNNNN = new Insets(0,0,0,0);
	GridBagLayout gbl = new GridBagLayout();

	__queryInput_JPanel = new JPanel();
	__queryInput_JPanel.setLayout(gbl);
	ui_SetInputPanelTitle (null, Color.black );

    query_JPanel.add("West", __queryInput_JPanel);

    y=-1;

	__dataStore_JTabbedPane = new JTabbedPane ();
    __dataStore_JTabbedPane.setVisible(false); // Let the initializing panel show first.
    JGUIUtil.addComponent(__queryInput_JPanel, __dataStore_JTabbedPane,
        0, ++y, 2, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);
    // The following will display during startup to wait for datastores to initialize, and will then be set not visible.
    JPanel __dataStoreInitializing_JPanel = new JPanel();
    __dataStoreInitializing_JPanel.setLayout(gbl);
    __dataStoreInitializing_JLabel = new JLabel("<html><b>Wait...initializing data connections...</html>");
    JGUIUtil.addComponent(__dataStoreInitializing_JPanel, __dataStoreInitializing_JLabel,
        0, 0, 1, 2, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    // Add at same location and __dataStore_JTabbedPane, which is not visible at start.
    JGUIUtil.addComponent(__queryInput_JPanel, __dataStoreInitializing_JPanel,
        0, y, 2, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);

    JPanel dataStore_JPanel = new JPanel();
    dataStore_JPanel.setLayout(gbl);
    int yDataStore = -1;
    __dataStore_JLabel = new JLabel("Datastore:");
    JGUIUtil.addComponent(dataStore_JPanel, __dataStore_JLabel,
        0, ++yDataStore, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
    __dataStore_JComboBox = new SimpleJComboBox(false);
    __dataStore_JComboBox.setMaximumRowCount ( 20 );
    String tooltip = "<html>Configured database and web service datastores <b>with no errors</b> - select a datastore OR input type.  See View...Datastores for status.</html>";
    __dataStore_JLabel.setToolTipText(tooltip);
    __dataStore_JComboBox.setToolTipText ( tooltip );
    __dataStore_JComboBox.addItemListener( this );
    JGUIUtil.addComponent(dataStore_JPanel, __dataStore_JComboBox,
        1, yDataStore, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    __dataStore_JTabbedPane.addTab ( "Datastore", dataStore_JPanel );

	// Add the menus.

	__JMenuBar = new JMenuBar();
	setJMenuBar ( __JMenuBar );

	ui_InitGUIMenus_File ( __JMenuBar );
	ui_InitGUIMenus_Edit ( __JMenuBar );
	ui_InitGUIMenus_View ( __JMenuBar );
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		ui_InitGUIMenus_Commands_StateCU ( __JMenuBar, menu_style );
		ui_InitGUIMenus_Commands_Table( __JMenuBar, menu_style );
		ui_InitGUIMenus_Run ( __JMenuBar );
		ui_InitGUIMenus_Results_StateCU ( __JMenuBar );
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		ui_InitGUIMenus_Commands_StateMod ( __JMenuBar, menu_style );
		ui_InitGUIMenus_Run ( __JMenuBar );
		ui_InitGUIMenus_Results_StateMod ( __JMenuBar );
	}
	ui_InitGUIMenus_Tools ( __JMenuBar );
	ui_InitGUIMenus_Help ( __JMenuBar );

	// Add a panel to the center of the JFrame.
	// The center panel is typically the only one that will resize and therefore needs to contain the resizable lists.
	// The layout of the panel is as follows (total grid bag width = 10).
	// JSplitPane use is envisioned where there are double lines.
	// To do this the command list and the label for commands are in one panel.
	//
	// The top is shown only if data set is displayed (default is do not).
	// +-----------++----------------++----------------------------------+
	// | Data Set  ||  Network tree  ||Data set component as list        |
	// | Component ||                ||                                  |
	// | List      ||                ||                                  |
	// |           ||                ||                                  |
	// |           ||                ||                                  |
	// |           ||                ||                                  |
	// |           ||                ||                                  |
	// +=================================================================+
	// | Commands list (JList - 10 wide)                                 |
	// +=================================================================+
	// | Results                                                         |
	// +-----------------------------------------------------------------+


	// Create the toolbar.

	__toolBar = new JToolBar("StateDMI Control Buttons");

	URL url = this.getClass().getResource( __RESOURCE_PATH + "/icon_newFile.gif" );
	String New_CommandFile_String = "New command file";

	if (url != null) {
		__toolBarNewButton = new SimpleJButton(new ImageIcon(url),
			New_CommandFile_String,
			New_CommandFile_String,
			insetsNNNN, false, this);
	}
	else {
		// Add text-labeled tools.
		__toolBarNewButton = new SimpleJButton(
			New_CommandFile_String,
			New_CommandFile_String,
			New_CommandFile_String,
			insetsNNNN, false, this);
	}

	if ( __toolBarNewButton != null ) {
		// Might be null if no files are found.
		__toolBar.add(__toolBarNewButton);
	}

	url = this.getClass().getResource( __RESOURCE_PATH + "/icon_openFile.gif");
	String Open_CommandFile_String = "Open command file";
	if (url != null) {
		__toolBarOpenButton = new SimpleJButton(new ImageIcon(url),
			Open_CommandFile_String,
			Open_CommandFile_String,
			insetsNNNN, false, this);
	}
	else {
		__toolBarOpenButton = new SimpleJButton(
			Open_CommandFile_String,
			Open_CommandFile_String,
			Open_CommandFile_String,
			insetsNNNN, false, this);
	}

	if ( __toolBarOpenButton != null ) {
		// Might be null if no files are found.
		__toolBar.add(__toolBarOpenButton);
	}

	url = this.getClass().getResource( __RESOURCE_PATH + "/icon_saveFile.gif");
	String Save_CommandFile_String = "Save command file";
	if (url != null) {
		__toolBarSaveButton = new SimpleJButton(new ImageIcon(url),
			Save_CommandFile_String,
			Save_CommandFile_String,
			insetsNNNN, false, this);
	}
	else {
		__toolBarSaveButton = new SimpleJButton(
			Save_CommandFile_String,
			Save_CommandFile_String,
			Save_CommandFile_String,
			insetsNNNN, false, this);
	}
	if ( __toolBarSaveButton != null ) {
		// Might be null if no files are found.
		__toolBar.add(__toolBarSaveButton);
	}

	JPanel center_JPanel = new JPanel();
	center_JPanel.setLayout (gbl);
	getContentPane().add ("Center", center_JPanel);
	getContentPane().add ("North", __toolBar);

	JSplitPane top_JSplitPane = null;
	if ( __datasetFeaturesEnabled ) {
		JPanel dataset_JPanel = new JPanel();
		dataset_JPanel.setLayout ( gbl );
		dataset_JPanel.setBorder( BorderFactory.createTitledBorder (
			BorderFactory.createLineBorder(Color.black),
			"Data Set Components (Primary Component Listed First)") );
		Dimension dimension = new Dimension( initial_width/2,
			(int)(initial_height*__LAYOUT_COMPONENTS_FRACTION));
		dataset_JPanel.setPreferredSize( dimension );
		// Allow zero minimum?
		//dataset_JPanel.setMinimumSize( dimension );

		JScrollPane dataset_tree_JScrollPane = null;
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			__statecuDataset_JTree = new StateCU_DataSet_JTree ( this, false );
			__statecuDataset_JTree.addTreeSelectionListener(this);
			dataset_tree_JScrollPane = new JScrollPane ( __statecuDataset_JTree );
			JGUIUtil.addComponent(dataset_JPanel,dataset_tree_JScrollPane,
				0, 0, 1, 1, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);
		}
		else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
			__statemodDataset_JTree = new StateMod_DataSet_JTree ( this, false, false );
			__statemodDataset_JTree.addTreeSelectionListener(this);
			dataset_tree_JScrollPane = new JScrollPane ( __statemodDataset_JTree );
			JGUIUtil.addComponent(dataset_JPanel,
				dataset_tree_JScrollPane,
				0, 0, 1, 1, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);
		}

		//Dimension minimum_Dimension = new Dimension( 300, 100 );
		//topsplit_JPanel.setMinimumSize( minimum_Dimension );

		// Top-right Data Component List

		__list_JPanel = new JPanel();
		__list_JPanel.setLayout ( gbl );
		__list_JPanel.setBorder(
			BorderFactory.createTitledBorder (BorderFactory.createLineBorder(Color.black),"List") );
		PropList props = new PropList ( "List" );
		props.add ( "JWorksheet.ShowRowHeader=true" );
		__list_JWorksheet = new JWorksheet ( 0, 0, props );
		__list_JWorksheet.setPreferredScrollableViewportSize(null);
	        JGUIUtil.addComponent(__list_JPanel,
			new JScrollPane(__list_JWorksheet),
			0, 0, 1, 1, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.WEST);

		top_JSplitPane = new JSplitPane ( JSplitPane.HORIZONTAL_SPLIT, dataset_JPanel, __list_JPanel);
		top_JSplitPane.setDividerLocation ( .50 );
	}
	else {
		top_JSplitPane = new JSplitPane ( JSplitPane.HORIZONTAL_SPLIT, new JPanel(), new JPanel());
		top_JSplitPane.setDividerLocation ( .50 );
		top_JSplitPane.setVisible(false);
	}

	// Command list.

    // Commands JPanel - 8 columns wide for grid bag layout.
	__commands_JPanel = new JPanel();
    __commands_JPanel.setLayout(gbl);
	__commands_JPanel.setBorder(
		BorderFactory.createTitledBorder (BorderFactory.createLineBorder(Color.black), "Commands" ));
	Dimension dimension = new Dimension( initial_width,(int)(initial_height*__LAYOUT_COMMANDS_FRACTION) );
	__commands_JPanel.setPreferredSize( dimension );
	dimension = new Dimension( 0, (int)(initial_height*__LAYOUT_COMMANDS_FRACTION));
	__commands_JPanel.setMinimumSize( dimension );

	// Initialize the command processor to interact with the GUI.
	__statedmiProcessor = new StateDMI_Processor();
	commandProcessor_SetInitialWorkingDir ( __initialWorkingDir );
	__statedmiProcessor.addCommandProcessorListener ( this );
	__commands_JListModel = new StateDMI_Processor_ListModel(__statedmiProcessor);
	__commands_JListModel.addListDataListener ( this );
	__commands_AnnotatedCommandJList = new AnnotatedCommandJList ( __commands_JListModel );
	__commands_JList = __commands_AnnotatedCommandJList.getJList();
	// Set the font to fixed font so that similar command text lines up.
	__commands_JList.setFont ( new Font(__COMMANDS_FONT, Font.PLAIN, 12 ) );
	// The following prototype value looks like nonsense,
	// but should ensure that the line height accommodates both very tall characters, and those that swoop below the line.
	//__commands_JList.setPrototypeCellValue("gjqqyAZ");
	// FIXME SAM 2008-01-25 Is the above needed?
	// Handling the ellipsis is dealt with in the annotated list.

	Dimension minimum_Dimension = new Dimension( 300, 100 );
	__commands_JList.setMinimumSize( minimum_Dimension );
	__commands_JList.addListSelectionListener(this);
	__commands_JList.addMouseListener(this);
	__commands_JList.addKeyListener(this);

	JGUIUtil.addComponent(__commands_JPanel, __commands_AnnotatedCommandJList,
		0, 1, 10, 3, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER );

	// Buttons that correspond to the command list.

	// Put on left because user is typically working in that area.
	__Run_SelectedCommands_JButton = new SimpleJButton(__Button_RunSelectedCommands_String,
		__Run_SelectedCommandsCreateOutput_String, this);
	__Run_SelectedCommands_JButton.setToolTipText ( "Run only selected commands to produce results." );
	JGUIUtil.addComponent(__commands_JPanel, __Run_SelectedCommands_JButton,
		1, 5, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
	__Run_AllCommands_JButton = new SimpleJButton(__Button_RunAllCommands_String,__Run_AllCommandsCreateOutput_String, this);
	__Run_AllCommands_JButton.setToolTipText ( "Run all commands to produce results." );
	JGUIUtil.addComponent(__commands_JPanel, __Run_AllCommands_JButton,
		2, 5, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
	// Put on right because we want it to be a decision to clear.
	__ClearCommands_JButton = new SimpleJButton( __Button_ClearCommands_String, this);
	__ClearCommands_JButton.setToolTipText ( "Delete selected commands, or delete all if none are selected." );
	JGUIUtil.addComponent(__commands_JPanel, __ClearCommands_JButton,
		9, 5, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);

	JSplitPane top2_JSplitPane = new JSplitPane ( JSplitPane.VERTICAL_SPLIT, top_JSplitPane, __commands_JPanel);
	top2_JSplitPane.setDividerLocation ( .50 );

	ui_InitGUIMenus_CommandsPopup ();

	// Results.

	JPanel results_tree_JPanel = new JPanel();
	results_tree_JPanel.setLayout ( gbl );
	// TODO SAM 2004-02-19 See if the other panels' sizes initialize without this.
	//dimension = new Dimension( initial_width, initial_height/3);
	//results_tree_JPanel.setPreferredSize( dimension );

	// FIXME SAM 2008-11-11 Evaluate whether to use.
	/*
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		__statecuResults_JTree = new StateCU_DataSet_JTree ( this, true );
		JScrollPane results_tree_JScrollPane = new JScrollPane ( __statecuResults_JTree );
		JGUIUtil.addComponent(results_tree_JPanel,
			results_tree_JScrollPane,
			0, 0, 1, 1, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		__statemodResults_JTree = new StateMod_DataSet_JTree ( this, true, false );
		JScrollPane results_tree_JScrollPane = new JScrollPane ( __statemodResults_JTree );
		JGUIUtil.addComponent(results_tree_JPanel,
			results_tree_JScrollPane,
			0, 0, 1, 1, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);
	}
	*/

	/* TODO SAM 2008-11-13 Evaluate whether needed.
	JPanel results_JPanel = new JPanel();
	results_JPanel.setLayout ( gbl );
	results_JPanel.setBorder(
		BorderFactory.createTitledBorder (BorderFactory.createLineBorder(Color.black),"Results") );
	*/

	__results_JTabbedPane = new JTabbedPane ();
    __results_JTabbedPane.setBorder(
        BorderFactory.createTitledBorder ( BorderFactory.createLineBorder(Color.black), "Results" ));
    JGUIUtil.addComponent(center_JPanel, __results_JTabbedPane,
        0, 1, 1, 1, 1.0, 1.0, insetsNNNN, GridBagConstraints.BOTH, GridBagConstraints.CENTER);

	// Results - output files.

    JPanel results_files_JPanel = new JPanel();
    results_files_JPanel.setLayout(gbl);
    JGUIUtil.addComponent(center_JPanel, results_files_JPanel,
        0, 3, 1, 1, 1.0, 0.0, insetsNNNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
    __resultsOutputFiles_JListModel = new DefaultListModel();
    __resultsOutputFiles_JList = new JList ( __resultsOutputFiles_JListModel );
    __resultsOutputFiles_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    __resultsOutputFiles_JList.addKeyListener ( this );
    __resultsOutputFiles_JList.addListSelectionListener ( this );
    __resultsOutputFiles_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_files_JPanel, new JScrollPane ( __resultsOutputFiles_JList ),
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "Output Files", results_files_JPanel );

	// Results - problems.

    JPanel results_problems_JPanel = new JPanel();
    results_problems_JPanel.setLayout(gbl);
    CommandLog_TableModel tableModel = null;
    try {
    	tableModel = new CommandLog_TableModel(new ArrayList<CommandLogRecord>());
    }
    catch ( Exception e ) {
    	// Should not happen but log.
    	Message.printWarning ( 3, routine, e );
    	Message.printWarning(3, routine, "Error creating table model for problem display.");
    	throw new RuntimeException ( e );
    }
	CommandLog_CellRenderer cellRenderer = new CommandLog_CellRenderer(tableModel);
	PropList commandStatusProps = new PropList ( "Problems" );
	commandStatusProps.add("JWorksheet.ShowRowHeader=true");
	commandStatusProps.add("JWorksheet.AllowCopy=true");
	// Initialize with null table model since no initial data.
	JScrollWorksheet sjw = new JScrollWorksheet ( cellRenderer, tableModel, commandStatusProps );
	__resultsProblems_JWorksheet = sjw.getJWorksheet ();
	__resultsProblems_JWorksheet.setColumnWidths (cellRenderer.getColumnWidths(), getGraphics() );
	__resultsProblems_JWorksheet.setPreferredScrollableViewportSize(null);
	// Listen for mouse events to?
	//__problems_JWorksheet.addMouseListener ( this );
	//__problems_JWorksheet.addJWorksheetListener ( this );
    JGUIUtil.addComponent(results_problems_JPanel, sjw,
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "Problems", results_problems_JPanel );

    // Results: properties.
    JPanel resultsProperties_JPanel = new JPanel();
    resultsProperties_JPanel.setLayout(gbl);
    PropList_TableModel propsTableModel = null;
    try {
        propsTableModel = new PropList_TableModel(new PropList("processor"),false,false);
        propsTableModel.setKeyColumnName("Property Name");
        propsTableModel.setValueColumnName("Property Value");
    }
    catch ( Exception e ) {
        // Should not happen but log.
        Message.printWarning ( 3, routine, e );
        Message.printWarning(3, routine, "Error creating table model for problem display.");
        throw new RuntimeException ( e );
    }
    PropList_CellRenderer propsCellRenderer = new PropList_CellRenderer(propsTableModel);
    PropList propsWsProps = new PropList ( "PropertiesWS" );
    propsWsProps.add("JWorksheet.ShowRowHeader=true");
    propsWsProps.add("JWorksheet.AllowCopy=true");
    // Initialize with null table model since no initial data.
    JScrollWorksheet psjw = new JScrollWorksheet ( propsCellRenderer, propsTableModel, propsWsProps );
    __resultsProperties_JWorksheet = psjw.getJWorksheet ();
    __resultsProperties_JWorksheet.setColumnWidths (cellRenderer.getColumnWidths(), getGraphics() );
    __resultsProperties_JWorksheet.setPreferredScrollableViewportSize(null);
    // Listen for mouse events to?
    //__problems_JWorksheet.addMouseListener ( this );
    //__problems_JWorksheet.addJWorksheetListener ( this );
    JGUIUtil.addComponent(resultsProperties_JPanel, new JLabel("Processor properties control processing and can be used in " +
        "some command parameters using ${Property} notation (see command documentation)."),
        0, 0, 8, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    JGUIUtil.addComponent(resultsProperties_JPanel, psjw,
        0, 1, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "Properties", resultsProperties_JPanel );


	// Results StateCU output components.

    JPanel resultsStateCUComponents_JPanel = new JPanel();
    resultsStateCUComponents_JPanel.setLayout(gbl);
    __resultsStateCUComponents_JListModel = new DefaultListModel();
    __resultsStateCUComponents_JList = new JList ( __resultsStateCUComponents_JListModel );
    __resultsStateCUComponents_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    __resultsStateCUComponents_JList.addKeyListener ( this );
    __resultsStateCUComponents_JList.addListSelectionListener ( this );
    __resultsStateCUComponents_JList.addMouseListener ( this );
    JGUIUtil.addComponent(resultsStateCUComponents_JPanel, new JScrollPane ( __resultsStateCUComponents_JList ),
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "StateCU Components", resultsStateCUComponents_JPanel );

    JPanel resultsStateModComponents_JPanel = new JPanel();
    resultsStateModComponents_JPanel.setLayout(gbl);
    __resultsStateModComponents_JListModel = new DefaultListModel();
    __resultsStateModComponents_JList = new JList ( __resultsStateModComponents_JListModel );
    __resultsStateModComponents_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    __resultsStateModComponents_JList.addKeyListener ( this );
    __resultsStateModComponents_JList.addListSelectionListener ( this );
    __resultsStateModComponents_JList.addMouseListener ( this );
    JGUIUtil.addComponent(resultsStateModComponents_JPanel, new JScrollPane ( __resultsStateModComponents_JList ),
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "StateMod Components", resultsStateModComponents_JPanel );

    // Results: tables.

    JPanel results_tables_JPanel = new JPanel();
    results_tables_JPanel.setLayout(gbl);
    /*
    results_tables_JPanel.setBorder(
        BorderFactory.createTitledBorder (
        BorderFactory.createLineBorder(Color.black),
        "Results: Tables" ));
        */
    //JGUIUtil.addComponent(center_JPanel, results_tables_JPanel,
    //    0, 2, 1, 1, 1.0, 0.0, insetsNNNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
    JGUIUtil.addComponent(results_tables_JPanel, new JLabel ("Tables:"),
        0, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
    __resultsTables_JListModel = new DefaultListModel();
    __resultsTables_JList = new JList ( __resultsTables_JListModel );
    __resultsTables_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    __resultsTables_JList.addKeyListener ( this );
    __resultsTables_JList.addListSelectionListener ( this );
    __resultsTables_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_tables_JPanel, new JScrollPane ( __resultsTables_JList ),
        0, 15, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    __results_JTabbedPane.addTab ( "Tables", results_tables_JPanel );

	// Add the results JTree.

	/* TODO SAM 2008-11-12 Evaluate whether to use.
	JGUIUtil.addComponent(results_JPanel, results_tree_JPanel,
		0, 3, 10, 10, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);
		*/

	JSplitPane main_JSplitPane = null;
	if ( __datasetFeaturesEnabled ) {
		// Include the data set pane at the top.
		//main_JSplitPane = new JSplitPane ( JSplitPane.VERTICAL_SPLIT, top2_JSplitPane, results_JPanel);
		main_JSplitPane = new JSplitPane ( JSplitPane.VERTICAL_SPLIT, top2_JSplitPane, __results_JTabbedPane);
	}
	else {
		// Put commands in the top split pane and results in the bottom.
		//main_JSplitPane = new JSplitPane ( JSplitPane.VERTICAL_SPLIT, __commands_JPanel, results_JPanel);
		main_JSplitPane = new JSplitPane ( JSplitPane.VERTICAL_SPLIT, __commands_JPanel, __results_JTabbedPane);
	}
	JGUIUtil.addComponent(center_JPanel, main_JSplitPane,
		0, 0, 10, 10, 1.0, 1.0, GridBagConstraints.BOTH, GridBagConstraints.CENTER);

	// Popup menu for results.

	ui_InitGUIMenus_ResultsPopup ();

	// Bottom panel for the information TextFields.
	// Add this as the south panel of the main interface since it is not resizable.

	JPanel bottom_JPanel = new JPanel();
	bottom_JPanel.setLayout (gbl);

	__message_JTextField = new JTextField();
	__message_JTextField.setEditable(false);
	JGUIUtil.addComponent(bottom_JPanel, __message_JTextField,
		0, 0, 5, 1, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);

	__processor_JProgressBar = new JProgressBar ();
	__processor_JProgressBar.setToolTipText ( "Indicates progress in processing all commands.");
	__processor_JProgressBar.setStringPainted ( true );
	JGUIUtil.addComponent(bottom_JPanel, __processor_JProgressBar,
		5, 0, 2, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
	__command_JProgressBar = new JProgressBar ();
	__command_JProgressBar.setToolTipText ( "Indicates progress in processing the current command that is running.");
	__command_JProgressBar.setStringPainted ( true );
	JGUIUtil.addComponent(bottom_JPanel, __command_JProgressBar,
		7, 0, 2, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);

	__status_JTextField = new JTextField ( 5 );
	__status_JTextField.setToolTipText ( "Wait = StateDMI is processing commands, Ready = ready for user input." );
	__status_JTextField.setEditable(false);
	JGUIUtil.addComponent(bottom_JPanel, __status_JTextField,
		9, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);

	getContentPane().add ("South", bottom_JPanel);

	// Setup window listener.
	addWindowListener (this);

	if ( __datasetFeaturesEnabled ) {
		ui_UpdateStatusTextFields ( -1, "StateDMI_JFrame.initGUI",
			null, "Open/create a data set or command file.", __STATUS_READY );
	}
	else {
		ui_UpdateStatusTextFields ( -1, "StateDMI_JFrame.initGUI",
			null, "Open a command file or add new commands.", __STATUS_READY );
	}
	ui_UpdateStatus ( true );
	pack();
	setSize ( initial_width, initial_height );
	JGUIUtil.center (this);
	setVisible(true);
}

/**
Add Check[Component] and WriteCheckFile() commands to the specified menu.
These commands are similar for all data components.
@param menu the menu being appended to.
@param menuName the name of the menu displayed to the user and used internally.
*/
private void ui_InitGUIMenus_Commands_AddCheckCommands ( JMenu menu, String menuName ) {
	menu.addSeparator();
	menu.add ( new SimpleJMenuItem(menuName,this));
	menu.add ( new SimpleJMenuItem(__Commands_Shared_WriteCheckFile_String,this));
}

/**
Setup Commands menu for a component within a group (e.g., "Stream Gage Stations").
@param style the commands menu style (MENU_STYLE_THREE_LEVEL or MENU_STYLE_TWO_LEVEL).
@param parent_JMenu The JMenu that other menus will be added to.
@param group_String The string to be used for group menus (e.g., "Stream Gage Data").
@param component_String The string to be used for component menus (e.g., "Stream Gage Stations").
@param add_as_JMenuItem Indicates whether the top-level component menu should actually be added as a JMenuItem.
This will be the case if for some reason the component does not
have commands to run, and will be disabled or have a warning dialog pop up.
@return a JMenu that should be used for subsequent menu additions for a component,
or null if the item is added as JMenuItem (no subsequent sub-menus).
*/
private JMenu ui_InitGUIMenus_Commands_AddComponentMenu (
		int style,
		JMenu parent_JMenu,
		String group_String,
		String component_String,
		boolean add_as_JMenuItem ) {
	JMenu component_JMenu = null;
	if ( add_as_JMenuItem ) {
		parent_JMenu.add( new SimpleJMenuItem(component_String, this));
		return null;
	}
	if ( style == MENU_STYLE_THREE_LEVEL ) {
		// Add the level for the component (e.g., "Stream Gage Stations").
		parent_JMenu.add( component_JMenu = new JMenu (component_String,true));
	}
	else if ( style == MENU_STYLE_TWO_LEVEL ) {
		// Add the menu for "Group Data - Component" (e.g., "Stream Gage Data - Stream Gage Stations")
		String dash = " - ";
		parent_JMenu.addSeparator();
		parent_JMenu.add( component_JMenu = new JMenu (group_String + dash + component_String,true));
	}
	// Add menu item at the top, consistent for all styles.
	String dash = " - ";
	component_JMenu.add( new SimpleJMenuItem(
			// group_String + dash +     // Seems too long.
			"<HTML><B>" + component_String + dash + "Commands</B></HTML>", this));
	component_JMenu.addSeparator ();
	component_JMenu.addSeparator ();
	return component_JMenu;
}

/**
Setup Commands menu for a group (e.g., for stream gage data).
@param style the commands menu style (MENU_STYLE_THREE_LEVEL or MENU_STYLE_TWO_LEVEL).
@param parent_JMenu The JMenu that other menus will be added to.
@param group_String The string to be used for group menus (e.g., "Stream Gage Data").
@param add_as_JMenuItem Indicates whether the top-level group menu should actually be added
as a JMenuItem.  This will be the case if for some reason the component does not
have commands to run, and will be disabled or have a warning dialog pop up.
@return a JMenu that should be used for subsequent menu additions for a component,
or null if the item is added as JMenuItem (no subsequent sub-menus).
*/
private JMenu ui_InitGUIMenus_Commands_AddGroupMenu (
		int style,
		JMenu parent_JMenu,
		String group_String,
		boolean add_as_JMenuItem ) {
	if ( add_as_JMenuItem ) {
		parent_JMenu.add( new SimpleJMenuItem(group_String, this));
		return null;
	}
	JMenu group_JMenu = null;
	if ( style == MENU_STYLE_THREE_LEVEL ) {
		// Add the level for the group, e.g. "Stream Gage Data"
		parent_JMenu.add( group_JMenu =	new JMenu(group_String, true) );
	}
	else if ( style == MENU_STYLE_TWO_LEVEL ) {
		// The group and component are shown in the same menu when the component is added.
		group_JMenu = parent_JMenu;
	}
	return group_JMenu;
}

/**
Initialize the general command menus.  These can be used with StateMod or StateCU.
@param style Menu style (see MENU_STYLE_*).
@param parent_JMenu The JMenu to which submenus should be attached.
*/
private void ui_InitGUIMenus_Commands_General ( int style, JMenu parent_JMenu ) {
	parent_JMenu.addSeparator();
	parent_JMenu.addSeparator();

	// Commands - Datastore Processing.
	JMenu Commands_Datastore_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
			style, parent_JMenu, __Commands_Datastore_String, false);
	Commands_Datastore_JMenu.add(__Commands_TableRead_ReadTableFromDataStore_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromDataStore_String, this));

	parent_JMenu.addSeparator();

	// Commands - Output File Processing.
	JMenu Commands_Output_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
			style, parent_JMenu, __Commands_Output_String, false);
	Commands_Output_JMenu.add(__Commands_Output_SplitStateModReport_JMenuItem =
			new SimpleJMenuItem(__Commands_Output_SplitStateModReport_String, this));

	parent_JMenu.addSeparator();

	// Commands - Spatial Processing.
	JMenu Commands_Spatial_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
			style, parent_JMenu, __Commands_Spatial_String, false);
	Commands_Spatial_JMenu.add(__Commands_Spatial_WriteTableToGeoJSON_JMenuItem =
			new SimpleJMenuItem(__Commands_Spatial_WriteTableToGeoJSON_String, this));
	Commands_Spatial_JMenu.add(__Commands_Spatial_WriteTableToShapefile_JMenuItem =
			new SimpleJMenuItem(__Commands_Spatial_WriteTableToShapefile_String, this));

	parent_JMenu.addSeparator();

	// Commands - Spreadsheet Processing.

	JMenu Commands_Spreadsheet_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
			style, parent_JMenu, __Commands_Spreadsheet_String, false);
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_NewExcelWorkbook_JMenuItem =
			new SimpleJMenuItem(__Commands_Spreadsheet_NewExcelWorkbook_String, this));
	Commands_Spreadsheet_JMenu.addSeparator();
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_ReadExcelWorkbook_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_ReadExcelWorkbook_String, this ) );
	Commands_Spreadsheet_JMenu.addSeparator();
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_ReadTableFromExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_ReadTableFromExcel_String, this ) );
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_ReadTableCellsFromExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_ReadTableCellsFromExcel_String, this ) );
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_ReadPropertiesFromExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_ReadPropertiesFromExcel_String, this ) );
	Commands_Spreadsheet_JMenu.addSeparator();
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_SetExcelCell_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_SetExcelCell_String, this ) );
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_SetExcelWorksheetViewProperties_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_SetExcelWorksheetViewProperties_String, this ) );
	Commands_Spreadsheet_JMenu.addSeparator();
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_WriteTableToExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_WriteTableToExcel_String, this ) );
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_WriteTableCellsToExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_WriteTableCellsToExcel_String, this ) );
	/*Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_WriteTimeSeriesToExcel_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_WriteTimeSeriesToExcel_String, this ) );
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String, this ) );*/
	Commands_Spreadsheet_JMenu.addSeparator();
	Commands_Spreadsheet_JMenu.add( __Commands_Spreadsheet_CloseExcelWorkbook_JMenuItem =
	        new SimpleJMenuItem( __Commands_Spreadsheet_CloseExcelWorkbook_String, this ) );


	parent_JMenu.addSeparator();
	parent_JMenu.addSeparator();

	// General - Comments.

	JMenu Commands_General_Comments_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_Comments_String, false );
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_Comment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_Comment_String, this));
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_StartComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_StartComment_String, this));
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_EndComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_EndComment_String, this));
	Commands_General_Comments_JMenu.addSeparator();
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_ReadOnlyComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_ReadOnlyComment_String, this));
	Commands_General_Comments_JMenu.addSeparator();
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_EnabledComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_EnabledComment_String, this));
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_ExpectedStatusFailureComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_ExpectedStatusFailureComment_String, this));
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_ExpectedStatusWarningComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_ExpectedStatusWarningComment_String, this));
	Commands_General_Comments_JMenu.addSeparator();
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_RequireApplicationComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_RequireApplicationComment_String, this));
	Commands_General_Comments_JMenu.add( __Commands_General_Comments_RequireDatastoreComment_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Comments_RequireDatastoreComment_String, this));

	// General - File Handling.

	JMenu Commands_General_FileHandling_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_FileHandling_String, false );
	//Commands_General_Logging_JMenu.add( __Commands_General_FileHandling_FTPGet_JMenuItem =
	//	new SimpleJMenuItem( __Commands_General_FileHandling_FTPGet_String, this));
	Commands_General_FileHandling_JMenu.add( __Commands_General_FileHandling_FTPGet_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_FTPGet_String, this));
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_WebGet_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_WebGet_String, this));
	Commands_General_FileHandling_JMenu.addSeparator();
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_AppendFile_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_AppendFile_String, this));
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_CopyFile_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_CopyFile_String, this));
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_ListFiles_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_ListFiles_String, this));
	Commands_General_FileHandling_JMenu.add( __Commands_General_FileHandling_RemoveFile_JMenuItem =
		new SimpleJMenuItem( __Commands_General_FileHandling_RemoveFile_String, this));
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_MergeListFileColumns_JMenuItem =
		new SimpleJMenuItem(__Commands_General_FileHandling_MergeListFileColumns_String, this));
	Commands_General_FileHandling_JMenu.addSeparator();
	Commands_General_FileHandling_JMenu.add(__Commands_General_FileHandling_UnzipFile_JMenuItem =
			new SimpleJMenuItem(__Commands_General_FileHandling_UnzipFile_String, this));

	// General - HydroBase

	JMenu Commands_General_HydroBase_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_HydroBase_String, false );
	Commands_General_HydroBase_JMenu.add( __Commands_General_HydroBase_OpenHydroBase_JMenuItem =
		new SimpleJMenuItem( __Commands_General_HydroBase_OpenHydroBase_String, this));

	// General - Logging

	JMenu Commands_General_Logging_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_Logging_String, false );
	Commands_General_Logging_JMenu.add( __Commands_General_Logging_StartLog_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Logging_StartLog_String, this));
	Commands_General_Logging_JMenu.add( __Commands_General_Logging_SetDebugLevel_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Logging_SetDebugLevel_String, this));
	Commands_General_Logging_JMenu.add( __Commands_General_Logging_SetWarningLevel_JMenuItem =
		new SimpleJMenuItem ( __Commands_General_Logging_SetWarningLevel_String, this));
	Commands_General_Logging_JMenu.addSeparator();
	Commands_General_Logging_JMenu.add(__Commands_General_Logging_Message_JMenuItem =
			new SimpleJMenuItem(__Commands_General_Logging_Message_String, this));

	// General - Running

	JMenu Commands_General_Running_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_Running_String, false );
//	Commands_General_Running_JMenu.add( __Commands_General_Running_SetProperty_JMenuItem =
//		new SimpleJMenuItem( __Commands_General_Running_SetProperty_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_SetOutputPeriod_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_SetOutputPeriod_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_SetOutputYearType_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_SetOutputYearType_String, this));
	Commands_General_Running_JMenu.add(__Commands_General_Running_SetProperty_JMenuItem =
			new SimpleJMenuItem(__Commands_General_Running_SetProperty_String, this));
	Commands_General_Running_JMenu.add(__Commands_General_Running_FormatDateTimeProperty_JMenuItem =
			new SimpleJMenuItem(__Commands_General_Running_FormatDateTimeProperty_String, this));
	Commands_General_Running_JMenu.add(__Commands_General_Running_FormatStringProperty_JMenuItem =
			new SimpleJMenuItem(__Commands_General_Running_FormatStringProperty_String, this));
	Commands_General_Running_JMenu.addSeparator();
	Commands_General_Running_JMenu.add ( __Commands_General_Running_WritePropertiesToFile_JMenuItem =
	        new SimpleJMenuItem(__Commands_General_Running_WritePropertiesToFile_String, this ) );
	Commands_General_Running_JMenu.addSeparator();
	Commands_General_Running_JMenu.add( __Commands_General_Running_RunCommands_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_RunCommands_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_RunProgram_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_RunProgram_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_RunPython_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_RunPython_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_RunR_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_RunR_String, this));
	Commands_General_Running_JMenu.addSeparator();
	Commands_General_Running_JMenu.add( __Commands_General_Running_Exit_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_Exit_String, this));
	Commands_General_Running_JMenu.add( __Commands_General_Running_SetWorkingDir_JMenuItem =
		new SimpleJMenuItem( __Commands_General_Running_SetWorkingDir_String, this));

	// General - Test Processing...

	JMenu Commands_General_TestProcessing_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (
		style, parent_JMenu, __Commands_General_TestProcessing_String, false );
	Commands_General_TestProcessing_JMenu.add( __Commands_General_TestProcessing_CompareFiles_JMenuItem =
		new SimpleJMenuItem( __Commands_General_TestProcessing_CompareFiles_String, this));
	Commands_General_TestProcessing_JMenu.addSeparator();
	Commands_General_TestProcessing_JMenu.add( __Commands_General_TestProcessing_CompareFiles_JMenuItem =
		new SimpleJMenuItem ( __Commands_General_TestProcessing_CreateRegressionTestCommandFile_String, this));
	Commands_General_TestProcessing_JMenu.add( __Commands_General_TestProcessing_StartRegressionTestResultsReport_JMenuItem =
		new SimpleJMenuItem( __Commands_General_TestProcessing_StartRegressionTestResultsReport_String, this));
}

/**
Define the popup menu for the commands area.
*/
private void ui_InitGUIMenus_CommandsPopup () {
	// Pop-up menu to manipulate commands.
	__Commands_JPopupMenu = new JPopupMenu("Command Actions");
	__Commands_JPopupMenu.add( __CommandsPopup_ShowCommandStatus_JMenuItem =
		new SimpleJMenuItem ( __CommandsPopup_ShowCommandStatus_String,	__CommandsPopup_ShowCommandStatus_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem =
		new SimpleJMenuItem( "Edit", __Edit_CommandWithErrorChecking_String, this ) );
	__Commands_JPopupMenu.addSeparator();
	__Commands_JPopupMenu.add( __CommandsPopup_Cut_JMenuItem =
		new SimpleJMenuItem( "Cut", __Edit_CutCommands_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_Copy_JMenuItem =
		new SimpleJMenuItem ( "Copy", __Edit_CopyCommands_String,this));
	__Commands_JPopupMenu.add( __CommandsPopup_Paste_JMenuItem=
		new SimpleJMenuItem("Paste (After Selected)", __Edit_PasteCommands_String,this));
	__Commands_JPopupMenu.addSeparator();
	__Commands_JPopupMenu.add(__CommandsPopup_Delete_JMenuItem=
		new SimpleJMenuItem( "Delete", __Edit_DeleteCommands_String, this ) );
	__Commands_JPopupMenu.addSeparator();
	__Commands_JPopupMenu.add( __CommandsPopup_FindCommandsUsingString_JMenuItem =
		new SimpleJMenuItem( __CommandsPopup_FindCommandsUsingString_String, this));
	__Commands_JPopupMenu.add( __CommandsPopup_FindCommandsUsingLineNumber_JMenuItem =
		new SimpleJMenuItem( __CommandsPopup_FindCommandUsingLineNumber_String, this));
	__Commands_JPopupMenu.add( __CommandsPopup_SelectAll_JMenuItem =
		new SimpleJMenuItem ( "Select All", __Edit_SelectAllCommands_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_DeselectAll_JMenuItem =
		new SimpleJMenuItem( "Deselect All", __Edit_DeselectAllCommands_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem =
		new SimpleJMenuItem (__Edit_ConvertSelectedCommandsToComments_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem =
		new SimpleJMenuItem ( __Edit_ConvertSelectedCommandsFromComments_String, this ) );
	__Commands_JPopupMenu.addSeparator();
	__Commands_JPopupMenu.add( __CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + __Run_AllCommandsCreateOutput_String,
		__Run_AllCommandsCreateOutput_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + __Run_AllCommandsIgnoreOutput_String,
		__Run_AllCommandsIgnoreOutput_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + __Run_SelectedCommandsCreateOutput_String,
		__Run_SelectedCommandsCreateOutput_String, this ) );
	__Commands_JPopupMenu.add( __CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + __Run_SelectedCommandsIgnoreOutput_String,
		__Run_SelectedCommandsIgnoreOutput_String, this ) );
	__Commands_JPopupMenu.add ( __CommandsPopup_CancelCommandProcessing_JMenuItem =
		new SimpleJMenuItem(__Run_CancelCommandProcessing_String,this));
}

/**
Initialize the Commands menu for StateCU.
*/
private void ui_InitGUIMenus_Commands_StateCU ( JMenuBar menuBar, int style ) {
	if ( menuBar != null ) {
		// Initialization.
		__Commands_JMenu = new JMenu("Commands", true);
		menuBar.add ( __Commands_JMenu );
	}

	boolean show_all_commands = false; // True indicates that a command file has been opened directly.
	if ( (__statecuDatasetType == StateCU_DataSet.TYPE_UNKNOWN) && (__statecuDataset == null) ) {
		// Startup or user is editing commands directly without a data set.
		// If at initialization, all menus will be available but will be disabled.
		// If a command file is opened directly, then the GUI state will be checked and menus will be enabled.
		show_all_commands = true;
	}

	// Response file submenu... (will there be commands?).

	// Control file submenu... (will there be commands?).

	// CU Locations Submenu.

	if ( __statecuDatasetType == StateCU_DataSet.TYPE_OTHER_USES ) {
		// Only for other uses.
		return;
	}

	// Below for everything except other uses.
	// Need for all other levels.

	// Climate stations data.

	JMenu Commands_StateCU_ClimateStationsData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateCU_ClimateStationsData_String, false );

	// Climate Stations.

	JMenu Commands_StateCU_ClimateStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateCU_ClimateStationsData_JMenu, __Commands_StateCU_ClimateStationsData_String,
		__Commands_StateCU_ClimateStations_String, false );
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_ReadClimateStationsFromList_JMenuItem
		= new SimpleJMenuItem(__Commands_StateCU_ClimateStations_ReadClimateStationsFromList_String,this));
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_JMenuItem
		= new SimpleJMenuItem(__Commands_StateCU_ClimateStations_ReadClimateStationsFromStateCU_String,this));
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_ReadClimateStationsFromHydroBase_String,this));
	Commands_StateCU_ClimateStations_JMenu.addSeparator();
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_SetClimateStation_JMenuItem
		= new SimpleJMenuItem(__Commands_StateCU_ClimateStations_SetClimateStation_String,this));
	Commands_StateCU_ClimateStations_JMenu.addSeparator();
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_FillClimateStationsFromHydroBase_String,this));
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_FillClimateStation_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_FillClimateStation_String,this));
	Commands_StateCU_ClimateStations_JMenu.addSeparator();
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_SortClimateStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_SortClimateStations_String,this));
	Commands_StateCU_ClimateStations_JMenu.addSeparator();
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_WriteClimateStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_WriteClimateStationsToList_String,this));
	Commands_StateCU_ClimateStations_JMenu.add(
		__Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_ClimateStations_WriteClimateStationsToStateCU_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_ClimateStations_JMenu,
		__Commands_StateCU_ClimateStations_CheckClimateStations_String);

	// Climate Stations - Temperature Time Series.

	ui_InitGUIMenus_Commands_AddComponentMenu (	style, Commands_StateCU_ClimateStationsData_JMenu,
		__Commands_StateCU_ClimateStationsData_String, __Commands_StateCU_ClimateStations_TemperatureTS_String,
		true );

	// Climate Stations - Frost Date Time Series.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateCU_ClimateStationsData_JMenu,
		__Commands_StateCU_ClimateStationsData_String, __Commands_StateCU_ClimateStations_FrostDatesTS_String,
		true );

	// Climate Stations - Precipitation Time Series.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateCU_ClimateStationsData_JMenu,
		__Commands_StateCU_ClimateStationsData_String,__Commands_StateCU_ClimateStations_PrecipitationTS_String, true );

	// Crop Characteristics and coefficients Data.

	JMenu Commands_StateCU_CropCharacteristicsData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateCU_CropCharacteristicsData_String, false );

	// Crop characteristics.

	JMenu Commands_StateCU_CropCharacteristics_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateCU_CropCharacteristicsData_JMenu, __Commands_StateCU_CropCharacteristicsData_String,
			__Commands_StateCU_CropCharacteristics_String, false );
	Commands_StateCU_CropCharacteristics_JMenu.add(
		__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromStateCU_String,this));
	Commands_StateCU_CropCharacteristics_JMenu.add(
		__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CropCharacteristics_ReadCropCharacteristicsFromHydroBase_String,this));
	Commands_StateCU_CropCharacteristics_JMenu.addSeparator();
	Commands_StateCU_CropCharacteristics_JMenu.add(
		__Commands_StateCU_CropCharacteristics_SetCropCharacteristics_JMenuItem =
		new SimpleJMenuItem (__Commands_StateCU_CropCharacteristics_SetCropCharacteristics_String,this));
	Commands_StateCU_CropCharacteristics_JMenu.add(
		__Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_JMenuItem =
		new SimpleJMenuItem (__Commands_StateCU_CropCharacteristics_TranslateCropCharacteristics_String,this));
	Commands_StateCU_CropCharacteristics_JMenu.addSeparator();
	Commands_StateCU_CropCharacteristics_JMenu.add (
		__Commands_StateCU_CropCharacteristics_SortCropCharacteristics_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CropCharacteristics_SortCropCharacteristics_String,this));

	Commands_StateCU_CropCharacteristics_JMenu.addSeparator();
	Commands_StateCU_CropCharacteristics_JMenu.add (
		__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToList_String,this));
	Commands_StateCU_CropCharacteristics_JMenu.add (
		__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CropCharacteristics_WriteCropCharacteristicsToStateCU_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_CropCharacteristics_JMenu,
		__Commands_StateCU_CropCharacteristics_CheckCropCharacteristics_String);

	// Blaney-Criddle Crop Coefficients Submenu.

	JMenu Commands_StateCU_BlaneyCriddle_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateCU_CropCharacteristicsData_JMenu,	__Commands_StateCU_CropCharacteristicsData_String,
		__Commands_StateCU_BlaneyCriddle_String, false );
	Commands_StateCU_BlaneyCriddle_JMenu.add(
		__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromStateCU_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.add(__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_ReadBlaneyCriddleFromHydroBase_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.addSeparator();
	Commands_StateCU_BlaneyCriddle_JMenu.add(__Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_SetBlaneyCriddle_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.add(__Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_TranslateBlaneyCriddle_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.addSeparator();
	Commands_StateCU_BlaneyCriddle_JMenu.add(__Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_SortBlaneyCriddle_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.addSeparator();
	Commands_StateCU_BlaneyCriddle_JMenu.add(__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToList_String,this));
	Commands_StateCU_BlaneyCriddle_JMenu.add(
		__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_BlaneyCriddle_WriteBlaneyCriddleToStateCU_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_BlaneyCriddle_JMenu,
		__Commands_StateCU_BlaneyCriddle_CheckBlaneyCriddle_String);

	// Penman-Monteith Crop Coefficients Submenu.

	JMenu Commands_StateCU_PenmanMonteith_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateCU_CropCharacteristicsData_JMenu,	__Commands_StateCU_CropCharacteristicsData_String,
		__Commands_StateCU_PenmanMonteith_String, false );
	Commands_StateCU_PenmanMonteith_JMenu.add(
		__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromStateCU_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.add(__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_ReadPenmanMonteithFromHydroBase_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.addSeparator();
	Commands_StateCU_PenmanMonteith_JMenu.add(__Commands_StateCU_PenmanMonteith_SetPenmanMonteith_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_SetPenmanMonteith_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.add(__Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_TranslatePenmanMonteith_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.addSeparator();
	Commands_StateCU_PenmanMonteith_JMenu.add(__Commands_StateCU_PenmanMonteith_SortPenmanMonteith_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_SortPenmanMonteith_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.addSeparator();
	Commands_StateCU_PenmanMonteith_JMenu.add(__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToList_String,this));
	Commands_StateCU_PenmanMonteith_JMenu.add(
		__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_PenmanMonteith_WritePenmanMonteithToStateCU_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_PenmanMonteith_JMenu,
		__Commands_StateCU_PenmanMonteith_CheckPenmanMonteith_String);

	// CU Locations Data.

	JMenu Commands_StateCU_CULocationsData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateCU_CULocationsData_String, false );

	// CU Locations.

	JMenu Commands_StateCU_CULocations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateCU_CULocationsData_JMenu, __Commands_StateCU_CULocationsData_String,
		__Commands_StateCU_CULocations_String, false );
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_ReadCULocationsFromList_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_ReadCULocationsFromStateCU_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_ReadCULocationsFromStateMod_String,this) );
	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_SetCULocation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetCULocation_String, this));
	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_SetCULocationsFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetCULocationsFromList_String,this));
	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetDiversionAggregate_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetDiversionAggregateFromList_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetDiversionSystem_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetDiversionSystemFromList_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetWellAggregate_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetWellAggregateFromList_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetWellSystem_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetWellSystemFromList_String,this));
	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_SortCULocations_JMenuItem=
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SortCULocations_String, this));
	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_FillCULocationsFromList_JMenuItem
		= new SimpleJMenuItem(__Commands_StateCU_CULocations_FillCULocationsFromList_String,this));
	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_FillCULocationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_FillCULocationsFromHydroBase_String,this));

	Commands_StateCU_CULocations_JMenu.add(__Commands_StateCU_CULocations_FillCULocation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_FillCULocation_String, this));

	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetCULocationClimateStationWeights_String, this));
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromList_String, this));
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(
		"<HTML><I>" +
		__Commands_StateCU_CULocations_SetCULocationClimateStationWeightsFromHydroBase_String +
		"</I></HTML>", this));
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_FillCULocationClimateStationWeights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_FillCULocationClimateStationWeights_String, this));

	Commands_StateCU_CULocations_JMenu.addSeparator();
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_WriteCULocationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_WriteCULocationsToList_String,this));
	Commands_StateCU_CULocations_JMenu.add(
		__Commands_StateCU_CULocations_WriteCULocationsToStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateCU_CULocations_WriteCULocationsToStateCU_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_CULocations_JMenu,
		__Commands_StateCU_CULocations_CheckCULocations_String);

	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_STRUCTURES) ) {
		// Parcels submenu.

		JMenu Commands_StateCU_Parcels_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
			Commands_StateCU_CULocationsData_JMenu, __Commands_StateCU_Parcels_String,
			__Commands_StateCU_Parcels_String, false );
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_ReadParcelsFromHydroBase_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_ReadParcelsFromHydroBase_String,this));
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_ReadParcelsFromIrrigatedLands_String,this));
		Commands_StateCU_Parcels_JMenu.addSeparator();
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_SetParcel_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_SetParcel_String,this));
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_SetParcelSurfaceWaterSupply_String,this));
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_SetParcelGroundWaterSupply_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_SetParcelGroundWaterSupply_String,this));
		Commands_StateCU_Parcels_JMenu.addSeparator();
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_CheckParcels_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_CheckParcels_String,this));
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_CheckIrrigatedLands_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_CheckIrrigatedLands_String,this));
		Commands_StateCU_Parcels_JMenu.addSeparator();
		Commands_StateCU_Parcels_JMenu.add(
	        __Commands_StateCU_Parcels_WriteParcelsToFile_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_Parcels_WriteParcelsToFile_String,this));
	}

	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_STRUCTURES) ) {
		// Crop Patterns Submenu.

		JMenu Commands_StateCU_CropPatternTS_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
			Commands_StateCU_CULocationsData_JMenu, __Commands_StateCU_CULocationsData_String,
			__Commands_StateCU_CropPatternTS_String, false );
		Commands_StateCU_CropPatternTS_JMenu.add( new SimpleJMenuItem(
			__Commands_General_Running_SetOutputPeriod_String,this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCULocationsFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCULocationsFromStateCU_String,this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetDiversionAggregate_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetDiversionAggregateFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetDiversionSystem_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetDiversionSystemFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetWellAggregate_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetWellAggregateFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetWellSystem_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetWellSystemFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_CreateCropPatternTSForCULocations_String,this) );
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromStateCU_String,this));
		/* FIXME SAM 2008-12-30 Remove if not needed.
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromDBF_String,this));
			*/
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetCropPatternTSFromList_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromHydroBase_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadCropPatternTSFromParcels_String,this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add ( __Commands_StateCU_CropPatternTS_SetCropPatternTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SetCropPatternTS_String,this) );
		Commands_StateCU_CropPatternTS_JMenu.add (
			__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_TranslateCropPatternTS_String,this) );
		Commands_StateCU_CropPatternTS_JMenu.add (
			__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_RemoveCropPatternTS_String,this) );
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		/* FIXME SAM 2008-12-30 Remove if not needed.
		Commands_StateCU_CropPatternTS_JMenu.add (
			__Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_ReadAgStatsTSFromDateValue_String,this) );
		*/
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_FillCropPatternTSConstant_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_FillCropPatternTSInterpolate_String,this));
		/* FIXME SAM 2008-12-30 Remove if not needed.
		 Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_FillCropPatternTSProrateAgStats_String,this));
		*/
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_FillCropPatternTSRepeat_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_JMenuItem =
			new SimpleJMenuItem("<HTML><I>" +
				__Commands_StateCU_CropPatternTS_FillCropPatternTSUsingWellRights_String + "</I></HTML>",this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_SortCropPatternTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_SortCropPatternTS_String,this));
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_WriteCropPatternTSToStateCU_String,this));
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_WriteCropPatternTSToDateValue_String,this));
		// TODO smalers 2021-01-24 - used for supplemental data?  Not sure if it was fully ever implemented.
		/*
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_WriteCropPatternParcelsToFile_String,this));
		*/
		Commands_StateCU_CropPatternTS_JMenu.addSeparator();
		Commands_StateCU_CropPatternTS_JMenu.add(
			__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_CropPatternTS_CompareCropPatternTSFiles_String,this));
		ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_CropPatternTS_JMenu,
			__Commands_StateCU_CropPatternTS_CheckCropPatternTS_String);
	}

	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED) ) {
		// Irrigation practice Time Series Submenu.

		JMenu Commands_StateCU_IrrigationPracticeTS_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
			Commands_StateCU_CULocationsData_JMenu, __Commands_StateCU_CULocationsData_String,
			__Commands_StateCU_IrrigationPracticeTS_String, false );
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_General_Running_SetOutputPeriod_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_ReadCULocationsFromStateCU_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregate_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetDiversionAggregateFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystem_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetDiversionSystemFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetWellAggregate_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetWellAggregateFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetWellSystem_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetWellSystemFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_JMenuItem =
			new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_CreateIrrigationPracticeTSForCULocations_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromStateCU_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromHydroBase_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromParcels_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_ReadIrrigationPracticeTSFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_ReadCropPatternTSFromStateCU_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSTotalAcreageToCropPatternTSTotalAcreage_String,
			this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSPumpingMaxUsingWellRights_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_JMenuItem
			= new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSSprinklerAcreageFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTS_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SetIrrigationPracticeTSFromList_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_ReadWellRightsFromStateMod_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_JMenuItem =
			new SimpleJMenuItem(
			__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSAcreageUsingWellRights_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSInterpolate_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_FillIrrigationPracticeTSRepeat_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_SortIrrigationPracticeTS_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToDateValue_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_WriteIrrigationPracticeTSToStateCU_String,this));
		Commands_StateCU_IrrigationPracticeTS_JMenu.addSeparator();
		Commands_StateCU_IrrigationPracticeTS_JMenu.add(
			__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_JMenuItem =
			new SimpleJMenuItem(__Commands_StateCU_IrrigationPracticeTS_CompareIrrigationPracticeTSFiles_String,this));
		ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateCU_IrrigationPracticeTS_JMenu,
			__Commands_StateCU_IrrigationPracticeTS_CheckIrrigationPracticeTS_String);

		// Diversion rights.

		Commands_StateCU_CULocationsData_JMenu.addSeparator();
		ui_InitGUIMenus_Commands_StateMod_DiversionRights ( style, Commands_StateCU_CULocationsData_JMenu );

		// Diversion time series.

		ui_InitGUIMenus_Commands_StateMod_DiversionHistoricalTSMonthly ( style,
			Commands_StateCU_CULocationsData_JMenu );

		// Well rights.

		ui_InitGUIMenus_Commands_StateMod_WellRights ( style,
			Commands_StateCU_CULocationsData_JMenu );

		// Well pumping time series

		ui_InitGUIMenus_Commands_StateMod_WellHistoricalPumpingTSMonthly ( style,
			Commands_StateCU_CULocationsData_JMenu );
	}

	/* TODO SAM 2009-06-08 Move to above to have the order make more sense - evaluate whether OK.
	if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED_BY_WATER_RIGHTS) ) {
		ui_InitGUIMenus_Commands_StateMod_DiversionRights ( style, Commands_StateCU_CULocationsData_JMenu );
	}
	*/

	// General Commands Submenu.

	ui_InitGUIMenus_Commands_General ( style, __Commands_JMenu );
}

/**
Initialize the Commands menu for StateMod.
*/
private void ui_InitGUIMenus_Commands_StateMod ( JMenuBar menuBar, int style ) {
	if ( menuBar != null ) {
		// Initialization.
		__Commands_JMenu = new JMenu("Commands", true);
		__Commands_JMenu.setToolTipText(
			"Insert new commands before first selected command or at end if no commands are selected.");
		menuBar.add ( __Commands_JMenu );
	}

	// Control Data.
	JMenu Commands_StateMod_ControlData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_ControlData_String, false );

	// Response.
	__Commands_StateMod_Response_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_ControlData_JMenu, __Commands_StateMod_Response_String,
		__Commands_StateMod_Response_String, false );
	__Commands_StateMod_Response_JMenu.add (
		__Commands_StateMod_Response_ReadResponseFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Response_ReadResponseFromStateMod_String,this));
	__Commands_StateMod_Response_JMenu.addSeparator();
	__Commands_StateMod_Response_JMenu.add(
		__Commands_StateMod_Response_WriteResponseToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Response_WriteResponseToStateMod_String,this));

	// Control.
	__Commands_StateMod_Control_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_ControlData_JMenu, __Commands_StateMod_Control_String,
		__Commands_StateMod_Control_String, false );
	__Commands_StateMod_Control_JMenu.add (
		__Commands_StateMod_Control_ReadControlFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Control_ReadControlFromStateMod_String,this));
	__Commands_StateMod_Control_JMenu.addSeparator();
	__Commands_StateMod_Control_JMenu.add(
		__Commands_StateMod_Control_WriteControlToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Control_WriteControlToStateMod_String,this));

	// Output Request.
	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_ControlData_JMenu,
		__Commands_StateMod_ControlData_String, __Commands_StateMod_OutputRequest_String, true );

	// Reach Data.
	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_ControlData_JMenu,
		__Commands_StateMod_ControlData_String, __Commands_StateMod_ReachData_String, true );

	// Consumptive Use Data.

	JMenu Commands_StateMod_ConsumptiveUseData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_ConsumptiveUseData_String, false );

	// StateCU Structure file.

	ui_InitGUIMenus_Commands_AddComponentMenu (	style, Commands_StateMod_ConsumptiveUseData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_StateCUStructure_String, true );

	//if ( show_all_commands || (__statecuDatasetType >= StateCU_DataSet.TYPE_STRUCTURES) ) {
		// Parcels submenu.

		JMenu Commands_StateMod_Parcels_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
			Commands_StateMod_ConsumptiveUseData_JMenu, __Commands_StateCU_Parcels_String,
			__Commands_StateCU_Parcels_String, false );
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_ReadParcelsFromHydroBase_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_ReadParcelsFromHydroBase_String,this));
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_ReadParcelsFromIrrigatedLands_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_ReadParcelsFromIrrigatedLands_String,this));
		Commands_StateMod_Parcels_JMenu.addSeparator();
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_SetParcel_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_SetParcel_String,this));
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_SetParcelSurfaceWaterSupply_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_SetParcelSurfaceWaterSupply_String,this));
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_SetParcelGroundWaterSupply_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_SetParcelGroundWaterSupply_String,this));
		Commands_StateMod_Parcels_JMenu.addSeparator();
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_CheckParcels_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_CheckParcels_String,this));
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_CheckIrrigatedLands_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_CheckIrrigatedLands_String,this));
		Commands_StateMod_Parcels_JMenu.addSeparator();
		Commands_StateMod_Parcels_JMenu.add(
	        __Commands_StateMod_Parcels_WriteParcelsToFile_JMenuItem =
			new SimpleJMenuItem(__Commands_StateMod_Parcels_WriteParcelsToFile_String,this));
	//}

	// Irrigation practice, yearly.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_ConsumptiveUseData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_IrrigationPracticeTS_String,true );

	// Consumptive water requirement, monthly and daily.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_ConsumptiveUseData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_ConsumptiveWaterRequirementTS_String,true );

	// Stream Gage Data.

	JMenu Commands_StateMod_StreamGageData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_StreamGageData_String, false );

	// Stream Gage Station Data.

	JMenu Commands_StateMod_StreamGageStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_StreamGageData_JMenu, __Commands_StateMod_StreamGageData_String,
		__Commands_StateMod_StreamGageStations_String, false );
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromList_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromNetwork_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_ReadStreamGageStationsFromStateMod_String,this));
	Commands_StateMod_StreamGageStations_JMenu.addSeparator ();
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_SetStreamGageStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_SetStreamGageStation_String,this));
	Commands_StateMod_StreamGageStations_JMenu.addSeparator ();
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_SortStreamGageStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_SortStreamGageStations_String,this));
	Commands_StateMod_StreamGageStations_JMenu.addSeparator ();
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromHydroBase_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_ReadNetworkFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_ReadNetworkFromStateMod_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_FillStreamGageStationsFromNetwork_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_FillStreamGageStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_FillStreamGageStation_String,this));
	Commands_StateMod_StreamGageStations_JMenu.addSeparator ();
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToList_String,this));
	Commands_StateMod_StreamGageStations_JMenu.add (
		__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamGageStations_WriteStreamGageStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_StreamGageStations_JMenu,
		__Commands_StateMod_StreamGageStations_CheckStreamGageStations_String);

	// Stream Gage Data - Historical TS (Monthly).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_StreamGageData_JMenu,
		__Commands_StateMod_StreamGageData_String, __Commands_StateMod_StreamGageHistoricalTS_String, true );

	// Stream Gage Data - Natural flow TS (Monthly).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_StreamGageData_JMenu,
		__Commands_StateMod_StreamGageData_String, __Commands_StateMod_StreamGageBaseTS_String, true );

	// Delay Table Data.

	JMenu Commands_StateMod_DelayTableData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_DelayTableData_String, false );

	// Delay Table Data... Monthly.

	JMenu Commands_StateMod_DelayTablesMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_DelayTableData_JMenu,	__Commands_StateMod_DelayTableData_String,
			__Commands_StateMod_DelayTablesMonthly_String, false );

	Commands_StateMod_DelayTablesMonthly_JMenu.add(
		__Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesMonthly_ReadDelayTablesMonthlyFromStateMod_String,this));
	Commands_StateMod_DelayTablesMonthly_JMenu.addSeparator();
	Commands_StateMod_DelayTablesMonthly_JMenu.add(
		__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToList_String,this));
	Commands_StateMod_DelayTablesMonthly_JMenu.add(
		__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesMonthly_WriteDelayTablesMonthlyToStateMod_String,this));
	//ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DelayTablesMonthly_JMenu,
	//	__Commands_StateMod_DelayTablesMonthly_CheckDelayTablesMonthly_String);

	// Delay Table Data... Daily.

	JMenu Commands_StateMod_DelayTablesDaily_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_DelayTableData_JMenu, __Commands_StateMod_DelayTableData_String,
		__Commands_StateMod_DelayTablesDaily_String, false );
	Commands_StateMod_DelayTablesDaily_JMenu.add(
		__Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesDaily_ReadDelayTablesDailyFromStateMod_String,this));
	Commands_StateMod_DelayTablesDaily_JMenu.addSeparator();
	Commands_StateMod_DelayTablesDaily_JMenu.add(
		__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToList_String,this));
	Commands_StateMod_DelayTablesDaily_JMenu.add(
		__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DelayTablesDaily_WriteDelayTablesDailyToStateMod_String,this));
	//ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DelayTablesDaily_JMenu,
	//	__Commands_StateMod_DelayTablesMonthly_CheckDelayTablesDaily_String);

	// Diversion Data.

	JMenu Commands_StateMod_DiversionData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_DiversionData_String, false );

	// Diversion stations.

	JMenu Commands_StateMod_DiversionStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_DiversionData_JMenu, __Commands_StateMod_DiversionData_String,
		__Commands_StateMod_DiversionStations_String, false );
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SetOutputYearType_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetOutputYearType_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_ReadDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_ReadDiversionStationsFromNetwork_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionAggregate_String,this));
	Commands_StateMod_DiversionStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionAggregateFromList_String,this));
	Commands_StateMod_DiversionStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionSystem_String,this));
	Commands_StateMod_DiversionStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionSystemFromList_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SetDiversionStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionStation_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SetDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SortDiversionStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_SortDiversionStations_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_FillDiversionStationsFromHydroBase_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_FillDiversionStationsFromNetwork_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_FillDiversionStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_FillDiversionStation_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromNetwork_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_DiversionStations_SetDiversionStationDelayTablesFromRTN_String,this));
	Commands_StateMod_DiversionStations_JMenu.addSeparator ();
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_WriteDiversionStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_WriteDiversionStationsToList_String,this));
	Commands_StateMod_DiversionStations_JMenu.add (
		__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionStations_WriteDiversionStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DiversionStations_JMenu,
		__Commands_StateMod_DiversionStations_CheckDiversionStations_String);

	// Diversion rights.

	ui_InitGUIMenus_Commands_StateMod_DiversionRights ( style, Commands_StateMod_DiversionData_JMenu );

	// Diversion historical time series, monthly.

	ui_InitGUIMenus_Commands_StateMod_DiversionHistoricalTSMonthly ( style, Commands_StateMod_DiversionData_JMenu );

	// Diversion historical ts daily.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_DiversionData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_DiversionHistoricalTSDaily_String, true );

	// Diversion demand time series, monthly.

	JMenu Commands_StateMod_DiversionDemandTSMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_DiversionData_JMenu, __Commands_StateMod_DiversionData_String,
		__Commands_StateMod_DiversionDemandTSMonthly_String,false );
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputPeriod_String, this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputYearType_String, this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregate_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregate_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregateFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionAggregateFromList_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystem_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionSystemFromList_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStruct_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionMultiStructFromList_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String,
		this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionStationEfficiencies_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStation_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionStationsToStateMod_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthly_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_CalculateDiversionDemandTSMonthlyAsMax_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadDiversionDemandTSMonthlyFromStateMod_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyAverage_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyConstant_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_ReadPatternFile_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_FillDiversionDemandTSMonthlyPattern_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_LimitDiversionDemandTSMonthlyToRights_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthly_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SetDiversionDemandTSMonthlyConstant_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_SortDiversionDemandTSMonthly_String,this));
	Commands_StateMod_DiversionDemandTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionDemandTSMonthly_WriteDiversionDemandTSMonthlyToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DiversionDemandTSMonthly_JMenu,
		__Commands_StateMod_DiversionDemandTSMonthly_CheckDiversionDemandTSMonthly_String);

	// Diversion demand TS (daily).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_DiversionData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_DiversionDemandTSDaily_String, true );

	// Diversion demands override, monthly.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_DiversionData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_DiversionDemandTSOverrideMonthly_String,true );

	// Diversion demands, average monthly.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_DiversionData_JMenu,
		__Commands_StateMod_DiversionData_String, __Commands_StateMod_DiversionDemandTSAverageMonthly_String,true );

	// Precipitation Data.

	JMenu Commands_StateMod_PrecipitationData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_PrecipitationData_String, false );

	// Precipitation time series (monthly, yearly).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_PrecipitationData_JMenu,
		__Commands_StateMod_PrecipitationData_String,__Commands_StateMod_PrecipitationTSMonthly_String,true );

	// Evaporation Data.

	JMenu Commands_StateMod_EvaporationData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu (	style,
		__Commands_JMenu, __Commands_StateMod_EvaporationData_String, false );

	// Evaporation time series (monthly, yearly).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_EvaporationData_JMenu,
		__Commands_StateMod_EvaporationData_String,	__Commands_StateMod_EvaporationTSMonthly_String,true );

	// Reservoir Data.

	JMenu Commands_StateMod_ReservoirData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_ReservoirData_String, false );

	// Reservoir Stations.

	JMenu Commands_StateMod_ReservoirStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_ReservoirData_JMenu, __Commands_StateMod_ReservoirData_String,
		__Commands_StateMod_ReservoirStations_String, false );
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromList_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromNetwork_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_ReadReservoirStationsFromStateMod_String,this));
	Commands_StateMod_ReservoirStations_JMenu.addSeparator ();
	Commands_StateMod_ReservoirStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SetReservoirAggregate_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SetReservoirAggregateFromList_String,this));
	/* TODO SAM 2004-07-07 maybe enable later.
	Commands_StateMod_ReservoirStations_JMenu.add(
		__Commands_StateMod_ReservoirStations_SetReservoirSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SetReservoirSystem_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add(
		__Commands_StateMod_ReservoirStations_SetReservoirSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SetReservoirSystemFromList_String,this));
	*/
	Commands_StateMod_ReservoirStations_JMenu.addSeparator ();
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_SetReservoirStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SetReservoirStation_String,this));
	Commands_StateMod_ReservoirStations_JMenu.addSeparator ();
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_SortReservoirStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_SortReservoirStations_String,	this));
	Commands_StateMod_ReservoirStations_JMenu.addSeparator ();
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_FillReservoirStationsFromHydroBase_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_FillReservoirStationsFromNetwork_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_FillReservoirStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_FillReservoirStation_String,this));
	Commands_StateMod_ReservoirStations_JMenu.addSeparator ();
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_WriteReservoirStationsToList_String,this));
	Commands_StateMod_ReservoirStations_JMenu.add (
		__Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirStations_WriteReservoirStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_ReservoirStations_JMenu,
		__Commands_StateMod_ReservoirStations_CheckReservoirStations_String);

	// Reservoir rights.

	JMenu Commands_StateMod_ReservoirRights_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_ReservoirData_JMenu, __Commands_StateMod_ReservoirData_String,
		__Commands_StateMod_ReservoirRights_String,	false );
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromList_String,this));
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_ReadReservoirStationsFromStateMod_String,this));
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SetReservoirAggregate_String,this));
	Commands_StateMod_ReservoirRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SetReservoirAggregateFromList_String,this));
	/* TODO SAM 2004-07-07 has not traditionally been used but might be.
	Commands_StateMod_ReservoirRights_JMenu.add(
		__Commands_StateMod_ReservoirRights_SetReservoirSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SetReservoirSystem_String,this));
	Commands_StateMod_ReservoirRights_JMenu.add(
		__Commands_StateMod_ReservoirRights_SetReservoirSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SetReservoirSystemFromList_String,this));
	*/
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromHydroBase_String,this));
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_ReadReservoirRightsFromStateMod_String,this));
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_SetReservoirRight_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SetReservoirRight_String,this));
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_SortReservoirRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_SortReservoirRights_String,this));
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_FillReservoirRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_FillReservoirRight_String,this));
	Commands_StateMod_ReservoirRights_JMenu.addSeparator ();
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_WriteReservoirRightsToList_String,this));
	Commands_StateMod_ReservoirRights_JMenu.add (
		__Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirRights_WriteReservoirRightsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_ReservoirRights_JMenu,
		__Commands_StateMod_ReservoirRights_CheckReservoirRights_String);

	// Reservoir return.

	JMenu Commands_StateMod_ReservoirReturn_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_ReservoirData_JMenu, __Commands_StateMod_ReservoirReturn_String,
		__Commands_StateMod_ReservoirReturn_String, false );
	Commands_StateMod_ReservoirReturn_JMenu.add (
		__Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirReturn_ReadReservoirReturnFromStateMod_String,this));
	Commands_StateMod_ReservoirReturn_JMenu.addSeparator();
	Commands_StateMod_ReservoirReturn_JMenu.add (
		__Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_ReservoirReturn_WriteReservoirReturnToStateMod_String,this));

	// Reservoir content and target time series.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_ReservoirData_JMenu,
		__Commands_StateMod_ReservoirData_String, __Commands_StateMod_ReservoirContentAndTargetTS_String, true );

	// Instream Flow Data.

	JMenu Commands_StateMod_InstreamFlowData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_InstreamFlowData_String, false );

	// Instream Flow Stations.

	JMenu Commands_StateMod_InstreamFlowStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_InstreamFlowData_JMenu, __Commands_StateMod_InstreamFlowData_String,
		__Commands_StateMod_InstreamFlowStations_String,false );
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromList_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromNetwork_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_ReadInstreamFlowStationsFromStateMod_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_SetInstreamFlowStation_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_SortInstreamFlowStations_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromHydroBase_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStationsFromNetwork_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_FillInstreamFlowStation_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToList_String,this));
	Commands_StateMod_InstreamFlowStations_JMenu.add (
		__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowStations_WriteInstreamFlowStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_InstreamFlowStations_JMenu,
		__Commands_StateMod_InstreamFlowStations_CheckInstreamFlowStations_String);

	JMenu Commands_StateMod_InstreamFlowRights_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_InstreamFlowData_JMenu, __Commands_StateMod_InstreamFlowData_String,
		__Commands_StateMod_InstreamFlowRights_String, false );
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromList_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowStationsFromStateMod_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromHydroBase_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_ReadInstreamFlowRightsFromStateMod_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_SetInstreamFlowRight_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_SortInstreamFlowRights_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_FillInstreamFlowRight_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToList_String,this));
	Commands_StateMod_InstreamFlowRights_JMenu.add (
		__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_InstreamFlowRights_WriteInstreamFlowRightsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_InstreamFlowRights_JMenu,
		__Commands_StateMod_InstreamFlowRights_CheckInstreamFlowRights_String);

	// StateMod ... Instream Flow Demand TS (Average Monthly).

	JMenu Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu (
		style, Commands_StateMod_InstreamFlowData_JMenu, __Commands_StateMod_InstreamFlowData_String,
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_String, false );
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputYearType_String, this));
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.addSeparator ();
	/* TODO SAM 2004-07-08 - see if data from rights is enough.
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowStationsFromStateMod_String,
		this));
	*/
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowDemandTSAverageMonthlyFromStateMod_String,
		this));
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_ReadInstreamFlowRightsFromStateMod_String,
		this));
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyFromRights_String,
		this));
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_SetInstreamFlowDemandTSAverageMonthlyConstant_String,
		this));
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.addSeparator ();
	Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu.add (
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_WriteInstreamFlowDemandTSAverageMonthlyToStateMod_String,
		this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_InstreamFlowDemandTSAverageMonthly_JMenu,
		__Commands_StateMod_InstreamFlowDemandTSAverageMonthly_CheckInstreamFlowDemandTSAverageMonthly_String);

	// Instream flow Demand (Monthly).

	ui_InitGUIMenus_Commands_AddComponentMenu (	style, Commands_StateMod_InstreamFlowData_JMenu,
		__Commands_StateMod_InstreamFlowData_String, __Commands_StateMod_InstreamFlowDemandTS_String, true );

	// Well Data.

	JMenu Commands_StateMod_WellData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_WellData_String, false );

	// Well stations.

	JMenu Commands_StateMod_WellStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_WellData_JMenu, __Commands_StateMod_WellData_String,
		__Commands_StateMod_WellStations_String, false );
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadWellStationsFromList_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadWellStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadWellStationsFromNetwork_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadWellStationsFromStateMod_String,this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellAggregate_String,this));
	Commands_StateMod_WellStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellAggregateFromList_String,this));
	Commands_StateMod_WellStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellSystem_String,this));
	Commands_StateMod_WellStations_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellSystemFromList_String,this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStation_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationsFromList_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadCropPatternTSFromStateCU_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationAreaToCropPatternTS_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadWellRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadWellRightsFromStateMod_String,	this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationCapacityToWellRights_String,	this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SortWellStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SortWellStations_String,this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_FillWellStationsFromDiversionStations_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_FillWellStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_FillWellStationsFromNetwork_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_FillWellStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_FillWellStation_String,this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationDelayTablesFromNetwork_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationDelayTablesFromRTN_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_SetWellStationDepletionTablesFromRTN_String,this));
	Commands_StateMod_WellStations_JMenu.addSeparator ();
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_WriteWellStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_WriteWellStationsToList_String,this));
	Commands_StateMod_WellStations_JMenu.add (
		__Commands_StateMod_WellStations_WriteWellStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellStations_WriteWellStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_WellStations_JMenu,
		__Commands_StateMod_WellStations_CheckWellStations_String);

	// Well rights.

	ui_InitGUIMenus_Commands_StateMod_WellRights ( style, Commands_StateMod_WellData_JMenu );

	// Well historical pumping TS (Monthly).

	ui_InitGUIMenus_Commands_StateMod_WellHistoricalPumpingTSMonthly ( style, Commands_StateMod_WellData_JMenu );

	// Well historical pumping time series (daily).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_WellData_JMenu,
		__Commands_StateMod_WellData_String, __Commands_StateMod_WellHistoricalPumpingTSDaily_String, true );

	// Well demand time series, monthly.

	JMenu Commands_StateMod_WellDemandTSMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_WellData_JMenu, __Commands_StateMod_WellData_String,
		__Commands_StateMod_WellDemandTSMonthly_String, false );
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputPeriod_String, this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputYearType_String, this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromList_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadWellStationsFromStateMod_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		__Commands_StateMod_WellDemandTSMonthly_SetWellAggregate_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellAggregate_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		__Commands_StateMod_WellDemandTSMonthly_SetWellAggregateFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellAggregateFromList_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		__Commands_StateMod_WellDemandTSMonthly_SetWellSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellSystem_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add(
		__Commands_StateMod_WellDemandTSMonthly_SetWellSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellSystemFromList_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadWellDemandTSMonthlyFromStateMod_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadIrrigationWaterRequirementTSMonthlyFromStateCU_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_CalculateWellStationEfficiencies_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_SetWellStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellStation_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellStationsFromList_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_WriteWellStationsToStateMod_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthly_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_CalculateWellDemandTSMonthlyAsMax_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthly_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SetWellDemandTSMonthlyConstant_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyAverage_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyConstant_String,	this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadPatternFile_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_FillWellDemandTSMonthlyPattern_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_ReadWellRightsFromStateMod_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_LimitWellDemandTSMonthlyToRights_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_SortWellDemandTSMonthly_String,this));
	Commands_StateMod_WellDemandTSMonthly_JMenu.add (
		__Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellDemandTSMonthly_WriteWellDemandTSMonthlyToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_WellDemandTSMonthly_JMenu,
			__Commands_StateMod_WellDemandTSMonthly_CheckWellDemandTSMonthly_String);

	// Well demand time series (daily).

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_WellData_JMenu,
		__Commands_StateMod_WellData_String, __Commands_StateMod_WellDemandTSDaily_String, true );

	// Plan stations.

	JMenu Commands_StateMod_PlanData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
			__Commands_JMenu, __Commands_StateMod_PlanData_String, false );
	JMenu Commands_StateMod_PlanStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_PlanData_JMenu, __Commands_StateMod_PlanData_String,
		__Commands_StateMod_PlanStations_String, false );
	Commands_StateMod_PlanStations_JMenu.add (
		__Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanStations_ReadPlanStationsFromStateMod_String,this));
	Commands_StateMod_PlanStations_JMenu.addSeparator();
	Commands_StateMod_PlanStations_JMenu.add (
		__Commands_StateMod_PlanStations_SetPlanStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanStations_SetPlanStation_String,this));
	Commands_StateMod_PlanStations_JMenu.addSeparator();
	Commands_StateMod_PlanStations_JMenu.add (
		__Commands_StateMod_PlanStations_WritePlanStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanStations_WritePlanStationsToStateMod_String,this));

	// Plan well augmentation.

	JMenu Commands_StateMod_PlanWellAugmentation_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_PlanData_JMenu, __Commands_StateMod_PlanData_String,
		__Commands_StateMod_PlanWellAugmentation_String, false );
	Commands_StateMod_PlanWellAugmentation_JMenu.add (
		__Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanWellAugmentation_ReadPlanWellAugmentationFromStateMod_String,this));
	Commands_StateMod_PlanWellAugmentation_JMenu.addSeparator();
	Commands_StateMod_PlanWellAugmentation_JMenu.add (
		__Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanWellAugmentation_WritePlanWellAugmentationToStateMod_String,this));

	// Plan return.

	JMenu Commands_StateMod_PlanReturn_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_PlanData_JMenu, __Commands_StateMod_PlanReturn_String,
		__Commands_StateMod_PlanReturn_String, false );
	Commands_StateMod_PlanReturn_JMenu.add (
		__Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanReturn_ReadPlanReturnFromStateMod_String,this));
	Commands_StateMod_PlanReturn_JMenu.addSeparator();
	Commands_StateMod_PlanReturn_JMenu.add (
		__Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_PlanReturn_WritePlanReturnToStateMod_String,this));

	// Stream Estimate Data.

	JMenu Commands_StateMod_StreamEstimateData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_StreamEstimateData_String, false );

	// Stream estimate stations.

	JMenu Commands_StateMod_StreamEstimateStations_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_StreamEstimateData_JMenu, __Commands_StateMod_StreamEstimateData_String,
		__Commands_StateMod_StreamEstimateStations_String, false );
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromList_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromNetwork_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_ReadStreamEstimateStationsFromStateMod_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_SetStreamEstimateStation_String,	this));
	Commands_StateMod_StreamEstimateStations_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_SortStreamEstimateStations_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromHydroBase_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_ReadNetworkFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_ReadNetworkFromStateMod_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStationsFromNetwork_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_FillStreamEstimateStation_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToList_String,this));
	Commands_StateMod_StreamEstimateStations_JMenu.add (
		__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateStations_WriteStreamEstimateStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_StreamEstimateStations_JMenu,
		__Commands_StateMod_StreamEstimateStations_CheckStreamEstimateStations_String);

	// Stream estimate coefficients.

	JMenu Commands_StateMod_StreamEstimateCoefficients_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu (
		style, Commands_StateMod_StreamEstimateData_JMenu, __Commands_StateMod_StreamEstimateData_String,
		__Commands_StateMod_StreamEstimateCoefficients_String, false );
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateCoefficientsFromStateMod_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromList_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromNetwork_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_ReadStreamEstimateStationsFromStateMod_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_SortStreamEstimateStations_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_SortStreamEstimateStations_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficientsPFGage_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_CalculateStreamEstimateCoefficients_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_SetStreamEstimateCoefficients_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.addSeparator ();
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToList_String,this));
	Commands_StateMod_StreamEstimateCoefficients_JMenu.add (
		__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_StreamEstimateCoefficients_WriteStreamEstimateCoefficientsToStateMod_String,
		this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_StreamEstimateCoefficients_JMenu,
		__Commands_StateMod_StreamEstimateCoefficients_CheckStreamEstimateCoefficients_String);

	// Stream estimate baseflow TS.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_StreamEstimateData_JMenu,
		__Commands_StateMod_StreamEstimateData_String, __Commands_StateMod_StreamEstimateBaseTS_String, true );

	// River Network Data.

	JMenu Commands_StateMod_RiverNetworkData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_RiverNetworkData_String, false );

	// Network (StateMod GUI/StateDMI).

	JMenu Commands_StateMod_Network_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_RiverNetworkData_JMenu, __Commands_StateMod_RiverNetworkData_String,
		__Commands_StateMod_Network_String, false );
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadNetworkFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadNetworkFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_AppendNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_AppendNetwork_String,this));
	Commands_StateMod_Network_JMenu.addSeparator ();
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadRiverNetworkFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadRiverNetworkFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadStreamGageStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadStreamGageStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadReservoirStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadReservoirStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadInstreamFlowStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadWellStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadWellStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add (__Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_ReadStreamEstimateStationsFromStateMod_String,this));
	Commands_StateMod_Network_JMenu.add(__Commands_StateMod_Network_CreateNetworkFromRiverNetwork_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_Network_CreateNetworkFromRiverNetwork_String,this));
	Commands_StateMod_Network_JMenu.addSeparator ();
	Commands_StateMod_Network_JMenu.add(__Commands_StateMod_Network_FillNetworkFromHydroBase_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_Network_FillNetworkFromHydroBase_String,this));
	Commands_StateMod_Network_JMenu.addSeparator ();
	/* TODO SAM 2006-06-13 Need to decide if this is one list with a node type column or separate list files for each node type.
	__Commands_StateMod_Network_JMenu.add(__Commands_StateMod_Network_WriteNetworkToList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_Network_WriteNetworkToList_String,this));
	*/
	Commands_StateMod_Network_JMenu.add(__Commands_StateMod_Network_WriteNetworkToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_WriteNetworkToStateMod_String,this));
	Commands_StateMod_Network_JMenu.addSeparator ();
	Commands_StateMod_Network_JMenu.add(__Commands_StateMod_Network_PrintNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_Network_PrintNetwork_String,this));

	JMenu Commands_StateMod_RiverNetwork_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_RiverNetworkData_JMenu, __Commands_StateMod_RiverNetworkData_String,
		__Commands_StateMod_RiverNetwork_String,false );
	Commands_StateMod_RiverNetwork_JMenu.add (
		__Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_ReadNetworkFromStateMod_String,this));
	Commands_StateMod_RiverNetwork_JMenu.addSeparator ();
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_CreateRiverNetworkFromNetwork_String,this));

	Commands_StateMod_RiverNetwork_JMenu.addSeparator ();
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_SetRiverNetworkNode_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_SetRiverNetworkNode_String,this));

	Commands_StateMod_RiverNetwork_JMenu.addSeparator ();
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_FillRiverNetworkFromHydroBase_String,this));
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_FillRiverNetworkFromNetwork_String,this));
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_FillRiverNetworkNode_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_FillRiverNetworkNode_String,this));
	Commands_StateMod_RiverNetwork_JMenu.addSeparator ();
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_WriteRiverNetworkToList_String,this));
	Commands_StateMod_RiverNetwork_JMenu.add(
		__Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_RiverNetwork_WriteRiverNetworkToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_RiverNetwork_JMenu,
			__Commands_StateMod_RiverNetwork_CheckRiverNetwork_String);

	// Operational Data.
	JMenu Commands_StateMod_OperationalData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_OperationalData_String, false );

	// Operational rights.
	__Commands_StateMod_OperationalRights_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		Commands_StateMod_OperationalData_JMenu, __Commands_StateMod_OperationalData_String,
		__Commands_StateMod_OperationalRights_String, false );
	__Commands_StateMod_OperationalRights_JMenu.add (
		__Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_OperationalRights_ReadOperationalRightsFromStateMod_String,this));
	__Commands_StateMod_OperationalRights_JMenu.addSeparator();
	__Commands_StateMod_OperationalRights_JMenu.add (
		__Commands_StateMod_OperationalRights_SetOperationalRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_OperationalRights_SetOperationalRight_String,this));
	__Commands_StateMod_OperationalRights_JMenu.addSeparator();
	__Commands_StateMod_OperationalRights_JMenu.add(
		__Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_OperationalRights_WriteOperationalRightsToStateMod_String,this));

	// Downstream call.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_OperationalData_JMenu,
		__Commands_StateMod_OperationalData_String, __Commands_StateMod_DownstreamCallTSDaily_String, true );

	// SanJuan recovery.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_OperationalData_JMenu,
			__Commands_StateMod_OperationalData_String, __Commands_StateMod_SanJuanSedimentRecoveryPlan_String, true );

	// Rio Grande spill.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_OperationalData_JMenu,
		__Commands_StateMod_OperationalData_String, __Commands_StateMod_RioGrandeSpill_String, true );

	// Spatial Data.

	JMenu Commands_StateMod_SpatialData_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
		__Commands_JMenu, __Commands_StateMod_SpatialData_String, false );

	// GeoView Project File.

	ui_InitGUIMenus_Commands_AddComponentMenu ( style, Commands_StateMod_SpatialData_JMenu,
		__Commands_StateMod_SpatialData_String, __Commands_StateMod_GeoViewProject_String, true );

	// General Commands Submenu.

	ui_InitGUIMenus_Commands_General ( style, __Commands_JMenu );
}

/**
Initialize the StateMod diversion historical time series (monthly) menus.
These can be used with StateMod or StateCU.
@param style Menu style (see MENU_STYLE_*).
@param parent_JMenu The JMenu to which submenus should be attached.
*/
private void ui_InitGUIMenus_Commands_StateMod_DiversionHistoricalTSMonthly ( int style, JMenu parent_JMenu ) {
	JMenu Commands_StateMod_DiversionHistoricalTSMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu (
		style, parent_JMenu, __Commands_StateMod_DiversionData_String,
		__Commands_StateMod_DiversionHistoricalTSMonthly_String, false );
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputPeriod_String, this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputYearType_String, this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregate_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregate_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregateFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionAggregateFromList_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystem_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add(
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionSystemFromList_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromHydroBase_String,
		this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionHistoricalTSMonthlyFromStateMod_String,
		this));
	/* TODO SAM 2007-06-26 - need to add fill.
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_fillDiversionRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_fillDiversionRight_String,this));
	*/
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthly_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionHistoricalTSMonthlyConstant_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyAverage_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyConstant_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadPatternFile_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_FillDiversionHistoricalTSMonthlyPattern_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_ReadDiversionRightsFromStateMod_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_LimitDiversionHistoricalTSMonthlyToRights_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SortDiversionHistoricalTSMonthly_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionHistoricalTSMonthlyToStateMod_String,
		this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationCapacitiesFromTS_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStation_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_SetDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionHistoricalTSMonthly_JMenu.add (
		__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionHistoricalTSMonthly_WriteDiversionStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DiversionHistoricalTSMonthly_JMenu,
		__Commands_StateMod_DiversionHistoricalTSMonthly_CheckDiversionHistoricalTSMonthly_String);
}

/**
Initialize the StateMod diversion rights command menus.  These can be used with StateMod or StateCU.
@param style Menu style (see MENU_STYLE_*).
@param parent_JMenu The JMenu to which submenus should be attached.
*/
private void ui_InitGUIMenus_Commands_StateMod_DiversionRights ( int style, JMenu parent_JMenu ) {
	JMenu Commands_StateMod_DiversionRights_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		parent_JMenu, __Commands_StateMod_DiversionData_String,
		__Commands_StateMod_DiversionRights_String, false );
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_ReadDiversionStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_ReadDiversionStationsFromList_String,this));
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_ReadDiversionStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_ReadDiversionStationsFromStateMod_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add(
		__Commands_StateMod_DiversionRights_SetDiversionAggregate_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SetDiversionAggregate_String,this));
	Commands_StateMod_DiversionRights_JMenu.add(
		__Commands_StateMod_DiversionRights_SetDiversionAggregateFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SetDiversionAggregateFromList_String,this));
	Commands_StateMod_DiversionRights_JMenu.add(
		__Commands_StateMod_DiversionRights_SetDiversionSystem_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SetDiversionSystem_String,this));
	Commands_StateMod_DiversionRights_JMenu.add(
		__Commands_StateMod_DiversionRights_SetDiversionSystemFromList_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SetDiversionSystemFromList_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_ReadDiversionRightsFromHydroBase_String,this));
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_ReadDiversionRightsFromStateMod_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_SetDiversionRight_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SetDiversionRight_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_SortDiversionRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_SortDiversionRights_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_FillDiversionRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_FillDiversionRight_String,this));
	Commands_StateMod_DiversionRights_JMenu.addSeparator ();
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_WriteDiversionRightsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_WriteDiversionRightsToList_String,this));
	Commands_StateMod_DiversionRights_JMenu.add (
		__Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_DiversionRights_WriteDiversionRightsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_DiversionRights_JMenu,
		__Commands_StateMod_DiversionRights_CheckDiversionRights_String);
}

/**
Initialize the StateMod historical well pumping (monthly) command menus.
These can be used with StateMod or StateCU.
@param style Menu style (see MENU_STYLE_*).
@param parent_JMenu The JMenu to which submenus should be attached.
*/
private void ui_InitGUIMenus_Commands_StateMod_WellHistoricalPumpingTSMonthly ( int style, JMenu parent_JMenu ) {
	JMenu Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu (
		style, parent_JMenu, __Commands_StateMod_WellData_String,
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_String, false );
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputPeriod_String, this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_General_Running_SetOutputYearType_String, this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromList_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellStationsFromStateMod_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregate_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellAggregateFromList_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystem_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add(	new SimpleJMenuItem(
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellSystemFromList_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateCU_String,
		this));
	/* TODO - maybe support later.
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellHistoricalPumpingTSMonthlyFromStateMod_String,
		this));
	*/
	/* TODO - need to add fill.
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	__Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellRight_JMenuItem =
		new SimpleJMenuItem(
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellRight_String,this));
	*/
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthly_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellHistoricalPumpingTSMonthlyConstant_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyAverage_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyConstant_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadPatternFile_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_FillWellHistoricalPumpingTSMonthlyPattern_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_ReadWellRightsFromStateMod_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_LimitWellHistoricalPumpingTSMonthlyToRights_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SortWellHistoricalPumpingTSMonthly_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellHistoricalPumpingTSMonthlyToStateMod_String,
		this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationCapacitiesFromTS_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStation_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_SetWellStationsFromList_String,this));
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.addSeparator ();
	Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu.add (
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellHistoricalPumpingTSMonthly_WriteWellStationsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_WellHistoricalPumpingTSMonthly_JMenu,
		__Commands_StateMod_WellHistoricalPumpingTSMonthly_CheckWellHistoricalPumpingTSMonthly_String);
}

/**
Initialize the StateMod well rights command menus.  These can be used with StateMod or StateCU.
@param style Menu style (see MENU_STYLE_*).
@param parent_JMenu The JMenu to which submenus should be attached.
*/
private void ui_InitGUIMenus_Commands_StateMod_WellRights ( int style, JMenu parent_JMenu ) {
	JMenu Commands_StateMod_WellRights_JMenu = ui_InitGUIMenus_Commands_AddComponentMenu ( style,
		parent_JMenu, __Commands_StateMod_WellData_String, __Commands_StateMod_WellRights_String, false );
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadWellStationsFromList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadWellStationsFromList_String,this));
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadWellStationsFromNetwork_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadWellStationsFromNetwork_String,this));
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadWellStationsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadWellStationsFromStateMod_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SetWellAggregate_String,this));
	Commands_StateMod_WellRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SetWellAggregateFromList_String,this));
	Commands_StateMod_WellRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SetWellSystem_String,this));
	Commands_StateMod_WellRights_JMenu.add(
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SetWellSystemFromList_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadParcelsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadParcelsFromHydroBase_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadWellRightsFromHydroBase_String,this));
	Commands_StateMod_WellRights_JMenu.add (
		__Commands_StateMod_WellRights_ReadWellRightsFromStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_ReadWellRightsFromStateMod_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_SetWellRight_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SetWellRight_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_FillWellRight_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_FillWellRight_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_MergeWellRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellRights_MergeWellRights_String,this));
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_AggregateWellRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellRights_AggregateWellRights_String,this));
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_SortWellRights_JMenuItem=
		new SimpleJMenuItem(__Commands_StateMod_WellRights_SortWellRights_String,this));
	Commands_StateMod_WellRights_JMenu.addSeparator ();
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_WriteWellRightsToList_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_WriteWellRightsToList_String,this));
	Commands_StateMod_WellRights_JMenu.add (__Commands_StateMod_WellRights_WriteWellRightsToStateMod_JMenuItem =
		new SimpleJMenuItem(__Commands_StateMod_WellRights_WriteWellRightsToStateMod_String,this));
	ui_InitGUIMenus_Commands_AddCheckCommands ( Commands_StateMod_WellRights_JMenu,
		__Commands_StateMod_WellRights_CheckWellRights_String);
}

/**
 * Initialize the table command menus.  These can be used with StateMod or StateCU.
 * @param style Menu style (see MENU_STYLE_*).
 * @param parent_JMenu The JMenu to which submenus should be attached.
 */
private void ui_InitGUIMenus_Commands_Table ( JMenuBar menuBar, int style ) {
	if ( menuBar != null ) {
		// Initialization.
		menuBar.add( __Commands_Table_JMenu = new JMenu( __Commands_Table_String, true));
		__Commands_Table_JMenu.setToolTipText("Insert command into commands list (above first selected command, or at end).");
	}

	// TODO evaluate whether needed.
	//boolean show_all_commands = false; // True indicates that a command file has been opened directly.
	if ( (__statecuDatasetType == StateCU_DataSet.TYPE_UNKNOWN) && (__statecuDataset == null) ) {
		// Startup or user is editing commands directly without a data set.
		// If at initialization, all menus will be available but will be disabled.
		// If a command file is opened directly, then the GUI state will be checked and menus will be enabled.
		//show_all_commands = true;
	}

	// Response file submenu (will there be commands?).

	// Control file submenu (will there be commands?).

	// CU Locations Submenu.

	if ( __statecuDatasetType == StateCU_DataSet.TYPE_OTHER_USES ) {
		// Only for other uses.
		return;
	}

	// Add group menu for Create, Copy, Free Table.
	JMenu Commands_TableCreate_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
			__Commands_Table_JMenu, __Commands_TableCreate_String, false );
	// Add Commands
	Commands_TableCreate_JMenu.add( __Commands_TableCreate_NewTable_JMenuItem =
			new SimpleJMenuItem( __Commands_TableCreate_NewTable_String, this ));
	Commands_TableCreate_JMenu.add( __Commands_TableCreate_CopyTable_JMenuItem =
			new SimpleJMenuItem( __Commands_TableCreate_CopyTable_String, this ));
	// ----
	Commands_TableCreate_JMenu.addSeparator();
	Commands_TableCreate_JMenu.add( __Commands_TableCreate_FreeTable_JMenuItem =
			new SimpleJMenuItem( __Commands_TableCreate_FreeTable_String, this ));

	// Add group menu for Read Table.
	JMenu Commands_TableRead_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu ( style,
			__Commands_Table_JMenu, __Commands_TableRead_String, false );
	// Add Commands.
	Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromDataStore_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromDataStore_String, this));
	Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromDBF_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromDBF_String, this));
	Commands_TableRead_JMenu.add( __Commands_TableRead_ReadTableFromDelimitedFile_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromDelimitedFile_String, this));
	Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromExcel_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromExcel_String, this));
	Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromFixedFormatFile_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromFixedFormatFile_String, this));
	/*Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromJSON_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromJSON_String, this));
	Commands_TableRead_JMenu.add(__Commands_TableRead_ReadTableFromXML_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRead_ReadTableFromXML_String, this));*/

	// Add group menu for Append, Join Tables.
	JMenu Commands_TableJoin_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu( style,
			__Commands_Table_JMenu, __Commands_TableJoin_String, false);
	// Add Commands.
	Commands_TableJoin_JMenu.add(__Commands_TableJoin_AppendTable_JMenuItem =
			new SimpleJMenuItem(__Commands_TableJoin_AppendTable_String, this));
	Commands_TableJoin_JMenu.add(__Commands_TableJoin_JoinTables_JMenuItem =
			new SimpleJMenuItem(__Commands_TableJoin_JoinTables_String, this));

	// Add group menu for Manipulate Table Values.
	JMenu Commands_TableManipulate_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu( style,
			__Commands_Table_JMenu, __Commands_TableManipulate_String, false);
	// Add Commands.
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_InsertTableColumn_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_InsertTableColumn_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_DeleteTableColumns_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_DeleteTableColumns_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_DeleteTableRows_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_DeleteTableRows_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_FormatTableString_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_FormatTableString_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_ManipulateTableString_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_ManipulateTableString_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_SetTableValues_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_SetTableValues_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_SplitTableColumn_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_SplitTableColumn_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_TableMath_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_TableMath_String, this));
	/*Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_TableTimeSeriesMath_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_TableTimeSeriesMath_String, this));*/
	Commands_TableManipulate_JMenu.addSeparator();
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_InsertTableRow_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_InsertTableRow_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_SortTable_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_SortTable_String, this));
	Commands_TableManipulate_JMenu.add(__Commands_TableManipulate_SplitTableRow_JMenuItem =
			new SimpleJMenuItem(__Commands_TableManipulate_SplitTableRow_String, this));

	// Add group menu for Append, Join Tables.
	JMenu Commands_TableAnalyze_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu( style,
			__Commands_Table_JMenu, __Commands_TableAnalyze_String, false);
	// Add Commands.
	Commands_TableAnalyze_JMenu.add(__Commands_TableAnalyze_CompareTables_JMenuItem =
			new SimpleJMenuItem(__Commands_TableAnalyze_CompareTables_String, this));

	// Add group menu for Output Table.
	JMenu Commands_TableOutput_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu( style,
			__Commands_Table_JMenu, __Commands_TableOutput_String, false);
	// Add Commands
	/*Commands_TableOutput_JMenu.add(__Commands_TableOutput_WriteTableToDataStore_JMenuItem =
			new SimpleJMenuItem(__Commands_TableOutput_WriteTableToDataStore_String, this));*/
	Commands_TableOutput_JMenu.add(__Commands_TableOutput_WriteTableToDelimitedFile_JMenuItem =
			new SimpleJMenuItem(__Commands_TableOutput_WriteTableToDelimitedFile_String, this));
	Commands_TableOutput_JMenu.add(__Commands_TableOutput_WriteTableToExcel_JMenuItem =
			new SimpleJMenuItem(__Commands_TableOutput_WriteTableToExcel_String, this));
	Commands_TableOutput_JMenu.add(__Commands_TableOutput_WriteTableToHTML_JMenuItem =
			new SimpleJMenuItem(__Commands_TableOutput_WriteTableToHTML_String, this));

	// Add group menu for Running and Properties.
	JMenu Commands_TableRunning_JMenu = ui_InitGUIMenus_Commands_AddGroupMenu( style,
			__Commands_Table_JMenu, __Commands_TableRunning_String, false);
	// Add Commands
	Commands_TableRunning_JMenu.add(__Commands_TableRunning_SetPropertyFromTable_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRunning_SetPropertyFromTable_String, this));
	Commands_TableRunning_JMenu.add(__Commands_TableRunning_CopyPropertiesToTable_JMenuItem =
			new SimpleJMenuItem(__Commands_TableRunning_CopyPropertiesToTable_String, this));
}

/**
Initialize the Edit menu.
*/
private void ui_InitGUIMenus_Edit ( JMenuBar menuBar ) {
	JMenu edit_JMenu = new JMenu ("Edit", true);
	menuBar.add (edit_JMenu);
	edit_JMenu.add( __Edit_CutCommands_JMenuItem = new SimpleJMenuItem ( __Edit_CutCommands_String, this ) );
	edit_JMenu.add( __Edit_CopyCommands_JMenuItem = new SimpleJMenuItem ( __Edit_CopyCommands_String, this ));
	edit_JMenu.add( __Edit_PasteCommands_JMenuItem = new SimpleJMenuItem ( __Edit_PasteCommands_String, this ) );

	edit_JMenu.addSeparator();
	edit_JMenu.add( __Edit_DeleteCommands_JMenuItem = new SimpleJMenuItem (__Edit_DeleteCommands_String, this) );

	edit_JMenu.addSeparator();
	edit_JMenu.add( __Edit_SelectAllCommands_JMenuItem =
		new SimpleJMenuItem(__Edit_SelectAllCommands_String, this ) );
	edit_JMenu.add( __Edit_DeselectAllCommands_JMenuItem=
		new SimpleJMenuItem(__Edit_DeselectAllCommands_String, this ) );

	edit_JMenu.addSeparator();
	edit_JMenu.add( __Edit_CommandWithErrorChecking_JMenuItem =
		new SimpleJMenuItem ( __Edit_CommandWithErrorChecking_String,this ) );

	edit_JMenu.add(new SimpleJMenuItem( __Edit_CommandFile_String, this));

	edit_JMenu.addSeparator();
	edit_JMenu.add( __Edit_ConvertSelectedCommandsToComments_JMenuItem =
		new SimpleJMenuItem (__Edit_ConvertSelectedCommandsToComments_String, this ) );
	edit_JMenu.add( __Edit_ConvertSelectedCommandsFromComments_JMenuItem =
		new SimpleJMenuItem (__Edit_ConvertSelectedCommandsFromComments_String, this ) );
}

/**
Initialize the file menu.
@param menuBar The JMenuBar for the application.
If null, assume that the menus have been set up previously and now the "Save" menu sub-menus are being added for the current data set type.
*/
private void ui_InitGUIMenus_File ( JMenuBar menuBar ) {
	JMenu fileJMenu = null;
	if ( menuBar != null ) {
		fileJMenu = new JMenu (__File_String, true);
	}

	if ( menuBar != null ) {
		// Adding menus for the first time.

		// First add the Open.
		fileJMenu.add( __File_Open_JMenu = new JMenu ( __File_Open_String ));
		// Open...Command File...
		__File_Open_JMenu.add( __File_Open_CommandFile_JMenuItem =
			new SimpleJMenuItem( __File_Open_CommandFile_String,this));
		__File_Open_JMenu.addSeparator();
		// Open...DataSet.
		if ( __datasetFeaturesEnabled ) {
			__File_Open_JMenu.addSeparator();
			__File_Open_JMenu.add( __File_Open_DataSet_JMenuItem =
				new SimpleJMenuItem (__File_Open_DataSet_String,this) );

			__File_Open_JMenu.add( __File_Open_DataSetComponent_JMenu =
				new JMenu (__File_Open_DataSetComponent_String ) );
			if ( __appType == StateDMI.APP_TYPE_STATECU ) {
				// StateCU components.
				__File_Open_DataSetComponent_JMenu.add(
				new SimpleJMenuItem( __File_Open_DataSetComponent_StateCU_Locations_String, this));
				__File_Open_DataSetComponent_JMenu.add(
				new SimpleJMenuItem(__File_Open_DataSetComponent_StateCU_CropCharacteristics_String,this));
				__File_Open_DataSetComponent_JMenu.add(
				new SimpleJMenuItem(__File_Open_DataSetComponent_StateCU_BlaneyCriddle_String,this));
				//__File_Open_DataSetComponent_JMenu.add(
				//	new SimpleJMenuItem(__File_Open_DataSetComponent_StateCU_PenmanMonteith_String,this));
				__File_Open_DataSetComponent_JMenu.add(
				new SimpleJMenuItem(__File_Open_DataSetComponent_StateCU_ClimateStations_String,this));
			}
		}
		__File_Open_CommandFileRecent_JMenuItem = new JMenuItem[this.MAX_RECENT_FILES];
	    for ( int i = 0; i < this.MAX_RECENT_FILES; i++ ) {
		    __File_Open_JMenu.add( __File_Open_CommandFileRecent_JMenuItem[i] =
		    	new SimpleJMenuItem( "", this ) );
	    }

		__File_Open_JMenu.addSeparator ();
		__File_Open_JMenu.add( __File_Open_ModelNetwork_JMenuItem =
			new SimpleJMenuItem(__File_Open_ModelNetwork_String,this));
		__File_Open_JMenu.addSeparator ();
		__File_Open_JMenu.add( __File_Open_HydroBase_JMenuItem =
			new SimpleJMenuItem(__File_Open_HydroBase_String,this));

		ui_InitGUIMenus_File_OpenRecentFiles();

		//
		// DataSet menus.
		//
		__File_New_JMenu = new JMenu(MENU_File_New);
		fileJMenu.add(__File_New_JMenu);
		if ( __datasetFeaturesEnabled ) {
			__File_New_DataSet_JMenu = new JMenu(MENU_File_New_DataSet);
			__File_New_JMenu.add(__File_New_DataSet_JMenu);
			if ( __appType == StateDMI.APP_TYPE_STATECU ) {
				__File_New_DataSet_StateCU_ClimateStations_JMenu =
				new JMenu(MENU_File_New_DataSet_StateCU_ClimateStations);
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_ClimateStations_JMenu);
				__File_New_DataSet_StateCU_ClimateStations_FromList_JMenuItem =
				new SimpleJMenuItem(MENU_File_New_DataSet_StateCU_ClimateStations_FromList,
				MENU_File_New_DataSet_StateCU_ClimateStations_FromList,this);
				__File_New_DataSet_StateCU_ClimateStations_JMenu.add(
				__File_New_DataSet_StateCU_ClimateStations_FromList_JMenuItem);
				__File_New_DataSet_StateCU_ClimateStations_FromHydroBase_JMenuItem =
				new SimpleJMenuItem(MENU_File_New_DataSet_StateCU_ClimateStations_FromHydroBase,
				MENU_File_New_DataSet_StateCU_ClimateStations_FromHydroBase,this);
				__File_New_DataSet_StateCU_ClimateStations_JMenu.add(
				__File_New_DataSet_StateCU_ClimateStations_FromHydroBase_JMenuItem );

				__File_New_DataSet_StateCU_Structures_JMenu = new JMenu(MENU_File_New_DataSet_StateCU_Structures );
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_Structures_JMenu);
				__File_New_DataSet_StateCU_Structures_FromList_JMenuItem
				= new SimpleJMenuItem(MENU_File_New_DataSet_StateCU_Structures_FromList,
				MENU_File_New_DataSet_StateCU_Structures_FromList,this);
				__File_New_DataSet_StateCU_Structures_JMenu.add(
				__File_New_DataSet_StateCU_Structures_FromList_JMenuItem);

				__File_New_DataSet_StateCU_WaterSupplyLimited_JMenu=
				new JMenu(MENU_File_New_DataSet_StateCU_WaterSupplyLimited);
				__File_New_DataSet_StateCU_WaterSupplyLimited_JMenu.setEnabled ( false );
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_WaterSupplyLimited_JMenu);
				__File_New_DataSet_StateCU_WaterSupplyLimitedByRights_JMenu =
				new JMenu(MENU_File_New_DataSet_StateCU_WaterSupplyLimitedByWaterRights);
				__File_New_DataSet_StateCU_WaterSupplyLimitedByRights_JMenu.setEnabled ( false );
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_WaterSupplyLimitedByRights_JMenu);
				__File_New_DataSet_StateCU_RiverDepletion_JMenu=
				new JMenu(MENU_File_New_DataSet_StateCU_RiverDepletions);
				__File_New_DataSet_StateCU_RiverDepletion_JMenu.setEnabled ( false );
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_RiverDepletion_JMenu);
				__File_New_DataSet_JMenu.addSeparator();
				__File_New_DataSet_StateCU_OtherUses_JMenu=	new JMenu( MENU_File_New_DataSet_StateCU_OtherUses);
				__File_New_DataSet_StateCU_OtherUses_JMenu.setEnabled (	false );
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateCU_OtherUses_JMenu);
			}
			else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
				__File_New_DataSet_StateMod_Historical_JMenu =
				new JMenu(MENU_File_New_DataSet_StateMod_Historical);
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateMod_Historical_JMenu);
				__File_New_DataSet_StateMod_Demands_JMenu =	new JMenu( MENU_File_New_DataSet_StateMod_Demands);
				__File_New_DataSet_JMenu.add(__File_New_DataSet_StateMod_Demands_JMenu);
			}
			//
			// DataSetComponent menus.
			//
			__File_New_DataSetComponent_JMenu =	new JMenu(MENU_File_New_DataSetComponent);
			__File_New_JMenu.add(__File_New_DataSetComponent_JMenu);
			if ( __appType == StateDMI.APP_TYPE_STATECU ) {
				__File_New_DataSetComponent_StateCU_Locations_JMenu=
				new JMenu(MENU_File_New_DataSetComponent_StateCU_Locations);
				__File_New_DataSetComponent_JMenu.add(
				__File_New_DataSetComponent_StateCU_Locations_JMenu);
				__File_New_DataSetComponent_StateCU_Locations_FromList_JMenuItem=
				new SimpleJMenuItem(MENU_File_New_DataSetComponent_StateCU_Locations_FromList,
				MENU_File_New_DataSetComponent_StateCU_Locations_FromList,this);
				__File_New_DataSetComponent_StateCU_Locations_JMenu.add(
				__File_New_DataSetComponent_StateCU_Locations_FromList_JMenuItem);
				__File_New_DataSetComponent_StateCU_CropCharacteristics_JMenu=
				new JMenu(MENU_File_New_DataSetComponent_StateCU_CropCharacteristics);
				__File_New_DataSetComponent_JMenu.add(
				__File_New_DataSetComponent_StateCU_CropCharacteristics_JMenu);
				__File_New_DataSetComponent_StateCU_CropCharacteristics_FromList_JMenuItem=
				new SimpleJMenuItem(MENU_File_New_DataSetComponent_StateCU_CropCharacteristics_FromList,
				MENU_File_New_DataSetComponent_StateCU_CropCharacteristics_FromList,this);
				__File_New_DataSetComponent_StateCU_CropCharacteristics_JMenu.add(
				__File_New_DataSetComponent_StateCU_CropCharacteristics_FromList_JMenuItem);
				__File_New_DataSetComponent_StateCU_BlaneyCriddle_JMenu=
				new JMenu(MENU_File_New_DataSetComponent_StateCU_BlaneyCriddle);
				__File_New_DataSetComponent_JMenu.add(
				__File_New_DataSetComponent_StateCU_BlaneyCriddle_JMenu);
				__File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList_JMenuItem=
				new SimpleJMenuItem(MENU_File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList,
				MENU_File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList,this);
				__File_New_DataSetComponent_StateCU_BlaneyCriddle_JMenu.add(
				__File_New_DataSetComponent_StateCU_BlaneyCriddle_FromList_JMenuItem);
				__File_New_DataSetComponent_StateCU_ClimateStations_JMenu=
				new JMenu(MENU_File_New_DataSetComponent_StateCU_ClimateStations);
				__File_New_DataSetComponent_JMenu.add(
				__File_New_DataSetComponent_StateCU_ClimateStations_JMenu);
				__File_New_DataSetComponent_StateCU_ClimateStations_FromList_JMenuItem=
				new SimpleJMenuItem(MENU_File_New_DataSetComponent_StateCU_ClimateStations_FromList,
				MENU_File_New_DataSetComponent_StateCU_ClimateStations_FromList,this);
				__File_New_DataSetComponent_StateCU_ClimateStations_JMenu.add(
				__File_New_DataSetComponent_StateCU_ClimateStations_FromList_JMenuItem);
			}
		}
		__File_New_JMenu.add( __File_New_CommandFile_JMenuItem =
			new SimpleJMenuItem(__File_New_CommandFile_String, this) );
		__File_New_JMenu.add( __File_New_ModelNetwork_JMenuItem =
			new SimpleJMenuItem(__File_New_NewModelNetwork_String,this));
	}
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		if ( menuBar != null ) {
			// Define the main Save button for the first time around.
			fileJMenu.add ( __File_Save_JMenu =	new JMenu(__File_Save_String) );
		}
		// Now add the sub-menus...
		__File_Save_JMenu.add ( __File_Save_Commands_JMenuItem =
			new SimpleJMenuItem(__File_Save_Commands_String, this));
		__File_Save_JMenu.add (	__File_Save_CommandsAs_JMenuItem =
			new SimpleJMenuItem( __File_Save_CommandsAs_String,this));

		if ( __datasetFeaturesEnabled ) {
			__File_Save_JMenu.add (
				__File_Save_DataSet_JMenuItem = new SimpleJMenuItem(__File_Save_DataSet_String, this));

			/* TODO - SAM 2004-02-27 figure out what to do with this later.
			__File_Save_StateCU_All_JMenuItem = new SimpleJMenuItem(MENU_File_Save_StateCU_All,	this);
			__File_Save_JMenu.add (	__File_Save_StateCU_All_JMenuItem );
			__File_Save_JMenu.addSeparator ();
			__File_Save_StateCU_Response_JMenuItem = new SimpleJMenuItem(
				MENU_File_Save_StateCU_Response,this);
			__File_Save_JMenu.add (	__File_Save_StateCU_Response_JMenuItem );
			__File_Save_StateCU_Control_JMenuItem = new SimpleJMenuItem( MENU_File_Save_StateCU_Control, this);

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_OTHER_USES ) {
			}
			else {
				// Most data sets need the following, but not other uses?
				__File_Save_JMenu.add (	__File_Save_StateCU_Control_JMenuItem );
				__File_Save_StateCU_CULocations_JMenuItem =
				new SimpleJMenuItem(MENU_File_Save_StateCU_CULocations,	this);
				__File_Save_JMenu.add (__File_Save_StateCU_CULocations_JMenuItem );
				__File_Save_StateCU_CropCharacteristics_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_CropCharacteristics,	this);
				__File_Save_JMenu.add (	__File_Save_StateCU_CropCharacteristics_JMenuItem );
			__File_Save_StateCU_BlaneyCriddleCropCoefficients_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_BlaneyCriddleCropCoefficients,this);
				__File_Save_JMenu.add ( __File_Save_StateCU_BlaneyCriddleCropCoefficients_JMenuItem );
				__File_Save_StateCU_ClimateStations_JMenuItem =
					new SimpleJMenuItem(ENU_File_Save_StateCU_ClimateStations,	this);
				__File_Save_JMenu.add (	__File_Save_StateCU_ClimateStations_JMenuItem );
				__File_Save_StateCU_TemperatureTSMonthly_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_TemperatureTSMonthly,this);
				__File_Save_JMenu.add (	__File_Save_StateCU_TemperatureTSMonthly_JMenuItem );
				__File_Save_StateCU_YearlyFrostDatesTS_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_YearlyFrostDatesTS,this);
				__File_Save_JMenu.add (	__File_Save_StateCU_YearlyFrostDatesTS_JMenuItem );
				__File_Save_StateCU_MonthlyPrecipitationTS_JMenuItem =
					new SimpleJMenuItem( MENU_File_Save_StateCU_MonthlyPrecipitationTS, this);
				__File_Save_JMenu.add( __File_Save_StateCU_MonthlyPrecipitationTS_JMenuItem);
			}

			// Level 2 (Structures).

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_STRUCTURES ) {
				__File_Save_JMenu.addSeparator();
				__File_Save_StateCU_CropPatternTS_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_CropPatternTS,this);
				__File_Save_JMenu.add (	__File_Save_StateCU_CropPatternTS_JMenuItem );
			}

			// Level 3 (Water Supply Limited).

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED ) {
				__File_Save_JMenu.addSeparator();
			}

			// Level 4 (Water Supply Limited by Water Rights).

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_WATER_SUPPLY_LIMITED_BY_WATER_RIGHTS ) {
				__File_Save_JMenu.addSeparator();
			}

			// Level 5 (River Depletion).

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_RIVER_DEPLETION) {
				__File_Save_JMenu.addSeparator();
			}
			*/
		}

		fileJMenu.add( __File_Print_JMenu=new JMenu(__File_Print_String,true));
	    __File_Print_JMenu.add ( __File_Print_Commands_JMenuItem =
	        new SimpleJMenuItem( __File_Print_Commands_String,__File_Print_Commands_String, this ) );
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		if ( menuBar != null ) {
			// Define the main Save button for the first time around.
			fileJMenu.add ( __File_Save_JMenu =	new JMenu(__File_Save_String) );
		}

		__File_Save_JMenu.add ( __File_Save_Commands_JMenuItem =
			new SimpleJMenuItem( __File_Save_Commands_String, this) );
		__File_Save_JMenu.add ( __File_Save_CommandsAs_JMenuItem =
			new SimpleJMenuItem( __File_Save_CommandsAs_String, this));

		if ( __datasetFeaturesEnabled ) {
			/* TODO Now add the sub-menus.
			__File_Save_StateCU_DataSet_JMenuItem = new SimpleJMenuItem(
				MENU_File_Save_StateCU_DataSet, this);
			__File_Save_JMenu.add ( __File_Save_StateCU_DataSet_JMenuItem );
			__File_Save_StateCU_All_JMenuItem = new SimpleJMenuItem( MENU_File_Save_StateCU_All, this);
			__File_Save_JMenu.add ( __File_Save_StateCU_All_JMenuItem );
			__File_Save_JMenu.addSeparator ();
			__File_Save_StateCU_Response_JMenuItem = new SimpleJMenuItem(
				MENU_File_Save_StateCU_Response, this);
			__File_Save_JMenu.add ( __File_Save_StateCU_Response_JMenuItem );
			__File_Save_StateCU_Control_JMenuItem = new SimpleJMenuItem(
				MENU_File_Save_StateCU_Control,	this);

			if ( __statecu_dataset_type == StateCU_DataSet.TYPE_OTHER_USES ) {
			}
			else {
				// Most data sets need the following, but not other uses?
				__File_Save_JMenu.add (	__File_Save_StateCU_Control_JMenuItem );
				__File_Save_StateCU_CULocations_JMenuItem =
				new SimpleJMenuItem( MENU_File_Save_StateCU_CULocations, this);
				__File_Save_JMenu.add (	__File_Save_StateCU_CULocations_JMenuItem );
				__File_Save_StateCU_CropCharacteristics_JMenuItem =
					new SimpleJMenuItem( MENU_File_Save_StateCU_CropCharacteristics,	this);
				__File_Save_JMenu.add ( __File_Save_StateCU_CropCharacteristics_JMenuItem );
			__File_Save_StateCU_BlaneyCriddleCropCoefficients_JMenuItem =
					new SimpleJMenuItem( MENU_File_Save_StateCU_BlaneyCriddleCropCoefficients, this);
				__File_Save_JMenu.add ( __File_Save_StateCU_BlaneyCriddleCropCoefficients_JMenuItem );
				__File_Save_StateCU_ClimateStations_JMenuItem =
					new SimpleJMenuItem( MENU_File_Save_StateCU_ClimateStations, this);
				__File_Save_JMenu.add ( __File_Save_StateCU_ClimateStations_JMenuItem );
				__File_Save_StateCU_TemperatureTSMonthly_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_TemperatureTSMonthly,this);
				__File_Save_JMenu.add (	__File_Save_StateCU_TemperatureTSMonthly_JMenuItem );
				__File_Save_StateCU_YearlyFrostDatesTS_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_YearlyFrostDatesTS,this);
				__File_Save_JMenu.add ( __File_Save_StateCU_YearlyFrostDatesTS_JMenuItem );
				__File_Save_StateCU_MonthlyPrecipitationTS_JMenuItem =
					new SimpleJMenuItem(MENU_File_Save_StateCU_MonthlyPrecipitationTS,this);
				__File_Save_JMenu.add( __File_Save_StateCU_MonthlyPrecipitationTS_JMenuItem);
			}
			*/
		}
		fileJMenu.add( __File_Print_JMenu=new JMenu(__File_Print_String,true));
	    __File_Print_JMenu.add ( __File_Print_Commands_JMenuItem =
	        new SimpleJMenuItem( __File_Print_Commands_String,__File_Print_Commands_String, this ) );
	}

	if ( menuBar == null ) {
		// No further setup is required.
		return;
	}

	fileJMenu.addSeparator();
	fileJMenu.add ( __File_Properties_JMenu = new JMenu (__File_Properties_String) );
	__File_Properties_JMenu.add ( __File_Properties_HydroBase_JMenuItem =
		new SimpleJMenuItem( __File_Properties_HydroBase_String,this));
	if ( __datasetFeaturesEnabled ) {
		__File_Properties_JMenu.add ( __File_Properties_DataSet_JMenuItem =
			new SimpleJMenuItem( __File_Properties_DataSet_String,this));
	}
	// TODO smalers 2019-06-26 need to remove.
	//fileJMenu.add(__File_SetWorkingDirectory_JMenuItem = new SimpleJMenuItem( __File_SetWorkingDirectory_String, this));

	fileJMenu.addSeparator();
	fileJMenu.add(__File_SwitchToStateCU_JMenuItem = new SimpleJMenuItem(__File_SwitchToStateCU_String, this));
	fileJMenu.add(__File_SwitchToStateMod_JMenuItem = new SimpleJMenuItem(__File_SwitchToStateMod_String, this));

	fileJMenu.addSeparator();
	fileJMenu.add(__File_Exit_JMenuItem = new SimpleJMenuItem( __File_Exit_String, this));
	if ( IOUtil.testing() ) {
		fileJMenu.addSeparator();
		fileJMenu.add(__File_Test_JMenuItem = new SimpleJMenuItem( __File_Test_String, this));
	}
	menuBar.add(fileJMenu);
}

/**
 * Reset the file... Open...Command Files (Recent) menu items to recent files.
 */
private void ui_InitGUIMenus_File_OpenRecentFiles(){
	List<String> history = this.session.readHistory();
	for(int i = 0; i < this.MAX_RECENT_FILES; i++){
		String filename = "";
		if(i >= history.size()){
			filename = "";
		}
		else{
			// Long filenames will make the menu unwieldy so show the front and the back
			// TODO Find a way to replace parts of the path with "..." to shorten the menu.
			// Maybe add as an IOUtil method.
			filename = history.get(i);
		}
		__File_Open_CommandFileRecent_JMenuItem[i].setText(filename);
		__File_Open_CommandFileRecent_JMenuItem[i].setToolTipText(filename);
	}
}

/**
Initialize the Help menu.
*/
private void ui_InitGUIMenus_Help ( JMenuBar menuBar ) {
	JMenu helpJMenu = new JMenu("Help", true);
	helpJMenu.add( __Help_AboutStateDMI_JMenuItem = new SimpleJMenuItem(__Help_AboutStateDMI_String, this));
	File docFile = new File(IOUtil.verifyPathForOS(IOUtil.getApplicationHomeDir() + "/doc/UserManual/StateDMI.pdf",true));
	if ( docFile.exists() ) {
		helpJMenu.addSeparator();
	    // Old single-PDF help document.
	    helpJMenu.add ( __Help_ViewDocumentation_JMenuItem = new SimpleJMenuItem(__Help_ViewDocumentation_String,this));
		//helpJMenu.add ( __Help_ViewTrainingMaterials_JMenuItem = new SimpleJMenuItem(__Help_ViewTrainingMaterials_String,this));
	}

	// Newer convention where documents are split apart.
	helpJMenu.addSeparator();
	helpJMenu.add ( __Help_ViewDocumentation_ReleaseNotes_JMenuItem =
	   new SimpleJMenuItem(__Help_ViewDocumentation_ReleaseNotes_String,this));
    helpJMenu.add ( __Help_ViewDocumentation_UserManual_JMenuItem =
       new SimpleJMenuItem(__Help_ViewDocumentation_UserManual_String,this));
    helpJMenu.add ( __Help_ViewDocumentation_CommandReference_JMenuItem =
       new SimpleJMenuItem(__Help_ViewDocumentation_CommandReference_String,this));
    helpJMenu.add ( __Help_ViewDocumentation_DatastoreReference_JMenuItem =
       new SimpleJMenuItem(__Help_ViewDocumentation_DatastoreReference_String,this));
    helpJMenu.add ( __Help_ViewDocumentation_Troubleshooting_JMenuItem =
       new SimpleJMenuItem(__Help_ViewDocumentation_Troubleshooting_String,this));

	menuBar.add(helpJMenu);
}

/**
Define the popup menus for results other than StateCU and StateMod.
*/
private void ui_InitGUIMenus_ResultsPopup () {
	__resultsTables_JPopupMenu = new JPopupMenu("Table Results Actions");
    ActionListener_ResultsTables tables_l = new ActionListener_ResultsTables();
    __resultsTables_JPopupMenu = new JPopupMenu("Table Results Actions");
    __resultsTables_JPopupMenu.add( new SimpleJMenuItem ( __Results_Table_Properties_String, tables_l ) );
}

/**
Initialize the Results menu for StateCU.
*/
private void ui_InitGUIMenus_Results_StateCU ( JMenuBar menuBar ) {
	if ( menuBar != null ) {
		__Results_JMenu = new JMenu("Results", true);
		__Results_JMenu.setToolTipText ( "Use the Results choices at the bottom of the window." );
		menuBar.add(__Results_JMenu);
	}

	// All data sets need the following.

	__Results_StateCU_ControlData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateCU_ControlData,this);
	__Results_JMenu.add ( __Results_StateCU_ControlData_JMenuItem );

	if ( __statecuDatasetType == StateCU_DataSet.TYPE_OTHER_USES ) {
		// All the files for Other Uses.
	}

	if ( __statecuDatasetType != StateCU_DataSet.TYPE_OTHER_USES ) {
		__Results_StateCU_ClimateStationsData_JMenuItem =
			new SimpleJMenuItem(MENU_Results_StateCU_ClimateStationsData,this);
		__Results_JMenu.add(__Results_StateCU_ClimateStationsData_JMenuItem);

		__Results_StateCU_CropCharacteristicsData_JMenuItem =
			new SimpleJMenuItem(MENU_Results_StateCU_CropCharacteristicsData,this);
		__Results_JMenu.add(__Results_StateCU_CropCharacteristicsData_JMenuItem);
	}

	if ( __statecuDatasetType >= StateCU_DataSet.TYPE_RIVER_DEPLETION ) {
		__Results_StateCU_DelayTablesData_JMenuItem =
			new SimpleJMenuItem(MENU_Results_StateCU_DelayTablesData,this);
		__Results_JMenu.add (__Results_StateCU_DelayTablesData_JMenuItem );
	}

	if ( __statecuDatasetType != StateCU_DataSet.TYPE_OTHER_USES ) {
		__Results_StateCU_CULocationsData_JMenuItem =
			new SimpleJMenuItem(MENU_Results_StateCU_CULocationsData,this);
		__Results_JMenu.add(__Results_StateCU_CULocationsData_JMenuItem );
	}
}

/**
Initialize the Results menu for StateMod.
*/
private void ui_InitGUIMenus_Results_StateMod ( JMenuBar menuBar ) {
	if ( menuBar != null ) {
		__Results_JMenu = new JMenu("Results", true);
		__Results_JMenu.setToolTipText ("Use the Results choices at the bottom of the window." );
		menuBar.add(__Results_JMenu);
	}

	// River Data.

	__Results_StateMod_RiverData_JMenuItem = new SimpleJMenuItem(MENU_Results_StateMod_RiverData,this);
	__Results_JMenu.add(__Results_StateMod_RiverData_JMenuItem);

	// Delay Table Data.

	__Results_StateMod_DelayTableData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_DelayTableData,this);
	__Results_JMenu.add(__Results_StateMod_DelayTableData_JMenuItem);

	// Diversion Data.

	__Results_StateMod_DiversionData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_DiversionData,this);
	__Results_JMenu.add(__Results_StateMod_DiversionData_JMenuItem);

	// Precipitation Data.

	__Results_StateMod_PrecipitationData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_PrecipitationData,this);
	__Results_JMenu.add(__Results_StateMod_PrecipitationData_JMenuItem);

	// Evaporation Data.

	__Results_StateMod_EvaporationData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_EvaporationData,this);
	__Results_JMenu.add(__Results_StateMod_EvaporationData_JMenuItem);

	// Reservoir Data.

	__Results_StateMod_ReservoirData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_ReservoirData,this);
	__Results_JMenu.add(__Results_StateMod_ReservoirData_JMenuItem);

	// InstreamFlow Data.

	__Results_StateMod_InstreamFlowData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_InstreamFlowData,this);
	__Results_JMenu.add(__Results_StateMod_InstreamFlowData_JMenuItem);

	// Well Data.

	__Results_StateMod_WellData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_WellData,this);
	__Results_JMenu.add(__Results_StateMod_WellData_JMenuItem);

	// RiverNetwork Data.

	__Results_StateMod_RiverNetworkData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_RiverNetworkData,this);
	__Results_JMenu.add(__Results_StateMod_RiverNetworkData_JMenuItem);

	// Operational Data.

	__Results_StateMod_OperationalData_JMenuItem = new SimpleJMenuItem(
		MENU_Results_StateMod_OperationalData,this);
	__Results_JMenu.add(__Results_StateMod_OperationalData_JMenuItem);
}

/**
Initialize the Insert menu.
*/
private void ui_InitGUIMenus_Run ( JMenuBar menuBar ) {
	if ( menuBar != null ) {
		__Run_JMenu = new JMenu ("Run", true);
	}
	__Run_JMenu.add ( __Run_AllCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem(__Run_AllCommandsCreateOutput_String,this));
	__Run_JMenu.add ( __Run_AllCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem(__Run_AllCommandsIgnoreOutput_String,this));
	__Run_JMenu.add ( __Run_SelectedCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem(__Run_SelectedCommandsCreateOutput_String,this));
	__Run_JMenu.add ( __Run_SelectedCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem(__Run_SelectedCommandsIgnoreOutput_String,this));
	__Run_JMenu.add ( __Run_CancelCommandProcessing_JMenuItem =
		new SimpleJMenuItem(__Run_CancelCommandProcessing_String,this));
	__Run_JMenu.addSeparator();
	__Run_JMenu.add( __Run_CommandsFromFile_JMenuItem = new SimpleJMenuItem( __Run_CommandsFromFile_String, this));
		__Run_CommandsFromFile_JMenuItem.setEnabled ( false );
	__Run_JMenu.addSeparator();
	__Run_JMenu.add ( __Run_RunStateCUVersion_JMenuItem =
		new SimpleJMenuItem( __Run_RunStateCUVersion_String, this));
	__Run_RunStateCUVersion_JMenuItem.setEnabled ( false );
	__Run_JMenu.add( __Run_RunStateModVersion_JMenuItem =
		new SimpleJMenuItem(__Run_RunStateModVersion_String, this));
	if ( menuBar != null ) {
		menuBar.add(__Run_JMenu);
	}
}

/**
Initialize the Tools menu.
*/
private void ui_InitGUIMenus_Tools ( JMenuBar menuBar ) {
	__Tools_JMenu = new JMenu(__Tools_String, true);

	__Tools_JMenu.add ( __Tools_AdministrationNumberCalculator_JMenuItem =
		new SimpleJMenuItem (__Tools_AdministrationNumberCalculator_String, this ));

	__Tools_JMenu.addSeparator();
	__Tools_JMenu.add( __Tools_CompareFiles_JMenu = new JMenu( __Tools_CompareFiles_String, true));
	__Tools_CompareFiles_JMenu.add (__Tools_CompareFiles_StateModWellRights_JMenuItem =
		new SimpleJMenuItem (__Tools_CompareFiles_StateModWellRights_String, this ));

	__Tools_JMenu.addSeparator();
	__Tools_JMenu.add (	__Tools_ListSurfaceWaterDiversions_JMenuItem =
		new SimpleJMenuItem ( __Tools_ListSurfaceWaterDiversions_String, this ));
	__Tools_JMenu.add ( __Tools_ListWellStationRightTotals_JMenuItem =
		new SimpleJMenuItem (__Tools_ListWellStationRightTotals_String, this ));

	__Tools_JMenu.addSeparator();
	__Tools_JMenu.add ( __Tools_HydrobaseParcelWaterSupply_JMenuItem =
		new SimpleJMenuItem (__Tools_HydrobaseParcelWaterSupply_String, this ));

	/* TODO SAM 2010-01-15 Enable later.
	__Tools_JMenu.addSeparator();
	__Tools_JMenu.add ( __Tools_MergeListFileColumns_JMenuItem =
		new SimpleJMenuItem ( __Tools_MergeListFileColumns_String, this ));
		*/

	// Attach the diagnostics menu and set up the listener for the log file viewer.

	__Tools_JMenu.addSeparator();
	Message.addMessageLogListener ( this );
	DiagnosticsJFrame diagnosticsJFrame = new DiagnosticsJFrame(this);
	diagnosticsJFrame.attachMainMenu(__Tools_JMenu);
	__Tools_JMenu.add ( __Tools_ViewLogFile_Startup_JMenuItem =
		new SimpleJMenuItem (__Tools_ViewLogFile_Startup_String, this ));

	menuBar.add(__Tools_JMenu);
}

/**
Initialize the View menu.
*/
private void ui_InitGUIMenus_View ( JMenuBar menuBar ) {
	JMenu viewJMenu = new JMenu ("View", true);
	menuBar.add (viewJMenu);

    viewJMenu.add ( __View_CommandFileDiff_JMenuItem=new SimpleJMenuItem( __View_CommandFileDiff_String, this));
    __View_CommandFileDiff_JMenuItem.setToolTipText("Use visual diff program to compare current commands with last saved version.");

	viewJMenu.add ( __View_DataStores_JMenuItem=new SimpleJMenuItem( __View_DataStores_String, this));

	viewJMenu.add ( __View_Map_JCheckBoxMenuItem = new JCheckBoxMenuItem(__View_Map_String) );
	__View_Map_JCheckBoxMenuItem.setState ( false );
	__View_Map_JCheckBoxMenuItem.addItemListener ( this );

	viewJMenu.add ( __View_ModelNetwork_JCheckBoxMenuItem = new JCheckBoxMenuItem(__View_ModelNetwork_String) );
	__View_ModelNetwork_JCheckBoxMenuItem.setState ( false );
	__View_ModelNetwork_JCheckBoxMenuItem.addItemListener ( this );

	if ( __datasetFeaturesEnabled ) {
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			__View_DataSetManager_JCheckBoxMenuItem = new JCheckBoxMenuItem(__View_DataSetManager_String);
			__View_DataSetManager_JCheckBoxMenuItem.setState(false);
			__View_DataSetManager_JCheckBoxMenuItem.addItemListener(this);
			viewJMenu.add(__View_DataSetManager_JCheckBoxMenuItem );
		}
	}

	viewJMenu.add ( __View_ThreeLevelCommandsMenu_JCheckBoxMenuItem =
		new JCheckBoxMenuItem(__View_ThreeLevelCommandsMenu_String) );
	__View_ThreeLevelCommandsMenu_JCheckBoxMenuItem.setState ( true );
	__View_ThreeLevelCommandsMenu_JCheckBoxMenuItem.addItemListener ( this );

	/* TODO
	JCheckBoxMenuItem view_tree_JCheckBoxMenuItem = new JCheckBoxMenuItem(__View_Tree_String);
	view_tree_JCheckBoxMenuItem.setState ( false );
	view_tree_JCheckBoxMenuItem.setEnabled ( false );
	viewJMenu.add ( view_tree_JCheckBoxMenuItem );
	*/
}

/**
Load a command file and display in the command list.
@param command_file Full path to command file to load.
@param runOnLoad If true, the commands will be run after loading.
*/
private void ui_LoadCommandFile ( String command_file, boolean runOnLoad ) {
    String routine = "StateDMI_JFrame.ui_LoadCommandFile";
    int numAutoChanges = 0; // Number of lines automatically changed during load.
    try {
        numAutoChanges = commandProcessor_ReadCommandFile ( command_file );
        // Add CommandProgressListener for each command so GUI can listen to command progress.
        List<Command> commands = __statedmiProcessor.getCommands();
        int commandsSize = 0;
        if ( commands != null ) {
        	commandsSize = commands.size();
        }
        Command command = null;
        for ( int i = 0; i < commandsSize; i++ ) {
        	command = commands.get(i);
        	// TODO SAM 2009-03-23 Evaluate whether to define and interface rather than rely on AbstractCommand here.
        	if ( command instanceof AbstractCommand ) {
        		((AbstractCommand)command).addCommandProgressListener ( this );
        	}
        }
        // Repaint the list to reflect the status of the commands.
        ui_ShowCurrentCommandListStatus();
    }
    catch ( FileNotFoundException e ) {
        Message.printWarning ( 1, routine, "Command file \"" + command_file + "\" does not exist." );
        Message.printWarning ( 3, routine, e );
        // Previous contents will remain.
        return;
    }
    catch ( IOException e ) {
        Message.printWarning ( 1, routine, "Error reading command file \"" + command_file +
            "\".  List of commands may be incomplete." );
        Message.printWarning ( 3, routine, e );
        // Previous contents will remain.
        return;
    }
    catch ( Exception e ) {
        // FIXME SAM 2007-10-09 Perhaps should revert to previous data model contents?
    	// For now allow partical contents to be displayed.
        //
        // Error opening the file (should not happen but maybe a read permissions problem).
        Message.printWarning ( 1, routine,
        "Unexpected error reading command file \"" + command_file +
        "\".  Displaying commands that could be read." );
        Message.printWarning ( 3, routine, e );
    }
    // If successful the StateDMIProcessor, as the data model, will
    // have fired actions to make the JList update.
    commandList_SetCommandFileName(command_file);
    if ( numAutoChanges == 0 ) {
        commandList_SetDirty(false);
    }
    // Clear the old results.
    results_Clear();
    ui_UpdateStatusTextFields ( 2, null, null, "Use the Run menu/buttons to run the commands.", __STATUS_READY );
    __processor_JProgressBar.setValue ( 0 );
    __command_JProgressBar.setValue ( 0 );
    // If requested, run the commands.
    if ( runOnLoad ) {
        // Run all commands and create output.
        uiAction_RunCommands ( true, true );
        // This will update the status text fields.
    }
}

/**
Indicate whether running commands should occur in a thread. The default is always true.
@return true if the commands should be run in a thread, false if not.
*/
private boolean ui_Property_RunCommandProcessorInThread() {
	//String RunCommandProcessorInThread_String =
	    //__props.getValue ( TSTool_Options_JDialog.TSTool_RunCommandProcessorInThread );
	// FIXME SAM 2008-01-25 Evaluate whether StateDMI needs a Tools...Options menu.
	String RunCommandProcessorInThread_String = "True";
	if ( (RunCommandProcessorInThread_String != null) &&
			RunCommandProcessorInThread_String.equalsIgnoreCase("False") ) {
		return false;
	}
	else {
		// Default.
		return true;
	}
}

/**
Select the command and position the display at the command.
This is used, for example, with the log file viewer, when pointing back to a command that generated a log message.
@param iline Command position (0+).
*/
private void ui_SelectCommand ( int iline ) {
	__commands_JList.setSelectedIndex ( iline );
	ui_UpdateStatus ( true );
}

/**
Set the directory for the last "File...Open Command File".
@param Dir_LastCommandFileOpened Directory for last command file opened.
*/
private void ui_SetDir_LastCommandFileOpened ( String Dir_LastCommandFileOpened ) {
	__Dir_LastCommandFileOpened = Dir_LastCommandFileOpened;
	// Also set the last directory opened by a dialog.
	JGUIUtil.setLastFileDialogDirectory(Dir_LastCommandFileOpened);
}

/**
Set whether ActionEvents should be ignored (or not).
In general they should not be ignored but in some cases when programatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
private void ui_SetIgnoreActionEvent ( boolean ignore ) {
	__ignoreActionEvent = ignore;
}

/**
Set whether ItemEvents should be ignored (or not).
In general they should not be ignored but in some cases when programatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
private void ui_SetIgnoreItemEvent ( boolean ignore ) {
	__ignoreItemEvent = ignore;
}

/**
Set whether ListSelectionEvents should be ignored (or not).
In general they should not be ignored but in some cases when programatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
private void ui_SetIgnoreListSelectionEvent ( boolean ignore ) {
	__ignoreListSelectionEvent = ignore;
}

/**
Set the initial working directory,
which will be the software startup home or the location where the command file has been read/saved.
@param initialWorkingDir The initial working directory (should be non-null).
*/
private void ui_SetInitialWorkingDir ( String initialWorkingDir ) {
	String routine = getClass().getSimpleName() + ".ui_SetInitialWorkingDir";
	Message.printStatus(2, routine, "Setting the initial working directory to \"" + initialWorkingDir + "\"" );
	__initialWorkingDir = initialWorkingDir;
	// Also set in the processor.
	commandProcessor_SetInitialWorkingDir ( initialWorkingDir );
}

/**
Set the title of the input panel.
@param title the title for the input/query panel.  If null, use the default of "Input/Query Options..." with a black border.
@param color color of the line border.
*/
private void ui_SetInputPanelTitle ( String title, Color color ) {
    if ( title == null ) {
        title = "Input/Query Options";
        color = Color.black;
    }
    __queryInput_JPanel.setBorder( BorderFactory.createTitledBorder (
        BorderFactory.createLineBorder(color),title ));
}

/**
Update the command list to show the current status.
This is called after all commands have been processed in run mode(), when a command has been edited(),
and when loading commands from a file.
*/
private void ui_ShowCurrentCommandListStatus () {
    __commands_AnnotatedCommandJList.repaint();
}

/**
Some menus have prefixes like:
<ul>
<li> "1: " to help guide the user in using a group of commands</li>
<li> The "[Legacy]" string may also be used to indicate old commands.</li>
<li> The "[Legacy] 3:" string may also be used to indicate both of the above.</li>
</ul>
This method strips the leading text so that generic command parsing code will only see the normal command name.
Normally this is only called in when adding and editing a new command.
@param menuString a menu label with or without the prefix
@return the stripped menu label
*/
private String ui_StripMenuSequencePrefix ( String menuString ) {
	// First strip "[Legacy]".
	if ( menuString.startsWith("[Legacy]") ) {
		// Strip it
		menuString = menuString.substring(8).trim();
	}

	// Next strip number.
	if ( menuString.charAt(1) == ':') {
		// Strip it
		return menuString.substring(2).trim();
	}
	else {
		// Just return.
		return menuString;
	}
}

/**
Update the main status information when the list contents have changed.  Interface tasks include:
<ol>
<li>	Set the title bar.
	If no command file has been read, the title will be:  "StateDMI - no commands saved".
	If a command file has been read but not modified, the title will be:  "StateDMI - "filename"".
	If a command file has been read and modified, the title will be:
	"StateDMI - "filename" (modified)".
	</li>
<li>	Call updateLabels() to indicate the number of selected and total
	commands and set the general status to "Ready".
	</li>
<li>	Optionally, call checkGUIState() to reset menus, etc.  Note this should be called
	independently when the list appearance changes (selections, etc.).
	</li>
</ol>
@param checkGuiState If true, then the checkGUIState() method is also called,
which checks many interface settings.
*/
private void ui_UpdateStatus ( boolean checkGuiState ) {
	// Title bar (command file name).

	String app_type = "";
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		app_type = "StateCU";
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		app_type = "StateMod";
	}
	String session_type = "";
	if ( __datasetFeaturesEnabled ) {
		// Might be in data set mode.
		if ( __sessionType != __SESSION_UNKNOWN ) {
			session_type = getSessionTypeName();
			if ( __sessionType == __SESSION_DATA_SET ) {
				if ( __appType == StateDMI.APP_TYPE_STATECU ) {
					session_type = " " +
						StateCU_DataSet.lookupDataSetName ( __statecuDatasetType ) + " " + session_type;
				}
				else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
					// StateMod does not really have data set types like StateCU.
					//StateMod_DataSet.lookupDataSetName ( __statemod_dataset_type ) + " " +session_type;
					//session_type = " "+StateMod_DataSet.NAME_UNKNOWN;
					session_type = "";
				}
			}
		}
		else if ( __commandFileName != null ) {
			session_type = " - No data set, processing commands directly";
		}
		setTitle ( "StateDMI (" + app_type + session_type + ")" );
	}
	else {
		// Always processing command file.
		if ( __commandFileName == null ) {
			setTitle ( "StateDMI (" + app_type + session_type + ") - no commands saved");
		}
		else {
	        if ( __commandsDirty ) {
				setTitle ( "StateDMI (" + app_type + session_type + ") - " + __commandFileName + "\" (modified)");
			}
			else {
	            setTitle ( "StateDMI (" + app_type + session_type + ") - " + __commandFileName + "\"");
			}
		}
	}

	// Commands.

	int selected_indices[] = ui_GetCommandJList().getSelectedIndices();
	int selected_size = 0;
	if ( selected_indices != null ) {
		selected_size = selected_indices.length;
	}
	if ( __commands_JPanel != null ) {
    	__commands_JPanel.setBorder(
		BorderFactory.createTitledBorder (
		BorderFactory.createLineBorder(Color.black),
		"Commands (" + __commands_JListModel.size() +
		" commands, " + selected_size + " selected, " +
		commandList_GetFailureCount() + " with failures, " +
		commandList_GetWarningCount() + " with warnings)") );
	}

	// Update the text fields with the information from above.
	// Currently no need since set directly above.
	//ui_UpdateStatusTextFields ( -1, "StateDMI_JFrame.updateStatus", commands_label, null, __STATUS_READY );

	// FIXME SAM 2008-11-11 Why is this called no matter what is passed in for the parameter?
	// Update GUI state if requested.
	//if ( checkGuiState ) {
		ui_CheckGUIState ();
	//}
}

/**
Update the text fields at the bottom of the main interface.
This does NOT update all text fields like the number of commands, etc.
@param level Message level.  If > 0 and the message is not null, call Message.printStatus() to record a message.
@param routine Routine name used if Message.printStatus() is called.
@param commandPanelStatus If not null, update the __commands_JPanel border to contain this text.
If null, leave the contents as previously shown.  Specify "" to clear the text.
@param message If not null, update the __message_JTextField to contain this text.
If null, leave the contents as previously shown.  Specify "" to clear the text.
@param status If not null, update the __status_JTextField to contain this text.
If null, leave the contents as previously shown.  Specify "" to clear the text.
*/
private void ui_UpdateStatusTextFields ( int level, String routine,
				String commandPanelStatus, String message, String status ) {
	if ( (level > 0) && (message != null) ) {
		// Print a status message to the messaging system.
		Message.printStatus ( 1, routine, message );
	}
	if ( message != null ) {
		// If the message is too long it makes the progress bar get small (even though the progress bar is not resizable).
		// Set to a reasonable length.
		if ( message.length() > 120 ) {
			__message_JTextField.setText (message.substring(0,120) + "...");
		}
		else {
			__message_JTextField.setText (message);
		}
	}
	if ( commandPanelStatus != null ) {
		__commands_JPanel.setBorder ( BorderFactory.createTitledBorder (
		BorderFactory.createLineBorder(Color.black), "Commands:  " + commandPanelStatus) );
	}
	if ( status != null ) {
		__status_JTextField.setText (status);
	}
}

/**
Handle "File...Exit" and X actions.
*/
private void uiAction_CloseClicked () {
	// If the commands are dirty, see if they want to save them.
	// This code is also in openCommandFile - might be able to remove copy once all actions are implemented.
	if ( __commandsDirty ) {
		if ( __commandFileName == null ) {
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this,
				IOUtil.getProgramName(), "Do you want to save the changes to commands?\n\n" +
				"To view differences, Cancel and use View / Command File Diff.",
				ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				setDefaultCloseOperation( DO_NOTHING_ON_CLOSE);
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				// Prompt for the name and then save.
				uiAction_WriteCommandFile ( __commandFileName, true);
			}
		}
		else {
			// A command file exists...  Warn the user.
			// They can save to the existing file name or can cancel and File...Save As... to a different name.
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(),
				"Do you want to save the changes you made to\n\"" + __commandFileName + "\"?\n\n" +
				"To view differences, Cancel and use View / Command File Diff.",
				ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				setDefaultCloseOperation( DO_NOTHING_ON_CLOSE);
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				uiAction_WriteCommandFile (__commandFileName, false);
			}
			// Else if No will just exit below.
		}
	}
	// Now make sure the user wants to exit - they might have a lot of data processed.
	int x = new ResponseJDialog (this, "Exit StateDMI", "Are you sure you want to exit StateDMI?",
		ResponseJDialog.YES| ResponseJDialog.NO).response();
	if (x == ResponseJDialog.YES) {
		setDefaultCloseOperation(DISPOSE_ON_CLOSE);
		setVisible(false);
		dispose();
		Message.closeLogFile();
		System.exit(0);
	}
	else {
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
	}
}

/**
Convert selected commands to/from comments.  When converting to commands:
Each Command instance is retrieved, its command string is taken from the Command,
and a new GenericCommand is create, and the original Command is replaced in the list.
When converting from commands, the GenericCommand is retrieved, a new Command instance is created, the original Command is replaced.
@param to_comment If true, convert commands to comments, if false, from comments.
*/
private void uiAction_ConvertCommandsToComments ( boolean to_comment ) {
	int selected_indexes[] = ui_GetCommandJList().getSelectedIndices();
	int selected_size = JGUIUtil.selectedSize ( ui_GetCommandJList() );
	String old_command_string = null;
	Command old_command = null;
	Command new_command = null;
	// It is OK to loop through each item below.  Even though the items in the data model will change,
	// if a command is replaced each time, the indices will still be relevant.
	for ( int i = 0; i < selected_size; i++ ) {
		old_command = (Command)__commands_JListModel.get(selected_indexes[i]);
		old_command_string = (String)old_command.toString();
		if ( to_comment ) {
			// Replace the current command with a new string that has the comment character.
			new_command = commandList_NewCommand(
					"# " + old_command_string,	// New command as comment.
					true );	// Create the command even if not recognized.
			commandList_ReplaceCommand ( old_command, new_command );
		}
		else {
		    // Remove comment.
			if ( old_command_string.startsWith("#") ) {
				new_command = commandList_NewCommand(
					old_command_string.substring(1).trim(),	// New command as comment.
					true );	// Create the command even if not recognized.
				commandList_ReplaceCommand ( old_command, new_command );
			}
		}
	}
	// Mark the commands as dirty.
	if ( selected_size > 0 ) {
		commandList_SetDirty ( true );
	}
}

/**
Get the selected commands from the commands list, clone a copy, and save in the cut buffer.
The commands can then be pasted into the command list with uiAction_PasteFromCutBufferToCommandList.
@param remove_original If true, then this is a Cut operation and the original commands should be removed from the list.
If false, a copy is made but the original commands will remain in the list.
*/
private void uiAction_CopyFromCommandListToCutBuffer ( boolean remove_original ) {
	int size = 0;
	int [] selected_indices = ui_GetCommandJList().getSelectedIndices();
	if ( selected_indices != null ) {
		size = selected_indices.length;
	}
	if ( size == 0 ) {
		return;
	}

	// Clear what may previously have been in the cut buffer.
	__commandsCutBuffer.clear();

	// Transfer Command instances to the cut buffer.
	Command command = null;	// Command instance to process.
	for ( int i = 0; i < size; i++ ) {
		command = (Command)__commands_JListModel.get(selected_indices[i]);
		__commandsCutBuffer.add ( (Command)command.clone() );
	}

	if ( remove_original ) {
		// If removing, delete the selected commands from the list.
		commandList_RemoveCommandsBasedOnUI();
	}
}

/**
The datastore choice has been clicked so process the event.
The only entry point to this method is if the user actually clicks on the choice.
In this case, the input type/name choices will be set to blank because the user has made a decision to work with a datastore.
If they subsequently choose to work with an input type, then they would select an input and the datastore choice would be blanked.
*/
private void uiAction_DataStoreChoiceClicked() {
    //String routine = getClass().getSimpleName() + ".uiAction_DataStoreChoiceClicked";
    /*if ( __dataStore_JComboBox == null ) {
        if ( Message.isDebugOn ) {
            Message.printDebug ( 1, routine, "Datastore has been selected but GUI is not yet initialized - no action taken in response to datastore selection.");
        }
        return; // Not done initializing.
    }
    // TODO SAM 2015-02-15 Need a graceful way to hide the following but set text to blank as work-around.
    // Otherwise, some of the text shows through behind the datastore panel.
    __dataStoreInitializing_JLabel.setText("");
    String selectedDataStoreName = __dataStore_JComboBox.getSelected();
    Message.printStatus(2, routine, "Selected datastore \"" + selectedDataStoreName + "\"." );
    if ( selectedDataStoreName.equals("") ) {
        // Selected blank for some reason - do nothing.
        return;
    }
    DataStore selectedDataStore = ui_GetSelectedDataStore();
    // This will select blank input type and name so that the focus is on the selected datastore.
    uiAction_InputTypeChoiceClicked(selectedDataStore);
    // Now fully initialize the input/query information based on the datastore.
    try {
        if ( selectedDataStore instanceof ColoradoHydroBaseRestDataStore ) {
            uiAction_SelectDataStore_ColoradoHydroBaseRest ( (ColoradoHydroBaseRestDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ColoradoWaterHBGuestDataStore ) {
            uiAction_SelectDataStore_ColoradoWaterHBGuest ( (ColoradoWaterHBGuestDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ColoradoWaterSMSDataStore ) {
            uiAction_SelectDataStore_ColoradoWaterSMS ( (ColoradoWaterSMSDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof GenericDatabaseDataStore ) {
            uiAction_SelectDataStore_GenericDatabaseDataStore ( (GenericDatabaseDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof HydroBaseDataStore ) {
            uiAction_SelectDataStore_HydroBase ( (HydroBaseDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof RccAcisDataStore ) {
            uiAction_SelectDataStore_RccAcis ( (RccAcisDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ReclamationHDBDataStore ) {
            uiAction_SelectDataStore_ReclamationHDB ( (ReclamationHDBDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ReclamationPiscesDataStore ) {
            uiAction_SelectDataStore_ReclamationPisces ( (ReclamationPiscesDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof RiversideDBDataStore ) {
            uiAction_SelectDataStore_RiversideDB ( (RiversideDBDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisDailyDataStore ) {
            uiAction_SelectDataStore_UsgsNwisDaily ( (UsgsNwisDailyDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisGroundwaterDataStore ) {
            uiAction_SelectDataStore_UsgsNwisGroundwater ( (UsgsNwisGroundwaterDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisInstantaneousDataStore ) {
            uiAction_SelectDataStore_UsgsNwisInstantaneous ( (UsgsNwisInstantaneousDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof PluginDataStore ) {
        	// Handle plugin
        	uiAction_SelectDataStore_Plugin ( selectedDataStore );
         }
        // The above does not select the input filter so do that next...
        ui_SetInputFilterForSelections();
    }
    catch ( Exception e ) {
        Message.printWarning( 2, routine, "Error selecting datastore \"" + selectedDataStore.getName() + "\"" );
        Message.printWarning ( 3, routine, e );
    }*/
}

/**
Deselect all commands in the commands list.  This occurs in response to a user selecting a menu choice.
*/
private void uiAction_DeselectAllCommands() {
	__commands_JList.clearSelection();
	// TODO SAM 2007-08-31 Should add list seletion listener to handle updateStatus call.
	ui_UpdateStatus ( false );
}

/**
Carry out the edit command action, triggered by:
<ol>
<li>	Popup menu edit of a command on the command list.</li>
<li>	Pressing the enter key on the command list.</li>
<li>	Double-clicking on a command in the command list.</li>
</ol>
This method will call the uiAction_EditCommand() method with a list of commands that were selected to be edited.
Multiple commands may be edited if a block of # delimited comments.
*/
private void uiAction_EditCommand () {
	int selected_size = 0;
	int [] selected = ui_GetCommandJList().getSelectedIndices();
	if ( selected != null ) {
		selected_size = selected.length;
	}
	if ( selected_size > 0 ) {
		Command command = (Command)__commands_JListModel.get(selected[0]);
		List<Command> v = null;
		if ( command instanceof Comment_Command ) {
			// Allow multiple lines to be edited in a comment.
			// This is handled in the called method, which brings up a multi-line editor for comments.
            // Only edit the contiguous # block. The first one is a # but stop adding when lines no longer start with #.
			v = new ArrayList ( selected_size );
			for ( int i = 0; i < selected_size; i++ ) {
				command = (Command)__commands_JListModel.get(selected[i]);
				if ( !(command instanceof Comment_Command) ) {
					break;
				}
				// Else add command to the list.
				v.add ( command );
			}
		}
		else {
            // Commands are one line.
			v = new ArrayList<>(1);
			v.add ( command );
		}
		commandList_EditCommand ( "", v, __UPDATE_COMMAND ); // No action event from menus
	}
}

/**
Create a new command file.  If any existing commands have been modified the user has the option of saving.
Then, the existing commands are cleared and the command file name is reset to null.
*/
private void uiAction_NewCommandFile () {
	// See whether the old commands need to be cleared.
	// This same code is in openCommandFile() - may be able to combine once all actions are in place.
	if ( __commandsDirty ) {
		if ( __commandFileName == null ) {
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(),
				"Do you want to save the changes you made?\n\n" +
				"To view differences, Cancel and use View / Command File Diff.",
				ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				// Prompt for the name and then save.
				uiAction_WriteCommandFile ( __commandFileName, true);
			}
		}
		else {
			// A command file exists...  Warn the user.
			// They can save to the existing file name or can cancel and File...Save As... to a different name.
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this,	IOUtil.getProgramName(),
				"Do you want to save the changes you made to\n\"" + __commandFileName + "\"?\n\n" +
				"To view differences, Cancel and use View / Command File Diff.",
				ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				uiAction_WriteCommandFile ( __commandFileName,false);
			}
			// Else if No will clear below.
		}
	}

	// Now clear the commands and reset the name to null.

	commandList_RemoveAllCommands ();
	commandList_SetDirty ( false );	// deleteCommands() sets to true but
					// since we are clearing the name, the commands re not dirty.
	commandList_SetCommandFileName ( null );
	results_Clear();
}

/**
Open a command file and read into the list of commands.
A check is made to see if the list contains anything and if it does the user is prompted as to
whether need to save the previous commands.
*/
private void uiAction_OpenCommandFile ( String commandFile, boolean runDiscoveryOnLoad)
{	String routine = getClass().getSimpleName() + ".uiAction_OpenCommandFile";
	// See whether the old commands need to be cleared.
	if ( __commandsDirty ) {
		if ( __commandFileName == null ) {
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(),
				"Do you want to save the changes you made?\n\n" +
				"To view differences, Cancel and use View / Command File Diff.",
				ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				// Prompt for the name and then save.
				uiAction_WriteCommandFile ( __commandFileName, true);
			}
		}
		else {
			// A command file exists...  Warn the user.
			// They can save to the existing file name or can cancel and File...Save As... to a different name.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
			    if ( __statedmiProcessor.getReadOnly() ) {
                    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                        "Do you want to save the changes you made to:\n"
                        + "\"" + __commandFileName + "\"?\n\n" +
                        "The commands are marked read-only.\n" +
                        "Press Yes to update the read-only file before opening a new file.\n" +
                        "Press No to discard edits before opening a new file.\n" +
                        "Press Cancel and then save to a new name if desired.\n" +
                        "To view differences, Cancel and use View / Command File Diff.",
                        ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			    }
			    else {
    				x = new ResponseJDialog ( this,	IOUtil.getProgramName(),
    				"Do you want to save the changes you made to:\n"
    				+ "\"" + __commandFileName + "\"?\n\n" +
    				"To view differences, Cancel and use View / Command File Diff.",
    				ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			    }
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				uiAction_WriteCommandFile ( __commandFileName,false);
			}
			// Else if No or OK will clear below before opening the other file.
		}
	}

	// Get the file.  Do not clear the list until the file has been chosen and is readable.
	if( commandFile == null){
		String initial_dir = ui_GetDir_LastCommandFileOpened();
		Message.printStatus ( 2, routine, "Initial directory for browsing:  \"" + initial_dir + "\"" );
		JFileChooser fc = JFileChooserFactory.createJFileChooser ( initial_dir );
		fc.setDialogTitle("Open " + IOUtil.getProgramName() + " Command File");
		List<String> extensionList = new ArrayList<>();
		extensionList.add("statedmi");
		extensionList.add("StateDMI");
		SimpleFileFilter sff = new SimpleFileFilter(extensionList, "StateDMI Command File");
		fc.addChoosableFileFilter(sff);
		fc.setFileFilter(sff);
		if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
			// If the user approves a selection do the following.
			String directory = fc.getSelectedFile().getParent();
			String path = fc.getSelectedFile().getPath();

			// TODO - is this necessary in Swing?
			// Set the "WorkingDir" property, which will NOT contain a trailing separator.
			IOUtil.setProgramWorkingDir(directory);
			ui_SetDir_LastCommandFileOpened(directory);
			__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
			ui_SetInitialWorkingDir ( __props.getValue ( "WorkingDir" ) );
			Message.printStatus(2, routine,
				"Working directory (and initial working directory) from command file is \"" +
				IOUtil.getProgramWorkingDir() );
			this.session.pushHistory(path);
			// Update the recent files in the File...Open menu, for the next menu access.
			ui_InitGUIMenus_File_OpenRecentFiles();
			// Load but do not automatically run.
			ui_LoadCommandFile ( path, false );
		}
	}
	else{
		// Set some state information, similar to above, but no need to update menus since picking from visible choice.
    	// TODO SAM 2014-12-19 maybe this information should be saved in the TSToolSession instance.
    	File f = new File(commandFile);
    	String directory = f.getParent();
		IOUtil.setProgramWorkingDir(directory);
		ui_SetDir_LastCommandFileOpened(directory);
		__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
		ui_SetInitialWorkingDir ( __props.getValue ( "WorkingDir" ) );
		// Save in the session.
		this.session.pushHistory(commandFile);
		// Update the recent files in the File...Open menu, for the next menu access.
		ui_InitGUIMenus_File_OpenRecentFiles();
    	// Load but do not automatically run.
    	ui_LoadCommandFile ( commandFile, false);
	}
	// New file has been opened or there was a cancel/error and the old list remains.
	//Message.printStatus ( 2, routine, "Done reading commands.  Calling ui_UpdateStatus...");
	ui_UpdateStatus ( true );
	//Message.printStatus ( 2, routine, "Back from update status." );
}

/**
Open the GeoView JFrame.  This method may be called due to a change of the
View... Map Interface status or because spatial data are detected in a data set
and are displayed automatically.
@param is_visible Indicates whether the GeoView should be visible at creation.
*/
private void uiAction_OpenGeoView ( boolean is_visible )
{	try {
		if ( __geoview_JFrame != null ) {
			// Just set the map visible...
			__geoview_JFrame.setVisible ( is_visible );
			// Make sure it is selected...
			__View_Map_JCheckBoxMenuItem.setSelected (
			true );
		}
		else {
			// No existing GeoView so create one.
			__geoview_JFrame = new GeoViewJFrame ( this, null );
			__geoview_JFrame.setVisible ( is_visible );
			// Add a window listener so StateDMI can listen for when the GeoView closes.
			__geoview_JFrame.addWindowListener ( this );
			JGUIUtil.center ( __geoview_JFrame );
			// Make sure it is selected.
			__View_Map_JCheckBoxMenuItem.setSelected (true );
		}
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, "StateDMI", "Error displaying map interface." );
		__geoview_JFrame = null;
	}
}

/**
Create a new HydroBaseDMI instance with a connection to the HydroBase database.
*/
private void uiAction_OpenHydroBase ()
{	String routine = "StateDMI_JFrame.openHydroBase";
	Message.printStatus(2, routine, "Opening HydroBase using configuration properties in \"" +
		HydroBase_Util.getConfigurationFile() + "\"" );
	String hbcfg = HydroBase_Util.getConfigurationFile();
	// FIXME SAM 2008-11-19 Fix similar to TSTool where batch is separate.
	if ( IOUtil.isBatch() || StateDMI.runGUIWithSelectedCommandFile  ) {
		// Running in batch mode or without a main GUI so automatically open HydroBase from the TSTool.cfg file information.
		// Get the input needed to process the file.
		PropList props = null;
		if ( IOUtil.fileExists(hbcfg) ) {
			// Use the configuration file to get HydroBase properties.
			try {
				props = HydroBase_Util.readConfiguration(hbcfg);
			}
			catch ( Exception e ) {
				Message.printWarning ( 1, routine,
				"Error reading HydroBase configuration file \""+
				hbcfg + "\".  Using defaults for HydroBase." );
				Message.printWarning ( 3, routine, e );
				props = null;
			}
		}

		try {
			// Now open the database.
			// This uses the guest login.  If properties were not found, then default HydroBase information will be used.
			__hbdmi = new HydroBaseDMI ( props );
			__hbdmi.open();
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error opening HydroBase.  HydroBase features will be disabled." );
			Message.printWarning ( 3, routine, e );
			__hbdmi = null;
		}
	}
	else {
		// Display the dialog to select the database.
		// This is a modal dialog that will not allow anything else to occur until the information is entered.
		// Use a PropList to pass information because there are a lot of parameters and the list may change in the future.

		if ( !IOUtil.fileExists(hbcfg) ) {
			// No HydroBase configuration file so don't create the connection.
			__hbdmi = null;
			return;
		}

		PropList props = new PropList ( "SelectHydroBase" );
		props.set ( "ValidateLogin", "false" );
		props.set ( "ShowWaterDivisions", "false" );
		props.set ( "ShowModels", "true" );

		// Pass in the previous HydroBaseDMI so that its information can be displayed as the initial values.

		SelectHydroBaseJDialog selectHydroBaseJDialog = null;
		try {
			selectHydroBaseJDialog = new SelectHydroBaseJDialog ( this, __hbdmi, props );

			// After getting to here, the dialog has been closed.  The HydroBaseDMI from the dialog can be retrieved and used.

			__hbdmi = selectHydroBaseJDialog.getHydroBaseDMI();
			// Set the HydroBaseDMI for the command processor.
			commandProcessor_SetHydroBaseDMI ( __hbdmi );

			if ( __hbdmi == null ) {
				Message.printWarning ( 1, routine, "HydroBase features will be disabled." );
			}

			// Define datastores if indicated in the HydroBase selector dialog.

			if ( selectHydroBaseJDialog.getDefineHydroBaseDatastore() ) {
				// Unlike TSTool there are not input filter UI elements to coordinate with.
				// Therefore just add or replace the datastore matching name 'HydroBase'.
				uiAction_OpenHydroBaseDataStore("HydroBase", "", __hbdmi);
			}
			Message.printStatus(2, routine, "After opening HydroBase datastore HydroBaseDMI is open:  " + __hbdmi.isOpen());
			Message.printStatus(2, routine, "After opening HydroBase datastore HydroBaseDMI is closed:  " + __hbdmi.getConnection().isClosed());

			if ( selectHydroBaseJDialog.getDefineHydroBaseVersionDatastore() ) {
				String version = this.__hbdmi.getDatabaseVersionFromName();
				uiAction_OpenHydroBaseDataStore("HydroBase", version, __hbdmi);
			}
			Message.printStatus(2, routine, "After opening HydroBase version datastore HydroBaseDMI is open:  " + __hbdmi.isOpen());
			Message.printStatus(2, routine, "After opening HydroBase version datastore HydroBaseDMI is closed:  " + __hbdmi.getConnection().isClosed());

			// Set the initial model to that specified by the user.
			String model = selectHydroBaseJDialog.getSelectedModel();
			if ( model.equalsIgnoreCase("StateCU") ) {
				uiAction_SwitchAppType ( StateDMI.APP_TYPE_STATECU );
			}
			else if ( model.equalsIgnoreCase("StateMod") ) {
				uiAction_SwitchAppType ( StateDMI.APP_TYPE_STATEMOD );
			}
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "HydroBase features will be disabled." );
			Message.printWarning ( 2, routine, e );
			__hbdmi = null;
		}
		ui_CheckGUIState();	// To update File...Properties...HydroBase.
	}
}

/**
 * Open a HydroBase datastore given its name.
 * @param baseName base datastore name, should be 'HydroBase'.
 * @param version database version to add to baseName, empty for 'HydroBase' and format 'YYYYMMDD' for datastore 'HydroBaseYYYYMMDD'.
 * @param dmi HydroBaseDMI to use in the datastore.
 */
private void uiAction_OpenHydroBaseDataStore(String baseName, String version, HydroBaseDMI dmi) {
	String routine = getClass().getSimpleName() + ".openHydroBaseDataStore";

	HydroBaseDataStore ds = null;
	String name = null;
	try {
		String description = null;
		if ( (version == null) || version.isEmpty() ) {
			name = "HydroBase";
			description = "HydroBase datastore using default name 'HydroBase'.";
		}
		else {
			name = "HydroBase" + version;
			description = "HydroBase datastore using name 'HydroBase' with version " + version + ".";
		}

		// See if a datastore exists for the requested name.
		DataStore dataStore = ((StateDMI_Processor)this.__statedmiProcessor).getDataStoreForName (
			"HydroBase", DatabaseDataStore.class );

		if ( dataStore != null ) {
			// Close the existing datastore/database.
			// Actually don't need to do anything because resetting below will replace the datastore instance in the processor.
			Message.printStatus(2, routine, "Detected exising datastore name \"" + name
				+ "\" - will replace in processor.");
		}

		// Open the new datastore.
		ds = new HydroBaseDataStore( name, description, dmi );
		// TODO smalers 2021-01-03 don't set a message because it is interpreted as an error.
		//ds.setStatusMessage("Opened based on SelectHydroBase login dialog input.");
		// Set the datastore in the processor.
		// TODO SAM 2021-01-03 property does not handled boolean so call method directly.
		//this.__statedmiProcessor.setPropContents ( "DataStore", ds );
		boolean closeOld = false;
		this.__statedmiProcessor.setDataStore( ds, closeOld );
	}
	catch ( Exception e ) {
		String message = "Error creating datastore \"" + name + "\" (" + e + ").";
		Message.printWarning ( 2, routine, message );
	}
}

/**
Create a new model network file and display.
*/
private void uiAction_OpenModelNetwork () {
	String routine = getClass().getSimpleName() + ".uiAction_openModelNetwork";

	// If the network exists, clear it.

	StateMod_NodeNetwork network = getModelNetwork();
	if ( (__network_JFrame != null) && (network != null) && __network_JFrame.isDirty() ) {
		// Warn the user to save.
		int x = ResponseJDialog.NO;
		if ( __commands_JListModel.size() > 0 ) {
			x = new ResponseJDialog ( this,	IOUtil.getProgramName(),
			"The network has been modified.  Open a new network without saving changes?",
			ResponseJDialog.YES| ResponseJDialog.CANCEL).response();
		}
		if ( x == ResponseJDialog.CANCEL ) {
			return;
		}

		// Close the old frame.

		__network_JFrame.dispose();
	}

	// Now prompt for the new file.

	JFileChooser fc = JFileChooserFactory.createJFileChooser ( JGUIUtil.getLastFileDialogDirectory() );
	fc.setDialogTitle("Select Model Network File");
	SimpleFileFilter sff = new SimpleFileFilter("net", "Makenet Network File");
	fc.addChoosableFileFilter(sff);
	// TODO SAM 2007-06-26 Evaluate why not used.
	//SimpleFileFilter xml_sff = new SimpleFileFilter("net","StateMod XML Network File");
	fc.addChoosableFileFilter(sff);
	fc.setFileFilter(sff);
	fc.setDialogType(JFileChooser.OPEN_DIALOG);
	if ( fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION ) {
		// Cancel...
		__View_ModelNetwork_JCheckBoxMenuItem.setState( false);
		return;
	}
	JGUIUtil.setLastFileDialogDirectory(fc.getSelectedFile().getParent());
	String filename = fc.getSelectedFile().getPath();

	try {
		__network_JFrame = new StateMod_Network_JFrame(	new StateDMI_NodeDataProvider(__hbdmi), filename );
		__network_JFrame.setSaveOnExit(true);
		__network_JFrame.addWindowListener(this);
	}
	catch (Exception ex) {
		Message.printWarning(1, routine, "Error displaying the network." );
		Message.printWarning(2, routine, ex);
		__network_JFrame = null;
		__View_ModelNetwork_JCheckBoxMenuItem.setState( false);
	}
}

/**
Select a new model network file and open the model network GUI with the ability to create a new network.
*/
private void uiAction_OpenNewModelNetwork() {
	String routine = getClass().getSimpleName() + ".uiAction_OpenNewModelNetwork()";

	// If the network exists, clear it.
	StateMod_NodeNetwork network = getModelNetwork();

	if ((__network_JFrame != null) && (network != null) && __network_JFrame.isDirty()) {
		// Warn the user to save.
		int x = ResponseJDialog.NO;
		if (__commands_JListModel.size() > 0) {
			x = new ResponseJDialog(this, IOUtil.getProgramName(),
				"The network has been modified.  Open a new network without saving changes?",
				ResponseJDialog.YES | ResponseJDialog.CANCEL).response();
		}
		if (x == ResponseJDialog.CANCEL) {
			return;
		}

		// Close the old frame.
		__network_JFrame.dispose();
	}

	try {
		__network_JFrame = new StateMod_Network_JFrame(	new StateDMI_NodeDataProvider(__hbdmi), null, true);
		__network_JFrame.setSaveOnExit(true);
		__network_JFrame.addWindowListener(this);
	}
	catch (Exception ex) {
		Message.printWarning(1, routine, "Error displaying the network.");
		Message.printWarning(2, routine, ex);
		__network_JFrame = null;
		__View_ModelNetwork_JCheckBoxMenuItem.setState(false);
	}
}

/**
Open a StateCU response file and read into memory.
A check is made to see if StateDMI contains a modified data set and if it does the user is prompted as to
whether they want to save the previous data.
*/
private void uiAction_OpenStateCUDataSet ( ) {
	String routine = getClass().getSimpleName() + ".uiAction_OpenStateCUDataSet";
	// See whether the old commands need to be cleared.
	if ( (__statecuDataset != null) && __statecuDataset.isDirty() ) {
		// Have not been saved before.
		int x = ResponseJDialog.NO;
		if ( __commands_JListModel.size() > 0 ) {
			x = new ResponseJDialog ( this,
			IOUtil.getProgramName(), "Do you want to save the changes you made to the commands?\n\n" +
			"To view differences, Cancel and use View / Command File Diff.",
			ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
		}
		if ( x == ResponseJDialog.CANCEL ) {
			return;
		}
		else if ( x == ResponseJDialog.YES ) {
			// Save the data set.
			// TODO - automatically save all or let saves be done file by file?
			//__statecu_dataset.writeStateCU ( true );
		}
	}

	// Get the file.  Do not clear the current data set until the file has been chosen is readable.

	JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
	fc.setDialogTitle("Open StateCU Data Set");
	fc.setAcceptAllFileFilterUsed ( false );
	SimpleFileFilter xml_sff = null;
	/* TODO SAM 2004-02-19 Enable when convince State to track.
		new SimpleFileFilter("xml", "StateCU Data Set File");
		fc.addChoosableFileFilter(xml_sff);
	*/
	SimpleFileFilter rcu_sff = new SimpleFileFilter("rcu", "StateCU Response File");
	fc.addChoosableFileFilter(rcu_sff);
	fc.setFileFilter(rcu_sff);
	if ( fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
		// Cancel.
		return;
	}
	// If the user approves a selection do the following.

	String directory = fc.getSelectedFile().getParent();
	String path = fc.getSelectedFile().getPath();

	// Set the "WorkingDir" property, which will NOT contain a trailing separator.

	IOUtil.setProgramWorkingDir(directory);
	JGUIUtil.setLastFileDialogDirectory(directory);
	__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
	__initialWorkingDir = __props.getValue ( "WorkingDir" );

	// Read all the data.
	StateCU_DataSet new_dataset = null;
	FileFilter ff = fc.getFileFilter();
	try {
		if ( ff == xml_sff ) {
			new_dataset = StateCU_DataSet.readXMLFile ( path, true);
		}
		else if ( ff == rcu_sff ) {
			new_dataset = StateCU_DataSet.readStateCUFile ( path,true );
		}
		__sessionType = __SESSION_DATA_SET;
		__statecuDataset_JTree.clear ();
		__statecuDataset_JTree.setDataSet ( new_dataset );
		__statecuDataset_JTree.displayDataSet ();

		// FIXME SAM 2008-11-11 Evaluate whether to use.
		//__statecuResults_JTree.clear ();
		//__statecuResults_JTree.setDataSet ( new_dataset );
		//__statecuResults_JTree.displayDataSet ();
	}
	catch ( Exception e ) {
		// Error opening the file (should not happen but maybe a read permissions problem).
		Message.printWarning ( 1, routine, "Error opening file \"" + path + "\"" );
		Message.printWarning ( 2, routine, e );
		return;
	}
	__statecuDataset = new_dataset;
	__statecuDatasetType = __statecuDataset.getDataSetType();
	// Reset the menus.
	uiAction_ResetMenusForDataSetType();
	// Add the map layers.
	// TODO - comment out for now for performance.
	//showStateCUDataSetMapLayers ();
	// Successfully have read a data set so now go ahead and update the state of the GUI.
	//deleteCommands ();
	//setCommandsDirty(false);

	// New data set has been opened or there was a cancel/error and the old data set remains.
	ui_UpdateStatus ( true );
}

/**
Open a StateMod response file (or data set file) and read the data set into memory.
A check is made to see if StateDMI contains a modified data set and if
it does the user is prompted as to whether they want to save the previous data.
*/
private void uiAction_OpenStateModDataSet () {
	String routine = getClass().getSimpleName() + ".uiAction_OpenStateModDataSet";
	// See whether the old commands need to be cleared.
	if ( (__statemodDataset != null) && __statemodDataset.isDirty() ) {
		// Have not been saved before.
		int x = ResponseJDialog.NO;
		if ( __commands_JListModel.size() > 0 ) {
			x = new ResponseJDialog ( this,
			IOUtil.getProgramName(), "Do you want to save the changes you made to the commands?\n\n" +
			"To view differences, Cancel and use View / Command File Diff.",
			ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
		}
		if ( x == ResponseJDialog.CANCEL ) {
			return;
		}
		else if ( x == ResponseJDialog.YES ) {
			// Save the data set.
			// TODO - automatically save all or let saves be done file by file?
			//__statemod_dataset.writeStateMod ( true );
		}
	}

	// Get the file.  Do not clear the current data set until the file has been chosen is readable.

	JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
	fc.setAcceptAllFileFilterUsed ( false );
	fc.setDialogTitle("Open StateMod Data Set");
	SimpleFileFilter xml_sff = null;
	/* TODO SAM 2004-02-19.
		new SimpleFileFilter("xml", "StateMod Data Set File");
		fc.addChoosableFileFilter(xml_sff);
	*/
	SimpleFileFilter rsp_sff = new SimpleFileFilter("rsp", "StateMod Response File");
	fc.addChoosableFileFilter(rsp_sff);
	fc.setFileFilter(rsp_sff);
	if ( fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION ) {
		return;
	}
	String directory = fc.getSelectedFile().getParent();
	String path = fc.getSelectedFile().getPath();

	// Set the "WorkingDir" property, which will NOT contain a trailing separator.
	IOUtil.setProgramWorkingDir(directory);
	JGUIUtil.setLastFileDialogDirectory(directory);
	__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
	__initialWorkingDir = __props.getValue ( "WorkingDir" );

	// Read all the data.
	StateMod_DataSet new_dataset = null;
	// TODO - does not seem to work?
	// Hide so that progress is shown in the main GUI.
	fc.setVisible ( false );
	FileFilter ff = fc.getFileFilter();
	try {
		if ( ff == xml_sff ) {
			// TODO
			//new_dataset =StateMod_DataSet.readXMLFile ( path,true );
		}
		else if ( ff == rsp_sff ) {
			// TODO - unlike StateCU, declare an instance first.
			new_dataset = new StateMod_DataSet ( StateMod_DataSet.TYPE_UNKNOWN );
			new_dataset.readStateModFile( path,	true, // Read data.
			true, // Read time series.
			true, // Using a GUI.
			this );
		}
		__sessionType = __SESSION_DATA_SET;
		__statemodDataset_JTree.clear ();
		__statemodDataset_JTree.setDataSet ( new_dataset );
		__statemodDataset_JTree.displayDataSet ();

		// FIXME SAM 2008-11-11 Evaluate whether to use.
		//__statemodResults_JTree.clear ();
		//__statemodResults_JTree.setDataSet ( new_dataset );
		//__statemodResults_JTree.displayDataSet ();
	}
	catch ( Exception e ) {
		// Error opening the file (should not happen but maybe a read permissions problem).
		Message.printWarning ( 1, routine, "Error opening file \"" + path + "\"" );
		Message.printWarning ( 2, routine, e );
		return;
	}
	__statemodDataset = new_dataset;
	// TODO SAM 2007-06-26 Evaluate use.
	//__statemod_dataset_type = __statemod_dataset.getDataSetType();
	// Reset the menus.
	uiAction_ResetMenusForDataSetType();
	// Add the map layers.
	// TODO -  need to read and display the GeoView project file.
	//showStateModDataSetMapLayers ();
	// Successfully have read a data set so now go ahead and update the state of the GUI.
	//deleteCommands ();
	//setCommandsDirty(false);
	// New data set has been opened or there was a cancel/error and the old data set remains.
	ui_UpdateStatus ( true );
}

/**
Paste the cut buffer containing Command instances that were previously cut or copied, inserting after the selected item.
*/
private void uiAction_PasteFromCutBufferToCommandList () {
	// Default selected to zero (empty list).
	int last_selected = -1;
	int list_size = __commands_JListModel.size();

	// Get the list of selected items.
	int [] selected_indices = ui_GetCommandJList().getSelectedIndices();
	int selectedsize = 0;
	if ( selected_indices != null ) {
		selectedsize = selected_indices.length;
	}
	if ( selectedsize > 0 ) {
		last_selected = selected_indices[selectedsize - 1];
	}
	else if ( list_size != 0 ) {
		// Nothing selected so set to last item in list.
		last_selected = list_size - 1;
	}
	// Else, nothing in list so will insert at beginning.

	// Transfer the cut buffer starting at one after the last selection.

	int buffersize = __commandsCutBuffer.size();

	Command command = null;
	for ( int i = 0; i < buffersize; i++ ) {
		command = __commandsCutBuffer.get(i);
		commandList_InsertCommandAt ( command, (last_selected + 1 + i) );
	}

	// Leave in the buffer so it can be pasted again.

	commandList_SetDirty ( true );
	ui_UpdateStatus ( true );
}

/**
Read a list file for climate stations and create a new data set.
*/
private void uiAction_ReadStateCUClimateStationsFromList () {
	String routine = getClass().getSimpleName() + ".uiAction_ReadStateCUClimateStationsFromList";
/*
	// See whether the old commands need to be cleared.
	if ( __dataDirty ) {
		if ( __commands_file_name == null ) {
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(), "Do you want to save the commands?",
				ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				// Prompt for the name and then save.
				writeCommandFile ( __commands_file_name, true);
			}
		}
		else {
			// A command file exists...  Warn the user.
			// They can save to the existing file name or can cancel and File...Save As... to a different name.
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(),
				"Do you want to save the changes you made to\n\"" + __commands_file_name + "\"?",
				ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				writeCommandFile ( __commands_file_name,false);
			}
			// Else if No will clear below before opening the other file.
		}
	}
*/
	// Get the base name for the new data set.

	String basename = "test";
	while ( true ) {
		basename = new TextResponseJDialog ( this, "Enter a data set (base) name",
		"Enter the name for the data set, which will be used as a default for file names.\n" +
		"General guidelines for a name are:\n" +
		"  * The data set name should not contain spaces.\n" +
		"  * The name should be short.\n" +
		"For example \"sp2003\" (South Platte, 2003 data set).\n",
		ResponseJDialog.OK | ResponseJDialog.CANCEL ).response();
		// TODO
		// Could also put here a selector for the data set type (monthly, daily).
		// Could also put here a selection for the map file.
		if ( basename == null ) {
			// Cancelled out so don't initialize a new data set.
			return;
		}
		basename = basename.trim();
		if ( basename.length() == 0 ) {
			Message.printWarning ( 1, routine, "A data set base name must be entered." );
			continue;
		}
		else {
			break;
		}
	}

	// Get the file.  Do not clear the list until the file has been chosen and is readable.

	JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
	fc.setDialogTitle( "Open Climate Stations List File (identifiers in first column)");
	fc.addChoosableFileFilter( new SimpleFileFilter("csv", "Climate Stations List File") );
	SimpleFileFilter sff = new SimpleFileFilter("txt", "Climate Stations List File");
	fc.setFileFilter(sff);
	if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
		return;
	}
	/* TODO SAM 2007-06-26 Evaluate why not enabled.
	// If the user approves a selection do the following.
	String directory = fc.getSelectedFile().getParent();
	String filename = fc.getSelectedFile().getName();
	String path = fc.getSelectedFile().getPath();

	JGUIUtil.setLastFileDialogDirectory ( directory );

	FileReader fr = null;
	BufferedReader br = null;
	try {
		br = new BufferedReader( new FileReader(path) );
	}
	catch ( Exception e ) {
		// Error opening the file (should not happen but maybe a read permissions problem).
		Message.printWarning ( 1, routine, "Error opening file \"" + path + "\"" );
		Message.printWarning ( 2, routine, e );
		return;
	}
	*/
/*
			// Successfully have a file so now go ahead and remove the list contents and update the list.
			deleteCommands ();
			setCommandFileName(path);
			String line;
			try {
				while ( true ) {
					line = br.readLine();
					if ( line == null ) {
						break;
					}
					addCommand ( line );
				}
				setCommandsDirty(false);
				br.close();
			}
			catch ( Exception e ) {
				Message.printWarning (1, routine, "Error reading from file \"" + path + "\"");
				Message.printWarning (2, routine, e );
			}
*/

	// Get the output directory (hard-code for now).

	//String dataset_dir = "C:\\TEMP";

	// If here, reset the state of the GUI to reflect that a new data set type is now active.

	__statecuDatasetType = StateCU_DataSet.TYPE_CLIMATE_STATIONS;
	uiAction_ResetMenusForDataSetType();

	// Declare a new data set.

	// TODO - handle exception
	//__statecu_dataset = new StateCU_DataSet ( __statecu_dataset_type, dataset_dir, basename );

	// New file has been opened or there was a cancel/error and the old list remains.

	ui_UpdateStatus ( true );
}

/**
Read a list file for climate stations and create a new data set.
*/
private void uiAction_ReadStateCUStructuresFromList () {
	//String routine = "StateDMI_JFrame.readStateCUStructuresFromList";
/*
	// See whether the old commands need to be cleared.
	if ( __dataDirty ) {
		if ( __commands_file_name == null ) {
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(), "Do you want to save the commands?",
				ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				// Prompt for the name and then save.
				writeCommandFile ( __commands_file_name, true);
			}
		}
		else {
			// A command file exists...  Warn the user.
			// They can save to the existing file name or can cancel and File...Save As... to a different name.
			// Have not been saved before.
			int x = ResponseJDialog.NO;
			if ( __commands_JListModel.size() > 0 ) {
				x = new ResponseJDialog ( this, IOUtil.getProgramName(),
				"Do you want to save the changes you made to\n\"" + __commands_file_name + "\"?",
				ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
			}
			if ( x == ResponseJDialog.CANCEL ) {
				return;
			}
			else if ( x == ResponseJDialog.YES ) {
				writeCommandFile ( __commands_file_name,false);
			}
			// Else if No will clear below before opening the other file.
		}
	}
*/

	// Get the file.  Do not clear the list until the file has been chosen and is readable.

	JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
	fc.setDialogTitle( "Open Structure List File (identifiers in first column)");
	fc.addChoosableFileFilter( new SimpleFileFilter("csv", "Structures List File") );
	SimpleFileFilter sff = new SimpleFileFilter("txt", "Structures List File");
	fc.setFileFilter(sff);
	if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
		return;
	}
	/* TODO SAM 2007-06-26 Evaluate why this is not enabled.
	// If the user approves a selection do the following.
	String directory = fc.getSelectedFile().getParent();
	String path = fc.getSelectedFile().getPath();

	FileReader fr = null;
	BufferedReader br = null;
	try {
		br = new BufferedReader( new FileReader(path) );
		JGUIUtil.setLastFileDialogDirectory ( directory );
	}
	catch ( Exception e ) {
		// Error opening the file (should not happen but maybe a read permissions problem).
		Message.printWarning ( 1, routine, "Error opening file \"" + path + "\"" );
		Message.printWarning ( 2, routine, e );
		return;
	}
	*/
/*
			// Successfully have a file so now go ahead and remove the list contents and update the list.
			deleteCommands ();
			setCommandFileName(path);
			String line;
			try {
				while ( true ) {
					line = br.readLine();
					if ( line == null ) {
						break;
					}
					addCommand ( line );
				}
				setCommandsDirty(false);
				br.close();
			}
			catch ( Exception e ) {
				Message.printWarning (1, routine, "Error reading from file \"" + path + "\"");
				Message.printWarning (2, routine, e );
			}
*/
	// If here, reset the state of the GUI to reflect that a new data set type is now active.
	uiAction_ResetMenusForDataSetType();
	// New file has been opened or there was a cancel/error and the old list remains.
	ui_UpdateStatus ( true );
}

/**
Reset the menus for the data set type.
Assume that the data set has been discarded and that menus can be reset based only on the data set type.
*/
private void uiAction_ResetMenusForDataSetType () {
	// First remove the listeners from the JFrame using the list of menus that were added previously.
	// Using a list is easier than duplicating logic and tracking individual components.

	Message.printStatus ( 1, "StateDMI_JFrame.resetMenusForDataSetType", "Resetting menus for data set type." );
	// TODO
/*
	int size = __dataset_menu_List.size();
	for ( int i = 0; i < size; i++ ) {
		// Remove the ActionListeners from this JFrame for each menu.
		removeListener( (JMenuItem)__dataset_menu_List.elementAt(i));
	}
*/
	// Remove the submenus but not the top-level menus themselves.

	__File_Save_JMenu.removeAll();
	__Results_JMenu.removeAll();
	__Commands_JMenu.removeAll();

	// Now reinitialize the menus.

	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		ui_InitGUIMenus_File ( null );	// Defines the Save menus.
		ui_InitGUIMenus_Commands_StateCU ( null, getCommandsMenuStyle() );
		ui_InitGUIMenus_Results_StateCU ( null );
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		ui_InitGUIMenus_File ( null );	// Defines the Save menus.
		ui_InitGUIMenus_Commands_StateMod ( null, getCommandsMenuStyle () );
		ui_InitGUIMenus_Results_StateMod ( null );
	}
	ui_CheckGUIState();
}

/**
Run the commands in the command list.
These time series are saved in __statedmiProcessor and are then available for export, analysis, or viewing.
This method should only be called if there are commands in the command list.
@param runAllCommands If false, then only the selected commands are run.  If true, then all commands are run.
@param createOutput If true, then all write* methods are processed by the processor.
If false, only the time series in memory remain at the end and can be viewed.
The former is suitable for batch files, both for the GUI.
*/
private void uiAction_RunCommands ( boolean runAllCommands, boolean createOutput ) {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommands";
	ui_UpdateStatusTextFields ( 1, routine, null, "Running commands...", __STATUS_BUSY);
	results_Clear ();
	System.gc();
	// Get commands to run (all or selected).
	List commands = commandList_GetCommands ( runAllCommands );
	// The limits of the command progress bar are handled in commandStarted().
	// Run the commands in the processor instance.
	if ( ui_Property_RunCommandProcessorInThread() ) {
		// Run the commands in a thread.
		commandProcessor_RunCommandsThreaded ( commands, createOutput );
		// Results are displayed when CommandProcessorListener.commandCompleted() detects that the last command is complete.
	}
}

/**
Display the results generated by a run.
Currently this only provides a list of the output files and output components.
Eventually it may also display/update the data set JTree.
This is handled as a "pinch point" in hand-off from the processor and the UI, to try to gracefully handle displaying output.
*/
private void uiAction_RunCommands_ShowResults() {
	Message.printStatus ( 1, getClass().getSimpleName() + ".uiAction_RunCommands_DisplayResults", "Displaying results..." );

	// This method may be called from a thread different than the Swing thread.
	// To avoid bad behavior in GUI components (like the results list having big gaps),
	// use the following to queue up GUI actions on the Swing thread.

	Runnable r = new Runnable() {
		public void run() {
            // Close the regression results report if it is open (have to do here because
            // layers of recursion can occur when running a command file).
            StateDMICommandProcessorUtil.closeRegressionTestReportFile();
			results_Clear();
			// Display the results in the results area for user selection.
			uiAction_RunCommands_ShowResultsOutputFiles();
			uiAction_RunCommands_ShowResultsProblems();
			uiAction_RunCommands_ShowResultsProperties();
			uiAction_RunCommands_ShowResultsStateCUComponents ();
			uiAction_RunCommands_ShowResultsStateModComponents ();
			uiAction_RunCommands_ShowResultsTables();
			// TODO SAM 2005-01-18 need to enable JTree.
			//ui_displayResultsComponentTree();

            // Repaint the list to reflect the status of the commands.
            ui_ShowCurrentCommandListStatus ();
		}
	};
	if ( SwingUtilities.isEventDispatchThread() ) {
		r.run();
	}
	else {
		SwingUtilities.invokeLater ( r );
	}
}

/**
Display the list of output files from the commands.
*/
private void uiAction_RunCommands_ShowResultsOutputFiles() {
	// Loop through the commands.  For any that implement the FileGenerator interface,
	// get the output file names and add to the list.
	// Only add a file if not already in the list.
	//Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsOutputFiles", "Entering method.");
	int size = __commands_JListModel.size();
	Command command;
	ui_SetIgnoreActionEvent(true);
	for ( int i = 0; i < size; i++ ) {
		command = (Command)__commands_JListModel.get(i);
		if ( command instanceof FileGenerator ) {
			List list = ((FileGenerator)command).getGeneratedFileList();
			if ( list != null ) {
				int size2 = list.size();
				for ( int ifile = 0; ifile < size2; ifile++ ) {
					results_OutputFiles_AddOutputFile ( (File)list.get(ifile));
				}
			}
		}
	}
	// Now add to the list.
	ui_SetIgnoreActionEvent(false);
	//Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsOutputFiles", "Leaving method.");
}

/**
Display the list of problems from the commands.
*/
private void uiAction_RunCommands_ShowResultsProblems() {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsProblems";
	//Message.printStatus ( 2, routine, "Entering method.");
	try {
		// Get all of the command log messages from all commands for all run phases.
        List commands = __statedmiProcessor.getCommands();
        // For normal commands, the log records will be for the specific command.
        // For RunCommand() commands, the log records will include commands in the command file that was run.
        CommandPhaseType [] commandPhases = { CommandPhaseType.RUN }; // If show discovery it can be confusing with ${Property}, etc.
        CommandStatusType [] statusTypes = new CommandStatusType[2];
        // List failures first.
        statusTypes[0] = CommandStatusType.FAILURE;
        statusTypes[1] = CommandStatusType.WARNING;
		List logRecordList = CommandStatusUtil.getLogRecordList ( commands, commandPhases, statusTypes );
		Message.printStatus( 2, routine, "There were " + logRecordList.size() + " problems processing the commands.");
		// Create a new table model for the problem list.
		// TODO SAM 2009-03-01 Evaluate whether should just update data in existing table model (performance?).
		CommandLog_TableModel tableModel = new CommandLog_TableModel ( logRecordList );
		CommandLog_CellRenderer cellRenderer = new CommandLog_CellRenderer( tableModel );
		__resultsProblems_JWorksheet.setCellRenderer ( cellRenderer );
		__resultsProblems_JWorksheet.setModel ( tableModel );
		__resultsProblems_JWorksheet.setColumnWidths ( cellRenderer.getColumnWidths() );
		ui_SetIgnoreActionEvent(false);
	}
	catch ( Exception e ) {
		Message.printWarning( 3 , routine, e);
		Message.printWarning ( 1, routine, "Unexpected error displaying problems from run (" + e +
			") - contact support.");
	}
	//Message.printStatus ( 2, "uiAction_RunCommands_ShowProblems", "Leaving method.");
}

/**
Display the list of properties from the command processor.
*/
private void uiAction_RunCommands_ShowResultsProperties() {
    String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsProperties";
    try {
        // Create a new table model for the command processor properties.
        // TODO SAM 2009-03-01 Evaluate whether should just update data in existing table model (performance?).
        StateDMI_Processor processor = commandProcessor_GetCommandProcessor();
        Collection<String> propertyNames = processor.getPropertyNameList(true, true);
        PropList props = new PropList("processor");
        Object propVal = null;
        for ( String propertyName : propertyNames ) {
        	try {
        		propVal = processor.getPropContents(propertyName);
        	}
        	catch ( Exception e ) {
        		Message.printWarning(2,routine,e);
        	}
            if ( propVal == null) {
                props.set(new Prop(propertyName, propVal, ""));
            }
            else {
                props.set(new Prop(propertyName, propVal, "" + processor.getPropContents(propertyName) ) );
            }
        }
        PropList_TableModel tableModel = new PropList_TableModel ( props, false, false );
        tableModel.setKeyColumnName("Property Name");
        tableModel.setValueColumnName("Property Value");
        PropList_CellRenderer cellRenderer = new PropList_CellRenderer( tableModel );
        __resultsProperties_JWorksheet.setCellRenderer ( cellRenderer );
        __resultsProperties_JWorksheet.setModel ( tableModel );
        __resultsProperties_JWorksheet.setColumnWidths ( cellRenderer.getColumnWidths() );
        ui_SetIgnoreActionEvent(false);
    }
    catch ( Exception e ) {
        Message.printWarning( 3 , routine, e);
        Message.printWarning ( 1, routine, "Unexpected error displaying processor properties (" + e + ") - contact support.");
    }
}

/**
Display the results of a run as a list of StateCU components.
The user can then select an item to display the results in a worksheet.
The action events will trigger a call to displayResultsComponentTable().
*/
private void uiAction_RunCommands_ShowResultsStateCUComponents () {
	//String routine = "StateDMI_JFrame.uiAction_RunCommands_ShowResultsStateCUComponents";
	List v = null;
	// A data set instance is needed to lookup information.
	StateCU_DataSet statecu_dataset = null;
	try {
		statecu_dataset = new StateCU_DataSet ();
	}
	catch ( Exception e ) {
		// Should not happen.
	}

	// Don't want to generate item events as combo boxes are modified.

	ui_SetIgnoreActionEvent (true);

	// List components in the order of the data set.

	v = __statedmiProcessor.getStateCUClimateStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CLIMATE_STATIONS));
	}

	// Climate station time series are not handled by StateDMI.  Use TSTool or some other software to view.

	v = __statedmiProcessor.getStateCUCropCharacteristicsList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CROP_CHARACTERISTICS));
	}

	v = __statedmiProcessor.getStateCUBlaneyCriddleList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_BLANEY_CRIDDLE));
	}

	v = __statedmiProcessor.getStateCUPenmanMonteithList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_PENMAN_MONTEITH));
	}

	// StateMod delay tables are also used by StateCU.
	v = __statedmiProcessor.getStateModDelayTableList( TimeInterval.MONTH );
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_DELAY_TABLES_MONTHLY));
	}

	v = __statedmiProcessor.getStateCULocationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CU_LOCATIONS));
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CU_LOCATION_CLIMATE_STATIONS));
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CU_LOCATION_COLLECTIONS));
	}

	v = __statedmiProcessor.getStateCUCropPatternTSList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY));
	}

	v = __statedmiProcessor.getStateCUIrrigationPracticeTSList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateCUComponents_AddComponents(
			statecu_dataset.lookupComponentName(StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY));
	}

	// The intervening files are not handled in StateDMI as part of StateCU data sets.

	ui_SetIgnoreActionEvent (false);
}

/**
Display the results of a run as a list of StateMod components.
The user can then select an item to display the results in a worksheet.
The action events will trigger a call to displayResultsComponentTable().
*/
private void uiAction_RunCommands_ShowResultsStateModComponents () {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsStateModComponents";
	List v = null;
	// Need instance for lookup method.
	StateMod_DataSet statemod_dataset = null;
	try {
		statemod_dataset = new StateMod_DataSet ();
	}
	catch ( Exception e ) {
		// Should not happen.
	}

	// Don't want to generate item events as combo boxes are modified.

	ui_SetIgnoreActionEvent (true);

	v = __statedmiProcessor.getStateModStreamGageStationList();
	if ( (v != null) && (v.size() > 0) ) {
		Message.printStatus ( 1, routine,"Listing stream gage station component" );
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_STREAMGAGE_STATIONS));
	}

	// Stream gage time series are not created by StateDMI so don't list here.

	v = __statedmiProcessor.getStateModDelayTableList( TimeInterval.MONTH );
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DELAY_TABLES_MONTHLY));
	}

	v = __statedmiProcessor.getStateModDelayTableList( TimeInterval.DAY );
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DELAY_TABLES_DAILY));
	}

	v = __statedmiProcessor.getStateModDiversionStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_STATIONS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_STATION_DELAY_TABLES));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_STATION_COLLECTIONS));
	}

	v = __statedmiProcessor.getStateModDiversionRightList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_RIGHTS));
	}

	v = __statedmiProcessor.getStateModDiversionHistoricalTSMonthlyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_TS_MONTHLY));
	}

	v = __statedmiProcessor.getStateModDiversionHistoricalTSDailyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DIVERSION_TS_DAILY));
	}

	v = __statedmiProcessor.getStateModDiversionDemandTSMonthlyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DEMAND_TS_MONTHLY));
	}

	v = __statedmiProcessor.getStateModDiversionDemandTSDailyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_DEMAND_TS_DAILY));
	}

	// The other diversion time series are not handled by StateDMI and should be displayed with TSTool or other software.

	// Precipitation and evaporation time series are not handled by StateDMI and should be displayed with TSTool or other software.

	v = __statedmiProcessor.getStateModReservoirStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATIONS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATION_ACCOUNTS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATION_PRECIP_STATIONS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATION_EVAP_STATIONS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATION_CURVE));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_STATION_COLLECTIONS));
	}

	// Reservoir time series are not handled by StateDMI and should be displayed with TSTool or other software.

	v = __statedmiProcessor.getStateModReservoirRightList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_RIGHTS));
	}

	v = __statedmiProcessor.getStateModReservoirReturnList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RESERVOIR_RETURN));
	}

	v = __statedmiProcessor.getStateModInstreamFlowStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_INSTREAM_STATIONS));
	}

	v = __statedmiProcessor.getStateModInstreamFlowRightList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_INSTREAM_RIGHTS));
	}

	v = __statedmiProcessor.getStateModInstreamFlowDemandTSAverageMonthlyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_INSTREAM_DEMAND_TS_AVERAGE_MONTHLY));
	}

	// Instream flow demand time series (monthly, daily) are not handled by StateDMI and should be displayed with TSTool or other software.

	v = __statedmiProcessor.getStateModWellStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_STATIONS));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_STATION_DELAY_TABLES));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_STATION_DEPLETION_TABLES));
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_STATION_COLLECTIONS));
	}

	v = __statedmiProcessor.getStateModWellRightList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_RIGHTS));
	}

	v = __statedmiProcessor.getStateModWellHistoricalPumpingTSMonthlyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_PUMPING_TS_MONTHLY) );
	}

	v = __statedmiProcessor.getStateModWellDemandTSMonthlyList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_WELL_DEMAND_TS_MONTHLY) );
	}

	// Well daily time series are not handled by StateDMI and should be displayed with TSTool or other software.

	v = __statedmiProcessor.getStateModPlanStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_PLANS));
	}

	v = __statedmiProcessor.getStateModPlanWellAugmentationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_PLAN_WELL_AUGMENTATION));
	}

	v = __statedmiProcessor.getStateModPlanReturnList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_PLAN_RETURN));
	}

	v = __statedmiProcessor.getStateModStreamEstimateStationList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_STREAMESTIMATE_STATIONS));
	}

	v = __statedmiProcessor.getStateModStreamEstimateCoefficientsList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_STREAMESTIMATE_COEFFICIENTS));
	}

	// Stream estimate series are not handled by StateDMI and should be displayed with TSTool or other software.

	v = __statedmiProcessor.getStateModRiverNetworkNodeList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_RIVER_NETWORK));
	}

	// Operational rights.

	v = __statedmiProcessor.getStateModOperationalRightList();
	if ( (v != null) && (v.size() > 0) ) {
		results_StateModComponents_AddComponents(
			statemod_dataset.lookupComponentName(StateMod_DataSet.COMP_OPERATION_RIGHTS));
	}

	// The other files are not currently handled by StateDMI.

	ui_SetIgnoreActionEvent ( false );
}

/**
Display the table results.
*/
private void uiAction_RunCommands_ShowResultsTables() {
    // Get the list of tables from the processor.
    List<DataTable> tableList = commandProcessor_GetTableResultsList();
    int size = 0;
    if ( tableList != null ) {
        size = tableList.size();
    }
    ui_SetIgnoreActionEvent(true);
    DataTable table;
    // Use HTML only when needed to show a zero size table.
    String htmlStart = "<html><span style=\"color:red;font-weight:bold\">", htmlStart2;
    String htmlEnd = "</span></html>", htmlEnd2;
    int nRows, nCols;
    for ( int i = 0; i < size; i++ ) {
        table = tableList.get(i);
        htmlStart2 = "";
        htmlEnd2 = "";
        nRows = table.getNumberOfRecords();
        nCols = table.getNumberOfFields();
        if ( (nRows == 0) || (nCols == 0) ) {
            htmlStart2 = htmlStart;
            htmlEnd2 = htmlEnd;
        }
        results_Tables_AddTable ( htmlStart2 + (i + 1) + ") " + table.getTableID() +
            " - " + nRows + " rows, " + nCols +
            " columns" + htmlEnd2 );

    }
    ui_SetIgnoreActionEvent(false);
}

/**
Select all commands in the commands list.  This occurs in response to a user selecting a menu choice.
*/
private void uiAction_SelectAllCommands() {
	JGUIUtil.selectAll(__commands_JList);
	ui_UpdateStatus ( true );
}

/**
Display the status of the selected command(s).
*/
private void uiAction_ShowCommandStatus() {
  SwingUtilities.invokeLater(new Runnable() {
    public void run() {
      try {
        String status = uiAction_ShowCommandStatus_GetCommandsStatus();

        HTMLViewer hTMLViewer = new HTMLViewer();
        hTMLViewer.setTitle ( "StateDMI - Command Status" );
        hTMLViewer.setHTML(status);
        hTMLViewer.setSize(700,600);
        hTMLViewer.setVisible(true);
      }
      catch(Throwable t) {
        Message.printWarning(1, "uiAction_ShowCommandStatus", "Problem showing Command status");
        String routine = "StateDMI_JFrame.showCommandStatus";
        Message.printWarning(2, routine, t);
      }
    }
  });
}

/**
 * Gets Commands status in HTML - this is currently only a helper for the above method.  Rename if it will be used generically.
 * @return
 */
private String uiAction_ShowCommandStatus_GetCommandsStatus() {
	List commands = commandList_GetCommandsBasedOnUI();
  String html = CommandStatusUtil.getHTMLStatusReport(commands);
  return html;
}

/**
Display a window showing the data set properties.
Output is formatted appropriately for a StateCU or a StateMod data set, or a command file.
*/
private void uiAction_ShowDataSetProperties () {
	PropList reportProp = new PropList ("Data Set Properties");
	reportProp.set ( "TotalWidth", "600" );
	reportProp.set ( "TotalHeight", "300" );
	reportProp.set ( "DisplayFont", "Courier" );
	reportProp.set ( "DisplaySize", "11" );
	reportProp.set ( "PrintFont", "Courier" );
	reportProp.set ( "PrintSize", "7" );
	reportProp.set ( "Title", "Data Set Properties" );
	reportProp.setUsingObject ( "ParentUIComponent", this );
	List<String> v = new ArrayList<>(4);
	String tab = "    ";
	v.add ( "StateDMI Data Set Properties" );
	v.add ( "" );
	if ( __appType == StateDMI.APP_TYPE_STATECU ) {
		v.add ( "Data set file(s) are for StateCU." );
		if ( (__statecuDataset == null) && (__commandFileName == null) ) {
			v.add ( "No data set or command file have been read or saved." );
		}
		else if ((__statecuDataset == null) && (__commands_JListModel.size() > 0) ) {
			v.add ( "No data set is loaded." );
			v.add ( "Commands are being run directly to create data set files." );
			v.add ( "The following summary reflects the most recent commands that were processed." );
		}
		else {
			// A data set is loaded.
			v.add ( "Data set type:  " + __statecuDataset.getDataSetName() );
			if ( __statecuDataset.getDataSetFileName().equals("")){
				v.add ( "Data set file:  NOT SAVED AS DATA SET.");
			}
			else {
				v.add ("Data set file:  " + __statecuDataset.getDataSetFileName() );
			}
		}
		v.add ( "" );
		if ( __commandFileName == null ) {
			v.add ( "No command file has been read or saved." );
		}
		else {
			v.add ( "Last command file read/saved:" );
			v.add ( tab + __commandFileName );
		}
		v.add ( "" );
		if ( __commandFileName == null ) {
			v.add ( "Current working directory (from startup or File...Set Working Directory):" );
		}
		else {
			v.add ( "Current working directory (from command file open/save):" );
		}
		v.add ( tab + __initialWorkingDir );
		if ( __statedmiProcessor == null ) {
			// No processor exists.
			v.add ( "" );
			v.add ( "Commands have not been processed." );
		}
		else {
			// Display information about the objects that are available from the last processing run.
			// Output period.
			v.add ( "" );
			if ( __commandsDirty ) {
				v.add ( "Results of the last run (commands have been modified and need to be rerun):" );
			}
			else {
				v.add ( "Results of the last run (commands and output are consistent):" );
			}
			v.add ( "" );
			if ( (__statedmiProcessor.getOutputPeriodStart() != null)&&
				(__statedmiProcessor.getOutputPeriodEnd()!=null)){
				v.add("Output period:  " + __statedmiProcessor.getOutputPeriodStart() +
				" to " + __statedmiProcessor.getOutputPeriodEnd());
			}
			else {
				v.add( "Output period:   not specified.");
			}
			// Print a table showing the number of objects.
			int n_CULocations = __statedmiProcessor.getStateCULocationList().size();
			int n_CUCropCharacteristics = __statedmiProcessor.getStateCUCropCharacteristicsList().size();
			int n_BlaneyCriddle = __statedmiProcessor.getStateCUBlaneyCriddleList().size();
			int n_PenmanMonteith = __statedmiProcessor.getStateCUPenmanMonteithList().size();
			int n_SMDelayTablesMonthly = __statedmiProcessor.getStateModDelayTableList(TimeInterval.MONTH).size();
			int n_SMDelayTablesDaily = __statedmiProcessor.getStateModDelayTableList(TimeInterval.DAY).size();
			int n_CUClimateStations = __statedmiProcessor.getStateCUClimateStationList().size();
			int n_CUCropPatternTS = __statedmiProcessor.getStateCUCropPatternTSList().size();
			int n_CUIrrigationPracticeTS = __statedmiProcessor.getStateCUIrrigationPracticeTSList().size();
			v.add ( "" );
			v.add ( "                                         Number of");
			v.add ( "Model    Data Set Component              Objects");
			// TODO SAM 2004-04-10 Enable the file when a data set is used.
			//"Objects     File");
			v.add ( "-------------------------------------------------------------------------------------------");
			v.add ( "StateCU  Climate Stations                  " + StringUtil.formatString( n_CUClimateStations,"%5d") );
			v.add ( "StateCU  Crop Characteristics              " + StringUtil.formatString(n_CUCropCharacteristics,"%5d"));
			v.add ( "StateCU  Blaney-Criddle Crop Coeff.        " + StringUtil.formatString(n_BlaneyCriddle,"%5d"));
			v.add ( "StateCU  Penman-Monteith Crop Coeff.       " + StringUtil.formatString(n_PenmanMonteith,"%5d"));
			v.add ( "StateCU  Delay Tables (Monthly)            " + StringUtil.formatString(n_SMDelayTablesMonthly,"%5d"));
			v.add ( "StateCU  Delay Tables (Daily)              " + StringUtil.formatString(n_SMDelayTablesDaily,"%5d"));
			v.add ( "StateCU  CU Locations                      " + StringUtil.formatString (n_CULocations, "%5d"));
			v.add ( "StateCU    CU Loc. w/ Crop Pattern TS      " + StringUtil.formatString( n_CUCropPatternTS,"%5d") );
			v.add ( "StateCU    CU Loc. w/ Irrig. Practice TS   " + StringUtil.formatString( n_CUIrrigationPracticeTS,"%5d") );
		}
	}
	else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
		v.add ( "Data set file(s) are for StateMod." );
	}
	new ReportJFrame ( v, reportProp );
}

/**
Show the datastores.
*/
private void uiAction_ShowDataStores () {
    String routine = getClass().getSimpleName() + "uiAction_ShowDataStores";
    try {
    	List<DataStoreSubstitute> dataStoreSubstituteList = new ArrayList<>();
        new DataStores_JFrame ( "Datastores", this, __statedmiProcessor.getDataStores(), dataStoreSubstituteList );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine, "Error displaying datastores (" + e + ")." );
    }
}

/**
Show an output file using the appropriate display software/editor.
@param selected Path to selected output file.
*/
private void uiAction_ShowResultsOutputFile ( String selected ) {
    String routine = getClass().getName() + ".uiAction_ShowResultsOutputFile";
    if ( selected == null ) {
        // May be the result of some UI event.
        return;
    }
    // Display the selected file.
    if ( !( new File( selected ).isAbsolute() ) ) {
        selected = IOUtil.getPathUsingWorkingDir( selected );
    }
    // First try the application that is configured.
    // TODO SAM 2011-03-31 What if a TSTool command file has been expanded?
    try {
        Desktop desktop = Desktop.getDesktop();
        desktop.open ( new File(selected) );
    }
    catch ( Exception e ) {
        // Else display as text (will show up in courier fixed width font, which looks better than the html browser).
        try {
            if ( IOUtil.isUNIXMachine() ) {
                // Use a built in viewer (may be slow).
                PropList reportProp = new PropList ("Output File");
                reportProp.set ( "TotalWidth", "800" );
                reportProp.set ( "TotalHeight", "600" );
                reportProp.set ( "DisplayFont", __FIXED_WIDTH_FONT );
                reportProp.set ( "DisplaySize", "11" );
                reportProp.set ( "PrintFont", __FIXED_WIDTH_FONT );
                reportProp.set ( "PrintSize", "7" );
                reportProp.set ( "Title", selected );
                reportProp.set ( "URL", selected );
               	reportProp.setUsingObject ( "ParentUIComponent", this );
                new ReportJFrame ( null, reportProp );
            }
            else {
                // Rely on Notepad on Windows.
                String [] command_array = new String[2];
                command_array[0] = "notepad";
                command_array[1] = IOUtil.getPathUsingWorkingDir(selected);
                ProcessManager p = new ProcessManager ( command_array );
                Thread t = new Thread ( p );
                t.start();
            }
        }
        catch (Exception e2) {
            Message.printWarning (1, routine, "Unable to view file \"" + selected + "\" (" + e2 + ")." );
            Message.printWarning ( 3, routine, e2 );
        }
    }
}

/**
Show a table using the built in display component.
@param selected table display string for the table to display "#) TableID - other information...".
*/
private void uiAction_ShowResultsTable ( String selected ) {
    String routine = getClass().getSimpleName() + ".uiAction_ShowResultsTable";
    if ( selected == null ) {
        // May be the result of some UI event.
        return;
    }
    // Display the table.
    String tableId = "";
    try {
        tableId = uiAction_ShowResultsTable_GetTableID ( selected );
        DataTable table = commandProcessor_GetTable ( tableId );
        if ( table == null ) {
            Message.printWarning (1, routine, "Unable to get table \"" + tableId + "\" from processor to view." );
        }
        new DataTable_JFrame ( this, "Table \"" + tableId + "\"", table );
    }
    catch (Exception e2) {
        Message.printWarning (1, routine, "Unable to view table \"" + tableId + "\"" );
        Message.printWarning ( 3, routine, e2 );
    }
}

/**
Helper method to get the table identifier from the displayed table results list string.
*/
private String uiAction_ShowResultsTable_GetTableID ( String tableDisplayString ) {
    // Determine the table identifier from the displayed string, which will always have at least one
    // dash, but table identifiers may also have a dash.
    if ( tableDisplayString == null ) {
        return null;
    }
    int pos1 = tableDisplayString.indexOf( ")"); // Count at start of string.
    int pos2 = tableDisplayString.indexOf( " -"); // Break between ID.
    String tableId = tableDisplayString.substring(pos1+1,pos2).trim();
    return tableId;
}

/**
Show the properties for a table.
*/
private void uiAction_ShowTableProperties () {
    String routine = getClass().getSimpleName() + "uiAction_ShowTableProperties";
    try {
        // Simple text display of HydroBase properties.
        PropList reportProp = new PropList ("Table Properties");
        reportProp.set ( "TotalWidth", "600" );
        reportProp.set ( "TotalHeight", "600" );
        reportProp.set ( "DisplayFont", __FIXED_WIDTH_FONT );
        reportProp.set ( "DisplaySize", "11" );
        reportProp.set ( "PrintFont", __FIXED_WIDTH_FONT );
        reportProp.set ( "PrintSize", "7" );
        reportProp.set ( "Title", "Table Properties" );
        List<String> v = new ArrayList<>();
        // Get the table of interest.
        if ( __resultsTables_JList.getModel().getSize() > 0 ) {
            // If something is selected, show properties for the selected.  Otherwise, show properties for all.
            // TODO SAM 2012-10-12 Add intelligence to select based on mouse click?
            int [] sel = __resultsTables_JList.getSelectedIndices();
            if ( sel.length == 0 ) {
                // Process all.
                sel = new int[__resultsTables_JList.getModel().getSize()];
                for ( int i = 0; i < sel.length; i++ ) {
                    sel[i] = i;
                }
            }
            for ( int i = 0; i < sel.length; i++ ) {
                // TODO SAM 2012-10-15 Evaluate putting this in DataTable class for general use.
                String displayString = __resultsTables_JList.getModel().getElementAt(sel[i]);
                String tableId = uiAction_ShowResultsTable_GetTableID ( displayString );
                DataTable t = commandProcessor_GetTable ( tableId );
                v.add ( "" );
                v.add ( "Table \"" + t.getTableID() + "\" properties:" );
                for ( int ifld = 0; ifld < t.getNumberOfFields(); ifld++ ) {
                	StringBuilder b = new StringBuilder();
                	b.append("   Column[" + ifld + "] name=\"" + t.getFieldName(ifld) + "\" type=");
                	if ( t.isColumnArray(t.getFieldDataType(ifld))) {
                		// Array column.
                		b.append("Array of " + TableColumnType.valueOf(t.getFieldDataType(ifld) - TableField.DATA_TYPE_ARRAY_BASE));
                	}
                	else {
                		b.append(TableColumnType.valueOf(t.getFieldDataType(ifld)));
                	}
                	b.append(" width=" + t.getFieldWidth(ifld) + " precision=" + t.getFieldPrecision(ifld));
                	v.add(b.toString());
                }
            }
        }
        reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
        new ReportJFrame ( v, reportProp );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine, "Error displaying table properties (" + e + ")." );
    }
}

/**
Switch the GUI application type, mainly menus.
@param app_type Specify as StateDMI.APP_TYPE_* to indicate the application whose
data set is being processed (the application being switched to).
*/
private void uiAction_SwitchAppType ( int app_type )
{	String routine = "StateDMI_JFrame.switchAppType";
	// TODO SAM 2004-04-10 Need to see if data set or commands need to
	// be saved before continuing.
	if ( app_type == StateDMI.APP_TYPE_STATECU ) {
		Message.printStatus ( 1, routine, "Switching to StateCU..." );
		if ( __statemodDataset != null ) {
			// Currently don't know how to handle swapping out a data set (but can handle commands-only swap).
			Message.printWarning ( 1, routine,
			"To access StateCU features after a StateMod data set has been loaded,\n" +
			"you currently must restart StateDMI with the -statecu option.");
			return;
		}
		// First remove the old menus.
		__Commands_JMenu.removeAll();
		__Run_JMenu.removeAll();
		__Results_JMenu.removeAll();
		// Now initialize the appropriate menus.
		__appType = app_type;
		ui_InitGUIMenus_Commands_StateCU ( null, getCommandsMenuStyle() );
		ui_InitGUIMenus_Run ( null );
		ui_InitGUIMenus_Results_StateCU ( null );
		Message.printStatus ( 1, routine, "Menus are now set for StateCU." );
	}
	else if ( app_type == StateDMI.APP_TYPE_STATEMOD ) {
		Message.printStatus ( 1, routine, "Switching to StateMod..." );
		if ( __statecuDataset != null ) {
			// Currently don't know how to handle swapping out a data set (but can handle commands-only swap).
			Message.printWarning ( 1, routine,
			"To access StateMod features after a StateCU data set has been loaded,\n" +
			"you currently must restart StateDMI with the -statemod option.");
		}
		// First remove the old menus.
		__Commands_JMenu.removeAll();
		__Run_JMenu.removeAll();
		__Results_JMenu.removeAll();
		// Now initialize the appropriate menus.
		__appType = app_type;
		ui_InitGUIMenus_Commands_StateMod ( null, getCommandsMenuStyle() );
		ui_InitGUIMenus_Run ( null );
		ui_InitGUIMenus_Results_StateMod ( null );
		Message.printStatus ( 1, routine, "Menus are now set for StateMod." );
	}
	// Update the title bar and check the state of the GUI.
	ui_UpdateStatus ( true );
}

/**
StateDMI -test is being run and the File...Test menu has been pressed.  Launch test code.
*/
private void uiAction_Test() {
	new Beta_CreateNaturalFlowShapefile();
}

/**
List the total rights for each well structure, using the well rights that are in memory.
*/
void uiAction_Tool_ListWellStationRightTotals () {
	String routine = getClass().getSimpleName() + ".toolListWellStationRightTotals";
	List<StateMod_WellRight> SMWellRight_List = __statedmiProcessor.getStateModWellRightList();
	int size_wer = SMWellRight_List.size();
	if ( size_wer == 0 ) {
		Message.printWarning ( 1, routine, "Well rights must first be processed (e.g., read well rights with a command." );
		return;
	}
	// Loop through the well rights.  For each right, try to find a matching
	// well station in the temporary list.  If one is found, increment the well station's capacity,
	// which represents the total of the decrees for this report.  If a well is not found,
	// add a new temporary well station.  Finally, print all the IDs and associated decree totals.
	String id;
	StateMod_WellRight wer;
	StateMod_Well wes = null;
	List<StateMod_Well> wes_List = new ArrayList<>();
	int size_wes;
	double decree;
	boolean found;
	for ( int iwer = 0; iwer < size_wer; iwer++ ) {
		wer = SMWellRight_List.get(iwer);
		decree = wer.getDcrdivw();
		if ( decree < 0.0 ) {
			continue;
		}
		id = wer.getCgoto();
		// Find the matching well station.
		size_wes = wes_List.size();
		found = false;
		for ( int iwes = 0; iwes < size_wes; iwes++ ) {
			wes = wes_List.get(iwes);
			if ( id.equalsIgnoreCase(wes.getID()) ) {
				found = true;
				break;
			}
		}
		if ( !found ) {
			// Add a new well station.
			wes = new StateMod_Well ( false );
			wes.setID ( id );
			wes_List.add ( wes );
		}
		if ( wes.getDivcapw() < 0.0 ) {
			wes.setDivcapw(decree);
		}
		else {
			wes.setDivcapw(decree+wes.getDivcapw());
		}
	}
	size_wes = wes_List.size();
	List<String> v = new ArrayList<>();
	v.add ( "\"ID\",\"Total Decree\"" );
	for ( int i = 0; i < size_wes; i++ ) {
		wes = wes_List.get(i);
		v.add ( wes.getID() + "," + StringUtil.formatString(wes.getDivcapw(),"%.2f") );
	}
	PropList reportProp = new PropList ("HydroBase Properties");
	reportProp.set ( "TotalWidth", "600" );
	reportProp.set ( "TotalHeight", "300" );
	reportProp.set ( "DisplayFont", "Courier" );
	reportProp.set ( "DisplaySize", "11" );
	reportProp.set ( "PrintFont", "Courier" );
	reportProp.set ( "PrintSize", "7" );
	reportProp.set ( "Title", "Well Station Right Totals" );
   	reportProp.setUsingObject ( "ParentUIComponent", this );
	new ReportJFrame ( v, reportProp );
}

/**
 * Show the difference between the current commands and the saved on disk command file.
 */
private void uiAction_ViewCommandFileDiff () {
	// If the diff tool is not configured, provide information.
	Prop prop = IOUtil.getProp("DiffProgram");
	String diffProgram = null;
	if ( prop != null ) {
		diffProgram = prop.getValue();
	}
	else {
         new ResponseJDialog ( this, IOUtil.getProgramName(),
             "The visual diff program has not been configured in the StateDMI configuration file.\n" +
             "Define the \"DiffProgram\" property as the path to a visual diff program, for example kdiff3\n" +
             "Cannot show the command file difference.",
             ResponseJDialog.OK).response();
         return;
	}
	if ( IOUtil.fileExists(diffProgram) ) {
		// Diff program exists so save a temporary file with UI commands and then compare with file version.
		// Run the diff program on the input and output files
		// (they should have existed because the button will have been disabled if not).
		String file1Path = this.__commandFileName;
		if ( file1Path == null ) {
	         new ResponseJDialog ( this, IOUtil.getProgramName(),
                  "No command file was previously read or saved.  The commands being edited are new.",
                  ResponseJDialog.OK).response();
	         return;
		}
		// Write the commands to a temporary file.
		String tempCommandFile = IOUtil.tempFileName();
		File f = new File(tempCommandFile);
		String tempFolder = f.getParent();
		String file2Path = tempFolder + File.separator + "StateDMI-commands.statedmi";
		try {
			uiAction_WriteCommandFile_Helper(file2Path);
		}
		catch ( Exception e ) {
			Message.printWarning(1, "", "Error saving commands to temporary file for diff (" + e + ")" );
			return;
		}
		// Run the diff program.
		String [] programAndArgsList = { diffProgram, file1Path, file2Path };
		try {
			ProcessManager pm = new ProcessManager ( programAndArgsList,
					0, // No timeout.
	                null, // Exit status indicator.
	                false, // Use command shell.
	                new File(tempFolder) );
			Thread t = new Thread ( pm );
            t.start();
		}
		catch ( Exception e ) {
			Message.printWarning(1, "", "Unable to run diff program (" + e + ")" );
		}
	}
	else {
		Message.printWarning(1, "", "Visual diff program does not exist:  " + diffProgram );
	}
}

/**
View the documentation by displaying using the desktop application.
@param command the string from the action event (menu string).
*/
private void uiAction_ViewDocumentation ( String command ) {
    String routine = getClass().getSimpleName() + ".uiAction_ViewDocumentation";
	if ( command.equals ( __Help_ViewDocumentation_String )) {
		// Legacy PDF documentation.
		// The location of the documentation is relative to the application home.
		String docFileName = IOUtil.getApplicationHomeDir() + "/doc/UserManual/StateDMI.pdf";
    	// Convert for the operating system.
    	docFileName = IOUtil.verifyPathForOS(docFileName, true);
    	// Now display using the default application for the file extension.
    	Message.printStatus(2, routine, "Opening documentation \"" + docFileName + "\"" );
    	try {
        	Desktop desktop = Desktop.getDesktop();
        	desktop.open ( new File(docFileName) );
    	}
    	catch ( Exception e ) {
        	Message.printWarning(1, "", "Unable to display documentation at \"" + docFileName + "\" (" + e + ")." );
    	}
	}
	else {
		// New online documentation.
		String docUri = formatHelpViewerUrl("", command);
	    if ( docUri != null ) {
	        try {
	            Desktop desktop = Desktop.getDesktop();
	            desktop.browse ( new URI(docUri) );
	        }
	        catch ( Exception e ) {
	            Message.printWarning(2, routine, "Unable to display documentation at \"" + docUri + "\" (" + e + ")." );
	        }
	    }
	    else {
			// Not able to open either URI.
	    	Message.printWarning(1, "", "Unable to determine URL for documentation for \"" + command + "\"." );
	    }
	}
}

/**
View the training materials by displaying in file browser.
*/
private void uiAction_ViewTrainingMaterials () {
    String routine = getClass().getName() + ".uiAction_ViewTrainingMaterials";
    // The location of the documentation is relative to the application home.
    String trainingFolderName = IOUtil.getApplicationHomeDir() + "/doc/Training";
    // Convert for the operating system.
    trainingFolderName = IOUtil.verifyPathForOS(trainingFolderName, true);
    // Now display using the default application for the file extension.
    Message.printStatus(2, routine, "Opening training material folder \"" + trainingFolderName + "\"" );
    try {
        Desktop desktop = Desktop.getDesktop();
        desktop.open ( new File(trainingFolderName) );
    }
    catch ( Exception e ) {
        Message.printWarning(1, "", "Unable to display training materials at \"" +
            trainingFolderName + "\" (" + e + ")." );
    }
}

/**
Write the current command file list (all lines, whether selected or not) to the specified file.
Do not prompt for header comments (and do not add).
@param prompt_for_file If true, prompt for the file name rather than using the value that is passed.
An extension of .StateDMI is enforced.
@param file Command file to write.
*/
private void uiAction_WriteCommandFile ( String file, boolean prompt_for_file ) {
	String routine = "StateDMI_JFrame.uiAction_WriteCommandFile";
    String directory = null;
	if ( prompt_for_file ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser(ui_GetDir_LastCommandFileOpened() );
		fc.setDialogTitle("Save Command File");
		// Default name.
		File default_file = new File("commands.statedmi");
		fc.setSelectedFile ( default_file );

		List<String> extensions = new ArrayList<>();
		extensions.add("statedmi");
		extensions.add("StateDMI");
		SimpleFileFilter sff = new SimpleFileFilter(extensions,"StateDMI Command File");
		fc.setFileFilter(sff);
		if (fc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
			directory = fc.getSelectedFile().getParent();
			file = fc.getSelectedFile().getPath();
			IOUtil.enforceFileExtension ( file, extensions );
			ui_SetDir_LastCommandFileOpened( directory );
		}
		else {
		    // Did not approve.
			return;
		}
	}
	// Now write the file.
	try {
	    PrintWriter out = new PrintWriter(new FileOutputStream(file));
		int size = __commands_JListModel.size();
		for (int i = 0; i < size; i++) {
			out.println(((Command)__commands_JListModel.get(i)).toString());
		}

		out.close();
		commandList_SetDirty(false);
		commandList_SetCommandFileName ( file );

		// Save the file in the history
		this.session.pushHistory(file);
		// Do this here because the write may be in a sequence of steps.
		ui_InitGUIMenus_File_OpenRecentFiles();

		if ( directory != null ) {
			// Set the "WorkingDir" property, which will NOT contain a trailing separator.
			IOUtil.setProgramWorkingDir(directory);
			ui_SetDir_LastCommandFileOpened(directory);
			__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
			ui_SetInitialWorkingDir (__props.getValue("WorkingDir"));
		}
	}
	catch ( Exception e ) {
		Message.printWarning (1, routine, "Error writing file:\n\"" + file + "\"");
		// Leave the dirty flag the previous value.
	}
	// Update the status information.
	ui_UpdateStatus ( false );
}

/** Helper method to write the commands to a file.
 * @param file Path to file to write.
 */
private void uiAction_WriteCommandFile_Helper(String file) throws FileNotFoundException {
	PrintWriter out = new PrintWriter(new FileOutputStream(file));
	int size = __commands_JListModel.size();
	Command command;
	for (int i = 0; i < size; i++) {
		command = (Command)__commands_JListModel.get(i);
		out.println(command.toString());
	}
	out.close();
}

/**
Write the current data set the specified file.  Do not prompt for header
comments (and do not add).  The files related to the data set are not written.
@param prompt_for_file If true, prompt for the file name rather than using the value that is passed.
@param file Data set (XML) file to write.
*/
private void uiAction_WriteDataSet ( String file, boolean prompt_for_file ) {
	String directory = null;
	if ( prompt_for_file ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser(JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle("Save Data Set File");
		// Default name.
		File default_file = null;
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			if ( !__statecuDataset.getBaseName().equals("") ) {
				default_file = new File( __statecuDataset.getBaseName() + ".xml");
				fc.setSelectedFile ( default_file );
			}
		}
		SimpleFileFilter sff = null;
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			sff=new SimpleFileFilter("xml","StateCU Data Set File");
		}
		else if ( __appType == StateDMI.APP_TYPE_STATEMOD ) {
			sff=new SimpleFileFilter("xml",	"StateMod Data Set File");
		}
		fc.addChoosableFileFilter( sff );
		fc.setFileFilter(sff);
		if (fc.showSaveDialog(this) != JFileChooser.APPROVE_OPTION) {
			return;
		}
		directory = fc.getSelectedFile().getParent();
		file = fc.getSelectedFile().getPath();
	}
	// Now write the file.
	try {
		if ( __appType == StateDMI.APP_TYPE_STATECU ) {
			StateCU_DataSet.writeXMLFile ( null, file, __statecuDataset, null );
		}
		// TODO - status updates?
		//setCommandsDirty(false);
		//setCommandFileName ( file );

		// Set the "WorkingDir" property, which will NOT contain a trailing separator.
		IOUtil.setProgramWorkingDir(directory);
		JGUIUtil.setLastFileDialogDirectory(directory);
		__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
		__initialWorkingDir = __props.getValue("WorkingDir");
	}
	catch ( Exception e ) {
		Message.printWarning (1, "writeDataSetFile", "Error writing file:\n\"" + file + "\"");
		// Leave the dirty flag the previous value.
	}
	// Update the status information.
	ui_UpdateStatus ( true );
}

/**
Handle ListSelectionListener events.
@param event ListSelectionEvent to process.
*/
public void valueChanged ( ListSelectionEvent e ) {
	// e.getSource() apparently does not return __commands_JList.
	// It must return a different component so don't check the object address.
	if ( ui_GetIgnoreListSelectionEvent() ) {
		return;
	}
    Object component = e.getSource();
    if ( component == __resultsOutputFiles_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = __resultsOutputFiles_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    uiAction_ShowResultsOutputFile( __resultsOutputFiles_JListModel.elementAt(i) );
                }
            }
        }
    }
    else if ( component == __resultsStateCUComponents_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = __resultsStateCUComponents_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    ui_DisplayResultsStateCUComponentTable ( __resultsStateCUComponents_JListModel.get(i) );
                }
            }
        }
    }
    else if ( component == __resultsStateModComponents_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = __resultsStateModComponents_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    ui_DisplayResultsStateModComponentTable ( __resultsStateModComponents_JListModel.get(i) );
                }
            }
        }
    }
    else if ( component == __resultsTables_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = __resultsTables_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    uiAction_ShowResultsTable( __resultsTables_JListModel.elementAt(i) );
                }
            }
        }
    }

	ui_UpdateStatus ( false );
}

/**
Handle TreeSelectionListener events.
@param event TreeSelectionEvent to process.
*/
public void valueChanged ( TreeSelectionEvent event ) {
	// For now just want to know when something changes so the GUI state can be checked.
	Object o = event.getSource();
	if ( (__appType == StateDMI.APP_TYPE_STATECU) && (o == __statecuDataset_JTree) ) {
		// User has selected a new component for editing/processing.
		// Only act on the first one.
		SimpleJTree_Node selected_node = __statecuDataset_JTree.getSelectedNode();
		// Only operate on groups...
		DataSetComponent comp = (DataSetComponent)selected_node.getData();
		if (	// TODO !comp.isGroup() ||
			// Allow individual components so that menus can be specifically enabled/disabled.
			(comp.getComponentType()== StateCU_DataSet.COMP_CONTROL_GROUP)){
			// No need to display a list.
			return;
		}
		__statecuSelectedComponent = comp;
		if ( __commandsDirty ) {
			// TODO - need to check to see if commands, etc., need to be saved before going to the next component group.
		}

		// Update the list.
		dataSet_UpdateList();
	}
	else if ((__appType == StateDMI.APP_TYPE_STATEMOD) && (o == __statemodDataset_JTree) ) {
		// User has selected a new component for editing/processing.  Only act on the first one.
		SimpleJTree_Node selected_node = __statemodDataset_JTree.getSelectedNode();
		// Only operate on groups.
		DataSetComponent comp = (DataSetComponent)selected_node.getData();
		if (	// TODO !cucomp.isGroup() ||
			// Allow individual components so that menus can be specifically enabled/disabled.
			(comp.getComponentType()== StateMod_DataSet.COMP_CONTROL_GROUP)){
			// No need to display a list.
			return;
		}
		__statemodSelectedComponent = comp;
		if ( __commandsDirty ) {
			// TODO - need to check to see if commands, etc., need to be saved before going to the next component group.
		}

		// Update the list.
		dataSet_UpdateList();
	}
	// This updates the menus to disable/enable based on the selected data component.
	ui_UpdateStatus ( true );
}

public void windowActivated(WindowEvent e) {
}

/**
Handle the closing of this window and the model network window because the GUI state is related.
*/
public void windowClosing(WindowEvent e) {
	// Verify before the window is closed.
	Component c = e.getComponent();
	if ( c == __network_JFrame ) {
		// Model network window is closing so turn off the model network window view (check it on to view it).
		__View_ModelNetwork_JCheckBoxMenuItem.setState(false);
		// Enable the File...New...Model Network (only want one of these open at a time).
		JGUIUtil.setEnabled ( __File_New_ModelNetwork_JMenuItem, true );
	}
	if ( c == this ) {
		// Check model network window - if it is open, give the user the option to save the results.
		if ( (__network_JFrame != null) && (__network_JFrame.isDirty() ) ) {
			// Changes have been made in the network and need to give the use the chance to save.
			int x = new ResponseJDialog ( this, "Network has not been saved.",
				"The network has edits that have not been saved.\n" +
				"Continue with exit and discard changes?",
				ResponseJDialog.YES|ResponseJDialog.NO).response();
			if ( x == ResponseJDialog.NO ) {
				setDefaultCloseOperation( DO_NOTHING_ON_CLOSE);
				return;
			}
		}
		uiAction_CloseClicked();
	}
}

public void windowClosed(WindowEvent e) {
	// Get the window that is being closed.  If it is the __geoview_JFrame, then set the __geoview_JFrame instance to null.
	Component c = e.getComponent();
	if ( (__geoview_JFrame != null) && (c == __geoview_JFrame) ) {
		// GeoView.
		__geoview_JFrame = null;
		__View_Map_JCheckBoxMenuItem.setSelected ( false );
	}
	else if ( (__statecuDatasetManager != null) && (c == __statecuDatasetManager) ) {
		// StateCU data set manager.
		__statecuDatasetManager = null;
		__View_DataSetManager_JCheckBoxMenuItem.setSelected ( false );
	}
}

public void windowDeactivated(WindowEvent e) {
}

public void windowDeiconified(WindowEvent e) {
}

public void windowIconified(WindowEvent e) {
}

public void windowOpened(WindowEvent e) {
}

/**
Internal class to handle action events from table results list.
*/
private class ActionListener_ResultsTables implements ActionListener {
    /**
    Handle a group of actions for the ensemble popup menu.
    @param event Event to handle.
    */
    public void actionPerformed (ActionEvent event) {
        String command = event.getActionCommand();

        if ( command.equals(__Results_Table_Properties_String) ) {
            uiAction_ShowTableProperties();
        }
    }
}

}