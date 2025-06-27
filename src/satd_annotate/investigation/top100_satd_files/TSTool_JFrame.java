// TSTool_JFrame - JFrame to provide the application interface for TSTool.

/* NoticeStart

TSTool
TSTool is a part of Colorado's Decision Support Systems (CDSS)
Copyright (C) 1994-2024 Colorado Department of Natural Resources

TSTool is free software:  you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

TSTool is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

You should have received a copy of the GNU General Public License
    along with TSTool.  If not, see <https://www.gnu.org/licenses/>.

NoticeEnd */

// TODO smalers 2004-08-29 Need to use HydroBase_Util preferredWDIDLength instead
// of carrying around a property - isolate all HydroBase properties to that
// package

package DWR.DMI.tstool;

// Swing UI classes from old AWT package.
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Toolkit;
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
import java.awt.print.PageFormat;
import java.awt.print.Paper;

// Classes for file I/O.
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
// Classes for reading web content.
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;

// Classes for Java utilities.
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

// Classes for UI Swing components (no longer part of Java core).
import javax.swing.BorderFactory;
import javax.swing.DefaultListModel;
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
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.JToolBar;
import javax.swing.ListSelectionModel;
import javax.swing.RootPaneContainer;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.event.ListDataEvent;
import javax.swing.event.ListDataListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.filechooser.FileFilter;

// Node network classes.
import org.openwaterfoundation.network.NodeNetwork;

import com.fasterxml.jackson.core.util.DefaultIndenter;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;
// Jackson classes for JSON processing.
import com.fasterxml.jackson.databind.ObjectMapper;

// Datastore core classes.
import riverside.datastore.DataStore;
import riverside.datastore.DataStoreSubstitute;
import riverside.datastore.DataStores_JFrame;
import riverside.datastore.GenericDatabaseDataStore;
import riverside.datastore.GenericDatabaseDataStore_TimeSeries_InputFilter_JPanel;
import riverside.datastore.PluginDataStore;

// Command processor core classes.
import rti.tscommandprocessor.core.GraphTemplateProcessor;
import rti.tscommandprocessor.core.TSCommandFactory;
import rti.tscommandprocessor.core.TSCommandFileRunner;
import rti.tscommandprocessor.core.TSCommandProcessor;
import rti.tscommandprocessor.core.TSCommandProcessorListModel;
import rti.tscommandprocessor.core.TSCommandProcessorThreadRunner;
import rti.tscommandprocessor.core.TSCommandProcessorUtil;
import rti.tscommandprocessor.core.TimeSeriesTreeView;
import rti.tscommandprocessor.core.TimeSeriesTreeView_JTree;
import rti.tscommandprocessor.core.TimeSeriesView;

// Command classes, some related to datastores that are built-in rather than plugins.
import rti.tscommandprocessor.commands.rccacis.RccAcisDataStore;
import rti.tscommandprocessor.commands.rccacis.RccAcis_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.reclamationhdb.ReclamationHDBDataStore;
import rti.tscommandprocessor.commands.reclamationhdb.ReclamationHDB_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.reclamationpisces.ReclamationPiscesDataStore;
import rti.tscommandprocessor.commands.reclamationpisces.ReclamationPisces_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.ts.FillPrincipalComponentAnalysis_JDialog;
import rti.tscommandprocessor.commands.ts.TSID_Command;
import rti.tscommandprocessor.commands.usgs.nwis.daily.UsgsNwisDailyDataStore;
import rti.tscommandprocessor.commands.usgs.nwis.daily.UsgsNwisDaily_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.usgs.nwis.groundwater.UsgsNwisGroundwaterDataStore;
import rti.tscommandprocessor.commands.usgs.nwis.groundwater.UsgsNwisGroundwater_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.usgs.nwis.instantaneous.UsgsNwisInstantaneousDataStore;
import rti.tscommandprocessor.commands.usgs.nwis.instantaneous.UsgsNwisInstantaneous_TimeSeries_InputFilter_JPanel;
import rti.tscommandprocessor.commands.util.Comment_Command;
import rti.tscommandprocessor.commands.util.Comment_JDialog;
import rti.tscommandprocessor.commands.util.EndFor_Command;
import rti.tscommandprocessor.commands.util.EndIf_Command;
import rti.tscommandprocessor.commands.util.Exit_Command;
import rti.tscommandprocessor.commands.util.For_Command;
import rti.tscommandprocessor.commands.util.If_Command;
// HydroBase datastore classes, which are built-in rather than a plugin.
import DWR.DMI.HydroBaseDMI.HydroBaseDMI;
import DWR.DMI.HydroBaseDMI.HydroBaseDataStore;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_AgriculturalCASSCropStats_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_AgriculturalCASSLivestockStats_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_AgriculturalNASSCropStats_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_CUPopulation_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_GroundWater_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_StationGeolocMeasType_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_StructureGeolocStructMeasType_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_GUI_StructureIrrigSummaryTS_InputFilter_JPanel;
import DWR.DMI.HydroBaseDMI.HydroBase_Util;
import DWR.DMI.HydroBaseDMI.ui.TSTool_HydroBase_GroundWaterWellsView_TableModel;
import DWR.DMI.HydroBaseDMI.ui.TSTool_HydroBase_StationGeolocMeasType_TableModel;
import DWR.DMI.HydroBaseDMI.ui.TSTool_HydroBase_StructureGeolocStructMeasType_TableModel;
import DWR.DMI.HydroBaseDMI.ui.TSTool_HydroBase_WellLevel_Day_TableModel;

// Data management interface utility code.
import RTi.DMI.DMI;
import RTi.DMI.ERDiagram_JFrame;

// TODO smalers 2023-02-02 old code that needs to be removed.
import RTi.DMI.NWSRFS_DMI.NWSCardTS;
import RTi.DMI.NWSRFS_DMI.NWSRFS_ConvertJulianHour_JDialog;
import RTi.DMI.NWSRFS_DMI.NWSRFS_DMI;

// GeoView map display classes.
import RTi.GIS.GeoView.GeoLayerView;
import RTi.GIS.GeoView.GeoRecord;
import RTi.GIS.GeoView.GeoViewJFrame;
import RTi.GIS.GeoView.GeoViewListener;

// Graphing general classes.
import RTi.GR.GRLimits;
import RTi.GR.GRPoint;
import RTi.GR.GRShape;

// Time series graphing classes.
import RTi.GRTS.TSProcessor;
import RTi.GRTS.TSProduct;
import RTi.GRTS.TSProductProcessor;
import RTi.GRTS.TSPropertiesJFrame;
import RTi.GRTS.TSViewJFrame;

// Time series core classes.
import RTi.TS.TS;
import RTi.TS.TSEnsemble;
import RTi.TS.TSIdent;
import RTi.TS.TSStatisticType;
import RTi.TS.TSUtil;
import RTi.TS.TSUtil_CreateTracesFromTimeSeries;
import RTi.TS.TSUtil_NewStatisticTimeSeriesFromEnsemble;
import RTi.TS.TransferDataHowType;

// UI classes built on Swing.
import RTi.Util.GUI.FindInJListJDialog;
import RTi.Util.GUI.HelpAboutJDialog;
import RTi.Util.GUI.InputFilter_JPanel;
import RTi.Util.GUI.JFileChooserFactory;
import RTi.Util.GUI.JGUIUtil;
import RTi.Util.GUI.JScrollWorksheet;
import RTi.Util.GUI.JWorksheet;
import RTi.Util.GUI.JWorksheet_AbstractRowTableModel;
import RTi.Util.GUI.JWorksheet_Listener;
import RTi.Util.GUI.ReportJFrame;
import RTi.Util.GUI.ResponseJDialog;
import RTi.Util.GUI.SimpleFileFilter;
import RTi.Util.GUI.SimpleJButton;
import RTi.Util.GUI.SimpleJComboBox;
import RTi.Util.GUI.SimpleJMenuItem;
import RTi.Util.GUI.TextResponseJDialog;

// Documentation help viewer classes.
import RTi.Util.Help.HelpViewer;
import RTi.Util.Help.HelpViewerUrlFormatter;

// I/O classes for commands and general utilities.
import RTi.Util.IO.AbstractCommand;
import RTi.Util.IO.AnnotatedCommandJList;
import RTi.Util.IO.Command;
import RTi.Util.IO.CommandAsText_JDialog;
import RTi.Util.IO.CommandDiscoverable;
import RTi.Util.IO.CommandListUI;
import RTi.Util.IO.CommandLogRecord;
import RTi.Util.IO.CommandLog_CellRenderer;
import RTi.Util.IO.CommandLog_TableModel;
import RTi.Util.IO.CommandPhaseType;
import RTi.Util.IO.CommandProcessor;
import RTi.Util.IO.CommandProcessorListener;
import RTi.Util.IO.CommandProcessorRequestResultsBean;
import RTi.Util.IO.CommandProgressListener;
import RTi.Util.IO.CommandSavesMultipleVersions;
import RTi.Util.IO.CommandStatus;
import RTi.Util.IO.CommandStatusProvider;
import RTi.Util.IO.CommandStatusType;
import RTi.Util.IO.CommandStatusUtil;
import RTi.Util.IO.DataUnits;
import RTi.Util.IO.DataUnits_JFrame;
import RTi.Util.IO.HTMLViewer;
import RTi.Util.IO.IOUtil;
import RTi.Util.IO.PropList_CellRenderer;
import RTi.Util.IO.PropList_TableModel;
import RTi.Util.IO.TextPrinterJob;
import RTi.Util.IO.ProcessManager;
import RTi.Util.IO.Prop;
import RTi.Util.IO.PropList;
import RTi.Util.IO.UnknownCommand;
import RTi.Util.IO.UnknownCommandException;

// JSON classes.
import RTi.Util.JSON.JSONObject;

// Custom logging classes.
import RTi.Util.Message.DiagnosticsJFrame;
import RTi.Util.Message.Message;
import RTi.Util.Message.MessageLogListener;

// String utility classes.
import RTi.Util.String.StringUtil;

// Data table utility classes.
import RTi.Util.Table.DataTable;
import RTi.Util.Table.DataTable_JFrame;
import RTi.Util.Table.TableColumnType;
import RTi.Util.Table.TableField;
import RTi.Util.Table.TableRecord;

// Date/time utility classes.
import RTi.Util.Time.DateTime;
import RTi.Util.Time.DateTimeBuilderJDialog;
import RTi.Util.Time.DateTimeToolsJDialog;
import RTi.Util.Time.StopWatch;
import RTi.Util.Time.TimeInterval;
import RTi.Util.Time.YearType;

// Classes to integrate TSTool with datastores, mainly time series catalog and filters used in the UI.
import cdss.app.tstool.datastore.cdss.datevalue.TSTool_DateValue;
import cdss.app.tstool.datastore.cdss.hydrobase.TSTool_HydroBase;
import cdss.app.tstool.datastore.cdss.hydrobaserest.TSTool_HydroBaseRest;
import cdss.app.tstool.datastore.cdss.statecu.TSTool_StateCU;
import cdss.app.tstool.datastore.cdss.statecub.TSTool_StateCUB;
import cdss.app.tstool.datastore.cdss.statemod.TSTool_StateMod;
import cdss.app.tstool.datastore.cdss.statemodb.TSTool_StateModB;
import cdss.app.tstool.datastore.csu.modsim.TSTool_Modsim;
import cdss.app.tstool.datastore.generic.TSTool_Generic;
import cdss.app.tstool.datastore.nwsrfs.card.TSTool_NwsrfsCard;
import cdss.app.tstool.datastore.nwsrfs.esp.TSTool_NwsrfsEsp;
import cdss.app.tstool.datastore.nwsrfs.fs5files.TSTool_FS5Files;
import cdss.app.tstool.datastore.plugin.TSTool_Plugin;
import cdss.app.tstool.datastore.rcc.acis.TSTool_RccAcis;
import cdss.app.tstool.datastore.usace.hecdss.TSTool_HecDss;
import cdss.app.tstool.datastore.usbr.hdb.TSTool_HDB;
import cdss.app.tstool.datastore.usbr.pisces.TSTool_Pisces;
import cdss.app.tstool.datastore.usbr.riverware.TSTool_RiverWare;
// Classes that integrate TSTool with datastores and input types.
import cdss.app.tstool.datastore.usgs.nwis.TSTool_UsgsNwis;

// HydroBase REST datastore, built-in and not a plugin.
import cdss.dmi.hydrobase.rest.ColoradoHydroBaseRestDataStore;
import cdss.dmi.hydrobase.rest.ui.ColoradoHydroBaseRest_ClimateStation_InputFilter_JPanel;
import cdss.dmi.hydrobase.rest.ui.ColoradoHydroBaseRest_Structure_InputFilter_JPanel;
import cdss.dmi.hydrobase.rest.ui.ColoradoHydroBaseRest_SurfaceWaterStation_InputFilter_JPanel;
import cdss.dmi.hydrobase.rest.ui.ColoradoHydroBaseRest_TelemetryStation_InputFilter_JPanel;
import cdss.dmi.hydrobase.rest.ui.ColoradoHydroBaseRest_Well_InputFilter_JPanel;

// CDSS node network core classes.
import cdss.domain.hydrology.network.HydrologyNode;
import cdss.domain.hydrology.network.HydrologyNodeNetwork;

/**
JFrame to provide the application interface for TSTool.
This class provides the following main functionality:
<ol>
<li>	Provide a left-to-right, top-to-bottom control of user interaction.</li>
<li>	Provide capability to interactively insert/delete/move/edit commands.</li>
<li>	Provide feedback on command initialization/discovery/run status.</li>
<li>	Execute a TSCommandProcessor to generate time series output and provide access to results.</li>
<li>	Interact with TSCommandProcessor via a list model (derived from AbstractListModel).</li>
</ol>
*/
@SuppressWarnings("serial")
public class TSTool_JFrame extends JFrame
implements
ActionListener, // To handle menu selections in GUI.
CommandListUI, // To integrate this UI with command tools.
CommandProcessorListener, // To handle command processor progress updates (when commands start/finish).
CommandProgressListener, // To update the status based on progress within a command.
GeoViewListener, // To handle map interaction (not well developed).
ItemListener, // To handle choice selections in GUI.
HelpViewerUrlFormatter, // To format URLs to display in a web browser.
JWorksheet_Listener, // To handle query result interaction.
KeyListener, // To handle keyboard input in GUI.
ListDataListener, // To change the GUI state when commands list change.
ListSelectionListener,
MessageLogListener, // To handle interaction between log view and command list.
MouseListener,
TSProductProcessor, // To handle requests from components to process *.tsp files.
WindowListener // To handle window/app shutdown, in particular if called in headless mode and TSView controls.
{

//================================
//  Data Members
//================================

/**
TSTool session information, used to track command file open history, etc.
*/
private TSToolSession session = null;

/**
 * Modifier for title, to customize the TSTool session:
 * - for example, this is used when running TSTool in Linux as root rather than a normal user, for automated tests
 */
private String titleMod = null;

/**
 * Datastore substitutions, to allow using general datastore name in commands but a more specific
 * datastore is actually configured.
 */
private List<DataStoreSubstitute> datastoreSubstituteList = new ArrayList<>();

/**
Map interface.
*/
private GeoViewJFrame __geoview_JFrame = null;

//================================
// Query area.
//================================

// TODO smalers 2013-04-15 Make local if tabbed pane works well for datastores and input types.
/**
Label for datastores, necessary because label will be set not visible if no datastores.
*/
private JLabel __dataStore_JLabel = null;

// TODO smalers phase in file datastore at some point.
/**
Tabbed panel to keep datastores and input types separate.
*/
private JTabbedPane __dataStore_JTabbedPane = null;

/**
Available datastores.
*/
private SimpleJComboBox __dataStore_JComboBox = null;

/**
Label to show at startup.
*/
private JPanel __dataStoreInitializing_JPanel = null;

/**
Available input types including enabled file and databases.
*/
private SimpleJComboBox	__inputType_JComboBox = null;

/**
Input name choice label.  This may be set (in)visible depending on selected datastore or input type.
*/
private JLabel __inputName_JLabel = null;

/**
Available input names for the input type (history of recent choices and allow browse where necessary).
*/
private SimpleJComboBox __inputName_JComboBox = null;

/**
Data type choice.
*/
private SimpleJComboBox __dataType_JComboBox = null;

/**
Time step for initial query.
*/
private SimpleJComboBox __timeStep_JComboBox = null;

/**
List of InputFilter_JPanel.
One of these will be visible at any time to provide query filter capability.
Each input type or datastore can have 1+ input filter panels, based on the data type and interval.
If no input filter is relevant, then the generic input filter with only text label (blank) is shown.
*/
private List<InputFilter_JPanel> __inputFilterJPanelList = new Vector<>();

/**
The currently selected input filter JPanel, used to check input and get the filter information for queries.
*/
private InputFilter_JPanel __selectedInputFilter_JPanel = null;

/**
JPanel for input types that do not support input filters.
*/
private InputFilter_JPanel __inputFilterGeneric_JPanel = null;

/**
JPanel for message when input input filters are disabled
(e.g., input type is selected but database connection is not available.
*/
private InputFilter_JPanel __inputFilterMessage_JPanel = null;

/**
Used to keep track of the layout position for the input filter panels because the
panel cannot be initialized until after database connections are made.
*/
private int __inputFilterY = 0;

// TODO smalers Evaluate usability - does not seem to work! - popup on popup.
/**
Used with input name to allow a new input name to be specified.
Tried using a "Browse..." choice but the problem is that an event will not be generated if the item state does not change.
*/
private JPopupMenu __input_name_JPopupMenu = null;

/**
Get Time Series List button.
*/
private SimpleJButton __get_ts_list_JButton;

/**
Copy selected time series from list to commands (as time series identifiers).
*/
private SimpleJButton __CopySelectedToCommands_JButton;

/**
Copy all time series from list to commands (as time series identifiers).
*/
private SimpleJButton __CopyAllToCommands_JButton;

/**
Panel for input options.
*/
private JPanel __queryInput_JPanel;

/**
Text field indicating that datastores are initializing.
*/
private JLabel __dataStoreInitializing_JLabel;

/**
Panel to hold results of time series header lists.
*/
private JPanel __query_results_JPanel;

/**
Panel for commands.
*/
private JPanel __commands_JPanel;

/**
Time series catalog worksheet.
*/
private JWorksheet __query_JWorksheet;

/**
Table model for query results.
*/
@SuppressWarnings("rawtypes")
private JWorksheet_AbstractRowTableModel __query_TableModel = null;

//================================
// Commands area.
//================================

/**
Annotated list to hold commands and display the command status.
*/
private AnnotatedCommandJList __commands_AnnotatedCommandJList;

/**
List model that maps the TSCommandProcessor Command data to the command JList:
- adding, removing, or changing items in the TSCommandProcessor will fire events in the model,
  which will cause the List to respond
*/
private TSCommandProcessorListModel __commands_JListModel;

/**
Run the selected commands.
*/
private SimpleJButton __Run_SelectedCommands_JButton;

/**
Run all the commands.
*/
private SimpleJButton __Run_AllCommands_JButton;

/**
Clear commands(s).
*/
private SimpleJButton __ClearCommands_JButton;

/**
The list of Command that is used with cut/copy/paste user actions.
*/
private List<Command> __commandsCutBuffer = new Vector<>(100,100);

// TODO smalers 2007-11-02 Evaluate putting in the processor.
/**
Indicates whether the commands have been edited without being saved.
This will trigger some changes in the UI, for example indicating that the commands
have been modified and need to be saved (or cancel) before exit.
*/
private boolean __commandsDirty = false;

/**
Name of the command file, as absolute path.
Don't set until selected by the user (or on the command line).
*/
private String __commandFileName = null;

//================================
// Results area.
//================================

/**
Tabbed pane to include all results.
*/
private JTabbedPane __results_JTabbedPane;

/**
Panel for TSEnsemble results.
*/
private JPanel __resultsTSEnsembles_JPanel;

/**
Final list showing in-memory time series ensemble results.
*/
private JList<String> __resultsTSEnsembles_JList;

/**
JList data model for final time series ensembles (basically a list of
time series associated with __results_tsensembles_JList).
*/
private DefaultListModel<String> __resultsTSEnsembles_JListModel;

/**
 * Button to graph an ensemble with the indicated template.
 */
private SimpleJButton __resultsTSEnsemblesGraphTemplates_JButton = null;

/**
 * ComboBox list of ensemble graph templates.
 */
private SimpleJComboBox __resultsTSEnsemblesGraphTemplates_JComboBox = null;

/**
Popup menu for ensemble results.
*/
private JPopupMenu __resultsTSEnsembles_JPopupMenu = null;

/**
Worksheet that contains a list of problems from processing:
- created once and reused
*/
private JWorksheet __resultsProblems_JWorksheet = null;

/**
Worksheet that contains a list of processor properties:
- created once and reused
*/
private JWorksheet __resultsProperties_JWorksheet = null;

/**
Panel for TS results.
*/
private JPanel __resultsTS_JPanel;

/**
Final list showing in-memory time series results.
*/
private JList<String> __resultsTS_JList;

/**
JList data model for final time series (basically a list of time series associated with __results_ts_JList).
*/
private DefaultListModel<String> __resultsTS_JListModel;

/**
 * Button to cause a graph template to be used to graph a time series:
 * - this is allows a user to streamline producing standard graphs
 */
private SimpleJButton __resultsTSGraphTemplates_JButton;

/**
 * ComboBox to list graph templates for the time series results.
 */
private SimpleJComboBox __resultsTSGraphTemplates_JComboBox;

/**
The command processor, which maintains a list of command objects, process the data, and the time series results.
There is only one command processor instance for a TSTool session and it is kept current with the application.
TODO smalers 2009-03-06 In the future, if threading is implemented, it may be possible to have,
for example, tabs for different command files, each with a TSCommandProcessor.
*/
private TSCommandProcessor __tsProcessor = new TSCommandProcessor(null);
// Create an instance to avoid null, but is recreated when initializing the UI.

/**
Thread that is used to run the command processor.
This will be set when the process starts and then set to null when complete.
The thread is used to allow kill on the processor.
*/
private Thread __tsProcessorThread = null;

/**
Popup menu for time series results.
*/
private JPopupMenu __resultsTS_JPopupMenu = null;

/**
List of results networks for viewing with an editor.
*/
private JList<String> __resultsNetworks_JList = null;

/**
Popup menu for networks results.
*/
private JPopupMenu __resultsNetworks_JPopupMenu = null;

/**
JList data model for networks (a list of network identifiers associated with __results_networks_JList).
*/
private DefaultListModel<String> __resultsNetworks_JListModel;

/**
List of results objects for viewing with an editor.
*/
private JList<String> __resultsObjects_JList = null;

/**
Popup menu for objects results.
*/
private JPopupMenu __resultsObjects_JPopupMenu = null;

/**
JList data model for objects (a list of object identifiers associated with __results_objects_JList).
*/
private DefaultListModel<String> __resultsObjects_JListModel;

/**
List of results output files for viewing with an editor.
*/
private JList<String> __resultsOutputFiles_JList = null;

/**
JList data model for final time series (a list of filenames associated with __resultsOutputFiles_JList).
*/
private DefaultListModel<String> __resultsOutputFiles_JListModel;

/**
Label for output file list, to indicate how many files.
*/
private JLabel __resultsOutputFiles_JLabel = null;

/**
Popup menu for objects results.
*/
private JPopupMenu __resultsOutputFiles_JPopupMenu = null;

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
Label for table file list, to indicate how many tables.
*/
private JLabel __resultsTables_JLabel = null;

/**
Panel for results views.
*/
private JPanel __resultsViews_JPanel;

/**
Tabbed pane for views within the view results.
*/
private JTabbedPane __resultsViews_JTabbedPane;

//================================
// Status-area related.
//================================

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

//================================
// General.
//================================

// TODO smalers 2011-05-18 It may be OK to phase these out in favor of processor properties
// (like the working directory) in particular since only a select few properties are handled here.
/**
A subset of TSTool application configuration properties, which are initialized from the configuration file
and are then updated in the TSTool environment.
*/
private PropList __props = null;

// TODO smalers 2021-07-29 remove this when tested out - initial properties are saved with the processor.
/**
 * Properties from the command line to be assigned in the processor before each run.
 * These properties can be specified on TSTool command line with Property==Value.
 */
//private PropList initialProps = null;

/**
The initial working directory corresponding to a command file read/write or File... Set Working Dir.
This is used when processing the list of setWorkingDir() commands passed to command editors.
Without the initial working directory,
relative changes in the working directory will result in an inaccurate initial state.
*/
private String __initialWorkingDir = "";

/**
 * Whether the command file has a #@sourceUrl annotation:
 * - used to enable/disable the View / Command File Source Diff menu
 * - change the value when inserting or editing a Comment_Command command
 */
private boolean commandsHaveSourceUrlAnnotation = false;

/**
The last directory selected with Run...Command File, to run an external command file.
*/
private String __Dir_LastExternalCommandFileRun = null;

/**
The last directory selected when loading a command file.
*/
private String __Dir_LastCommandFileOpened = null;

/**
Lets the checkGUIState() method avoid checking for many null components during startup.
*/
private boolean __guiInitialized = false;

/**
Use this to temporarily ignore item action performed events,
necessary when programmatically modifying the contents of combo boxes.
*/
private boolean __ignoreActionEvent = false;

// TODO smalers 2007-10-19 Evaluate whether still needed with new list model.
/**
Use this to temporarily ignore item listener events,
necessary when programmatically modifying the contents of combo boxes.
*/
private boolean __ignoreItemEvent = false;

/**
This is used in some cases to disable updates during bulk operations to the commands list.
*/
private boolean __ignoreListSelectionEvent = false;

/**
Indicates which built-in datastores and input types are enabled.
Defaults are actually definitively set when the configuration file properties are evaluated.
*/
private boolean
    __source_ColoradoHydroBaseRest_enabled = true, // By default - allow all to access web service.
	__source_DateValue_enabled = true,
	__source_DelftFews_enabled = true,
	__source_HECDSS_enabled = true,
	__source_HydroBase_enabled = true,
	__source_MODSIM_enabled = true,
	__source_NrcsAwdb_enabled = true,
	__source_NWSCard_enabled = true,
	__source_NWSRFS_FS5Files_enabled = false,
	__source_NWSRFS_ESPTraceEnsemble_enabled = false,
	__source_RCCACIS_enabled = false,
	__source_ReclamationHDB_enabled = false,
	__source_ReclamationPisces_enabled = false,
	__source_RiverWare_enabled = true,
	__source_SHEF_enabled = true,
	__source_StateCU_enabled = true,
	__source_StateCUB_enabled = true,
	__source_StateMod_enabled = true,
	__source_StateModB_enabled = true,
	__source_UsgsNwisDaily_enabled = true,
	__source_UsgsNwisGroundwater_enabled = true,
	__source_UsgsNwisInstantaneous_enabled = true,
	__source_UsgsNwisRdb_enabled = true,
	__source_WaterML_enabled = true,
	__source_WaterOneFlow_enabled = false;

/**
Indicates if the main GUI should be shown.
This is normally true but if false then only graph windows will be shown, and when closed the app will close.
This is used when calling TSTool from other software (e.g., to provide graphing capabilities to GIS applications).
*/
//private boolean __show_main = true;

//================================
// Main toolbar
//================================

private SimpleJButton
    __toolbarNew_JButton = null,
    __toolbarOpen_JButton = null,
    __toolbarSave_JButton = null;


/**
TSTool_JFrame constructor.
@param session TSTool session, which provides user and environment information.
@param commandFile Name of the command file to load at initialization.
@param runOnLoad If true, a successful load of a command file will be followed by running the commands.
If false, the command file will be loaded but not automatically run.
@param pluginDataStoreClassList list of classes for plugin datastores.
@param pluginCommandClassList list of classes for plugin commands.
@param initialProps properties to initialize in the command processor at the start of processing
@param datastoreSubstituteMap used by the processor to map datastore names in command files with the datastore to be used,
useful for testing to globally use a different datastore
@param titleMod modifier for the title, used with --ui-title to customize the TSTool title
*/
public TSTool_JFrame (
	TSToolSession session,
	String commandFile,
	boolean runOnLoad,
	@SuppressWarnings("rawtypes") List<Class> pluginDataStoreClassList,
	@SuppressWarnings("rawtypes") List<Class> pluginDataStoreFactoryClassList,
	@SuppressWarnings("rawtypes") List<Class> pluginCommandClassList,
	PropList initialProps,
	List<DataStoreSubstitute> datastoreSubstituteList,
	String titleMod ) {
	super();

	// Stopwatch to track performance.
	StopWatch swMain = new StopWatch();
	swMain.start();
	String routine = "TSTool_JFrame";

	// Let the Message class know the frame so that message dialogs can pop up on top:
	// - this can also be used when instantiating Runnable instances that can't access 'this' for the JFrame

	Message.setTopLevel ( this );

	// Session to track command file history and other user session properties.
	this.session = session;

	// Save the list of plugin datastores, which will be used to initialize datastores.
	TSTool_Plugin.getInstance(this).setPluginDataStoreClassList ( pluginDataStoreClassList );
	TSTool_Plugin.getInstance(this).setPluginDataStoreFactoryClassList ( pluginDataStoreFactoryClassList );

	// Save the list of plugin classes, which will be used to initialize command menus.
	TSTool_Plugin.getInstance(this).setPluginCommandClassList ( pluginCommandClassList );

	// Save the title modifier.
	if ( titleMod == null ) {
		this.titleMod = "";
	}
	else {
		this.titleMod = titleMod;
	}

	// TODO smalers 2021-07-29 Remove when tested out - initial properties are in the processor.
	// Set the processor properties.
	//this.initialProps = initialProps;

	// Set the initial working directory up front because it is used in the command processor and edit dialogs.

	this.__props = new PropList("TSTool_JFrame");
	this.__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
	ui_SetInitialWorkingDir (this.__props.getValue ( "WorkingDir" ));

	addWindowListener ( this );

	// Initialize the input types and datastores based on the configuration.
	ui_EnableInputTypesForConfiguration ();

	// Values determined at run-time.

	this.__props.setHowSet ( Prop.SET_AS_RUNTIME_DEFAULT );
	this.__props.set ( "WorkingDir", IOUtil.getProgramWorkingDir() );
	Message.printStatus ( 1, "", "Working directory is " + this.__props.getValue ( "WorkingDir" ) );
	this.__props.setHowSet ( Prop.SET_AT_RUNTIME_BY_USER );

	// Set the icon to use for windows.
	TSToolMain.setIcon ( "CDSS" );

	// Create the UI:
	// - this also creates the processor instance so will be non-null after this call
	StopWatch in = new StopWatch();
	in.start();
	ui_InitGUI ( initialProps );
	in.stop();

	// Set the plugin command classes in the processor:
	// - this is necessary so that they can be used when TSCommandFactory instance is created
	this.__tsProcessor.setPluginCommandClasses ( pluginCommandClassList, false );

	// Set the datastore substitute map:
	// - also save locally for use when showing the datastores
	this.__tsProcessor.setDatastoreSubstituteList(datastoreSubstituteList);
	this.datastoreSubstituteList = datastoreSubstituteList;

    // Get database connection information.  Force a login if the database connection cannot be made.
	// The login is interactive and is disabled if no main GUI is to be shown.

	swMain.stop();

	// Show the HydroBase login dialog only if a CDSS license.
	// Or, configure HydroBase information in the TSTool configuration file.
	// FIXME smalers 2008-10-02 Need to confirm that information can be put in the file.
	if ( this.__source_HydroBase_enabled ) { //&& license_IsInstallCDSS(__licenseManager) ) { // }
		// Login to HydroBase using information in the TSTool configuration file.
		TSTool_HydroBase.getInstance(this).openHydroBase ( true, TSToolMenus.File_Properties_HydroBase_JMenuItem );
		// Force the choices to refresh.
		if ( TSTool_HydroBase.getInstance(this).getHydroBaseDMILegacy() != null ) {
			this.__inputType_JComboBox.select ( null );
			this.__inputType_JComboBox.select (TSToolConstants.INPUT_TYPE_HydroBase);
			// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
			this.__dataStore_JTabbedPane.setSelectedIndex(0);
		}
	}
	if ( this.__source_NWSRFS_FS5Files_enabled ) {
		// Open NWSRFS FS5Files using information in the TSTool configuration file.
		TSTool_FS5Files.getInstance(this).openNwsrfsFS5Files ( null, true, TSToolMenus.File_Properties_NWSRFSFS5Files_JMenuItem );
		// Force the choices to refresh.
		if ( TSTool_FS5Files.getInstance(this).getNwsrfsFS5FilesDMI() != null ) {
			/* TODO smalers 2004-09-10 DO NOT DO THIS BECAUSE IT THEN PROMPTS FOR a choice.
			__inputType_JComboBox.select ( null );
			__inputType_JComboBox.select ( __INPUT_TYPE_NWSRFS_FS5Files );
			*/
		}
	}

	// Open remaining datastores, displaying dialog if SystemLogin or SystemPassword property is "prompt".
	// TODO smalers 2010-09-03 migrate more input types to datastores.
	try {
		Message.printStatus(2, routine, "Opening datastores from TSTool GUI...");
	    TSToolMain.openDataStoresAtStartup(session,__tsProcessor,
	    	TSTool_Plugin.getInstance(this).getPluginDataStoreClassList(),
	    	TSTool_Plugin.getInstance(this).getPluginDataStoreFactoryClassList(),false);
	}
	catch ( Exception e ) {
	    Message.printStatus ( 1, routine, "Error opening datastores (" + e + ")." );
	}

	// Populate the datastore choices in the UI.

	ui_DataStoreList_Populate ();

	// Add GUI features that depend on the databases.
	// The appropriate panel will be set visible as input types and data types are chosen.
	// The panels are currently only initialized once so changing databases or enabling new databases after setup may require
	// some code changes if not implemented already.
	// Set the wait cursor because queries are done during setup.

	JGUIUtil.setWaitCursor ( this, true );
	try {
	    ui_InitGUIInputFilters ( ui_GetInputFilterY() );
	}
	catch ( Exception e ) {
		Message.printWarning ( 3, routine, "For developers:  caught exception initializing input filters at setup." );
		Message.printWarning ( 3, routine, e );
	}
	// TODO smalers 2007-01-23 Evaluate use.
	// Force everything to refresh based on the current GUI layout.  Still evaluating this.
	this.invalidate ();
	JGUIUtil.setWaitCursor ( this, false );

	// Use the window listener.

	ui_UpdateStatus ( true );

	// If running with a command file from the command line, we don't.
	// normally want to see the main window so handle with a special case.

	// TSTool has been started with a command file so try to open and display.  It should already be absolute.
	boolean runDiscoveryOnLoad = true;
	if ( (commandFile != null) && (commandFile.length() > 0) ) {
	    ui_LoadCommandFile ( commandFile, runOnLoad, runDiscoveryOnLoad );
	}

	Message.printStatus(2, routine, "====================================================================================");
	Message.printStatus(2, routine, "Done initializing the TSTool user interface (UI) and datastores:" );
	Message.printStatus(2, routine, " - following log messages will be in response to user actions and running commands" );
	Message.printStatus(2, routine, " - start TSTool with -d 1 (or higher number) to turn on debug for troubleshooting" );
	Message.printStatus(2, routine, "====================================================================================");
}

/**
Handle action events (menu and button actions).
@param event Event to handle.
*/
public void actionPerformed (ActionEvent event) {
	if ( ui_GetIgnoreActionEvent() ) {
		// Ignore ActionEvent for programmatic modification of data models.
		return;
	}
	try {
        // This will chain, calling several methods, so that each method does not get so large.

		uiAction_ActionPerformed01_MainActions(event);

		// Check the GUI state and disable buttons, etc., depending on the selections that are made.

		ui_UpdateStatus ( true );
	}
	catch ( Exception e ) {
		// Unexpected exception - user will likely see no result from their action.
		String routine = getClass().getSimpleName() + ".actionPerformed";
		Message.printWarning ( 2, routine, e );
		JGUIUtil.setWaitCursor ( this, false );
	}
}

/**
Indicate that a command has been canceled.
The success/failure of the command is not indicated (see CommandStatusProvider).
@param icommand The command index (0+).
@param ncommand The total number of commands to process
@param command The reference to the command that has been canceled, either the
one that has just been processed, or potentially the next one, depending on when the cancel was requested.
@param percent_complete If >= 0, the value can be used to indicate progress running a list of commands (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its
own determination (e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandCanceled ( int icommand, int ncommand, Command command, float percent_complete, String message ) {
	String routine = getClass().getSimpleName() + ".commandCanceled";

	// Refresh the results with what is available.
	//String command_string = command.toString();
	ui_UpdateStatusTextFields ( 1, routine,	"Canceled command processing.",
			//"Canceled: " + command_string,
				null, TSToolConstants.STATUS_CANCELED );
	uiAction_RunCommands_ShowResults ();
}

/**
Indicate that a command has completed.
The success/failure of the command is not indicated (see CommandStatusProvider).
@param icommand The command index (0+).
@param ncommand The total number of commands to process
@param command The reference to the command that is completed,
provided to allow future interaction with the command.
@param percent_complete If >= 0, the value can be used to indicate progress running a list of commands (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its
own determination (e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandCompleted ( int icommand, int ncommand, Command command, float percent_complete, String message ) {
	String routine = getClass().getSimpleName() + ".commandCompleted";
	// Update the progress bar to indicate progress (1 to number of commands... completed).
	this.__processor_JProgressBar.setValue ( icommand + 1 );
	// For debugging.
	//Message.printStatus(2,getClass().getSimpleName()+".commandCompleted", "Setting processor progress bar to " + (icommand + 1));
	this.__command_JProgressBar.setValue ( this.__command_JProgressBar.getMaximum() );
	// Set the tooltip text for the progress bar to indicate the numbers.
	String tip = "Completed command " + (icommand + 1) + " of " + ncommand;
    this.__processor_JProgressBar.setToolTipText ( tip );

    // If the last command was a comment with @require that was not met, need to detect:
    // - for now brute force design is to search for "Exit processing" in command log message.
    // - TODO smalers 2021-10-19 could detect specific case with more coding
    boolean requireExit = false;
    if ( command instanceof Comment_Command ) {
    	Comment_Command comment = (Comment_Command)command;
    	if ( comment.getCommandString().indexOf("@require user") > 0 ) {
    		// Currently the only case where an exit may result:
    		// - don't need to do a full update of results, just the gutters
            // - repaint the list to reflect the status of the commands
            ui_ShowCurrentCommandListStatus (CommandPhaseType.RUN);
    	}
    }
	if ( ((icommand + 1) == ncommand) || command instanceof Exit_Command || requireExit ) {
		// Last command has completed (or Exit() command) so refresh the time series results.
		// Only need to do if threaded because otherwise will handle synchronously
		// in the uiAction_RunCommands() method.
		String command_string = command.toString();
		ui_UpdateStatusTextFields ( 1, routine, null, "Processed: " + command_string, TSToolConstants.STATUS_READY );
		if ( ui_Property_RunCommandProcessorInThread() ) {
			uiAction_RunCommands_ShowResults ();
		}
	}
}

/**
 * Check command list comments for needed information.
 * Currently this only checks for #@sourceUrl in order to enable/disable the View / Command File Source Diff menu.
 */
private void commandList_CheckComments() {
	// Loop through the commands.
	int size = this.__commands_JListModel.size();
	Object command = null;
	String commandStringUpper = null;
	Comment_Command commentCommand = null;

	for ( int i = 0; i < size; i++ ) {
		command = (Object)this.__commands_JListModel.get(i);
		if ( command instanceof Comment_Command ) {
			commentCommand = (Comment_Command)command;
			commandStringUpper = commentCommand.getCommandString().toUpperCase();
			if ( commandStringUpper.contains("@SOURCEURL") ) {
				// This should be fast if the comment exists at the top of the command file.
				this.commandsHaveSourceUrlAnnotation = true;
				break;
			}
		}
	}
}

/**
Determine whether commands are equal.
To allow for multi-line commands, each command is stored in a list (but typically only the first String is used.
@param originalCommand Original command as a list of String or Command.
@param editedCommand Edited command as a list of String or Command.
*/
private boolean commandList_CommandsAreEqual(List originalCommand, List editedCommand) {
	if ( (originalCommand == null) && (editedCommand != null) ) {
		return false;
	}
	else if ( (originalCommand != null) && (editedCommand == null) ) {
		return false;
	}
	else if ( (originalCommand == null) && (editedCommand == null) ) {
		// Should never occur?
		return true;
	}
	int originalSize = originalCommand.size();
	int editedSize = editedCommand.size();
	if ( originalSize != editedSize ) {
		return false;
	}
	Object originalObject, editedObject;
	String originalString = null, editedString = null;
	for ( int i = 0; i < originalSize; i++ ) {
		originalObject = originalCommand.get(i);
		editedObject = editedCommand.get(i);
		if ( originalObject instanceof String ) {
			originalString = (String)originalObject;
		}
		else if ( originalObject instanceof Command ) {
			originalString = ((Command)originalObject).toString();
		}
		if ( editedObject instanceof String ) {
			editedString = (String)editedObject;
		}
		else if ( editedObject instanceof Command ) {
			editedString = ((Command)editedObject).toString();
		}
		// Must be an exact match.
		if ( (originalString == null) && (editedString != null) ) {
			return false;
		}
		else if ((originalString != null) && (editedString == null)) {
			return false;
		}
		else if ((originalString == null) && (editedString == null)) {
			continue;
		}
		else if ( !originalString.equals(editedString) ) {
			return false;
		}
	}
	// Must be the same.
	return true;
}

/**
 * Determine the indent spaces for a command that is being inserted.
 * This method should be called before inserting the command.
 * The indent is determined as follows:
 * <ul>
 * <li> If the previous command is null, return an empty string.</li>
 * <li> If the previous command is an If or For, indent one level more than the previous command.</li>
 * <li> If the current command is an EndIf or EndFor, indent one level less than the previous command (or zero).</li>
 * <li> Else, use the same indent as the previous command.</li>
 * </ul>
 * @param commandToInsert the command that will be inserted
 * @param commandPrevious previous command
 */
private String commandList_DetermineNewCommandIndent(Command commandToInsert, Command commandPrevious) {
	if ( commandPrevious == null ) {
		// No previous command.
		return "";
	}
	String routine = getClass().getSimpleName() + "commandList_DetermineNewCommandIndent";
	String prevIndentSpaces = "";
	String indentSpaces = "";
	// Get the previous command.
	if ( Message.isDebugOn ) {
		Message.printStatus(2, routine, "Determining indent spaces for new command \"" + commandToInsert
			+ "\" after command \"" + commandPrevious + "\"");
	}
	if ( commandPrevious instanceof AbstractCommand ) {
		prevIndentSpaces = ((AbstractCommand)commandPrevious).getIndentSpaces();
	}
	if ( (commandToInsert instanceof EndIf_Command) || (commandToInsert instanceof EndFor_Command) ) {
		if ( (commandPrevious instanceof If_Command) || (commandPrevious instanceof For_Command) ) {
			// No need to adjust the indent since the end is immediately after the start.
			indentSpaces = prevIndentSpaces;
			if ( Message.isDebugOn ) {
				Message.printStatus(2, routine, "  New EndIf or Endif.  Previous command was If or For so use the same indent for new If or For command.");
			}
		}
		else if ( prevIndentSpaces.startsWith(TSToolConstants.INDENT_SPACES) ) {
			// Previous command is not If or For so can attempt to unindent.
			indentSpaces = prevIndentSpaces.substring(TSToolConstants.INDENT_SPACES.length());
			if ( Message.isDebugOn ) {
				Message.printStatus(2, routine, "  New EndIf or EndFor command.  Previous command is not If or For so reducing indent.");
			}
		}
	}
	else if ( (commandPrevious instanceof If_Command) || (commandPrevious instanceof For_Command) ) {
		indentSpaces = prevIndentSpaces + TSToolConstants.INDENT_SPACES;
		if ( Message.isDebugOn ) {
			Message.printStatus(2, routine, "  Previous command was If or For so increasing indent.");
		}
	}
	else {
		// Indent spaces is the same as the previous command.
		indentSpaces = prevIndentSpaces;
		if ( Message.isDebugOn ) {
			Message.printStatus(2, routine, "  Previous command is a normal command so using the same indent.");
		}
	}
	// Return the indent spaces string determined above.
	if ( Message.isDebugOn ) {
		Message.printStatus(2, routine, "  New command indent is \"" + indentSpaces + "\", length=" + indentSpaces.length() );
	}
	return indentSpaces;
}

/**
Edit a command in the command list using the command's editor dialog.
@param action the string containing the event's action value.
Typically this is the command name and a description: "CommandName() <description>".
This is checked for new commands.
When editing existing commands, commandsToEdit will contain a list of Command class instances.
Normally only the first command will be edited as a single-line command.
However, multiple # comment lines can be selected and edited at once.
@param commandsToEdit If an update, this contains the current Command instances to edit.
If a new command, this is null and the action string will be consulted to construct the appropriate command.
The only time that multiple commands will be edited are when they are in a {# delimited comment block).
@param mode the action to take when editing the command (INSERT for a new command or UPDATE for an existing command).
*/
private void commandList_EditCommand ( String action, List<Command> commandsToEdit, CommandEditType mode ) {
	boolean editAsText = false;
	commandList_EditCommand ( action, commandsToEdit, mode, editAsText );
}

/**
Edit a command in the command list using the command's edit dialog or a text editor.
@param action the string containing the event's action value.
Typically this is the command name and a description: "CommandName() <description>".
This is checked for new commands.
When editing existing commands, commandsToEdit will contain a list of Command class instances.
Normally only the first command will be edited as a single-line command.
However, multiple # comment lines can be selected and edited at once.
@param commandsToEdit If an update, this contains the current Command instances to edit.
If a new command, this is null and the action string will be consulted to construct the appropriate command.
The only time that multiple commands will be edited are when they are in a {# delimited comment block).
@param mode the action to take when editing the command (INSERT for a new command or UPDATE for an existing command).
@param editAsText if true, use a simple text editor rather than the command dialog editor
(this is useful if the user is efficient at editing or if the editor is slow,
such as when dealing with database metadata).
*/
private void commandList_EditCommand ( String action, List<Command> commandsToEdit, CommandEditType mode, boolean editAsText ) {
	String routine = getClass().getSimpleName() + ".commandList_editCommand";
	int dl = 1; // Debug level

    // Make absolutely sure that warning level 1 messages are shown to the user in a dialog.
    // This may have been turned off in command processing.
    // Should not need this if set properly in the command processor.
    //Message.setPropValue ( "ShowWarningDialog=true" );

	// FIXME smalers 2011-02-19 Need to do a better job positioning the cursor in the list after edit.

	if ( mode == CommandEditType.CONVERT ) {
	    // Special case for converting TSID commands to Read() commands.
	    StringBuffer b = new StringBuffer();
	    Command command;
	    boolean requireSpecific = false; // OK to use ReadTimeSeries().
	    if ( !action.equals(TSToolConstants.Edit_ConvertTSIDTo_ReadTimeSeries_String)) {
	        requireSpecific = true; // Need to have specific read command.
	    }
	    for ( int iCommand = 0; iCommand < commandsToEdit.size(); iCommand++ ) {
	        // Should only operate on TSID, otherwise ignore.
	        command = commandsToEdit.get(iCommand);
	        if ( command instanceof TSID_Command ) {
	            // Create a TSIdent from the command.
	            try {
	                Command newCommand = TSCommandProcessorUtil.convertTSIDToReadCommand (
	                    this.__tsProcessor, command.toString(), requireSpecific );
	                // Replace the current command with the new command.
	                int insertPos = commandList_IndexOf(command);
	                commandList_RemoveCommand(command);
	                commandList_InsertCommandAt(newCommand,insertPos);
	                // Run discovery mode on the command.
	                if ( newCommand instanceof CommandDiscoverable ) {
	                    commandList_EditCommand_RunDiscovery ( newCommand );
	                    // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
	                }
	            }
	            catch ( Exception e ) {
	                if ( b.length() != 0 ) {
	                    b.append ( ", " );
	                }
	                b.append ( "\"" + command.toString() + "\" (" + e + ")" );
	            }
	        }
	    }
	    if ( b.length() > 0 ) {
	        b.insert(0, "There were errors converting TSID to Read...() commands:  " );
	        Message.printWarning(1,routine,b.toString());
	    }
	    ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
	    return;
	}

	// Indicate whether the commands are a block of # comments.
	// If so then need to use a special editor rather than typical one-line editors.
	boolean isCommentBlock = false;
	if ( mode == CommandEditType.UPDATE ) {
		isCommentBlock = commandList_IsCommentBlock ( this.__tsProcessor,
			commandsToEdit,
			true,	// All must be comments.
			true );	// Comments must be contiguous.
	}
	else {
		// New command, so look for comment actions:
		// - list in the order of the UI
		if ( action.equals(TSToolConstants.Commands_General_Comments_Comment_String) ||
		    // -----------
		    action.equals(TSToolConstants.Commands_General_Comments_AuthorComment_String) ||
		    action.equals(TSToolConstants.Commands_General_Comments_VersionComment_String) ||
		    action.equals(TSToolConstants.Commands_General_Comments_VersionDateComment_String) ||
		    action.equals(TSToolConstants.Commands_General_Comments_SourceUrlComment_String) ||
		    // -----------
		    action.equals(TSToolConstants.Commands_General_Comments_ReadOnlyComment_String) ||
		    action.equals(TSToolConstants.Commands_General_Comments_RunDiscoveryFalseComment_String) ||
		    action.equals(TSToolConstants.Commands_General_Comments_TemplateComment_String) ||
		    // -----------
		    action.equals(TSToolConstants.Commands_General_Comments_EnabledComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_EnabledIfApplicationComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_EnabledIfDatastoreComment_String) ||
		    // -----------
            action.equals(TSToolConstants.Commands_General_Comments_ExpectedStatusFailureComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_ExpectedStatusWarningComment_String) ||
            //action.equals(Commands_General_Comments_FileModTimeComment_String) ||
            //action.equals(Commands_General_Comments_FileSizeComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_IdComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_OrderComment_String) ||
		    // -----------
            action.equals(TSToolConstants.Commands_General_Comments_RequireApplicationComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_RequireDatastoreComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_RequireUserComment_String) ||
		    // -----------
            action.equals(TSToolConstants.Commands_General_Comments_FixMeComment_String) ||
            action.equals(TSToolConstants.Commands_General_Comments_ToDoComment_String) ||
		    // -----------
            action.equals(TSToolConstants.Commands_General_Comments_DocExampleComment_String) ) {
		    // -----------
			isCommentBlock = true;
		}
	}
	if ( isCommentBlock ) {
		Message.printStatus(2, routine, "Command is a comment block.");
	}

	try {
        // Main try to help with troubleshooting since there is a lot going on.

		// First make sure we have a Command object to edit.
		// If an old-style command or unknown command then it will be stored in a GenericCommand.
		// The Command object is inserted in the processor in any case, to take advantage
		// of processor information (such as being able to get the time series identifiers from previous commands.
		// If a new command is being inserted and a cancel occurs, the command will simply be removed from the list.
		// If an existing command is being updated and a cancel occurs, the changes need to be ignored.

		Command commandToEditOriginal = null; // Command being edited (original).
		Command commandToEdit = null; // Command being edited (clone).
		if ( mode == CommandEditType.UPDATE ) {
			// Get the command from the processor.
			if ( isCommentBlock ) {
				// Use the string-based editor dialog and then convert each comment line into a command.
				// Don't do anything to the command list yet.
			}
			else {
				// Get the original command.
				commandToEditOriginal = commandsToEdit.get(0);
				// Clone it so that the edit occurs on the copy.
				commandToEdit = (Command)commandToEditOriginal.clone();
				Message.printStatus(2, routine, "Cloned command to edit: \"" + commandToEdit + "\"" );
				// Remove the original command.
				int pos = commandList_IndexOf ( commandToEditOriginal );
				commandList_RemoveCommand ( commandToEditOriginal );
				// Insert the copy during the edit.
				commandList_InsertCommandAt ( commandToEdit, pos );
				Message.printStatus(2, routine, "Will edit the copy and restore to the original if the edit is canceled.");
			}
		}
		else if ( mode == CommandEditType.INSERT ) {
			if ( isCommentBlock ) {
				// Don't do anything here.  New comments will be inserted in code below.
			}
			else if ( action.equals(TSToolConstants.Commands_General_Comments_Empty_String) ) {
				// Blank line
				commandToEdit = commandList_NewCommand( "", true );
				Message.printStatus(2, routine, "Created new empty string command to insert:  \"" + commandToEdit + "\"" );

				// Add it to the processor at the insert point of the edit (before the first selected command).

				commandList_InsertCommandBasedOnUI ( commandToEdit );
				Message.printStatus(2, routine, "Inserted empty string command for editing.");
			}
			else if ( action.equals(TSToolConstants.Commands_Create_TSID_String) ) {
				// TSID command:
				// - have to pass the full string to 'commandList_NewCommand'
				commandToEdit = commandList_NewCommand( TSToolConstants.Commands_Create_TSID_String, true );
				Message.printStatus(2, routine, "Created new TSID command to insert:  \"" + commandToEdit + "\"" );

				// Add it to the processor at the insert point of the edit (before the first selected command).

				commandList_InsertCommandBasedOnUI ( commandToEdit );
				Message.printStatus(2, routine, "Inserted TSID command for editing.");
			}
			else {
				// New command so create a command as a place-holder for editing (filled out during the editing).
				// Get everything before the ) in the command and then re-add the ").
				// TODO smalers 2007-08-31 Why is this done?
				// Need to handle:
				//	1) Traditional commands foo()
				//	2) Comments # blocks
				//  3) TS alias = foo()
				//  4) Time series identifiers.
				//  5) Don't allow edit of /* */ comments - just insert/delete
				String command_string = StringUtil.getToken(action,")",0,0)+ ")";
				if ( Message.isDebugOn ) {
					Message.printDebug ( dl, routine, "Using command factory to create new command for \"" + command_string + "\"" );
				}

				commandToEdit = commandList_NewCommand( command_string, true );
				Message.printStatus(2, routine, "Created new command to insert:  \"" + commandToEdit + "\"" );

				// Add it to the processor at the insert point of the edit (before the first selected command.

				commandList_InsertCommandBasedOnUI ( commandToEdit );
				Message.printStatus(2, routine, "Inserted command for editing.");
			}
		}

		// Second, edit the command, whether an update or an insert.

		boolean editCompleted = false;
		Command commandToEditNew = null; // New command if editing as text resulted in completely new command.
		List<String> newComments = new ArrayList<>(); // Used if comments are edited.
		if ( isCommentBlock ) {
			// Edit using the old-style editor.
			editCompleted = commandList_EditCommandOldStyleComments ( mode, action, commandsToEdit, newComments );
		}
		else if ( editAsText ) {
			// Edit using the a text editor.
			String originalCommandName = commandToEdit.getCommandName().toUpperCase();
			editCompleted = new CommandAsText_JDialog ( this, commandToEdit ).ok();
			// The above edits the command string so have to possibly create a new command and always re-parse parameters.
			String newCommandString = ((AbstractCommand)commandToEdit).getCommandString().trim();
			Message.printStatus(2, routine, "Original command name: " + originalCommandName);
			Message.printStatus(2, routine, "New command string: " + newCommandString);
			if ( !newCommandString.toUpperCase().startsWith(originalCommandName + "(") ) {
				// Edit has change the command name so need to create a new command.
				//TSCommandFactory factory = new TSCommandFactory();
				TSCommandFactory factory = new TSCommandFactory(TSTool_Plugin.getInstance(this).getPluginCommandClassList());
				commandToEditNew = factory.newCommand(newCommandString);
	 			// Clear out the old parameters first so there is no leftover.
				commandToEditNew.getCommandParameters().clear();
				commandToEditNew.parseCommand(newCommandString);
				// Also check the command parameters, similar to how checkInput() is called in command editors.
				try {
					commandToEditNew.checkCommandParameters( commandToEditNew.getCommandParameters(), null, 1);
				}
				catch ( Exception e ) {
					// The warning would have been printed in the check code so just absorb and let user respond.
					// If they don't fix then there will be a run-time error also.
				}
			}
			else {
	 			// Clear out the old parameters first so there is no leftover.
			    commandToEdit.getCommandParameters().clear();
				commandToEdit.parseCommand(newCommandString);
				// Also check the command parameters, similar to how checkInput() is called in command editors.
				try {
					commandToEdit.checkCommandParameters( commandToEdit.getCommandParameters(), null, 1);
				}
				catch ( Exception e ) {
					// The warning would have been printed in the check code so just absorb and let user respond.
					// If they don't fix then there will be a run-time error also.
				}
			}
		}
		else {
		    // Editing a single one-line command.
	        try {
	   			// Edit with the new style editors.
	   			Message.printStatus(2, routine, "Editing Command with new-style editor.");
	   			editCompleted = commandList_EditCommandNewStyle ( commandToEdit );
	        }
	        catch ( Exception e ) {
	            Message.printWarning (1 , routine, "Unexpected error editing command - refer to log and report to software support." );
	            Message.printWarning( 3, routine, e );
	            editCompleted = false;
	        }
		}

		// Third, make sure that the edits are to be saved.
		// If not (cancel), restore the original copy (if an update) or discard the command (if a new insert).
	    // If the command implements CommandDiscoverable, try to make the discovery run.

		if ( editCompleted ) {
			if ( mode == CommandEditType.INSERT ) {
				if ( isCommentBlock ) {
					// Insert the comments at the insert point.
					commandList_InsertCommentsBasedOnUI ( newComments );
					commandList_CheckComments();
				}
				else {
					// The command has already been inserted in the list.
					Message.printStatus(2, routine, "After insert, command is:  \"" + commandToEdit + "\"" );
	                // Connect the command to the UI to handle progress when the command is run.
	                // TODO smalers 2009-03-23 Evaluate whether to define an interface rather than rely on AbstractCommand here.
	                if ( commandToEdit instanceof AbstractCommand ) {
	                    ((AbstractCommand)commandToEdit).addCommandProgressListener ( this );
	                }
	                if ( commandToEdit instanceof CommandDiscoverable ) {
	                    commandList_EditCommand_RunDiscovery ( commandToEdit );
	                    // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
	                }
				}
				commandList_SetDirty(true);
			}
			else if ( mode == CommandEditType.UPDATE ) {
				// The command was updated.
				if ( isCommentBlock ) {
					// Remove the commands that were selected and insert the new ones.
					commandList_ReplaceComments ( commandsToEdit, newComments );
					if ( !commandList_CommandsAreEqual(commandsToEdit,newComments)) {
						commandList_SetDirty(true);
						commandList_CheckComments();
					}
				}
				else {
					// The contents of the command will have been modified so there is no need to do anything more.
					// The exception is if the command was edited as text and a new command had to be created.
					if ( commandToEditNew != null ) {
						// Swap out the original command with the new one.
					    Message.printStatus(2, routine, "Command was edited as text and new command name was used.  Replacing pre-edit command with \"" + commandToEditNew + "\"" );
						int pos = commandList_IndexOf(commandToEdit);
						commandList_RemoveCommand(commandToEdit);
						commandList_InsertCommandAt(commandToEditNew, pos);
						commandList_SetDirty(true);
		                if ( commandToEditNew instanceof CommandDiscoverable ) {
		                    commandList_EditCommand_RunDiscovery ( commandToEditNew );
		                    // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
		                }
					}
					else {
						Message.printStatus(2, routine, "After edit, command is:  \"" + commandToEdit + "\"" );
						if ( !commandToEditOriginal.toString().equals(commandToEdit.toString()) || (commandToEditNew != null) ) {
							commandList_SetDirty(true);
						}
		                if ( commandToEdit instanceof CommandDiscoverable ) {
		                    commandList_EditCommand_RunDiscovery ( commandToEdit );
		                    // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
		                }
					}
				}
			}
		}
		else {
	        // The edit was canceled.  If it was a new command being inserted, remove the command from the processor.
			if ( mode == CommandEditType.INSERT ) {
				if ( isCommentBlock ) {
					// No comments were inserted at start of edit.  No need to do anything.
				}
				else {
					// A temporary new command was inserted so remove it.
					commandList_RemoveCommand(commandToEdit);
					Message.printStatus(2, routine, "Edit was canceled.  Removing from command list." );
				}
			}
			else if ( mode == CommandEditType.UPDATE ) {
				if ( isCommentBlock ) {
					// The original comments will remain.  No need to do anything.
				}
				else {
					// Else was an update so restore the original command.
				    Message.printStatus(2, routine, "Edit was canceled.  Restoring pre-edit command." );
			    	// Edit was done in command dialog.
					int pos = commandList_IndexOf(commandToEdit);
					commandList_RemoveCommand(commandToEdit);
					commandList_InsertCommandAt(commandToEditOriginal, pos);
				}
			}
		}

		// TODO smalers 2007-12-07 Evaluate whether to refresh the command list status?

	    ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
	}
	catch ( Exception e2 ) {
		// TODO smalers 2005-05-18 Evaluate handling of unexpected error.
		Message.printWarning(1, routine, "Unexpected error editing command (" + e2 + ")." );
		Message.printWarning ( 3, routine, e2 );
	}
}

/**
Run discovery on the command. This will, for example, make available a list of time series
to be requested with the ObjectListProvider.getObjectList() method.
*/
private void commandList_EditCommand_RunDiscovery ( Command command_to_edit ) {
   String routine = getClass().getSimpleName() + ".commandList_EditCommand_RunDiscovery";
    // Run the discovery.
    Message.printStatus(2, routine, "Running discovery mode on command:  \"" + command_to_edit + "\"" );
    try {
        JGUIUtil.setWaitCursor ( this, true );
        ((CommandDiscoverable)command_to_edit).runCommandDiscovery(__tsProcessor.indexOf(command_to_edit));
        // Redraw the status area.
        ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
    }
    catch ( Exception e ) {
        // TODO smalers 2011-02-17 Need to show warning to user?  With current design, code should have complete input.
        // For now ignore because edit-time input may not be complete.
        String message = "Unable to make discover run - may be OK if partial data.";
        Message.printStatus(2, routine, message);
        Message.printWarning(3, routine, e);
    }
    finally {
        JGUIUtil.setWaitCursor ( this, false );
    }
}

/**
Edit a new-style command, which has a custom editor.
@param commandToEdit the command to edit.
*/
private boolean commandList_EditCommandNewStyle ( Command commandToEdit ) {
	return commandToEdit.editCommand(this);
}

/**
Edit comments using an old-style editor.
@param mode Mode of editing, whether updating or inserting.
@param action If not null, then the comments are new (insert).
@param commandList Comments being edited as a list of GenericCommand, as passed from the legacy code.
@param newComments The new comments as a list of String, to be inserted into the command list.
@return true if the command edits were committed, false if canceled.
*/
private boolean commandList_EditCommandOldStyleComments (
	CommandEditType mode, String action, List<Command> commandList, List<String> newComments ) {
	//else if ( action.equals(__Commands_General_Comment_String) ||
	//	command.startsWith("#") ) {
    List<String> commandStrings = new ArrayList<>();
	int size = 0;
	if ( commandList != null ) {
		size = commandList.size();
	}
	Command command = null;
	for ( int i = 0; i < size; i++ ) {
		command = commandList.get(i);
		commandStrings.add( command.toString() );
	}
	List<String> editedCommandStrings = new Comment_JDialog ( this, commandStrings ).getText();
	if ( editedCommandStrings == null ) {
		return false;
	}
	else {
		// Transfer to the list that was passed in.
		int size2 = editedCommandStrings.size();
		for ( int i = 0; i < size2; i++ ) {
			newComments.add ( editedCommandStrings.get(i) );
		}
		return true;
	}
}

/**
Get the list of commands to process, as a list of Command, guaranteed to be non-null but may be zero length.
@param get_all If false, return those that are selected in the command list, unless none are selected,
in which case all are returned.  If true, all are returned, regardless of which are selected.
@return the commands as a list of Command.
*/
private List<Command> commandList_GetCommands ( boolean get_all ) {
	if ( this.__commands_JListModel.size() == 0 ) {
		return new ArrayList<>();
	}

	int [] selected = ui_GetCommandJList().getSelectedIndices();
	int selected_size = 0;
	if ( selected != null ) {
		selected_size = selected.length;
	}

	if ( (selected_size == 0) || get_all ) {
		// Nothing selected or want to get all, get all.
		selected_size = this.__commands_JListModel.size();
		List<Command> itemList = new ArrayList<>(selected_size);
		for ( int i = 0; i < selected_size; i++ ) {
			itemList.add ( (Command)this.__commands_JListModel.get(i) );
		}
		return itemList;
	}
	else {
	    // Else something selected so get them.
	    List<Command> itemList = new ArrayList<>(selected_size);
		for ( int i = 0; i < selected_size; i++ ) {
			itemList.add ( (Command)this.__commands_JListModel.get(selected[i]) );
		}
		return itemList;
	}
}

/**
Get the list of commands to process.  If any are selected, only they will be returned.
If none are selected, all will be returned.
@return the commands as a list of Command.
*/
private List<Command> commandList_GetCommandsBasedOnUI ( ) {
	return commandList_GetCommands ( false );
}

/**
Get the list of commands to process, as a list of String.
@param get_all If false, return those that are selected unless none are selected, in which case all are returned.
If true, all are returned, regardless of which are selected.
@return the commands as a list of String.
*/
private List<String> commandList_GetCommandStrings ( boolean get_all ) {
	// Get the Command list, will not be non-null.
    List<Command> commands = commandList_GetCommands ( get_all );
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
@return the number of commands with failure as max severity
*/
private int commandList_GetFailureCount() {
	int size = this.__commands_JListModel.size();
	CommandStatusProvider command;
	int failureCount = 0;
	for ( int i = 0; i < size; i++ ) {
		command = (CommandStatusProvider)this.__commands_JListModel.get(i);
		if ( CommandStatusUtil.getHighestSeverity(command).equals(CommandStatusType.FAILURE) ) {
			++failureCount;
		}
	}
	return failureCount;
}

/**
Return the number of commands with notifications.
@return the number of commands with notifications
*/
private int commandList_GetNotificationCount() {
	int size = this.__commands_JListModel.size();
	CommandStatusProvider command;
	int notificationCount = 0;
	for ( int i = 0; i < size; i++ ) {
		command = (CommandStatusProvider)this.__commands_JListModel.get(i);
		CommandStatusProvider csp = (CommandStatusProvider)command;
		CommandStatus status = csp.getCommandStatus();
		if ( status.getHasNotification(CommandPhaseType.ANY) ) {
			++notificationCount;
		}
	}
	return notificationCount;
}

/**
Return the number of commands with warnings as maximum severity.
@return the number of commands with warnings as maximum severity
*/
private int commandList_GetWarningCount() {
	int size = this.__commands_JListModel.size();
	CommandStatusProvider command;
	int warningCount = 0;
	for ( int i = 0; i < size; i++ ) {
		command = (CommandStatusProvider)this.__commands_JListModel.get(i);
		if ( CommandStatusUtil.getHighestSeverity(command).equals(CommandStatusType.WARNING) ) {
			++warningCount;
		}
	}
	return warningCount;
}

/**
Return the index position of the command from the command list.
Currently this assumes that there is a one to one correspondence between
items in the list and commands in the processor.
@param command The Command instance to determine the position in the command list.
@return the index position (0+) of the command from the command list
*/
private int commandList_IndexOf ( Command command ) {
	return this.__tsProcessor.indexOf(command);
}

/**
Insert a command at the indicated position.
@param command The Command to insert.
@param pos The index in the command list at which to insert.
*/
private void commandList_InsertCommandAt ( Command command, int pos ) {
	this.__tsProcessor.insertCommandAt( command, pos );
	ui_GetCommandJList().ensureIndexIsVisible ( pos );
	// Since an insert, mark the commands list as dirty.
	//commandList_SetDirty(true);
	ui_UpdateStatus ( false );
}

/**
Insert a new command into the command list,
utilizing the selected commands in the displayed list to determine the insert position.
If any commands are selected in the GUI, the insert will occur before the selection.
If none are selected, the insert will occur at the end of the list.
For example this can occur in the following cases:
<ol>
<li>	The user is interacting with the command list via command menus.</li>
<li>	Time series identifiers are being transferred to the commands area from the query results list.</li>
</ol>
The GUI should call this method WHENEVER a command is being inserted and is coded to respond to changes in the data model.
The indent for the inserted command is determined based on the previous command.
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
		if ( insert_pos > 0 ) {
			// Determine the indent from the previous command.
			Command commandPrevious = (Command)this.__commands_JListModel.getElementAt(insert_pos - 1);
			String indentSpaces = commandList_DetermineNewCommandIndent(inserted_command, commandPrevious);
			// Insert the command in the list model.
			if ( indentSpaces.length() > 0 ) {
				// Add the indent to the command string:
				// - the number of spaces will be set by the following method
				inserted_command.setCommandString(indentSpaces + inserted_command);
			}
		}
		this.__commands_JListModel.insertElementAt ( inserted_command, insert_pos );
		Message.printStatus(2, routine, "Inserting command \"" + inserted_command + "\" at [" + insert_pos + "]" );
	}
	else {
		// Insert position is one after the current size, 0 index.
		insert_pos = this.__commands_JListModel.size();
		if ( insert_pos > 0 ) {
			// Determine the indent from the previous command.
			Command commandPrevious = (Command)this.__commands_JListModel.getElementAt(insert_pos - 1);
			String indentSpaces = "";
			if ( this.__commands_JListModel.size() > 0 ) {
				indentSpaces = commandList_DetermineNewCommandIndent(inserted_command, commandPrevious);
			}
			if ( indentSpaces.length() > 0 ) {
				// Add the indent to the command string.
				inserted_command.setCommandString(indentSpaces + inserted_command);
			}
		}
	    // Insert at end of commands list.
		this.__commands_JListModel.addElement ( inserted_command );
	}
	// Make sure that the list scrolls to the position that has been updated.
	if ( insert_pos >= 0 ) {
	    ui_GetCommandJList().ensureIndexIsVisible ( insert_pos );
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
		inserted_command = commandList_NewCommand ( new_comments.get(i), true );
		// Check the command parameters to trigger an OK status - otherwise
		// the UI will decorate the command to indicate status unknown.
		try {
		    inserted_command.checkCommandParameters(null, "", 3);
		}
		catch ( Exception e ) {
		    // Should not happen.
		}
		if (selectedSize > 0) {
			// Insert before the first selected item.
			int insert_pos0 = selectedIndices[0];
			insert_pos = insert_pos0 + i;
			this.__commands_JListModel.insertElementAt ( inserted_command, insert_pos );
			Message.printStatus(2, routine, "Inserting comment \"" + inserted_command + "\" at [" + insert_pos + "]" );
		}
		else {
		    // Insert at end of command list.
			this.__commands_JListModel.addElement ( inserted_command );
			insert_pos = this.__commands_JListModel.size() - 1;
		}
	}
	// Make sure that the list scrolls to the position that has been updated.
	if ( insert_pos >= 0 ) {
	    ui_GetCommandJList().ensureIndexIsVisible ( insert_pos );
	}
	// Since an insert, mark the command list as dirty.
	//commandList_SetDirty(true);
}

/**
Determine whether a list of commands is a comment block consisting of multiple # comments.
@param processor The TSCommandProcessor that is processing the results,
used to check for positions of commands.
@param commands list of Command instances to check.
@param allMustBeComments If true then all must be comment lines
for true to be returned.  If false, then only one must be a comment.
This allows a warning to be printed that only a block of ALL comments can be edited at once.
@param must_be_contiguous If true, then the comments must be contiguous
for true to be returned.  The GUI code should check this and disallow comment edits if not contiguous.
*/
private boolean commandList_IsCommentBlock ( TSCommandProcessor processor,
    List<Command> commands, boolean allMustBeComments, boolean mustBeContiguous ) {
	int size_commands = commands.size();
	boolean is_comment_block = true;
	boolean is_contiguous = true;
	// Loop through the commands to check.
	Command command = null;
	int comment_count = 0;
	int pos_prev = -1;
	for ( int i = 0; i < size_commands; i++ ) {
		command = commands.get(i);
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
	String routine = getClass().getSimpleName() + ".commandList_NewCommand";
	if ( Message.isDebugOn ) {
		Message.printDebug ( dl, routine,
		"Using command factory to create a new command for \"" + commandString + "\"" );
	}
	Command command = null;
	try {
		if ( commandString.equals(TSToolConstants.Commands_Create_TSID_String) ) {
			// Adding a new TSID:
			// - be careful to not use the factory because it causes issues
			command = new TSID_Command();
			if ( Message.isDebugOn ) {
				Message.printStatus ( 2, routine, "Created TSID command for \"" + commandString + "\"");
			}
		}
		else {
			TSCommandFactory commandFactory = new TSCommandFactory(TSTool_Plugin.getInstance(this).getPluginCommandClassList());
			command = commandFactory.newCommand(commandString);
			if ( Message.isDebugOn ) {
				Message.printStatus ( 2, routine, "Created command from factory for \"" + commandString + "\"");
				Message.printStatus ( 2, routine, "Command class is \"" + command.getClass().getName() + "\"");
			}
		}
	}
	catch ( UnknownCommandException e ) {
		// Processor does not know the command so create an UnknownCommand.
		command = new UnknownCommand();
		if ( Message.isDebugOn ) {
			Message.printStatus ( 2, routine, "Created unknown command for \"" + commandString + "\"");
		}
	}
	catch ( Exception e ) {
		// This should not happen, but may occur during development.
		Message.printWarning ( 1, routine, "Error creating new command for \"" + commandString + "\".  Software issue.");
		return null;
	}

	// TODO smalers 2007-08-31 This is essentially validation.
	// Need to evaluate for old-style commands, impacts on error-handling.
	// New is command from the processor.
	try {
		if ( command instanceof TSID_Command && commandString.equals(TSToolConstants.Commands_Create_TSID_String)) {
			// Don't want to use the command string from the menu,
			// so initialize with empty TSID TODO smalers 2018-06-29 maybe should initialize with "loc.source.type.interval",
			// but UI could ensure this.
			command.initializeCommand ( "", this.__tsProcessor, true );	// Full initialization.
		}
		else {
			// Initialize the command using the command string.
			command.initializeCommand ( commandString, this.__tsProcessor, true );	// Full initialization.
		}
		if ( Message.isDebugOn ) {
			Message.printDebug ( dl, routine, "Initialized command for \"" + commandString + "\"" );
		}
	}
	catch ( Exception e ) {
		// Absorb the warning and make the user try to deal with it in the editor dialog.  They can always cancel out.

		// TODO smalers 2005-05-09 Need to handle parse error.
		// Should the editor come up with limited information?
		Message.printWarning ( 3, routine, "Unexpected error initializing command \"" + commandString + "\"." );
		Message.printWarning ( 3, routine, e );
	}
	return command;
}

/**
Remove all commands in the list.  The delete is done independent of what is selected in the UI.
If UI selects are relevant, use commandList_ClearBasedOnUI.
*/
private void commandList_RemoveAllCommands () {
	// Do this so that the status only needs to be updated once.
	String routine = getClass().getSimpleName() + ".commandList_RemoveAllCommands";
	Message.printStatus(2,routine, "Calling list model removeAllElements.");
	this.__commands_JListModel.removeAllElements();
	commandList_SetDirty ( true );
	ui_UpdateStatus ( false );
}

/**
Remove the indicated command from the command list.
@param command The Command instance to remove from the command list.
*/
private void commandList_RemoveCommand ( Command command ) {
	int pos = commandList_IndexOf ( command );
	this.__commands_JListModel.removeElementAt(pos);
	//commandList_SetDirty(true);
	ui_UpdateStatus ( false );
}

/*
Remove selected command list, using the data model.  If any items are selected, then only those are selected.
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
	//String routine = getClass().getSimpleName() + ".commandList_RemoveCommandsBasedOnUI";
	//Message.printStatus ( 2, routine, "There are " + size +
	//		" commands selected for remove.  If zero all will be removed." );
	if ( (size == this.__commands_JListModel.size()) || (size == 0) ) {
		int x = new ResponseJDialog ( this, "Delete Commands?",
			"Are you sure you want to delete ALL the commands?",
			ResponseJDialog.YES|ResponseJDialog.NO).response();
		if ( x == ResponseJDialog.NO ) {
			return;
		}
	}
	if ( size == 0 ) {
		// Nothing selected so remove all.
		this.__commands_JListModel.removeAllElements();
	}
	else {
	    // Need to remove from back of selected_indices so that removing elements
		// will not affect the index of items before that index.  At some point need to add an undo feature.
		JGUIUtil.setWaitCursor ( this, true );
		ui_SetIgnoreItemEvent ( true );
		ui_SetIgnoreListSelectionEvent ( true );
		for ( int i = (size - 1); i >= 0; i-- ) {
			this.__commands_JListModel.removeElementAt ( selected_indices[i] );
		}
		ui_SetIgnoreItemEvent ( false );
		ui_SetIgnoreListSelectionEvent ( false );
		selected_indices = null;
		JGUIUtil.setWaitCursor ( this, false );
	}
	commandList_SetDirty ( true );
	results_TimeSeries_Clear();
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
	int pos_old = this.__tsProcessor.indexOf(old_command);
	if ( pos_old < 0 ) {
		// Can't find the old command so return.
		return;
	}
	// Remove the old command.
	this.__tsProcessor.removeCommandAt ( pos_old );
	// Insert the new command at the same position.
	// Handle the case that it is now at the end of the list.
	if ( pos_old < this.__tsProcessor.size() ) {
		// Have enough elements to add at the requested position.
		this.__tsProcessor.insertCommandAt( new_command, pos_old );
	}
	else {
		// Add at the end.
		this.__tsProcessor.addCommand ( new_command );
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
private void commandList_ReplaceComments ( List<Command> old_comments, List<String> new_comments ) {
	//String routine = getClass().getSimpleName() + ".commandList_ReplaceComments";
	// Probably could get the index passed in from list operations but
	// do the lookup through the data model to be more independent.
	int pos_old = this.__tsProcessor.indexOf((Command)old_comments.get(0));
	if ( pos_old < 0 ) {
		// Can't find the old command so return.
		return;
	}
	// Remove the old commands.  They will shift so OK to keep removing at the single index.
	int size = old_comments.size();
	for ( int i = 0; i < size; i++ ) {
		this.__tsProcessor.removeCommandAt ( pos_old );
	}
	// Insert the new commands at the same position.
	// Handle the case that it is now at the end of the list.
	int size_new = new_comments.size();
	if ( pos_old < this.__tsProcessor.size() ) {
		// Have enough elements to add at the requested position.
		for ( int i = 0; i < size_new; i++ ) {
			Command new_command = commandList_NewCommand ( new_comments.get(i), true );
			// Check the command parameters to trigger an OK status - otherwise
	        // the UI will decorate the command to indicate status unknown.
	        try {
	            new_command.checkCommandParameters(null, "", 3);
	        }
	        catch ( Exception e ) {
	            // Should not happen.
	        }
			//Message.printStatus ( 2, routine, "Inserting " + new_command + " at " + (pos_old + 1));
			__tsProcessor.insertCommandAt( new_command, (pos_old + i) );
		}
	}
	else {
		// Add at the end.
		for ( int i = 0; i < size_new; i++ ) {
			Command new_command = commandList_NewCommand ( new_comments.get(i), true );
			//Message.printStatus ( 2, routine, "Adding " + new_command + " at end" );
			this.__tsProcessor.addCommand ( new_command );
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
	ui_GetCommandJList().setSelectedIndex ( iline );
	if ( ensure_visible ) {
		// Position the list to make the selected item visible.
	    ui_GetCommandJList().ensureIndexIsVisible(iline);
	}
	ui_UpdateStatus ( false);
}

/**
Set the command file name.
This also will refresh any interface components that display the command file name.
It DOES NOT cause the commands to be reloaded - it is a simple setter.
@param command_file_name Name of current command file (can be null).
*/
private void commandList_SetCommandFileName ( String commandFileName ) {
	// Set the file name used in the TSTool UI.
	this.__commandFileName = commandFileName;
	// Also set the initial working directory for the processor as the parent folder of the command file.
    if ( commandFileName != null ) {
        File file = new File ( commandFileName );
        commandProcessor_SetInitialWorkingDir ( file.getParent(), true );
    }
	// Update the title bar.
	ui_UpdateStatus ( false );
}

/**
Indicate whether the commands have been modified.  The application title is also updated to indicate this.
@param dirty Specify as true if the commands have been modified in some way.
*/
private void commandList_SetDirty ( boolean dirty ) {
	this.__commandsDirty = dirty;
	ui_UpdateStatus ( false );
	// TODO smalers 2007-08-31 Evaluate whether processor should have "dirty" property.
}

/**
Indicate the progress that is occurring within a command.
This may be a chained call from a CommandProcessor that implements CommandListener to listen to a command.
This level of monitoring is useful if more than one progress indicator is present in an application UI.
@param istep The number of steps being executed in a command (0+).
@param nstep The total number of steps to process within a command.
@param command The reference to the command that is running.
@param percentComplete If >= 0, the value can be used to indicate progress running a single command (not the single command).
If less than zero, then no estimate is given for the percent complete and calling code can make its
own determination (e.g., ((istep + 1)/nstep)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandProgress ( int istep, int nstep, Command command, float percentComplete, String message ) {
	if ( istep == 0 ) {
		// Initialize the limits of the command progress bar.
		this.__command_JProgressBar.setMinimum ( 0 );
		this.__command_JProgressBar.setMaximum ( nstep );
	}
	// Set the current value.
    if ( percentComplete > 0.0 ) {
        // Calling code is providing the percent complete.
        this.__command_JProgressBar.setValue ( (int)(nstep*percentComplete/100.0) );
    }
    else {
        // Calling code wants percentage to be computed here.
        this.__command_JProgressBar.setValue ( istep + 1 );
    }
}

// All of the following methods perform and interaction with the command processor,
// beyond basic command list insert/delete/update.

/**
Kill all processes that are still running for RunProgram(), RunDSSUTL(), RunPython(), and RunR commands.
This may be needed because a process is hung (e.g., waiting for input).
*/
private void commandProcessor_CancelCommandProcessesExternal () {
    String routine = getClass().getSimpleName() + ".commandProcessor_CancelCommandProcessesExternal";
    Message.printStatus(2, routine, "Killing all external processes started by commands..." );
    TSCommandProcessorUtil.killCommandProcesses(__tsProcessor.getCommands());
}

/**
Get the command processor AutoExtendPeriod.
This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global AutoExtendPeriod as a Boolean from the command processor or null if not yet determined.
*/
private Boolean commandProcessor_GetAutoExtendPeriod() {
	if ( __tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = __tsProcessor.getPropContents ( "AutoExtendPeriod" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (Boolean)o;
	}
}

/**
Return the command processor instance that is being used.
This method should be called to avoid direct interaction with the processor data member.
@return the TSCommandProcessor instance that is being used.
*/
public TSCommandProcessor commandProcessor_GetCommandProcessor () {
    return __tsProcessor;
}

/**
Get the thread that is running the command processor.
*/
private Thread commandProcessor_GetCommandProcessorThread () {
	return this.__tsProcessorThread;
}

/**
Get the command processor time series ensemble results for an index position.
Typically this corresponds to a user selecting the ensemble from the results list, for further display.
@param pos Position (0+ for the time series).
@return The time series ensemble at the requested position in the results or null
if the processor is not available.
*/
private TSEnsemble commandProcessor_GetEnsembleAt( int pos ) {
    String message, routine = getClass().getSimpleName() + ".commandProcessor_GetEnsembleAt";
    if ( this.__tsProcessor == null ) {
        return null;
    }
    PropList request_params = new PropList ( "" );
    request_params.setUsingObject ( "Index", new Integer(pos) );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = this.__tsProcessor.processRequest( "GetEnsembleAt", request_params);
    }
    catch ( Exception e ) {
        message = "Error requesting GetEnsembleAt(Index=" + pos + ") from processor.";
        Message.printWarning(2, routine, message );
        Message.printWarning ( 3, routine, e );
    }
    PropList bean_PropList = bean.getResultsPropList();
    Object o_TSEnsemble = bean_PropList.getContents ( "TSEnsemble" );
    TSEnsemble tsensemble = null;
    if ( o_TSEnsemble == null ) {
        message = "Null TSEnsemble returned from processor for GetEnsembleAt(Index=\"" + pos + "\").";
        Message.printWarning ( 2, routine, message );
    }
    else {
        tsensemble = (TSEnsemble)o_TSEnsemble;
    }
    return tsensemble;
}

/**
Get the command processor table results list.
@return The table results list or null if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<TSEnsemble> commandProcessor_GetEnsembleResultsList() {
    String routine = getClass().getSimpleName() + ".commandProcessor_GetEnsembleResultsList";
    Object o = null;
    try {
        o = this.__tsProcessor.getPropContents ( "EnsembleResultsList" );
    }
    catch ( Exception e ) {
        String message = "Error requesting EnsembleResultsList from processor.";
        Message.printWarning(2, routine, message );
    }
    if ( o == null ) {
        return null;
    }
    else {
        return (List<TSEnsemble>)o;
    }
}

/**
Get the size of the command processor ensemble results list.
@return the size of the command processor ensemble results list.
*/
private int commandProcessor_GetEnsembleResultsListSize() {
    List<TSEnsemble> results = commandProcessor_GetEnsembleResultsList();
    if ( results == null ) {
        return 0;
    }
    return results.size();
}

/**
Get the command processor HydroBaseDMIList.
This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The HydroBaseDMIList as a list from the command processor or null if not yet determined or no connections.
*/
@SuppressWarnings("unchecked")
private List<HydroBaseDMI> commandProcessor_GetHydroBaseDMIList() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "HydroBaseDMIList" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (List<HydroBaseDMI>)o;
	}
}

/**
Get the command processor IncludeMissingTS.  This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global IncludeMissingTS as a Boolean from the command processor or null if not yet determined.
*/
private Boolean commandProcessor_GetIncludeMissingTS() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "IncludeMissingTS" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (Boolean)o;
	}
}

/**
Get the command processor InputEnd.  This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global InputEnd as a DateTime from the command processor or null if not yet determined.
*/
private DateTime commandProcessor_GetInputEnd() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = __tsProcessor.getPropContents ( "InputEnd" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (DateTime)o;
	}
}

/**
Get the command processor InputStart.  This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global InputStart as a DateTime from the command processor or null if not yet determined.
*/
private DateTime commandProcessor_GetInputStart() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "InputStart" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (DateTime)o;
	}
}

/**
Get the command processor network results for a network identifier.
Typically this corresponds to a user selecting the network from the results list, for further display.
@param networkId identifier for table to display
@return The matching network or null if not available from the processor.
*/
private NodeNetwork commandProcessor_GetNetwork ( String networkId ) {
    String message, routine = getClass().getSimpleName() + ".commandProcessor_GetNetwork";
    if ( this.__tsProcessor == null ) {
        return null;
    }
    PropList request_params = new PropList ( "" );
    request_params.set ( "NetworkID", networkId );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = this.__tsProcessor.processRequest( "GetNetwork", request_params);
    }
    catch ( Exception e ) {
        message = "Error requesting GetNetwork(NetworkID=\"" + networkId + "\") from processor.";
        Message.printWarning(2, routine, message );
        Message.printWarning ( 3, routine, e );
    }
    PropList bean_PropList = bean.getResultsPropList();
    Object o_network = bean_PropList.getContents ( "Network" );
    NodeNetwork network = null;
    if ( o_network == null ) {
        message = "Null network returned from processor for GetNetwork(NetworkID=\"" + networkId + "\").";
        Message.printWarning ( 2, routine, message );
    }
    else {
        network = (NodeNetwork)o_network;
    }
    return network;
}

/**
Get the command processor network results list.
@return The network results list or null if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<NodeNetwork> commandProcessor_GetNetworkResultsList() {
    String routine = getClass().getSimpleName() + ".commandProcessor_GetNetworkResultsList";
    Object o = null;
    try {
        o = this.__tsProcessor.getPropContents ( "NetworkResultsList" );
    }
    catch ( Exception e ) {
        String message = "Error requesting NetworkResultsList from processor.";
        Message.printWarning(2, routine, message );
    }
    if ( o == null ) {
        return null;
    }
    else {
        return (List<NodeNetwork>)o;
    }
}

/**
Get the command processor object results for an object identifier.
Typically this corresponds to a user selecting the object from the results list, for further display.
@param objectId identifier for object to display
@return The matching object or null if not available from the processor.
*/
private JSONObject commandProcessor_GetObject ( String objectId ) {
    String message, routine = getClass().getSimpleName() + ".commandProcessor_GetObject";
    if ( this.__tsProcessor == null ) {
        return null;
    }
    PropList request_params = new PropList ( "" );
    request_params.set ( "ObjectID", objectId );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = this.__tsProcessor.processRequest( "GetObject", request_params);
    }
    catch ( Exception e ) {
        message = "Error requesting GetObject(ObjectID=\"" + objectId + "\") from processor.";
        Message.printWarning(2, routine, message );
        Message.printWarning ( 3, routine, e );
    }
    PropList bean_PropList = bean.getResultsPropList();
    Object o_object = bean_PropList.getContents ( "Object" );
    JSONObject object = null;
    if ( o_object == null ) {
        message = "Null object returned from processor for GetObject(ObjectID=\"" + objectId + "\").";
        Message.printWarning ( 2, routine, message );
    }
    else {
        object = (JSONObject)o_object;
    }
    return object;
}

/**
Get the command processor object results list.
@return The object results list or null
if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<JSONObject> commandProcessor_GetObjectResultsList() {
    String routine = getClass().getSimpleName() + ".commandProcessor_GetObjectResultsList";
    Object o = null;
    try {
        o = this.__tsProcessor.getPropContents ( "ObjectResultsList" );
    }
    catch ( Exception e ) {
        String message = "Error requesting ObjectResultsList from processor.";
        Message.printWarning(2, routine, message );
    }
    if ( o == null ) {
        return null;
    }
    else {
        return (List<JSONObject>)o;
    }
}

/**
Get the command processor OutputEnd.  This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global OutputEnd as a DateTime from the command processor or null if not yet determined.
*/
private DateTime commandProcessor_GetOutputEnd() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "OutputEnd" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (DateTime)o;
	}
}

/**
Get the command processor OutputStart.  This method is meant for simple reporting.
Any errors in the processor should be detected during command initialization and processing.
@return The global OutputStart as a DateTime from the command processor or null if not yet determined.
*/
private DateTime commandProcessor_GetOutputStart() {
	if ( this.__tsProcessor == null ) {
		return null;
	}
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "OutputStart" );
	}
	catch ( Exception e ) {
		return null;
	}
	if ( o == null ) {
		return null;
	}
	else {
	    return (DateTime)o;
	}
}

/**
Get the command processor table results for a table identifier.
Typically this corresponds to a user selecting the table from the results list, for further display.
@param tableId identifier for table to display
@return The matching table or null if not available from the processor.
*/
private DataTable commandProcessor_GetTable ( String tableId ) {
    String message, routine = getClass().getSimpleName() + ".commandProcessor_GetTable";
    if ( this.__tsProcessor == null ) {
        return null;
    }
    PropList request_params = new PropList ( "" );
    request_params.set ( "TableID", tableId );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = this.__tsProcessor.processRequest( "GetTable", request_params);
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
    String routine = getClass().getSimpleName() + ".commandProcessor_GetTableResultsList";
    Object o = null;
    try {
        o = this.__tsProcessor.getPropContents ( "TableResultsList" );
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
Get the command processor time series results for an index position.
Typically this corresponds to a user selecting the time series from the results list, for further display.
@param pos Position (0+ for the time series).
@return The time series at the requested position in the results or null if the processor is not available.
*/
private TS commandProcessor_GetTimeSeries( int pos ) {
	String message, routine = getClass().getSimpleName() + ".commandProcessor_GetTimeSeries";
	if ( this.__tsProcessor == null ) {
		return null;
	}
	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "Index", new Integer(pos) );
	CommandProcessorRequestResultsBean bean = null;
	try {
		bean = this.__tsProcessor.processRequest( "GetTimeSeries", request_params);
	}
	catch ( Exception e ) {
		message = "Error requesting GetTimeSeries(Index=" + pos + ") from processor.";
		Message.printWarning(2, routine, message );
		Message.printWarning ( 3, routine, e );
	}
	PropList bean_PropList = bean.getResultsPropList();
	Object o_TS = bean_PropList.getContents ( "TS" );
	TS ts = null;
	if ( o_TS == null ) {
		message = "Null TS returned from processor for GetTimeSeries(Index=\"" + pos + "\").";
		Message.printWarning ( 2, routine, message );
	}
	else {	ts = (TS)o_TS;
	}
	return ts;
}

/**
Get the command processor time series results list.
@return The time series results list or null if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<TS> commandProcessor_GetTimeSeriesResultsList() {
	String routine = getClass().getSimpleName() + ".commandProcessor_GetTimeSeriesResultsList";
	Object o = null;
	try {
	    o = this.__tsProcessor.getPropContents ( "TSResultsList" );
	}
	catch ( Exception e ) {
		String message = "Error requesting TSResultsList from processor.";
		Message.printWarning(2, routine, message );
	}
	if ( o == null ) {
		return null;
	}
	else {
		return (List <TS>)o;
	}
}

/**
Get the size of the command processor time series results list.
@return the size of the command processor time series results list.
*/
private int commandProcessor_GetTimeSeriesResultsListSize() {
    List<TS> results = commandProcessor_GetTimeSeriesResultsList();
	if ( results == null ) {
		return 0;
	}
	return results.size();
}

/**
Get the command processor time series view results list.
@return The time series view results list or null if the processor is not available.
*/
@SuppressWarnings("unchecked")
private List<TimeSeriesView> commandProcessor_GetTimeSeriesViewResultsList() {
    String routine = getClass().getSimpleName() + ".commandProcessor_GetTimeSeriesViewResultsList";
    Object o = null;
    try {
        o = this.__tsProcessor.getPropContents ( "TimeSeriesViewResultsList" );
    }
    catch ( Exception e ) {
        String message = "Error requesting TimeSeriesViewResultsList from processor.";
        Message.printWarning(2, routine, message );
    }
    if ( o == null ) {
        return null;
    }
    else {
        return (List<TimeSeriesView>)o;
    }
}

// TODO smalers 2008-01-05 Evaluate whether this should live in the processor.
/**
Process ensembles from the results list into a product (graph, etc).
@param ensembleFromUI ensemble to graph (when ensemble time series are created in response to user action)
or null when processing list of indices corresponding to processor results list
@param tslistFromUI list of time series to graph
(corresponding to ensemble and potentially other time series such as statistics for ensemble),
or null when processing list of indices corresponding to processor results list
@param indices Indices of the ensembles to process.
@param props Properties to control output (graph type).
*/
private void commandProcessor_ProcessEnsembleResultsList ( TSEnsemble ensembleFromUI, List<TS> tslistFromUI, int [] indices, PropList props ) {
    String routine = getClass().getSimpleName() + ".commandProcessor_ProcessEnsembleResultsList";
    if ( (tslistFromUI == null) && (indices == null) ) {
        // No ensembles are selected so return.
        Message.printWarning( 1, "", "Select a time series or ensemble to graph." );
        return;
    }
    if ( tslistFromUI != null ) {
	    try {
		    // Display the list of time series.
		    PropList request_params = new PropList ( "" );
		    request_params.setUsingObject ( "TSList", tslistFromUI );
		    request_params.setUsingObject ( "Properties", props );
	        this.__tsProcessor.processRequest( "ProcessTimeSeriesResultsList", request_params );
	    }
	    catch ( Exception e ) {
	        String message = "Error requesting ProcessTimeSeriesResultsList(TSList=\"...\"," +
	        " Properties=\"" + props + "\") from processor.";
	        Message.printWarning(2, routine, message );
	    }
    }
    else {
	    // Translate the ensemble indices into time series indices.
	    // Get the list of time series results.
	    Object o_tslist = null;
	    try {
	        o_tslist = this.__tsProcessor.getPropContents ( "TSResultsList" );
	    }
	    catch ( Exception e ) {
	        String message = "Error getting time series from processor.";
	        Message.printWarning(1, routine, message );
	        Message.printWarning(3, routine, e );
	        return;
	    }
	    if ( o_tslist == null ) {
	        String message = "No time series are available from processor - null list.";
	        Message.printWarning(1, routine, message );
	        return;
	    }
	    @SuppressWarnings("unchecked")
	    List<TS> tslist = (List <TS>)o_tslist;
	    int tslist_size = tslist.size();
	    if ( tslist_size == 0 ) {
	        String message = "No time series are available from processor.";
	        Message.printWarning(1, routine, message );
	        return;
	    }
	    // Get the list of ensembles.
	    List<Integer> matchIndexList = new ArrayList<>(); // List of matching time series indices.
	    for ( int i = 0; i < indices.length; i++ ) {
	        PropList request_params = new PropList ( "" );
	        // String is of format 1) EnsembleID - EnsembleName,
	        // where Ensemble ID can contain dashes but generally not dashes and spaces.
	        String fullLabel = this.__resultsTSEnsembles_JListModel.elementAt(indices[i]);
	        int posParen = fullLabel.indexOf(")");
	        int posDash = fullLabel.indexOf(" -");
	        String EnsembleID = fullLabel.substring(posParen + 1, posDash).trim();
	        Message.printStatus ( 2, routine, "Getting processor ensemble results for \"" + EnsembleID + "\"" );
	        request_params.setUsingObject ( "EnsembleID", EnsembleID );
	        CommandProcessorRequestResultsBean bean = null;
	        try {
	            bean = this.__tsProcessor.processRequest( "GetEnsemble", request_params );
	        }
	        catch ( Exception e ) {
	            String message = "Error requesting GetEnsemble(EnsembleID=\"" + EnsembleID + "\") from processor.";
	            Message.printWarning(2, routine, message );
	            return;
	        }
	        PropList results_props = bean.getResultsPropList();
	        Object o_ensemble = results_props.getContents ( "TSEnsemble" );
	        if ( o_ensemble == null ) {
	            String message = "Null ensemble requesting GetEnsemble(EnsembleID=\"" + EnsembleID + "\") from processor.";
	            Message.printWarning(2, routine, message );
	            return;
	        }
	        TSEnsemble ensemble = (TSEnsemble)o_ensemble;
	        // Loop through the time series in the ensemble and add to the time series index list for matches.
	        int ensemble_size = ensemble.size();
	        TS ens_ts, ts;
	        for ( int iens = 0; iens < ensemble_size; iens++ ) {
	            ens_ts = ensemble.get(iens);
	            for ( int its = 0; its < tslist_size; its++ ) {
	                ts = tslist.get(its);
	                if ( ens_ts == ts ) {
	                    // Have a matching time series.
	                    matchIndexList.add ( new Integer(its));
	                }
	            }
	        }
	    }
	    // Convert the indices to an array.
	    int [] indices2 = new int[matchIndexList.size()];
	    for ( int i = 0; i < indices2.length; i++ ) {
	        indices2[i] = matchIndexList.get(i).intValue();
	    }
	    // Now display the list of time series.
	    PropList request_params = new PropList ( "" );
	    request_params.setUsingObject ( "Indices", indices2 );
	    request_params.setUsingObject ( "Properties", props );

	    try { //bean =
	        this.__tsProcessor.processRequest( "ProcessTimeSeriesResultsList", request_params );
	    }
	    catch ( Exception e ) {
	        String message = "Error requesting ProcessTimeSeriesResultsList(Indices=\"" + indices + "\"," +
	        " Properties=\"" + props + "\") from processor.";
	        Message.printWarning(2, routine, message );
	    }
    }
}

/**
Process time series from the results list into a product (graph, etc).
@param indices array of time series results positions (0+) to process, or null to process all
@param props properties to configure the display
*/
private void commandProcessor_ProcessTimeSeriesResultsList ( int [] indices, PropList props ) {
	String routine = getClass().getSimpleName() + ".commandProcessor_ProcessTimeSeriesResultsList";
	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "Indices", indices );
	request_params.setUsingObject ( "Properties", props );
	//CommandProcessorRequestResultsBean bean = null;
	try { //bean =
		this.__tsProcessor.processRequest( "ProcessTimeSeriesResultsList", request_params );
	}
	catch ( Exception e ) {
		String message = "Error requesting ProcessTimeSeriesResultsList(Indices=\"" + indices + "\"," +
		" Properties=\"" + props + "\") from processor.";
		Message.printWarning(2, routine, message );
	}
}

/**
Read and load a command file into the processor.
@param path Absolute path to the command file to read.
@param runDiscoveryOnLoad if true, run discovery on the commands as they are loaded (the normal case);
if false (may be useful for very large command files), do not run discovery when loading commands
@return the number of lines that are automatically changed during the read (1 if the size is different after read).
@exception IOException if there is an error reading the command file.
*/
private int commandProcessor_ReadCommandFile ( String path, boolean runDiscoveryOnLoad )
throws IOException {
	String routine = getClass().getSimpleName() + ".commandProcessor_ReadCommandFile";
    // Read the command file for use with output:
	// - the UI is updated because the data model receives events
	// - to improve performance and avoid stack overflow for the UI initialization, disable model events and then trigger at the end
	// TODO smalers 2024-11-06 figure why loading some command files results in StackOverflowException:
	// - is it due to not being able to determine the size of a component?
	// - is it due to null or undefined data at the start?
	//this.__commands_JListModel.setIgnoreEvents(true);
	this.__tsProcessor.readCommandFile ( path,
			true, // Create UnknownCommand instances for unrecognized commands.
			false, // Do not append to the current processor contents.
			runDiscoveryOnLoad );
	//this.__commands_JListModel.setIgnoreEvents(false);
	// Now trigger changes.
	//this.__commands_JListModel.commandChanged(0, (this.__tsProcessor.size() - 1));

    // Refresh the UI command list to show the status done in call to this method.

	// If any lines in the file are different from the commands, mark the command file as dirty:
	// - this reflects changes that may automatically occur during the load because of automated updates to command parameter syntax
	BufferedReader in = new BufferedReader ( new InputStreamReader(IOUtil.getInputStream ( path )) );
	List<String> strings = new Vector<>();
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
	if ( size_orig != this.__tsProcessor.size() ) {
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
	    command = this.__tsProcessor.get(i);
	    if ( !line.equals(command.toString()) ) {
	        Message.printStatus( 2, routine, "Command " + (i + 1) +
	            " was automatically updated during load (usually due to software update or manually-edited command file)." );
	        commandList_SetDirty ( true );
	        ++numAutoChanges;
	        if ( command instanceof CommandStatusProvider ) {
	            csp = (CommandStatusProvider)command;
	            // FIXME smalers 2008-05-11 This message gets clobbered by re-initialization before running.
	            // Add a message that the command was updated during load.
	            csp.getCommandStatus().addToLog ( CommandPhaseType.INITIALIZATION,
	                new CommandLogRecord(CommandStatusType.UNKNOWN,
	                    "Command was automatically updated during load (usually due to software update or manually-edited command file).",
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
private void commandProcessor_RunCommandsThreaded ( List<Command> commands, boolean createOutput ) {
	String routine = getClass().getSimpleName() + ".commandProcessor_RunCommandsThreaded";

	PropList requestParams = new PropList ( "" );
	requestParams.setUsingObject ( "CommandList", commands );
	requestParams.setUsingObject ( "InitialWorkingDir", ui_GetInitialWorkingDir() );
	requestParams.setUsingObject ( "CreateOutput", new Boolean(createOutput) );
	// TODO smalers 2017-02-08 the following does not seem to be recognized.
	requestParams.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
	try {
		TSCommandProcessorThreadRunner runner = new TSCommandProcessorThreadRunner ( __tsProcessor, requestParams );
		Message.printStatus ( 2, routine, "Running commands in separate thread.");
		Thread thread = new Thread ( runner );
		commandProcessor_SetCommandProcessorThread(thread);
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
Set the thread that is running for the command processor.
This is set to allow a kill of the thread if necessary.
*/
private void commandProcessor_SetCommandProcessorThread ( Thread thread ) {
	this.__tsProcessorThread = thread;
}

/**
Set the command processor HydroBase instance that is opened via the GUI.
@param hbdmi Open HydroBaseDMI instance.
The input name is blank since it is the default HydroBaseDMI.
*/
public void commandProcessor_SetHydroBaseDMI( HydroBaseDMI hbdmi ) {
	// Call the overloaded method that takes a processor as a parameter.
	commandProcessor_SetHydroBaseDMI( this.__tsProcessor, hbdmi );
}

/**
Set the command processor HydroBase instance that is opened via the GUI.
This version is generally called by the overloaded version and when processing an external command file.
@param processor The command processor to set the HydroBase DMI instance.
@param hbdmi Open HydroBaseDMI instance.
The input name is blank since it is the default HydroBaseDMI.
*/
private void commandProcessor_SetHydroBaseDMI( CommandProcessor processor, HydroBaseDMI hbdmi ) {
	String message, routine = getClass().getSimpleName() + "commandProcessor_SetHydroBaseDMI";
	if ( hbdmi == null ) {
		return;
	}
	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "HydroBaseDMI", hbdmi );
	//CommandProcessorRequestResultsBean bean = null;
	try { //bean =
		processor.processRequest( "SetHydroBaseDMI", request_params );
	}
	catch ( Exception e ) {
		message = "Error requesting SetHydroBaseDMI(HydroBaseDMI=\"" + hbdmi + " from processor.";
		Message.printWarning(2, routine, message );
	}
}

/**
Set the command processor initial working directory.
@param dir Initial working directory.
@param setWorkingDir if true, also set the working directory to the same value
*/
private void commandProcessor_SetInitialWorkingDir ( String InitialWorkingDir, boolean setWorkingDir ) {
    String routine = getClass().getSimpleName() + ".commandProcessor_setInitialWorkingDir";
	try {
		this.__tsProcessor.setPropContents( "InitialWorkingDir", InitialWorkingDir );
	}
	catch ( Exception e ) {
		String message = "Error setting InitialWorkingDir(\"" + InitialWorkingDir + "\") in processor.";
		Message.printWarning(2, routine, message );
	}
	if ( setWorkingDir ) {
	    try {
	        this.__tsProcessor.setPropContents( "WorkingDir", InitialWorkingDir );
	    }
	    catch ( Exception e ) {
	        String message = "Error setting WorkingDir(\"" + InitialWorkingDir + "\") in processor.";
	        Message.printWarning(2, routine, message );
	    }
	}
}

/**
Set the command processor NWSRFS FS5Files DMI instance that is opened via the GUI.
@param nwsrfs_dmi Open NWSRFS FS5Files instance.
*/
public void commandProcessor_SetNWSRFSFS5FilesDMI( NWSRFS_DMI nwsrfs_dmi ) {
	commandProcessor_SetNWSRFSFS5FilesDMI( this.__tsProcessor, nwsrfs_dmi );
}

/**
Set the command processor NWSRFS FS5Files DMI instance that is opened via the GUI.
Typically this method is only called when running an external command file.
@param processor the Processor that is being updated.
@param nwsrfs_dmi Open NWSRFS FS5Files instance.
*/
private void commandProcessor_SetNWSRFSFS5FilesDMI( TSCommandProcessor processor, NWSRFS_DMI nwsrfs_dmi ) {
	String message, routine = getClass().getSimpleName() + "commandProcessor_SetNWSRFSFS5FilesDMI";
	if ( nwsrfs_dmi == null ) {
		return;
	}
	PropList request_params = new PropList ( "" );
	request_params.setUsingObject ( "NWSRFSFS5FilesDMI", nwsrfs_dmi );
	//CommandProcessorRequestResultsBean bean = null;
	try { //bean =
		processor.processRequest( "SetNWSRFSFS5FilesDMI", request_params );
	}
	catch ( Exception e ) {
		message = "Error requesting SetNWSRFSFS5FilesDMI(NWSRFSFS5FilesDMI=\"" + nwsrfs_dmi + " from processor.";
		Message.printWarning(2, routine, message );
	}
}

/**
Indicate that a command has started running.
@param icommand The command index (0+) in the list of commands being run (see ncommand)
@param ncommand The total number of commands to process (will be selected number if running selected)
@param command The reference to the command that is starting to run,
provided to allow future interaction with the command.
@param percent_complete If >= 0, the value can be used to indicate progress
running a list of commands (not the single command).  If less than zero, then
no estimate is given for the percent complete and calling code can make its
own determination (e.g., ((icommand + 1)/ncommand)*100).
@param message A short message describing the status (e.g., "Running command ..." ).
*/
public void commandStarted ( int icommand, int ncommand, Command command, float percent_complete, String message ) {
	String routine = getClass().getSimpleName() + ".commandStarted";
	// commandCompleted updates the progress bar after each command.
	// For this method, only reset the bounds of the progress bar and clear if the first command.
	String tip = "Running command " + (icommand + 1) + " of " + ncommand;
	// If RunCommands() is being run, then also put the input file name to make it easier to understand progress.
	String additionalInfo = "";
	String commandName = command.getCommandName();
	if ( commandName.equalsIgnoreCase("RunCommands") ) {
	    additionalInfo = command.getCommandParameters().getValue("InputFile");
	    if ( additionalInfo.length() > 30 ) {
	        additionalInfo = additionalInfo.substring(0,30);
	    }
	    additionalInfo += "...";
	}
	// Use level zero because the command processor is already printing a log message when each command is run.
	ui_UpdateStatusTextFields ( 0, routine, null, tip + ": \"" + commandName + "(..." +
	    additionalInfo + ")\"", TSToolConstants.STATUS_BUSY );
	if ( icommand == 0 ) {
		this.__processor_JProgressBar.setMinimum ( 0 );
		this.__processor_JProgressBar.setMaximum ( ncommand );
		this.__processor_JProgressBar.setValue ( 0 );
	}
	// Set the tooltip text for the progress bar to indicate the numbers.
	this.__processor_JProgressBar.setToolTipText ( tip );
	// Always set the value for the command progress so that it shows up as zero.
	// The commandProgres() method will do a better job of setting the limits and current status for a specific command.
	this.__command_JProgressBar.setMinimum ( 0 );
	this.__command_JProgressBar.setMaximum ( 100 );
	this.__command_JProgressBar.setValue ( 0 );
}

/**
Required by ListDataListener - receive notification when the contents of the commands list have changed.
*/
public void contentsChanged ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
 * Format a URL to display help for a topic.
 * The document root is taken from TSTool configuration properties and otherwise the
 * URL pattern follows the standard created for the documentation.
 * @param group a group (category) to organize items.
 * For example, the group might be "command".
 * @param item the specific item for the URL.
 * For example, the item might be a command name.
 */
public String formatHelpViewerUrl ( String group, String item ) {
	return formatHelpViewerUrl ( group, item, null );
}

// TODO smalers 2018-08-28 in the future may need a lookup file to ensure portability
// of documentation across software versions but for now assume the organization.
/**
 * Format a URL to display help for a topic.
 * The document root is taken from TSTool configuration properties and otherwise the
 * URL pattern follows the standard created for the documentation.
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
    String docRootUri = TSToolMain.getPropValue ( "TSTool.UserDocumentationUri" );
    String docRootUri2 = TSToolMain.getPropValue ( "TSTool.UserDocumentationUri2" );
    List<String> docRootUriList= new ArrayList<>();
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
    if ( (rootUrl != null) && !rootUrl.isEmpty() ) {
    	// First replace "latest" with the software version so that specific version is shown.
    	String docRootUriVersion = rootUrl.replace("latest", version);
    	docRootUriList.add(docRootUriVersion);
    	if ( !docRootUriVersion.equals(rootUrl) ) {
    		// Add the URL with "latest".
    		docRootUriList.add(rootUrl);
    	}
    }
    if ( (docRootUri == null) || docRootUri.isEmpty() ) {
    	Message.printWarning(2, "",
    		"Unable to determine documentation for group \"" + group + "\" and item \"" +
    		item + "\" - no TSTool.UserDocumenationUri configuration property defined." );
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
			    if ( item.equals(TSToolConstants.Help_ViewDocumentation_ReleaseNotes_String) ) {
			        docUri = uri + "appendix-release-notes/release-notes/";
			    }
			    else if ( item.equals(TSToolConstants.Help_ViewDocumentation_UserManual_String) ) {
			        docUri = uri; // Go to the main documentation.
			    }
			    else if ( item.equals(TSToolConstants.Help_ViewDocumentation_CommandReference_String) ) {
			        docUri = uri + "command-ref/overview/";
			    }
			    else if ( item.equals(TSToolConstants.Help_ViewDocumentation_DatastoreReference_String) ) {
			        docUri = uri + "datastore-ref/overview/";
			    }
			    else if ( item.equals(TSToolConstants.Help_ViewDocumentation_Troubleshooting_String) ) {
			        docUri = uri + "troubleshooting/troubleshooting/";
			    }
			    // Generic requests by group, such as for command reference from editors.
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

/**
Handle the label redraw event from another GeoView (likely a ReferenceGeoView).
Do not do anything here because we assume that application code is setting the labels.
@param record Feature being draw.
*/
public String geoViewGetLabel(GeoRecord record) {
	return null;
}

// TODO smalers 2007-11-02 Review code.  Should this do the same as a select?
/**
Do nothing.
@param devlimits Limits of select in device coordinates(pixels).
@param datalimits Limits of select in data coordinates.
@param selected list of selected GeoRecord.  Currently ignored.
*/
public void geoViewInfo(GRShape devlimits, GRShape datalimits, List<GeoRecord> selected) {
}

/**
Do nothing.
*/
public void geoViewInfo(GRPoint devlimits, GRPoint datalimits, List<GeoRecord> selected) {
}

/**
Do nothing.
*/
public void geoViewInfo(GRLimits devlimits, GRLimits datalimits, List<GeoRecord> selected) {
}

/**
Handle the mouse motion event from another GeoView (likely a ReferenceGeoView).  Does nothing.
@param devpt Coordinates of mouse in device coordinates(pixels).
@param datapt Coordinates of mouse in data coordinates.
*/
public void geoViewMouseMotion(GRPoint devpt, GRPoint datapt) {
}

// TODO smalers 2006-03-02 Evaluate code.
// Should the select use the coordinates?  Not all time series have this information available.
/**
If a selection is made from the map, use the attributes specified in the lookup
table file to match the attributes in the layer with time series in the query list.
The coordinates of the select ARE NOT used in the selection.
@param devlimits Limits of select in device coordinates(pixels).
@param datalimits Limits of select in data coordinates.
@param selected list of selected GeoRecord.
This is used to match the attributes for the selected feature with the time series query list.
*/
public void geoViewSelect ( GRShape devlimits, GRShape datalimits, List<GeoRecord> selected, boolean append ) {
	String routine = getClass().getSimpleName() + ".geoViewSelect";

	try {
	    // Main try, for development and troubleshooting.
    	Message.printStatus ( 1, routine, "Selecting time series that match map selection." );

    	// Select from the time series query list matching the attributes in the selected layer.

    	// TODO smalers 2006-03-02 Need to evaluate how to best read this file once.

    	// Read the time series to layer lookup file.

    	String filename = TSToolMain.getPropValue ( "TSTool.MapLayerLookupFile" );
    	if ( filename == null ) {
    		Message.printWarning ( 3, routine,
    		"The TSTool.MapLayerLookupFile is not defined - cannot link map and time series." );
    		return;
    	}

    	String full_filename = IOUtil.getPathUsingWorkingDir ( filename );
    	if ( !IOUtil.fileExists(full_filename) ) {
    		Message.printWarning ( 3, routine, "The map layer lookup file \"" + full_filename +
    		"\" does not exist.  Cannot link map and time series." );
    		return;
    	}

    	PropList props = new PropList ("");
    	props.set ( "Delimiter=," );		// See existing prototype.
    	props.set ( "CommentLineIndicator=#" );	// New - skip lines that start with this.
    	props.set ( "TrimStrings=True" );	// If true, trim strings after reading.
    	DataTable table = null;
    	try {
    	    table = DataTable.parseFile ( full_filename, props );
    	}
    	catch ( Exception e ) {
    		Message.printWarning ( 3, routine, "Error reading the map layer lookup file \"" + full_filename +
    		"\".  Cannot link map and time series." );
    		return;
    	}

    	int tsize = 0;
    	int TS_InputTypeCol_int = -1;
    	int TS_DataTypeCol_int = -1;
    	int TS_IntervalCol_int = -1;
    	int Layer_NameCol_int = -1;
    	int Layer_LocationCol_int = -1;
    	int Layer_DataSourceCol_int = -1;
    	if ( table != null ) {
    		tsize = table.getNumberOfRecords();

    		try {
    		    TS_InputTypeCol_int = table.getFieldIndex ( "TS_InputType" );
    		}
    		catch ( Exception e ) {
    			Message.printWarning ( 3, routine, "Error finding TS_InputType column in lookup file \"" +
    			full_filename + "\".  Cannot link map and time series." );
    			Message.printWarning ( 3, routine, e );
    			JGUIUtil.setWaitCursor ( this, false);
    			return;
    		}
    		try {
    		    TS_DataTypeCol_int = table.getFieldIndex("TS_DataType");
    		}
    		catch ( Exception e ) {
    			Message.printWarning ( 3, routine, "Error finding TS_InputType column in lookup file \"" +
    			full_filename + "\".  Cannot link map and time series." );
    			Message.printWarning ( 3, routine, e );
    			JGUIUtil.setWaitCursor ( this, false);
    			return;
    		}
    		try {
    		    TS_IntervalCol_int = table.getFieldIndex("TS_Interval");
    		}
    		catch ( Exception e ) {
    			Message.printWarning ( 3, routine, "Error finding TS_Interval column in lookup file \"" +
    			full_filename + "\".  Cannot link map and time series." );
    			Message.printWarning ( 3, routine, e );
    			JGUIUtil.setWaitCursor ( this, false);
    			return;
    		}
    		try {
    		    Layer_NameCol_int = table.getFieldIndex ( "Layer_Name");
    		}
    		catch ( Exception e ) {
    			Message.printWarning ( 3, routine, "Error finding Layer_Name column in lookup file \"" +
    			full_filename + "\".  Cannot link map and time series." );
    			Message.printWarning ( 3, routine, e );
    			JGUIUtil.setWaitCursor ( this, false);
    			return;
    		}
    		try {
    		    Layer_LocationCol_int = table.getFieldIndex ("Layer_Location");
    		}
    		catch ( Exception e ) {
    			Message.printWarning ( 3, routine, "Error finding Layer_Location column in lookup file \""+
    			full_filename + "\".  Cannot link map and time series." );
    			Message.printWarning ( 3, routine, e );
    			JGUIUtil.setWaitCursor ( this, false);
    			return;
    		}
    		try {
    		    Layer_DataSourceCol_int = table.getFieldIndex ("Layer_DataSource");
    		}
    		catch ( Exception e ) {
    			// Non-fatal.
    			Message.printWarning ( 3, routine, "Error finding TS_InputType column in lookup file \"" +
    			full_filename + "\".  Data source will not be considered in lookups." );
    			Layer_DataSourceCol_int = -1;
    		}
    		Message.printStatus ( 2, routine, "TimeSeriesLookup table for "+
    		"map has columns...TS_InputType=" + TS_InputTypeCol_int +
    		",TS_DataType=" + TS_DataTypeCol_int +
    		",TS_Interval=" + TS_IntervalCol_int +
    		",Layer_Name=" + Layer_NameCol_int +
    		",Layer_Location=" + Layer_LocationCol_int +
    		",Layer_DataSource=" + Layer_DataSourceCol_int );
    	}

    	// Now search through the time series that are in the query list and select those that match the list of GeoRecord.
    	// The current selections ARE NOT cleared first (the user can clear them manually if they want).
    	// In this way multiple selections can be made from the map.

    	int nrows = __query_TableModel.getRowCount();
    	Message.printStatus ( 2, routine, "Selecting query list time series based on map selections..." );
    	JGUIUtil.setWaitCursor ( this, true );
    	ui_SetIgnoreListSelectionEvent ( true ); // To increase performance during transfer.
    	ui_SetIgnoreItemEvent ( true );	// To increase performance.
    	int match_count = 0;
    	int ngeo = 0;
    	if ( selected != null ) {
    		ngeo = selected.size();
    	}
    	// Loop through the selected features.
    	GeoRecord georec;
    	GeoLayerView geolayerview = null;
    	TableRecord rec = null; // Lookup table record.
    	String geolayer_name = null;
    	TSTool_TS_TableModel generic_tm = null;
    	String ts_inputtype = null; // The TS input type from lookup file.
    	String ts_datatype = null; // The TS data type from lookup file.
    	String ts_interval = null; // The TS interval from lookup file.
    	String layer_name = null; // The layer name from lookup file.
    	String layer_location = null; // The layer location attribute from the lookup file.
    	int layer_location_field_int =0; // Column index in attribute table for georecord location.
    	String layer_datasource = null; // The layer data source attribute from the lookup file.
    	int layer_datasource_field_int =0; // Column index in attribute table for georecord data source.
    	String georec_location = null; // The georec location value.
    	String georec_datasource = null; // The georec data source value.
    	String tslist_id = null; // The time series location ID from the time series list.
    	String tslist_datasource = null; // The time series data source from the time series list.
    	String tslist_datatype = null; // The time series data type from the time series list.
    	String tslist_interval = null; // The time series interval from the time series list.
    	for ( int igeo = 0; igeo < ngeo; igeo++ ) {
    		// Get the GeoRecord that was selected.
    		georec = (GeoRecord)selected.get(igeo);
    		// Get the name of the layer that corresponds to the GeoRecord, which is used to locate the record in the lookup file.
    		geolayerview = georec.getLayerView();
    		geolayer_name = geolayerview.getName();
    		// Find layer that matches the record, using the layer name in the lookup table.
    		// More than one visible layer may be searched.  The data interval is also used to find a layer to match.
    		for ( int ilook = 0; ilook < tsize; ilook++ ) {
    			Message.printStatus ( 2, routine, "Searching lookup file for the layer named \"" + geolayer_name + "\"" );
    			try {
    			    rec = table.getRecord(ilook);
    				ts_inputtype = (String)rec.getFieldValue(TS_InputTypeCol_int);
    				ts_datatype = (String)rec.getFieldValue(TS_DataTypeCol_int);
    				ts_interval = (String)rec.getFieldValue(TS_IntervalCol_int);
    				layer_name = (String)rec.getFieldValue(Layer_NameCol_int);
    				layer_location = (String)rec.getFieldValue(Layer_LocationCol_int);
    				layer_datasource = (String)rec.getFieldValue(Layer_DataSourceCol_int);
    				// TODO smalers 2006-03-02 Evaluate code.
    				// Add layer_interval if such an attribute exists, and use this in addition to the
    				// layer name to find an appropriate layer in the lookup table.
    				Message.printStatus ( 2, routine,
    				"Lookup file [" + ilook + "] " +
    				"TS_InputType=\"" + ts_inputtype + "\" " +
    				"TS_DataType=\"" + ts_datatype + "\" " +
    				"TS_Interval=\"" + ts_interval + "\" " +
    				"Layer_Name=\"" + layer_name + "\" " +
    				"Layer_Location=\"" + layer_location + "\" " +
    				"Layer_DataSource=\"" + layer_datasource+"\"" );
    			}
    			catch ( Exception e ) {
    				// Just ignore.
    				Message.printWarning ( 3, routine, "Unable to get data from lookup.  Ignoring record." );
    				Message.printWarning ( 3, routine, e );
    				continue;
    			}
    			if ( !geolayer_name.equalsIgnoreCase( layer_name) ) {
    				// The lookup record layer name does not match the selected GeoRecord layer name.
    				continue;
    			}

    			// If here then a layer was found so match the selected features with time series in the list.

    			Message.printStatus ( 2, routine, "Matching layer \"" + layer_name +
    			"\" features with time series using attribute \"" + layer_location + "\"." );

    			try {
    			    layer_location_field_int = georec.getLayer().getAttributeTable().getFieldIndex( layer_location );
    				Message.printStatus ( 2, routine, "Attribute \"" + layer_location +
    				"\" is field [" + layer_location_field_int+"]");
    			}
    			catch ( Exception e ) {
    				Message.printWarning ( 3, routine, "Layer attribute column \"" + layer_location +
    				    "\" is not found.  Cannot link time series and map." );
    				Message.printWarning ( 3, routine, e );
    				JGUIUtil.setWaitCursor ( this, false);
    				return;
    			}
    			if ( Layer_DataSourceCol_int >= 0 ) {
    				try {
    				    layer_datasource = (String)rec.getFieldValue(Layer_DataSourceCol_int);
    					try {
    					    layer_datasource_field_int =
    						georec.getLayer().getAttributeTable().getFieldIndex(layer_datasource);
    						Message.printStatus ( 2, routine, "Attribute \"" + layer_datasource +
    						"\" is field [" + layer_datasource_field_int+"]");
    					}
    					catch ( Exception e ) {
    						Message.printWarning ( 3, routine, "Data source attribute column \"" +
    						layer_datasource + "\" is not found.  Ignoring data source." );
    						Message.printWarning ( 3, routine, e );
    						JGUIUtil.setWaitCursor ( this, false);
    						layer_datasource = null;
    					}
    				}
    				catch ( Exception e ) {
    					Message.printWarning ( 3, routine,
    						"Unable to determine data data source from layer attribute table.  Ignoring data source." );
    					// Ignore for now.
    					layer_datasource = null;
    				}
    			}

    			// TODO smalers 2006-03-02 Add attributes other than strings.
    			// For now only deal with string attributes - later need to handle other types.

    			// Get the attribute to be checked for the ID, based on the attribute name in the lookup file.

    			// TODO smalers 2006-03-02 Optimize code.
    			// Need to implement DbaseDataTable.getTableRecord to
    			// handle on the fly reading to make this a little more directly.

    			try {
    			    georec_location = (String)georec.getLayer().getAttributeTable().getFieldValue(
    				georec.getShape().index, layer_location_field_int );
    				Message.printStatus ( 2, routine, "Trying to find time series with location ID \""
    				+ georec_location + "\"..." );
    			}
    			catch ( Exception e ) {
    				Message.printWarning ( 3, routine,
    				"Cannot get value for \"" + layer_location + "\" attribute.  Skipping record." );
    				// Ignore for now.
    				Message.printWarning ( 3, routine, e );
    				continue;
    			}
    			// Get the attribute to be checked for the data source,
    			// based on the attribute name in the lookup file.
    			if ( (Layer_DataSourceCol_int >= 0) && (layer_datasource != null) ) {
        			try {
        			    georec_datasource = (String)georec.getLayer().getAttributeTable().getFieldValue(
        				georec.getShape().index, layer_datasource_field_int );
        				Message.printStatus ( 2, routine, "Trying to find time series with data source \""
        				+ georec_datasource + "\"..." );
        			}
        			catch ( Exception e ) {
        				Message.printWarning ( 3, routine, "Cannot get value for \"" + layer_datasource +
        				"\" attribute.  Skipping record." );
        				// Ignore for now.
        				Message.printWarning ( 3, routine, e );
        				continue;
        			}
    			}
    			// Now use the TS fields in the lookup table to match time series that are listed in the query results.
    			// This is done brute force by searching everything in the table model.
    			for ( int its = 0; its < nrows; its++ ) {
    				// Get the attributes from the time series query list table model.
    				// TODO smalers 2006-03-02 Refactor/optimize.
    				// Probably what is needed here is a generic interface on time series table models to
    				// have methods that return TSIdent or TSID parts.  For now do it brute force.
    				if ( this.__query_TableModel instanceof TSTool_TS_TableModel ) {
    					generic_tm = (TSTool_TS_TableModel)this.__query_TableModel;
    					tslist_id = (String)generic_tm.getValueAt(its, generic_tm.COL_ID );
    					tslist_datasource = (String)generic_tm.getValueAt(its,generic_tm.COL_DATA_SOURCE);
    					tslist_datatype = (String)generic_tm.getValueAt(its, generic_tm.COL_DATA_TYPE );
    					tslist_interval = (String)generic_tm.getValueAt(its, generic_tm.COL_TIME_STEP );
    				}
    				else if(this.__query_TableModel instanceof TSTool_HydroBase_StationGeolocMeasType_TableModel ) {
    				    TSTool_HydroBase_StationGeolocMeasType_TableModel model =
    				        (TSTool_HydroBase_StationGeolocMeasType_TableModel)this.__query_TableModel;
    					tslist_id = (String)model.getValueAt(its, model.COL_ID );
    					tslist_datasource =(String)model.getValueAt(its,model.COL_DATA_SOURCE);
    					tslist_datatype = (String)model.getValueAt(its,model.COL_DATA_TYPE);
    					tslist_interval = (String)model.getValueAt(its,model.COL_TIME_STEP);
    				}
                    else if(this.__query_TableModel instanceof TSTool_HydroBase_StructureGeolocStructMeasType_TableModel ) {
                        TSTool_HydroBase_StructureGeolocStructMeasType_TableModel model =
                            (TSTool_HydroBase_StructureGeolocStructMeasType_TableModel)this.__query_TableModel;
                        tslist_id = (String)model.getValueAt(its, model.COL_ID );
                        tslist_datasource =(String)model.getValueAt(its,model.COL_DATA_SOURCE);
                        tslist_datatype = (String)model.getValueAt(its,model.COL_DATA_TYPE);
                        tslist_interval = (String)model.getValueAt(its,model.COL_TIME_STEP);
                    }
                    else if(this.__query_TableModel instanceof TSTool_HydroBase_GroundWaterWellsView_TableModel ) {
                        TSTool_HydroBase_GroundWaterWellsView_TableModel model =
                            (TSTool_HydroBase_GroundWaterWellsView_TableModel)this.__query_TableModel;
                        tslist_id = (String)model.getValueAt(its, model.COL_ID );
                        tslist_datasource =(String)model.getValueAt(its,model.COL_DATA_SOURCE);
                        tslist_datatype = (String)model.getValueAt(its,model.COL_DATA_TYPE);
                        tslist_interval = (String)model.getValueAt(its,model.COL_TIME_STEP);
                    }
    				// Check the attributes against that in the map.
    				// Use some of the look interval information for data type and interval,
    				// unless that is supplied in a layer attribute.
    				// TODO smalers 2006-03-02 Need to optimize/refactor.
    				// Currently check the ID and get the data type and interval from the lookup file.
    				// Later can get the interval from the layer attribute data.
    				if ( !georec_location.equalsIgnoreCase(tslist_id) ) {
    					// The ID in the selected feature does not match the time series ID in the list.
    					continue;
    				}
    				if ( (georec_datasource != null) && !georec_datasource.equalsIgnoreCase(tslist_datasource) ) {
    					// The data source in the selected feature does not match the time series ID in the list.
    					continue;
    				}
    				if ( !ts_datatype.equalsIgnoreCase(tslist_datatype) ) {
    					// The data type in lookup file for the selected layer does not match the
    					// time series data type in the list.
    					continue;
    				}
    				if ( !ts_interval.equalsIgnoreCase(tslist_interval) ) {
    					// The data interval in lookup file for the selected layer does not match the
    					// time series data interval in the list.
    					continue;
    				}
    				// The checked attributes match so select the time series and increment the count (do not deselect first).
    				Message.printStatus ( 2, routine, "Selecting time seris [" + its + "]" );
    				this.__query_JWorksheet.selectRow ( its, false );
    				// TODO smalers 2006-03-02 Evaluate usability - should the worksheet automatically scroll to the last select?
    				++match_count;
    			}
    		}
    	}
    	if ( match_count != ngeo ) {
    		Message.printWarning ( 1, routine, "The number of matched time series (" + match_count +
    		") is less than the number of selected features (" + ngeo +
    		").\nVerify that the map layer matches the time series list " +
    		"and that the lookup file has accurate information." );
    	}
    	ui_SetIgnoreListSelectionEvent ( false );
    	ui_SetIgnoreItemEvent ( false );
    	ui_UpdateStatus ( true );
    	JGUIUtil.setWaitCursor ( this, false );
    	Message.printStatus ( 1, routine, "Selected all time series." );
	}
	catch ( Exception e ) {
		// Unexpected error.
		Message.printWarning ( 1, routine, "Unable to link map and TSTool.  See log file." );
		Message.printWarning ( 3, routine, e );
		JGUIUtil.setWaitCursor ( this, false );
	}
}

public void geoViewSelect(GRPoint devlimits, GRPoint datalimits, List<GeoRecord> selected, boolean append) {
	geoViewSelect((GRShape)devlimits, (GRShape)datalimits, selected, append);
}

public void geoViewSelect(GRLimits devlimits, GRLimits datalimits, List<GeoRecord> selected, boolean append) {
	geoViewSelect((GRShape)devlimits, (GRShape)datalimits, selected, append);
}

/**
Handle the zoom event from the GeoView map interface.
This resets the data limits for this GeoView to those specified (if not null) and redraws the GeoView.
In this class it does nothing.
@param devlimits Limits of zoom in device coordinates(pixels).
@param datalimits Limits of zoom in data coordinates.
*/
public void geoViewZoom(GRShape devlimits, GRShape datalimits) {
}

public void geoViewZoom (GRLimits devlim, GRLimits datalim ) {
}

/**
 * Get the command processor, needed to hand off to internal classes.
 */
protected TSCommandProcessor getProcessor () {
	return this.__tsProcessor;
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
		int iline = StringUtil.atoi(command_line) - 1;
		if ( (iline >= 0) && (iline < this.__commands_JListModel.size()) ) {
			// Clear previous selections.
		    ui_GetCommandJList().clearSelection();
			// Select the current tag.
			commandList_SelectCommand ( iline, true );
		}
	}
}

/**
Insert a command in the command list, depending on the state of the UI (e.g., insert before highlighted commands).
This method is called by command editors that are also stand-alone tools,
when transferring commands to the main command processor.
@param command single command to insert
*/
public void insertCommand ( Command command ) {
    // Chain to the private method.
    commandList_InsertCommandBasedOnUI ( command );
}

/**
Insert multiple commands in the command list, depending on the state of the UI (e.g., insert before highlighted commands).
This method is called by command editors that are also stand-alone tools,
when transferring commands to the main command processor.
@param command single command to insert
*/
/* FIXME smalers 2009-06-12 Enable when needed.
public void insertCommands ( List<Command> commands ) {
    // Chain to the private method
    commandList_InsertCommandsBasedOnUI ( commands );
}
*/

/**
Required by ListDataListener - receive notification when the contents of the
commands list have changed due to commands being added.
*/
public void intervalAdded ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
Required by ListDataListener - receive notification when the contents of the
commands list have changed due to commands being removed.
*/
public void intervalRemoved ( ListDataEvent e ) {
	// The contents of the command list changed so check the GUI state.
	ui_UpdateStatus ( true );	// true = also call checkGUIState();
}

/**
Respond to ItemEvents.  If in the final list, the behavior is similar to Microsoft tools:
<ol>
<li>	Click selects on item.</li>
<li>	Shift-click selects forward or backward to nearest selection.</li>
<li>	Control-click toggles one item.</li>
</ol>
*/
public void itemStateChanged ( ItemEvent evt ) {
	String routine = getClass().getSimpleName() + ".itemStateChanged";

	if ( !this.__guiInitialized ) {
		// Some objects are probably still null so ignore the event.
		return;
	}

	if ( ui_GetIgnoreItemEvent() ) {
		// A programmatic change to a list is occurring and we want to ignore the event that will result.
		return;
	}

	Object o = evt.getItemSelectable();
	String selectedInputType = ui_GetSelectedInputType();

	// If any of the choices are changed, clear the main list so that the choices and list are in agreement.

	try {
    	// List in the order of the GUI.

        if ( (o == this.__dataStore_JComboBox) && (evt.getStateChange() == ItemEvent.SELECTED) ) {
            // New datastore selected.
            uiAction_DataStoreChoiceClicked();
        }
        else if ( (o == this.__inputType_JComboBox) && (evt.getStateChange() == ItemEvent.SELECTED) ) {
    		// New input type selected.
    		queryResultsList_Clear();
    		uiAction_InputTypeChoiceClicked(null); // null indicates datastore selection is not driving action.
    	}
    	else if((o == this.__inputName_JComboBox) && (evt.getStateChange() == ItemEvent.SELECTED) ) {
    		// New input name selected.
    		if ( selectedInputType.equals( TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files) &&
    			!this.__inputName_JComboBox.getSelected().equals( TSToolConstants.PLEASE_SELECT) ) {
    			// If the default "Please Select" is shown, the it is initialization - don't force a selection.
    			try {
    			    TSTool_FS5Files.getInstance(this).selectInputName ( false );
    			}
    			catch ( Exception e ) {
    				Message.printWarning ( 1, routine, "Error opening NWSRFS FS5Files connection." );
    				Message.printWarning ( 2, routine, e );
    			}
    		}
            else if(selectedInputType.equals(TSToolConstants.INPUT_TYPE_HECDSS )) {
                TSTool_HecDss.getInstance(this).selectInputName ( false );
            }
    		else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateCU ) ){
    			TSTool_StateCU.getInstance(this).selectInputType ( false );
    		}
            else if(selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateCUB )) {
                TSTool_StateCUB.getInstance(this).selectInputType ( false );
            }
    		else if(selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateModB )) {
    			TSTool_StateModB.getInstance(this).selectInputType ( false );
    		}
    	}
    	else if ( o == this.__dataType_JComboBox && (evt.getStateChange() == ItemEvent.SELECTED) ) {
    		queryResultsList_Clear();
    		uiAction_DataTypeChoiceClicked();
    	}
    	else if ( o == this.__timeStep_JComboBox && (evt.getStateChange() == ItemEvent.SELECTED) ) {
    		queryResultsList_Clear();
    		uiAction_TimeStepChoiceClicked();
    	}
        else if ( o == TSToolMenus.View_MapInterface_JCheckBoxMenuItem ) {
    		if ( TSToolMenus.View_MapInterface_JCheckBoxMenuItem.isSelected() ) {
    			// User wants the map to be displayed.
    			try {
    			    if ( this.__geoview_JFrame != null ) {
    					// Just set the map visible.
    					this.__geoview_JFrame.setVisible ( true );
    				}
    				else {
    				    // No existing GeoView so create one.
    					this.__geoview_JFrame = new GeoViewJFrame ( this, null );
    					// Add a GeoViewListener so TSTool can handle selects from the map.
    					this.__geoview_JFrame.getGeoViewJPanel().getGeoView().addGeoViewListener(this);
    					// Add a window listener so TSTool can listen for when the GeoView closes.
    					this.__geoview_JFrame.addWindowListener ( this );
    					JGUIUtil.center ( this.__geoview_JFrame );
    				}
    			}
    			catch ( Exception e ) {
    				Message.printWarning ( 1, "TSTool", "Error displaying map interface." );
    				this.__geoview_JFrame = null;
    			}
    		}
    		else {
                // Map is deselected.  Just set the map frame to not visible.
                if ( this.__geoview_JFrame != null ) {
                    this.__geoview_JFrame.setVisible ( false );
                }
    		}
    	}
    	ui_UpdateStatus ( true );
	}
	catch ( Exception e ) {
		// Unexpected exception.
		Message.printWarning ( 2, getClass().getSimpleName() + ".itemStateChanged", e );
	}
}

/**
Respond to KeyEvents.
Most single-key events are handled in keyReleased to prevent multiple events.
Do track when the shift is pressed here.
*/
public void keyPressed ( KeyEvent event ) {
	int code = event.getKeyCode();

	if ( code == KeyEvent.VK_SHIFT ) {
		JGUIUtil.setShiftDown ( true );
	}
	else if ( code == KeyEvent.VK_CONTROL ) {
		JGUIUtil.setControlDown ( true );
	}
}

/**
Respond to KeyEvents.
*/
public void keyReleased ( KeyEvent event ) {
	int code = event.getKeyCode();

	if ( code == KeyEvent.VK_ENTER ) {
		if ( event.getSource() == ui_GetCommandJList() ) {
			// Same as the Edit...Command event.
			uiAction_EditCommand ();
		}
	}
	else if ( code == KeyEvent.VK_DELETE ) {
		// Clear a command.
		if ( event.getSource() == ui_GetCommandJList() ) {
			commandList_RemoveCommandsBasedOnUI();
		}
	}
	ui_UpdateStatus ( true );
}

public void keyTyped ( KeyEvent event ) {
}

/**
Merge a new configuration file with the old configuration file.
It is assumed that the current configuration file is the most complete,
likely being distributed with a demo or new version of the software.
Therefore the merge will accomplish the following cases:
<ol>
<li>    If the user is merging with a complete old configuration file,
		the old license and settings will be applied to the new software.
		New settings will still be in effect.</li>
<li>    If the user is applying a new license, for example to a demo installation,
		then only the license properties will be applied.<li>
</ol>
@param currentConfigFile Current configuration file that was distributed with the current software.
@param configFileToMerge The configuration file to merge with the current configuration file.
@exception IOException if there is an error writing the file.
*/
private void license_MergeConfigFiles ( File currentConfigFile, File configFileToMerge )
throws IOException {
    String routine = getClass().getSimpleName() + ".license_MergeConfigFiles";
    int updatedPropCount = 0;
    // Read the current configuration.
    PropList currentProps = new PropList ( "current" );
    currentProps.setPersistentName ( currentConfigFile.getPath() );
    try {
        // Read and save literals as properties so that comments can be output similar to the original file.
        currentProps.readPersistent( true, true );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine,
            "Error reading current configuration file - cannot merge configuration properties." );
        return;
    }
    // Read the configuration to merge.
    PropList configToMergeProps = new PropList ( "current" );
    configToMergeProps.setPersistentName ( configFileToMerge.getPath() );
    try {
        configToMergeProps.readPersistent();
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine,
            "Error reading configuration file to merge - cannot merge configuration properties." );
        return;
    }
    // Loop through he properties in the current file and reset to those in the file to merge.
    List<Prop> props = currentProps.getList();
    int size = props.size();
    for ( int i = 0; i < size; i++ ) {
        // Get out of the current list.
        Prop prop = props.get(i);
        String currentPropName = prop.getKey();
        String currentPropValue = prop.getValue();
        // See if there is a match in the properties to be merged.
        String matchPropValue = configToMergeProps.getValue(currentPropName);
        if ( (matchPropValue != null) && !currentPropValue.equals(matchPropValue) ) {
            // Property names match and values are different so reset in the current properties.
            prop.setValue ( matchPropValue );
            ++updatedPropCount;
        }
    }
    if ( updatedPropCount > 0 ) {
        // Had at least one match so rewrite the property file to the same name.
        currentProps.writePersistent();
    }
}

/**
Handle mouse clicked event.
*/
public void mouseClicked ( MouseEvent event ) {
	Object source = event.getSource();
	if ( source == ui_GetCommandJList() ) {
		if ( event.getClickCount() == 2 ) {
			// Edit the first selected item, unless a comment, in which case all are edited.
			uiAction_EditCommand ();
		}
	}
}

/**
Handle mouse entered event.  Nothing is done.
*/
public void mouseEntered ( MouseEvent event ) {
}

/**
Handle mouse exited event.  Nothing is done.
*/
public void mouseExited ( MouseEvent event ) {
}

/**
Handle mouse pressed event.
*/
public void mousePressed ( MouseEvent event ) {
	int mods = event.getModifiers();
	Component c = event.getComponent();
	String selectedInputType = ui_GetSelectedInputType();
    // Popup for commands.
	if ( (c == ui_GetCommandJList()) && (this.__commands_JListModel.size() > 0) &&
		((mods & MouseEvent.BUTTON3_MASK) != 0) ) {
		Point pt = JGUIUtil.computeOptimalPosition ( event.getPoint(), c, TSToolMenus.Commands_JPopupMenu );
		TSToolMenus.Commands_JPopupMenu.show ( c, pt.x, pt.y );
	}
    // Popup for time series results list (right click).
	else if ( (c == this.__resultsTS_JList) && (this.__resultsTS_JListModel.size() > 0) &&
		((mods & MouseEvent.BUTTON3_MASK) != 0) ) {
		Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsTS_JPopupMenu );
		__resultsTS_JPopupMenu.show ( c, pt.x, pt.y );
	}
    // Popup for ensemble results list.
    else if ( (c == this.__resultsTSEnsembles_JList) && (this.__resultsTSEnsembles_JListModel.size() > 0) &&
        ((mods & MouseEvent.BUTTON3_MASK) != 0) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsTSEnsembles_JPopupMenu );
        this.__resultsTSEnsembles_JPopupMenu.show ( c, pt.x, pt.y );
    }
    // Popup for network results list, right click since left click automatically shows network.
    else if ( (c == this.__resultsNetworks_JList) && (this.__resultsNetworks_JListModel.size() > 0)
        && ((mods & MouseEvent.BUTTON3_MASK) == MouseEvent.BUTTON3_MASK) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsNetworks_JPopupMenu );
        this.__resultsNetworks_JPopupMenu.show ( c, pt.x, pt.y );
    }
    // Popup for object results list, right click since left click automatically shows object.
    else if ( (c == this.__resultsObjects_JList) && (this.__resultsObjects_JListModel.size() > 0)
        && ((mods & MouseEvent.BUTTON3_MASK) == MouseEvent.BUTTON3_MASK) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsObjects_JPopupMenu );
        this.__resultsObjects_JPopupMenu.show ( c, pt.x, pt.y );
    }
    // Popup for output files results list, right click since left click automatically shows object.
    else if ( (c == this.__resultsOutputFiles_JList) && (this.__resultsOutputFiles_JListModel.size() > 0)
        && ((mods & MouseEvent.BUTTON3_MASK) == MouseEvent.BUTTON3_MASK) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsOutputFiles_JPopupMenu );
        this.__resultsOutputFiles_JPopupMenu.show ( c, pt.x, pt.y );
    }
    // Popup for table results list, right click since left click automatically shows table.
    else if ( (c == this.__resultsTables_JList) && (this.__resultsTables_JListModel.size() > 0)
        && ((mods & MouseEvent.BUTTON3_MASK) == MouseEvent.BUTTON3_MASK) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__resultsTables_JPopupMenu );
        this.__resultsTables_JPopupMenu.show ( c, pt.x, pt.y );
    }
	// Popup for input name.
    else if ( (c == this.__inputName_JComboBox) && ((mods & MouseEvent.BUTTON3_MASK) != 0) &&
        selectedInputType.equals(TSToolConstants.INPUT_TYPE_HECDSS) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__input_name_JPopupMenu );
        this.__input_name_JPopupMenu.removeAll();
        this.__input_name_JPopupMenu.add( new SimpleJMenuItem (TSToolConstants.InputName_BrowseHECDSS_String, this ) );
        this.__input_name_JPopupMenu.show ( c, pt.x, pt.y );
    }
    else if ( (c == this.__inputName_JComboBox) && ((mods & MouseEvent.BUTTON3_MASK) != 0) &&
        selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateCUB) ) {
        Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__input_name_JPopupMenu );
        this.__input_name_JPopupMenu.removeAll();
        this.__input_name_JPopupMenu.add( new SimpleJMenuItem (TSToolConstants.InputName_BrowseStateCUB_String, this ) );
        this.__input_name_JPopupMenu.show ( c, pt.x, pt.y );
    }
	else if ( (c == this.__inputName_JComboBox) && ((mods & MouseEvent.BUTTON3_MASK) != 0) &&
		selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateModB) ) {
		Point pt = JGUIUtil.computeOptimalPosition (event.getPoint(), c, this.__input_name_JPopupMenu );
		this.__input_name_JPopupMenu.removeAll();
		this.__input_name_JPopupMenu.add( new SimpleJMenuItem (TSToolConstants.InputName_BrowseStateModB_String, this ) );
		this.__input_name_JPopupMenu.show ( c, pt.x, pt.y );
	}
	else if ( c == this.__query_JWorksheet ) {
		// Check the state of the "Copy Selected to Commands" button based on whether any worksheet cells are selected.
		if ( (this.__query_JWorksheet != null) && (this.__query_JWorksheet.getSelectedRowCount() > 0) ) {
			JGUIUtil.setEnabled ( this.__CopySelectedToCommands_JButton, true );
		}
		else {
            JGUIUtil.setEnabled ( this.__CopySelectedToCommands_JButton, false );
		}
		// Update the border to reflect selections.
		ui_UpdateStatus ( false );
	}
}

/**
Handle mouse released event.  If the object is a results file, display the selected items.
*/
public void mouseReleased ( MouseEvent event ) {
}

/**
Process a time series product file.
*/
public void processTSProduct ( String productFile, PropList props ) {
	TSProcessor p = new TSProcessor ();
	// Set up the time series supplier.
	if ( this.__tsProcessor != null ) {
		// Time series should be in memory so add the TSCommandProcessor as a supplier.
		// This should result in quick supplying of in-memory time series.
		p.addTSSupplier ( this.__tsProcessor );
	}
	// Now process the product.
	PropList override_props = new PropList ("TSTool");
	DateTime now = new DateTime ( DateTime.DATE_CURRENT );
	override_props.set ( "CurrentDateTime=", now.toString() );
	boolean view_gui = true;
	if ( view_gui ) {
		override_props.set ( "InitialView", "Graph" );
		override_props.set ( "PreviewOutput", "True" );
	}
	try {
		p.processProduct ( productFile, override_props );
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, "", "Error processing TSProduct file (" + e + ")." );
		Message.printWarning ( 3, "", e );
	}
}

/**
Display the time series list query results in a string format.
These results are APPENDED to the list of strings already found in the __commands_JList.
@param location Location part of TSIdent.
@param source Source part of TSIdent.
@param type Data type part of TSIdent.
@param interval Interval part of TSIdent.
@param scenario Scenario part of TSIdent (null or empty for no scenario).
@param sequence_number Sequence number part of TSIdent (null or empty for no sequence number).
@param input_type The type of input (e.g., DateValue, NWSCard, USGSNWIS).
@param input_name The input location for the data (a database connection or file name).
@param comment Comment for time series (null or empty for no comment).
@param use_alias If true, then the location contains the alias and the other
TSID fields are ignored when putting together the TSID command.
@param insertOffset the position to offset the insert (used to ensure that inserting multiple
time series results in the same order in the commands, rather than first in last out appearance
that could occur when inserting after a selected command).
@return the number of commands inserted (may be 2 if a comment is inserted).  This is only used when
commands are selected and prevents the insert from occurring in reverse order.
*/
public int queryResultsList_AppendTSIDToCommandList ( String location,
					String source,
					String type,
					String interval,
					String scenario,
					String sequence_number,
					String input_type,
					String input_name,
					String comment,
					boolean use_alias,
					int insertOffset ) {
	// Add after the last selected item or at the end if nothing is selected.
	int selected_indices[] = ui_GetCommandJList().getSelectedIndices();
	int selected_size = 0;
	if ( selected_indices != null ) {
		selected_size = selected_indices.length;
	}
	int insert_pos = 0;
	String scenario2 = "";
	if ( (scenario != null) && !scenario.equals("") ) {
		scenario2 = "." + scenario;
	}
	String sequence_number2 = "";
	if ( (sequence_number != null) && !sequence_number.equals("") ) {
		sequence_number2 = "[" + sequence_number + "]";
	}
	// If there is an input_name, always use an input_type.
	String input = "";
	if ( (input_name != null) && (input_name.length() != 0) ) {
		input = "~" + input_type + "~" + input_name;
	}
	else if ( (input_type != null) && (input_type.length() != 0) ) {
		// Only have the input type.
		input = "~" + input_type;
	}
	if ( selected_size > 0 ) {
		// Insert after the last item.
	    // If this is part of a block of inserts, the insertOffset is also added to ensure that the
	    // insert occurs at the end of the block (incremental).
		// Otherwise the insert is first in last out and reversed the order of the block.
		insert_pos = selected_indices[selected_size - 1] + 1 + insertOffset;
	}
	else {
	    // Insert at the end.
		insert_pos = this.__commands_JListModel.size();
	}

	int i = 0;	// Leave this in case we add looping.
	int offset = 0;	// Handles cases where a comment is inserted prior to the command.
	int numberInserted = 0;
	if ( (comment != null) && !comment.equals("") ) {
	    // Insert a comment prior to the command, for example to include the station description.
	    Command commentCommand = commandList_NewCommand ( "# " + comment, true );
	    // Run the comment to set the status from unknown to success.
        try {
            commentCommand.checkCommandParameters(null, "", 3);
        }
        catch ( Exception e ) {
            // Should not happen.
        }
		this.__commands_JListModel.insertElementAt ( commentCommand, (insert_pos + i*2));
		++numberInserted;
		offset = 1;
	}
	String tsident_string = null;
	if ( use_alias ) {
		// Just use the short alias.
		tsident_string = location + input;
	}
	else {
	    // Use a full time series identifier.
		tsident_string = location + "." + source + "." + type + "." +
			interval + scenario2 + sequence_number2 + input;
	}
	if ( Message.isDebugOn ) {
		Message.printDebug ( 1, "", "Inserting \"" + tsident_string +
		"\" at " + (insert_pos + i*2 + offset) );
	}
	//__commands_JListModel.insertElementAt ( tsident_string, (insert_pos + i*2 + offset));
	Command tsid_command = commandList_NewCommand ( tsident_string, true );
	this.__commands_JListModel.insertElementAt ( tsid_command, (insert_pos + i*2 + offset));
    ++numberInserted;
	//commandList_SetDirty ( true );
	//ui_UpdateStatus ( false );
    if ( tsid_command instanceof CommandDiscoverable ) {
        // Run discovery on the command to do initial validation and provide data to other commands.
        commandList_EditCommand_RunDiscovery ( tsid_command );
        // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
    }
    ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
    commandList_SetDirty ( true );
    return numberInserted;
}

// TODO smalers 2023-02-02 Remove when tested out.
// This method is now in each datastore to list class:  cdss.app.tstool.datastore.*
/**
Add the time series list query results TSID to the command list.
These results are APPENDED to the list of strings already found in the __commands_JList.
This version of the method is simpler than the overloaded version that takes as input the separate TSID parts.
@param tsidentString Full time series identifier string to be inserted as a command.
@param comment Comment for time series (null or empty for no comment).
If provided it will be inserted above the TSID command.
@param insertOffset the position to offset the insert (used to ensure that inserting multiple
time series results in the same order in the commands, rather than first in last out appearance
that could occur when inserting after a selected command).
@return the number of commands inserted (may be 2 if a comment is inserted).
This is only used when commands are selected and prevents the insert from occurring in reverse order.
*/
/*
private int queryResultsList_AppendTSIDToCommandList ( String tsidentString, String comment, int insertOffset ) {
	// Add after the last selected item or at the end if nothing is selected.
	int selected_indices[] = ui_GetCommandJList().getSelectedIndices();
	int selected_size = 0;
	if ( selected_indices != null ) {
		selected_size = selected_indices.length;
	}
	int insert_pos = 0;
	if ( selected_size > 0 ) {
		// Insert after the last item.
	    // If this is part of a block of inserts,
		// the insertOffset is also added to ensure that the insert occurs at the end of the block (incremental).
		// Otherwise the insert is first in last out and reversed the order of the block.
		insert_pos = selected_indices[selected_size - 1] + 1 + insertOffset;
	}
	else {
	    // Insert at the end.
		insert_pos = this.__commands_JListModel.size();
	}

	int i = 0;	// Leave this in case we add looping.
	int offset = 0;	// Handles cases where a comment is inserted prior to the command.
	int numberInserted = 0;
	if ( (comment != null) && !comment.equals("") ) {
	    // Insert a comment prior to the command, for example to include the station description.
	    Command commentCommand = commandList_NewCommand ( "# " + comment, true );
	    // Run the comment to set the status from unknown to success.
        try {
            commentCommand.checkCommandParameters(null, "", 3);
        }
        catch ( Exception e ) {
            // Should not happen.
        }
		this.__commands_JListModel.insertElementAt ( commentCommand, (insert_pos + i*2));
		++numberInserted;
		offset = 1;
	}
	if ( Message.isDebugOn ) {
		Message.printDebug ( 1, "", "Inserting \"" + tsidentString + "\" at " + (insert_pos + i*2 + offset) );
	}
	//this.__commands_JListModel.insertElementAt ( tsident_string, (insert_pos + i*2 + offset));
	Command tsid_command = commandList_NewCommand ( tsidentString, true );
	this.__commands_JListModel.insertElementAt ( tsid_command, (insert_pos + i*2 + offset));
    ++numberInserted;
	//commandList_SetDirty ( true );
	//ui_UpdateStatus ( false );
    if ( tsid_command instanceof CommandDiscoverable ) {
        // Run discovery on the command to do initial validation and provide data to other commands.
        commandList_EditCommand_RunDiscovery ( tsid_command );
        // TODO smalers 2011-03-21 Should following commands run discovery - could be slow.
    }
    ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
    commandList_SetDirty ( true );
    return numberInserted;
}
*/

/**
Clear the query list (e.g., when a choice changes).
*/
public void queryResultsList_Clear () {
	if ( (this.__query_JWorksheet == null) || (this.__query_TableModel == null) ) {
		// Not initialized.
		return;
	}
	if ( this.__query_TableModel.getRowCount() > 0 ) {
       	try {
       	    this.__query_JWorksheet.clear();
		}
		catch ( Exception e ) {
			// Absorb the exception in most cases - print if developing to see if this issue can be resolved.
			if ( Message.isDebugOn && IOUtil.testing()  ) {
				String routine = "TSTool_JFrame.queryResultsList_Clear";
				Message.printWarning ( 3, routine,
				"For developers:  caught exception in clearQueryList JWorksheet at setup." );
				Message.printWarning ( 3, routine, e );
			}
		}
	}

	// Set the data lists to empty and redraw the label (check for null because it seems to be an issue at startup).

	ui_UpdateStatus ( false );
}

/**
Select a station from the query list and create a time series identifier in the command list.
@param row Row that is selected in the query list.
This method can be called once for a single event or multiple times from transferAll().
@param update_status If true, then the GUI state is checked after the transfer.
This should only be set to true when transferring one command.
If many are transferred, this slows down the GUI.
@param insertOffset used when processing multiple time series - ensures that inserts after a selected
command occur in order and not first in last out.
@return the number of commands that are added (1 or maybe 2 if a comment is inserted before the command).
*/
private int queryResultsList_TransferOneTSFromQueryResultsListToCommandList (
    int row, boolean update_status, int insertOffset ) {
	String routine = getClass().getSimpleName() + ".queryResultsList_TransferOneTSFromQueryResultsListToCommandList";
	boolean useAlias = false;
    int numCommandsAdded = 0; // Used when inserting blocks of time series.
    String selectedInputType = ui_GetSelectedInputType();
    DataStore selectedDataStore = ui_GetSelectedDataStore();
    // If the datastore name is null, an input type can be used below.
    String selectedDataStoreName = null;
    if ( selectedDataStore != null ) {
    	selectedDataStoreName = selectedDataStore.getName();
    	// The selected datastore might be the actual datastore name or a substitute:
    	// - if a substitute name is used (and was selected in the UI),
    	//   the substitute name will result in returning the original datastore with original name
    	// - therefore, need to look up the substitute name here again
    	List<DataStoreSubstitute> datastoreSubstituteList = this.__tsProcessor.getDataStoreSubstituteList();
    	for ( DataStoreSubstitute dssub : datastoreSubstituteList ) {
    		if ( dssub.getDatastoreNameToUse().equals(selectedDataStoreName) ) {
    			// The selected datastore name matches a substitute's original name so use the substitute name.
    			selectedDataStoreName = dssub.getDatastoreNameInCommands();
    		}
    	}
    }

    if ( (selectedDataStore != null) && (selectedDataStore instanceof ColoradoHydroBaseRestDataStore) ) {
    	// Start ColoradoHydroBaseRestDataStore.
		numCommandsAdded = TSTool_HydroBaseRest.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset,
			this.__query_TableModel, selectedDataStoreName );
    }
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_DateValue) ) {
		numCommandsAdded = TSTool_DateValue.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof GenericDatabaseDataStore) ) {
		numCommandsAdded = TSTool_Generic.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
    }
	else if (  selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HECDSS ) ) {
		numCommandsAdded = TSTool_HecDss.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
    }
	else if ( ((selectedDataStore != null) && (selectedDataStore instanceof HydroBaseDataStore)) ||
	    selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HydroBase )) {
		numCommandsAdded = TSTool_HydroBase.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset,
			this.__query_TableModel, selectedDataStoreName );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_MODSIM ) ) {
    	numCommandsAdded = TSTool_Modsim.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSCARD ) ) {
    	numCommandsAdded = TSTool_NwsrfsCard.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals( TSToolConstants.INPUT_TYPE_NWSRFS_ESPTraceEnsemble)) {
    	numCommandsAdded = TSTool_NwsrfsEsp.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset,
    		this.__query_TableModel );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files ) ) {
    	numCommandsAdded = TSTool_FS5Files.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof PluginDataStore) ) {
    	numCommandsAdded = TSTool_Plugin.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset,
			this.__query_TableModel, selectedDataStore );
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof RccAcisDataStore) ) {
    	numCommandsAdded = TSTool_RccAcis.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Daily(row, useAlias, insertOffset );
    }
	else if ( (selectedDataStore != null) && (selectedDataStore instanceof ReclamationHDBDataStore) ) {
    	numCommandsAdded = TSTool_HDB.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
    }
	else if ( (selectedDataStore != null) && (selectedDataStore instanceof ReclamationPiscesDataStore) ) {
		numCommandsAdded = TSTool_Pisces.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Daily ( row, useAlias, insertOffset );
    }
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_RiverWare ) ) {
    	numCommandsAdded = TSTool_RiverWare.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateCU ) ) {
	    // Most time series are still handled generically but XOP time series have additional columns in the table.
		numCommandsAdded = TSTool_StateCU.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateCUB ) ) {
	    // Most time series are still handled generically but XOP time series have additional columns in the table.
		numCommandsAdded = TSTool_StateCUB.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateMod ) ) {
	    // Most time series are still handled generically but XOP time series have additional columns in the table.
		numCommandsAdded = TSTool_StateMod.getInstance(this).transferOneTimeSeriesCatalogRowToCommands ( row, useAlias, insertOffset );
	}
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateModB ) ) {
    	numCommandsAdded = TSTool_StateModB.getInstance(this).transferOneTimeSeriesCatalogRowToCommands(row, useAlias, insertOffset );
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisDailyDataStore) ) {
    	numCommandsAdded = TSTool_UsgsNwis.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Daily(row, useAlias, insertOffset );
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisGroundwaterDataStore) ) {
    	numCommandsAdded = TSTool_UsgsNwis.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Groundwater(row, useAlias, insertOffset );
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisInstantaneousDataStore) ) {
    	numCommandsAdded = TSTool_UsgsNwis.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Instantaneous(row, useAlias, insertOffset );
    }
	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_UsgsNwisRdb ) ) {
    	numCommandsAdded = TSTool_UsgsNwis.getInstance(this).transferOneTimeSeriesCatalogRowToCommands_Rdb(row, useAlias, insertOffset );
	}
	else {
	    Message.printWarning(1, routine, "Transfer from query list to commands has not been implemented for \"" +
            selectedInputType + "\" input type." );
	    numCommandsAdded = 0;
	}
	// Check the GUI.
	if ( update_status ) {
		ui_UpdateStatus ( true );
	}
	return numCommandsAdded;
}

/**
Clear the results displays.
*/
private void results_Clear() {
    results_Ensembles_Clear();
    results_Networks_Clear();
    results_Objects_Clear();
    results_OutputFiles_Clear();
    results_Problems_Clear();
    results_Properties_Clear();
    results_Tables_Clear();
	results_TimeSeries_Clear();
    results_Views_Clear();
}

/**
Add a time series ensemble description at the end of the time series ensemble results list.
Note that this does not add the actual ensemble, only a description string.
The ensembles are still accessed by the positions in the list.
@param tsensemble_info Time series ensemble information to add at the end of the list.
*/
private void results_Ensembles_AddEnsembleToResults ( final String tsensemble_info ) {
    this.__resultsTSEnsembles_JListModel.addElement ( tsensemble_info );
}

/**
Clear the results ensemble List.  Updates to the label are also done.
*/
private void results_Ensembles_Clear() {
    // Clear the visible list of results.
    this.__resultsTSEnsembles_JListModel.removeAllElements();
    ui_UpdateStatus ( false );
}

/**
Get the ensemble identifier from a displayed ensemble item, which is in the format "N) EnsembleID - Ensemble Name".
*/
private TSEnsemble results_Ensembles_GetEnsembleID ( String displayItem ) {
    String routine = getClass().getSimpleName() + ".results_Ensembles_GetEnsembleID";
    String message;
    // Get the "N) EnsembleID" string.
    // This could still be an issue if the ensemble ID has " - " in the name, but at least it is less likely than just "-".
    int pos = displayItem.indexOf( " - " );
    String s = displayItem.substring(0,pos).trim();
    // Now get the ensemble ID part of the string.
    pos = displayItem.indexOf( ")" );
    String ensembleID = s.substring(pos + 1).trim();
    PropList requestParams = new PropList ( "" );
    requestParams.set ( "EnsembleID", ensembleID );
    CommandProcessorRequestResultsBean bean = null;
    try {
        bean = this.__tsProcessor.processRequest( "GetEnsemble", requestParams);
    }
    catch ( Exception e ) {
        message = "Error requesting GetEnsemble(EnsembleID=\"" + ensembleID + "\".";
        Message.printWarning(3, routine, message );
        return null;
    }
    PropList bean_PropList = bean.getResultsPropList();
    Object o_tsEnsemble = bean_PropList.getContents ( "TSEnsemble" );
    if ( o_tsEnsemble == null ) {
        message = "Null TSEnsemble requesting GetEnsemble(EnsembleID=\"" + ensembleID + "\".";
        Message.printWarning(3, routine, message );
        return null;
    }
    TSEnsemble ensemble = (TSEnsemble)o_tsEnsemble;
    return ensemble;
}

// TODO smalers 2009-05-08 Evaluate sorting the files - maybe need to put in a worksheet so they can be sorted.
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
    /* TODO smalers 2015-07-10 Remove if the replacement code works.
    if ( !IOUtil.fileExists(filePathString)) {
        // File does not exist so don't show in the list of output files.
        return;
    }
    */
	if ( (file == null) || !file.exists() ) {
		// File does not exist so don't show in the list of output files
		return;
	}
    if ( JGUIUtil.indexOf(this.__resultsOutputFiles_JList, filePathString, false, true) < 0 ) {
        this.__resultsOutputFiles_JListModel.addElement( filePathString );
    }
}

/**
Add the specified network to the list of networks that can be selected for viewing.
@param networkid network identifier for network generated by the processor.
*/
private void results_Networks_AddNetwork ( String networkid ) {
    this.__resultsNetworks_JListModel.addElement( networkid );
}

/**
Clear the list of results networks.  This is normally called immediately before the commands are run.
*/
private void results_Networks_Clear() {
    this.__resultsNetworks_JListModel.removeAllElements();
}

/**
Add the specified object to the list of objects that can be selected for viewing.
@param objectid object identifier for object generated by the processor.
*/
private void results_Objects_AddObject ( String objectid ) {
    this.__resultsObjects_JListModel.addElement( objectid );
}

/**
Clear the list of results objects.  This is normally called immediately before the commands are run.
*/
private void results_Objects_Clear() {
    this.__resultsObjects_JListModel.removeAllElements();
}

/**
Clear the list of output files.  This is normally called before the commands are run.
*/
private void results_OutputFiles_Clear() {
	this.__resultsOutputFiles_JListModel.removeAllElements();
    ui_UpdateStatus ( false );
}

/**
Add the specified table to the list of tables that can be selected for viewing.
@param tableid table identifier for table generated by the processor.
*/
private void results_Tables_AddTable ( String tableid ) {
    this.__resultsTables_JListModel.addElement( tableid );
}

/**
Clear the list of results problems.  This is normally called immediately before the commands are run.
*/
private void results_Problems_Clear() {
    this.__resultsProblems_JWorksheet.clear();
}

/**
Clear the list of results processor properties.  This is normally called immediately before the commands are run.
*/
private void results_Properties_Clear() {
    this.__resultsProperties_JWorksheet.clear();
}

/**
Clear the list of results tables.  This is normally called immediately before the commands are run.
*/
private void results_Tables_Clear() {
    this.__resultsTables_JListModel.removeAllElements();
}

/**
Add a time series description at the end of the time series results list.
Note that this does not add the actual time series, only a description string.
The time series are still accessed by the positions in the list.
@param ts_info Time series information to add at the end of the list.
*/
private void results_TimeSeries_AddTimeSeriesToResults ( final String ts_info ) {
	this.__resultsTS_JListModel.addElement ( ts_info );
}

/**
Clear the final time series List.  Updates to the label are also done. Also set the engine to null.
*/
private void results_TimeSeries_Clear() {
	// Clear the visible list of results.
	this.__resultsTS_JListModel.removeAllElements();
	ui_UpdateStatus ( false );
}

/**
 * Get the time series results.
 * This is used by UI code that operates directly on the time series results,
 * whereas graphing code calls the processor to do the work.
 * @param selectedOnly if true, return only the selected time series (all if none are selected)
 * @return the list of time series from the results
 */
private List<TS> results_TimeSeries_GetList ( boolean selectedOnly ) {
	List<TS> tslist = new ArrayList<>();
	// Work on the time series list model, which reflects selections.
    int [] selectedIndices = this.__resultsTS_JList.getSelectedIndices();
    if ( selectedOnly ) {
    	if ( selectedIndices.length == 0 ) {
    		// Return the full list.
    		tslist = commandProcessor_GetTimeSeriesResultsList();
    	}
    	else {
    		// Return the time series that are selected.
    		List<TS> tsresultsList = commandProcessor_GetTimeSeriesResultsList();
    		for ( int selectedIndex : selectedIndices ) {
    			tslist.add(tsresultsList.get(selectedIndex));
    		}
    	}
    }
    else {
    	// Return all.
    	tslist = commandProcessor_GetTimeSeriesResultsList();
    }
    if ( tslist == null ) {
    	// Create an empty list.
    	tslist = new ArrayList<>();
    }
    return tslist;
}

/**
Add the specified view to the list of views that can be selected for viewing.
@param view time series view generated by the processor.
*/
private void results_Views_AddView ( TimeSeriesView view ) {
    String viewid = view.getViewID();
    // The tabbed pane is cleared before running commands so adding a view should be as simple
    // as adding a new panel to the tabbed pane.
    if ( view instanceof TimeSeriesTreeView ) {
        // See the StateMod_DataSet_JTree for a more complex tree - this is pretty simple for now.
        TimeSeriesTreeView treeView = (TimeSeriesTreeView)view;
        //__resultsViews_JTabbedPane.add(viewid,new JScrollPane(new JTree(treeView.getRootNode())));
        TimeSeriesTreeView_JTree tree = new TimeSeriesTreeView_JTree(treeView.getRootNode());
        tree.setTSProductProcessor(this); // Allows popup to graph time series with product file.
        this.__resultsViews_JTabbedPane.add(viewid,new JScrollPane(tree));
    }
    else {
        this.__resultsViews_JTabbedPane.add ( new JLabel("View is not implemented.") );
    }
}

/**
Clear the list of results views.  This is normally called immediately before the commands are run.
*/
private void results_Views_Clear() {
    this.__resultsViews_JTabbedPane.removeAll();
}

/**
Show and hide the main frame.
@param state true if showing the frame, false if hiding it.
*/
public synchronized void setVisible(boolean state) {
	if (state) {
		setLocation(50, 50);
	}
	super.setVisible(state);
}

/**
Check the state of the GUI and enable/disable features as necessary.
For example, if no time series are selected, disable output options.
This is a more primitive call than ui_UpdateStatus(),
which should generally be used rather than directly calling this method.
*/
private void ui_CheckGUIState () {
	// Early on the GUI may not be initialized and some of the components seem to still be null.
	if ( !this.__guiInitialized ) {
		return;
	}

	boolean enabled = true; // Used to enable/disable main menus based on sub-menus.

	// Get the needed list sizes.

	int queryListSize = 0;
	if ( this.__query_TableModel != null ) {
		queryListSize = this.__query_TableModel.getRowCount();
	}

	int commandListSize = 0;
	int selectedCommandsSize = 0;
	if ( this.__commands_JListModel != null ) {
		commandListSize = this.__commands_JListModel.size();
		selectedCommandsSize = JGUIUtil.selectedSize ( ui_GetCommandJList() );
	}

	int tsListSize = 0;
	if ( this.__resultsTS_JListModel != null ) {
		tsListSize = this.__resultsTS_JListModel.size();
	}

	int dataStoreListSize = 0;
	if ( this.__tsProcessor != null ) {
	    dataStoreListSize = this.__tsProcessor.getDataStores().size();
	}

	// If no datastores are available, don't even show the datastore choices - this should hopefully
	// minimize confusion between datastores and input type/name selections.
	/* TODO smalers 2013-04-15 Remove this if the tabbed pane works well for data stores and input types.
	if ( dataStoreListSize == 0 ) {
	    __dataStore_JLabel.setVisible(false);
	    __dataStore_JComboBox.setVisible(false);
	}
	else {
	    __dataStore_JLabel.setVisible(true);
	    __dataStore_JComboBox.setVisible(true);
	}
	*/

	// List menus in the order of the GUI.  Popup menu items are checked as needed mixed in below.

	// File menu.

	enabled = false;
	if ( commandListSize > 0 ) {
		// Have commands shown.
		if ( this.__commandsDirty  ) {
			JGUIUtil.setEnabled ( TSToolMenus.File_Save_Commands_JMenuItem,true );
		}
		else {
            JGUIUtil.setEnabled ( TSToolMenus.File_Save_Commands_JMenuItem,false );
		}
		JGUIUtil.setEnabled ( TSToolMenus.File_Save_CommandsAs_JMenuItem, true );
		// TODO smalers 2023-02-19 remove ASAP since not used.
		//JGUIUtil.setEnabled ( TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem, true );
		JGUIUtil.setEnabled ( TSToolMenus.File_Print_Commands_JMenuItem, true );
		JGUIUtil.setEnabled ( TSToolMenus.File_Print_JMenu, true );
		enabled = true;
	}
	else {
	    // No commands are shown.
		JGUIUtil.setEnabled ( TSToolMenus.File_Save_Commands_JMenuItem, false );
		JGUIUtil.setEnabled ( TSToolMenus.File_Save_CommandsAs_JMenuItem, false );
		// TODO smalers 2023-02-19 remove ASAP since not used.
		//JGUIUtil.setEnabled ( TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem, false );
	    JGUIUtil.setEnabled ( TSToolMenus.File_Print_Commands_JMenuItem, false );
		JGUIUtil.setEnabled ( TSToolMenus.File_Print_JMenu, false );
	}
	if ( tsListSize > 0 ) {
		JGUIUtil.setEnabled ( TSToolMenus.File_Save_TimeSeriesAs_JMenuItem, true);
		enabled = true;
	}
	else {
        JGUIUtil.setEnabled ( TSToolMenus.File_Save_TimeSeriesAs_JMenuItem,false);
	}
	JGUIUtil.setEnabled ( TSToolMenus.File_Save_JMenu, enabled );

	if ( this.commandsHaveSourceUrlAnnotation ) {
	    JGUIUtil.setEnabled ( TSToolMenus.File_CheckForUpdate_JMenuItem, true );
	}
	else {
	    JGUIUtil.setEnabled ( TSToolMenus.File_CheckForUpdate_JMenuItem, false );
	}

	if ( TSTool_HydroBase.getInstance(this).getHydroBaseDMILegacy() != null ) {
		JGUIUtil.setEnabled ( TSToolMenus.File_Properties_HydroBase_JMenuItem,true );
	}
	else {
        JGUIUtil.setEnabled ( TSToolMenus.File_Properties_HydroBase_JMenuItem,false );
	}
	if ( TSTool_FS5Files.getInstance(this).getNwsrfsFS5FilesDMI() != null ) {
		JGUIUtil.setEnabled (TSToolMenus.File_Properties_NWSRFSFS5Files_JMenuItem,true );
	}
	else {
        JGUIUtil.setEnabled (TSToolMenus.File_Properties_NWSRFSFS5Files_JMenuItem,false );
	}

	// Edit menu.

	enabled = false;
	if ( commandListSize > 0 ) {
	    enabled = true;
	}
	JGUIUtil.setEnabled ( TSToolMenus.Edit_SelectAllCommands_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_SelectAll_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_DeselectAllCommands_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_DeselectAll_JMenuItem, enabled );

	enabled = false;
	if ( selectedCommandsSize > 0 ) {
	    enabled = true;
	}
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_IndentRight_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_IndentLeft_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_CutCommands_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Cut_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_CopyCommands_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Copy_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_DeleteCommands_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Delete_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_CommandWithErrorChecking_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_ConvertSelectedCommandsToComments_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Edit_ConvertSelectedCommandsFromComments_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Edit_ConvertTSIDTo_ReadTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Edit_ConvertTSIDTo_ReadCommand_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadCommand_JMenuItem, enabled );

	if ( this.__commandsCutBuffer.size() > 0 ) {
		// Paste button should be enabled.
		JGUIUtil.setEnabled ( TSToolMenus.Edit_PasteCommands_JMenuItem, true );
		JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Paste_JMenuItem, true );
	}
	else {
		JGUIUtil.setEnabled ( TSToolMenus.Edit_PasteCommands_JMenuItem, false );
		JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_Paste_JMenuItem, false );
	}

	// View menu.

	if ( this.commandsHaveSourceUrlAnnotation ) {
	    JGUIUtil.setEnabled ( TSToolMenus.View_CommandFileSourceDiff_JMenuItem, true );
	}
	else {
	    JGUIUtil.setEnabled ( TSToolMenus.View_CommandFileSourceDiff_JMenuItem, false );
	}
	if ( dataStoreListSize > 0 ) {
	    JGUIUtil.setEnabled ( TSToolMenus.View_DataStores_JMenuItem, true );
	}
	else {
	    JGUIUtil.setEnabled ( TSToolMenus.View_DataStores_JMenuItem, false );
	}
    if ( TSViewJFrame.getTSViewWindowManager().getWindowCount() > 0 ) {
        JGUIUtil.setEnabled ( TSToolMenus.View_CloseAllViewWindows_JMenuItem, true );
    }
    else {
        JGUIUtil.setEnabled ( TSToolMenus.View_CloseAllViewWindows_JMenuItem, false );
    }

	// Commands menu.

	enabled = false;
	if ( commandListSize > 0 ) {
	    // Some commands are available so enable commands that operate on other time series.
	    enabled = true;
	}
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Select_DeselectTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Select_SelectTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Select_Free_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Select_SortTimeSeries_JMenuItem, enabled );

    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_Delta_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ResequenceTimeSeriesData_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ChangeInterval_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ChangeIntervalToLarger_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ChangeIntervalToSmaller_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ChangeIntervalIrregularToRegular_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_ChangeIntervalRegularToIrregular_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_Copy_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_Disaggregate_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_LookupTimeSeriesFromTable_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_NewDayTSFromMonthAndDayTS_JMenuItem,	enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_NewEndOfMonthTSFromDayTS_JMenuItem,enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_Normalize_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_RelativeDiff_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_NewStatisticTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_NewStatisticMonthTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_NewStatisticYearTS_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Create_RunningStatisticTimeSeries_JMenuItem, enabled );

	if ( this.__tsProcessor.getDataStoresByType(ReclamationHDBDataStore.class).size() > 0 ) {
	    JGUIUtil.setEnabled ( TSToolMenus.Commands_Read_ReadReclamationHDB_JMenuItem, enabled );
	}
	else {
	    JGUIUtil.setEnabled ( TSToolMenus.Commands_Read_ReadReclamationHDB_JMenuItem, false );
	}

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillConstant_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillFromTS_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillHistMonthAverage_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillHistYearAverage_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillInterpolate_JMenuItem, enabled );
	// TODO smalers 2005-04-26 This fill method is not enabled - may not be needed.
	//JGUIUtil.setEnabled(TSToolMenus.Commands_Fill_fillMOVE1_JMenuItem,enabled);
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillMOVE2_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillMixedStation_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillPattern_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillProrate_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillRegression_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillRepeat_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillUsingDiversionComments_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_FillTimeSeries_JMenu, enabled );

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_ReplaceValue_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetConstant_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetDataValue_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetFromTS_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetTimeSeriesValuesFromLookupTable_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetTimeSeriesValuesFromTable_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetToMax_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetToMin_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Set_SetTimeSeriesProperty_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_SetTimeSeries_JMenu, enabled );

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Add_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_AddConstant_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_AdjustExtremes_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_ARMA_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Blend_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_ChangePeriod_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_ChangeTimeZone_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_ConvertDataUnits_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Cumulate_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Divide_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Multiply_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Scale_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_ShiftTimeByInterval_JMenuItem,enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Manipulate_Subtract_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_ManipulateTimeSeries_JMenu, enabled );

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Analyze_AnalyzePattern_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Analyze_CalculateTimeSeriesStatistic_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Analyze_CompareTimeSeries_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Analyze_ComputeErrorTimeSeries_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_AnalyzeTimeSeries_JMenu, enabled );

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Models_Routing_JMenu, enabled );

	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteDateValue_JMenuItem, enabled );
	//JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteDelftFewsPiXml_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteDelimitedFile_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteHecDss_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteNwsCard_JMenuItem, enabled );
	if ( this.__tsProcessor.getDataStoresByType(ReclamationHDBDataStore.class).size() > 0 ) {
	    JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteReclamationHDB_JMenuItem, enabled );
	}
	else {
	    JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteReclamationHDB_JMenuItem, false );
	}
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteRiverWare_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteSHEF_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteStateCU_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteStateMod_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteSummary_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteTimeSeriesToDataStore_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteTimeSeriesToDataStream_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteTimeSeriesToHydroJSON_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteTimeSeriesToJson_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteWaterML_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_WriteWaterML2_JMenuItem, enabled );

    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_CopyEnsemble_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_SetEnsembleProperty_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_NewStatisticEnsemble_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_WeightTraces_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_JMenuItem, enabled );

    JGUIUtil.setEnabled ( TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeries_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_JMenuItem, enabled );

    JGUIUtil.setEnabled ( TSToolMenus.Commands_Deprecated_RunningAverage_JMenuItem, enabled );

    JGUIUtil.setEnabled ( TSToolMenus.Commands_Spatial_WriteTimeSeriesToGeoJSON_JMenuItem, enabled );
    JGUIUtil.setEnabled ( TSToolMenus.Commands_Spatial_WriteTimeSeriesToKml_JMenuItem, enabled );

	/* TODO - it is irritating to not be able to run commands when external input changes (or during debugging).
	if ( __commands_dirty || (!__commands_dirty && (ts_list_size == 0)) ) {
		JGUIUtil.setEnabled ( __run_commands_JButton, true );
	}
	else {
        JGUIUtil.setEnabled ( __run_commands_JButton, false );
	}
	*/
	if ( selectedCommandsSize > 0 ) {
		JGUIUtil.setEnabled ( this.__Run_SelectedCommands_JButton, true );
	}
	else {
        JGUIUtil.setEnabled ( this.__Run_SelectedCommands_JButton, false );
	}
	JGUIUtil.setEnabled ( this.__Run_AllCommands_JButton, true );
	JGUIUtil.setEnabled ( this.__ClearCommands_JButton, true );

	enabled = false;
	if ( selectedCommandsSize > 0 ) {
	    enabled = true;
	}
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadTimeSeries_JMenuItem, enabled );
	JGUIUtil.setEnabled ( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadCommand_JMenuItem, enabled );

	// Run menu.

	ui_CheckGUIState_RunMenu ( commandListSize, selectedCommandsSize );

	// Results menu.

	if ( tsListSize > 0 ) {
		JGUIUtil.setEnabled ( TSToolMenus.Results_JMenu, true );
	}
	else {
        // DISABLE file and view options.
		JGUIUtil.setEnabled ( TSToolMenus.Results_JMenu, false );
	}

	// Tools menu.

	if ( tsListSize > 0 ) {
		JGUIUtil.setEnabled ( TSToolMenus.Tools_Analysis_JMenu, true );
		JGUIUtil.setEnabled ( TSToolMenus.Tools_Report_JMenu, true );
	}
	else {
        JGUIUtil.setEnabled ( TSToolMenus.Tools_Analysis_JMenu, false );
		JGUIUtil.setEnabled ( TSToolMenus.Tools_Report_JMenu, false );
	}
	if ( (queryListSize > 0) && (__geoview_JFrame != null) ) {
		JGUIUtil.setEnabled ( TSToolMenus.Tools_SelectOnMap_JMenuItem, true );
	}
	else {
        JGUIUtil.setEnabled ( TSToolMenus.Tools_SelectOnMap_JMenuItem, false );
	}
	if ( commandListSize > 0 ) {
        JGUIUtil.setEnabled ( TSToolMenus.Tools_Commands_JMenu, true );
	}
	else {
        JGUIUtil.setEnabled ( TSToolMenus.Tools_Commands_JMenu, false );
	}

	// Enable/disable features related to the query list.

	if ( queryListSize > 0 ) {
		JGUIUtil.setEnabled ( this.__CopyAllToCommands_JButton, true );
	}
	else {
        JGUIUtil.setEnabled ( this.__CopyAllToCommands_JButton, false );
	}
	if ( (queryListSize > 0) && (this.__query_JWorksheet != null) &&
		(this.__query_JWorksheet.getSelectedRowCount() > 0) ) {
		JGUIUtil.setEnabled ( this.__CopySelectedToCommands_JButton, true );
	}
	else {
        JGUIUtil.setEnabled ( this.__CopySelectedToCommands_JButton, false );
	}

	// TODO Not available as a command yet - logic not coded.
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Fill_FillMOVE1_JMenuItem, false );

	// TODO - can this be phased out?
	JGUIUtil.setEnabled ( TSToolMenus.Commands_Output_SetOutputDetailedHeaders_JMenuItem, false );
}

/**
Enable/disable Run menu items based on the state of the GUI.
@param commandListSize the number of commands
@param selectedCommandsSize the number of selected commands
*/
private void ui_CheckGUIState_RunMenu ( int commandListSize, int selectedCommandsSize ) {
	// Running, so allow cancel but not another run.
	boolean enable_run = false;
	if ( (this.__tsProcessor != null) && this.__tsProcessor.getIsRunning() ) {
		// Running, so allow cancel but not another run.
		enable_run = false;  // Handled below in second if.
		JGUIUtil.setEnabled (TSToolMenus.Run_CancelCommandProcessing_JMenuItem, true);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_CancelCommandProcessing_JMenuItem,true);

	}
	else {
		// Not running, so disable cancel, but do allow run if there are commands (see below).
		enable_run = true;
		JGUIUtil.setEnabled (TSToolMenus.Run_CancelCommandProcessing_JMenuItem, false);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_CancelCommandProcessing_JMenuItem,false );
	}
	if ( commandListSize > 0 ) {
		/* TODO smalers 2007-11-01 Evaluate need.
		if ( __commands_dirty || (__commands_dirty && (ts_list_size == 0)) ) {
			JGUIUtil.setEnabled (__run_commands_JButton, true );
		}
		else {
		    JGUIUtil.setEnabled ( __run_commands_JButton, false );
		}
		*/
		// Run all commands menus always enabled if not already running.
		JGUIUtil.setEnabled(TSToolMenus.Run_AllCommandsCreateOutput_JMenuItem, enable_run);
		JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem,enable_run);
		JGUIUtil.setEnabled(TSToolMenus.Run_AllCommandsIgnoreOutput_JMenuItem, enable_run);
		JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem,enable_run);
		JGUIUtil.setEnabled ( this.__Run_AllCommands_JButton, enable_run );
		if ( selectedCommandsSize > 0 ) {
			// Run selected commands menus.
			JGUIUtil.setEnabled(TSToolMenus.Run_SelectedCommandsCreateOutput_JMenuItem, enable_run);
			JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,enable_run);
			JGUIUtil.setEnabled(TSToolMenus.Run_SelectedCommandsIgnoreOutput_JMenuItem, enable_run);
			JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,enable_run);
			// Run buttons.
			JGUIUtil.setEnabled (this.__Run_SelectedCommands_JButton, enable_run );
		}
		else {
			// Run selected commands menus are false (because none selected).
			JGUIUtil.setEnabled(TSToolMenus.Run_SelectedCommandsCreateOutput_JMenuItem, false);
			JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,false);
			JGUIUtil.setEnabled(TSToolMenus.Run_SelectedCommandsIgnoreOutput_JMenuItem, false);
			JGUIUtil.setEnabled(TSToolMenus.CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,false);
			JGUIUtil.setEnabled (__Run_SelectedCommands_JButton, false );
		}
		// Have commands so can clear.
		JGUIUtil.setEnabled ( this.__ClearCommands_JButton, true );
	}
	else {
	    // No commands in list.
		JGUIUtil.setEnabled (TSToolMenus.Run_AllCommandsCreateOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.Run_AllCommandsIgnoreOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.Run_SelectedCommandsCreateOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.Run_SelectedCommandsIgnoreOutput_JMenuItem,false);
		JGUIUtil.setEnabled (TSToolMenus.CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem,false);
		JGUIUtil.setEnabled ( this.__Run_SelectedCommands_JButton, false );
		JGUIUtil.setEnabled ( this.__Run_AllCommands_JButton, false );
		JGUIUtil.setEnabled ( this.__ClearCommands_JButton, false );
	}
}

/**
 * This function can be called to clear the initial label that is displayed.
 * TODO smalers 2015-02-15 Need a graceful way to hide the following but set text to blank as work-around:
 * - otherwise, some of the text shows through behind the datastore panel
 * - I've tried several things and finally just call this in opportune places to make sure the old label is not shown
 */
private void ui_ClearDataStoreInitializing() {
    if ( this.__dataStoreInitializing_JLabel != null ) {
    	this.__dataStoreInitializing_JLabel.setText("");
        this.__dataStoreInitializing_JLabel.setText(""); // No longer need to show message.
    }
    if ( this.__dataStoreInitializing_JPanel != null ) {
        this.__dataStoreInitializing_JPanel.setVisible(false); // No longer need to show message.
    }
}

/**
Take a full filename string and if it is too long, create an abbreviated filename that fits into the GUI better.
The front and the rear of the file are retained, with ... in the middle.
@param fullFilename the full filename string to check.
@return the abbreviated filename, if longer than the maximum allowed for display purposes.
*/
public String ui_CreateAbbreviatedVisibleFilename(String fullFilename) {
    int maxLengthAllowed = 60;
    if ( fullFilename.length() < maxLengthAllowed ) {
        return fullFilename;
    }
    else {
        // First try - remove the middle characters, retaining the ends without checking path breaks.
        int numCharsToRemove = fullFilename.length() - maxLengthAllowed;
        int numCharsToRetainEachEnd = (fullFilename.length() - numCharsToRemove)/2;
        return fullFilename.substring(0,numCharsToRetainEachEnd) + "..." +
            fullFilename.substring(fullFilename.length() - numCharsToRetainEachEnd);
    }
}

/**
Populate the datastore list from available processor datastores.
*/
private void ui_DataStoreList_Populate () {
    this.__dataStore_JComboBox.removeAll();
    List<String> dataStoreNameList = new ArrayList<>();
    // Get all enabled datastores, even those not active - the View ... Datastores menu can be used to show errors.
    List<DataStore> dataStoreList = this.__tsProcessor.getDataStores();
    for ( DataStore dataStore : dataStoreList ) {
        if ( dataStore.getClass().getName().endsWith(".NrcsAwdbDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisDailyDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisGroundwaterDataStore") ||
            dataStore.getClass().getName().endsWith(".UsgsNwisInstantaneousDataStore") ) {
            // For now disable in the main browser since no interactive browsing ability has been implemented.
            // FIXME smalers 2012-10-26 For USGS enable when USGS site service is enabled.
            // FIXME smalers 2012-12-18 Enable with filter panel is developed specific to web services.
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
    // Also list any substitute datastore names so the original or substitute can be used:
    // - only add if not already in the datastore list
    List<DataStoreSubstitute> datastoreSubstituteList = this.__tsProcessor.getDataStoreSubstituteList();
    for ( DataStoreSubstitute dssub : datastoreSubstituteList ) {
    	boolean found = false;
		String substituteName = null;
    	for ( String choice : dataStoreNameList ) {
    		if ( choice.equals(dssub.getDatastoreNameToUse()) ) {
    			// The substitute original name matches a datastore name so also add the substitute.
    			found = true;
    			substituteName = dssub.getDatastoreNameInCommands();
    			break;
    		}
    	}
    	if ( found ) {
    		boolean found2 = false;
    		for ( String dsname : dataStoreNameList ) {
    			if ( dsname.equals(substituteName) ) {
    				found2 = true;
    			}
    		}
    		if ( !found2 ) {
    			dataStoreNameList.add(substituteName);
    		}
    	}
    }
    Collections.sort(dataStoreNameList, String.CASE_INSENSITIVE_ORDER);
    dataStoreNameList.add ( 0, "" ); // Blank when picking input type and name separately.
    this.__dataStore_JComboBox.setData(dataStoreNameList);
    // Select the blank.
    this.__dataStore_JComboBox.select("");
}

/**
Enable the input and datastore types based on the TSTool configuration.
*/
private void ui_EnableInputTypesForConfiguration () {
    // Determine which data sources are available.
	// This controls the look and feel of the GUI.  Alphabetize the checks.
	// A default value is set for the case where the configuration file may not contain a property,
	// and then a check of the string value is done to set to a value other than the default.

    String propValue = null;

    // State of Colorado HydroBase REST web service disabled by default
    // (can be slow at startup due to input filter initialization) but can turn on.

    this.__source_ColoradoHydroBaseRest_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.ColoradoHydroBaseRestEnabled" );
    String propValueUser = this.session.getUserConfigPropValue ( "TSTool.ColoradoHydroBaseRestEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "ColoradoHydroBaseRestEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
    	this.__source_ColoradoHydroBaseRest_enabled = true;
    }

    // DateValue enabled by default.

    this.__source_DateValue_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.DateValueEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.DateValueEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "DateValueEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_DateValue_enabled = false;
    }

    // DELFT FEWS disabled by default.

    this.__source_DelftFews_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.DelftFewsEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.DelftFewsEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "DelftFewsEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
    	this.__source_DelftFews_enabled = true;
    }

    // HEC-DSS enabled by default on Windows and always off on UNIX because DLLs are for Windows.
    // TODO smalers 2009-04-14 Emailed Bill Charley and waiting on answer for support of other OS.

    if ( IOUtil.isUNIXMachine() ) {
        // Disable on UNIX.
        __source_HECDSS_enabled = false;
    }
    else {
        __source_HECDSS_enabled = true;
        propValue = TSToolMain.getPropValue ( "TSTool.HEC-DSSEnabled" );
        propValueUser = this.session.getUserConfigPropValue ( "TSTool.HEC-DSSEnabled" );
        if ( (propValueUser == null) || propValueUser.isEmpty() ) {
        	propValueUser = this.session.getUserConfigPropValue ( "HEC-DSSEnabled" );
        }
        if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
        	// User configuration value takes precedence.
        	propValue = propValueUser;
        }
        if ( (propValue != null)&& propValue.equalsIgnoreCase("false") ) {
            this.__source_HECDSS_enabled = false;
        }
    }

    // State of Colorado HydroBase disabled by default (users must have a local HydroBase).

    this.__source_HydroBase_enabled = false;
    // Newer.
    propValue = TSToolMain.getPropValue ( "TSTool.HydroBaseEnabled" );
    if ( propValue == null ) {
        // Older.
        propValue = TSToolMain.getPropValue ("TSTool.HydroBaseCOEnabled" );
    }
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.HydroBaseEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	// Try alternative.
    	propValueUser = this.session.getUserConfigPropValue ( "HydroBaseEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_HydroBase_enabled = true;
    }
    if ( this.__source_HydroBase_enabled ) {
        // Use newer notation.
        this.__props.set ( "TSTool.HydroBaseEnabled", "true" );
        propValue = TSToolMain.getPropValue ( "HydroBase.WDIDLength" );
        if ( (propValue != null) && StringUtil.isInteger(propValue)){
            this.__props.set ( "HydroBase.WDIDLength", propValue );
            // Also set in global location.
            HydroBase_Util.setPreferredWDIDLength ( StringUtil.atoi ( propValue ) );
        }
        else {
            // Default.
            this.__props.set ( "HydroBase.WDIDLength", "7" );
        }
        propValue = TSToolMain.getPropValue ( "HydroBase.OdbcDsn" );
        if ( propValue != null ) {
            this.__props.set ( "HydroBase.OdbcDsn", propValue );
        }
    }
    else {
        this.__props.set ( "TSTool.HydroBaseEnabled", "false" );
    }

    // MODSIM always enabled by default.

    this.__source_MODSIM_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.MODSIMEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.MODSIMEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "MODSIMEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_MODSIM_enabled = false;
    }

    // NWS Card enabled by default.

    this.__source_NWSCard_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.NWSCardEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.NWSCardEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "NWSCardEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_NWSCard_enabled = false;
    }

    // NWSRFS_ESPTraceEnsemble disabled by default.

    this.__source_NWSRFS_ESPTraceEnsemble_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.NWSRFSESPTraceEnsembleEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.NWSRFSESPTraceEnsembleEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "NWSRFSESPTraceEnsembleEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_NWSRFS_ESPTraceEnsemble_enabled = true;
    }
    // Always disable if not available in the Jar file.
    if ( !IOUtil.classCanBeLoaded( "RTi.DMI.NWSRFS_DMI.NWSRFS_ESPTraceEnsemble") ) {
        this.__source_NWSRFS_ESPTraceEnsemble_enabled = false;
    }

    // NWSRFS FS5Files disabled by default.

    this.__source_NWSRFS_FS5Files_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.NWSRFSFS5FilesEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.NWSRFSFS5FilesEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "NWSRFSFS5FilesEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ){
        this.__source_NWSRFS_FS5Files_enabled = true;
        propValue = TSToolMain.getPropValue ( "NWSRFSFS5Files.UseAppsDefaults" );
        if ( propValue != null ) {
            this.__props.set( "NWSRFSFS5Files.UseAppsDefaults",propValue );
        }
        else {
            // Default is to use files.  If someone has Apps
            // Defaults configured, this property can be changed.
            this.__props.set ( "NWSRFSFS5Files.UseAppsDefaults","false");
        }
        propValue = TSToolMain.getPropValue ( "NWSRFSFS5Files.InputName" );
        if ( propValue != null ) {
            this.__props.set( "NWSRFSFS5Files.InputName",propValue );
        }
    }

    // RCC ACIS disabled by default but distributed configuration file has enabled by default.

    this.__source_RCCACIS_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.RCCACISEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.RCCACISEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "RCCACISEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_RCCACIS_enabled = true;
    }

    // Reclamation HDB disabled by default (not many users would have).

    this.__source_ReclamationHDB_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.ReclamationHDBEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.ReclamationHDBEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "ReclamationHDBEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_ReclamationHDB_enabled = true;
    }

    // Reclamation Pisces disabled by default (not many users would have).

    this.__source_ReclamationPisces_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.ReclamationPiscesEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.ReclamationPiscesEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "ReclamationPiscesEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_ReclamationPisces_enabled = true;
    }

    // RiverWare enabled by default.

    this.__source_RiverWare_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.RiverWareEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.RiverWareEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "RiverWareEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_RiverWare_enabled = false;
    }

    // SHEF disabled by default.

    this.__source_SHEF_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.SHEFEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.SHEFEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "SHEFEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_SHEF_enabled = true;
    }

    // StateCU enabled by default.

    this.__source_StateCU_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.StateCUEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.StateCUEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "StateCUEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_StateCU_enabled = false;
    }

    // StateCUB enabled by default.

    this.__source_StateCUB_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.StateCUBEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.StateCUBEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "StateCUBEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_StateCUB_enabled = false;
    }

    // StateMod enabled by default.

    this.__source_StateMod_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.StateModEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.StateModEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "StateModEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_StateMod_enabled = false;
    }

    // StateModB enabled by default.

    this.__source_StateModB_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.StateModBEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.StateModBEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "StateModBEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_StateModB_enabled = false;
    }

    // UsgsNwisDaily enabled by default.

    this.__source_UsgsNwisDaily_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.UsgsNwisDailyEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.UsgsNwisDailyEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "UsgsNwisDailyEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_UsgsNwisDaily_enabled = false;
    }

    // UsgsNwisGroundwater enabled by default.

    this.__source_UsgsNwisGroundwater_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.UsgsNwisGroundwaterEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.UsgsNwisGroundwaterEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "UsgsNwisGroundwaterEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_UsgsNwisGroundwater_enabled = false;
    }

    // UsgsNwisInstantaneous enabled by default.

    this.__source_UsgsNwisInstantaneous_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.UsgsNwisInstantaneousEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.UsgsNwisInstantaneousEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "UsgsNwisInstantaneousEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_UsgsNwisInstantaneous_enabled = false;
    }

    // UsgsNwisRdb enabled by default.

    this.__source_UsgsNwisRdb_enabled = true;
    // New...
    propValue = TSToolMain.getPropValue ( "TSTool.UsgsNwisRdbEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.UsgsNwisRdbEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "UsgsNwisRdbEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    // Legacy.
    if ( propValue == null ) {
        propValue = TSToolMain.getPropValue ( "TSTool.USGSNWISEnabled" );
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_UsgsNwisRdb_enabled = false;
    }

    // WaterML enabled by default.

    this.__source_WaterML_enabled = true;
    propValue = TSToolMain.getPropValue ( "TSTool.WaterMLEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.WaterMLEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "WaterMLEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("false") ) {
        this.__source_WaterML_enabled = false;
    }

    // WaterOneFlow disabled by default until get it working.

    this.__source_WaterOneFlow_enabled = false;
    propValue = TSToolMain.getPropValue ( "TSTool.WaterOneFlowEnabled" );
    propValueUser = this.session.getUserConfigPropValue ( "TSTool.WaterOneFlowEnabled" );
    if ( (propValueUser == null) || propValueUser.isEmpty() ) {
    	propValueUser = this.session.getUserConfigPropValue ( "WaterOneFlowEnabled" );
    }
    if ( (propValueUser != null) && !propValueUser.isEmpty() ) {
    	// User configuration value takes precedence.
    	propValue = propValueUser;
    }
    if ( (propValue != null) && propValue.equalsIgnoreCase("true") ) {
        this.__source_WaterOneFlow_enabled = true;
    }
}

/**
Return the command list component.  Do it this way because the command component may evolve.
*/
private JList ui_GetCommandJList() {
    return this.__commands_AnnotatedCommandJList.getJList();
}

/**
Return the data type JComboBox, used for datastore integration.
@return the data type JComboBox.
*/
public SimpleJComboBox ui_GetDataTypeJComboBox() {
    return this.__dataType_JComboBox;
}

/**
Return the directory for the last "File...Open Command File".
*/
private String ui_GetDir_LastCommandFileOpened() {
    String routine = getClass().getSimpleName() + ".ui_GetDir_LastCommandFileOpened";
	if ( this.__Dir_LastCommandFileOpened != null ) {
	    Message.printStatus ( 2, routine, "Returning last (non null) command file directory: " + this.__Dir_LastCommandFileOpened );
	    return this.__Dir_LastCommandFileOpened;
	}

	// Try to get the generic dialog selection location.
	this.__Dir_LastCommandFileOpened = JGUIUtil.getLastFileDialogDirectory();
    if ( this.__Dir_LastCommandFileOpened != null ) {
        Message.printStatus ( 2, routine, "Returning last command file directory from last dialog selection: " + this.__Dir_LastCommandFileOpened );
        return this.__Dir_LastCommandFileOpened;
    }
	// This will check user.dir
	this.__Dir_LastCommandFileOpened = IOUtil.getProgramWorkingDir ();
	Message.printStatus ( 2, routine, "Returning last command file directory from working directory: " + this.__Dir_LastCommandFileOpened );
	return this.__Dir_LastCommandFileOpened;
}

/**
Return the last directory for "Run Command File",
which runs an external command file but does not show the results.
*/
private String ui_GetDir_LastExternalCommandFileRun() {
    if ( this.__Dir_LastExternalCommandFileRun != null ) {
        return this.__Dir_LastExternalCommandFileRun;
    }
    // Try to get the generic dialog selection location.
	this.__Dir_LastExternalCommandFileRun = JGUIUtil.getLastFileDialogDirectory();
	if ( this.__Dir_LastExternalCommandFileRun == null ) {
	    // This will check the "user.dir" property.
        this.__Dir_LastExternalCommandFileRun = IOUtil.getProgramWorkingDir ();
    }
	return this.__Dir_LastExternalCommandFileRun;
}

/**
Return whether ActionEvents should be ignored.
*/
private boolean ui_GetIgnoreActionEvent() {
    return this.__ignoreActionEvent;
}

/**
Return whether ItemEvents should be ignored.
*/
private boolean ui_GetIgnoreItemEvent() {
    return this.__ignoreItemEvent;
}

/**
Return whether ListSelectionEvents should be ignored.
*/
private boolean ui_GetIgnoreListSelectionEvent() {
    return this.__ignoreListSelectionEvent;
}

// FIXME smalers 2007-11-01 Need to use /tmp etc for a startup home if not specified so the software install home is not used.
/**
Return the initial working directory, which will be the software startup home, or the location of new command files.
This directory is suitable for initializing a workflow processing run.
@return the initial working directory, which should always be non-null.
*/
private String ui_GetInitialWorkingDir () {
	return this.__initialWorkingDir;
}

/**
Return the list of input filter JPanel.
This used by datastore UI code.
*/
public List<InputFilter_JPanel> ui_GetInputFilterJPanelList () {
	return this.__inputFilterJPanelList;
}

/**
Return the Y layout coordinate used with the input filter panel.
This is saved because input types can be opened interactively and need to be added to the same location in the layout.
*/
public int ui_GetInputFilterY() {
    return this.__inputFilterY;
}

/**
Return the message input filter panel, with the indicated message.
This is used, for example, when displaying a message that a database datastore connection is unavailable,
rather than just showing the generic input filter that provides no information.
*/
public InputFilter_JPanel ui_GetInputFilterMessageJPanel ( String text ) {
    this.__inputFilterMessage_JPanel.setText ( text );
    return this.__inputFilterMessage_JPanel;
}

/**
Return the input filter panel for the specified datastore name.
By design, this method should only be called when working with datastores.
Eventually all the "database" input types will be handled (including binary files and relational databases).
@param selectedDataStoreName name of datastore to match
@param selectedDataType the selected data type (e.g., "Streamflow, no "Group - " prefix)
@param selectedTimeStep the selected time step (e.g., "Day")
@return the input filter panel that matches the datastore name, or null if not found
*/
public InputFilter_JPanel ui_GetInputFilterPanelForDataStoreName ( String selectedDataStoreName,
    String selectedDataType, String selectedTimeStep ) {
    String routine = getClass().getSimpleName() + ".ui_GetInputFilterPanelForDataStoreName";
    // This is a bit brute force because the name is embedded in the datastore but is not
    // a data member of the input panel.
    // Alphabetize by "instanceof" argument.
   	if ( Message.isDebugOn ) {
   		Message.printStatus ( 2, routine, "Setting input filter for current selected datastore \"" + selectedDataStoreName +
   			"\" data type=\"" + selectedDataType + "\" time step=\"" + selectedTimeStep + "\"" );
   	}
    // If a match is found in the loop return the panel.
    // Otherwise, the loop goes to the next input panel and checks it.
    for ( InputFilter_JPanel panel : this.__inputFilterJPanelList ) {
    	if ( Message.isDebugOn ) {
    		Message.printStatus(2, routine, "Panel name is \"" + panel.getName() + "\"");
    	}
    	// Start ColoradoHydroBaseRestDataStore REST web services.
        if ( (panel instanceof ColoradoHydroBaseRest_ClimateStation_InputFilter_JPanel) ) {
            // This type of filter uses a DataStore.
        	if ( Message.isDebugOn ) {
        		Message.printStatus(2, routine, "Checking ColoradoHydroBaseRest climate station input panel...");
        	}
            ColoradoHydroBaseRestDataStore datastore =
                ((ColoradoHydroBaseRest_ClimateStation_InputFilter_JPanel)panel).getColoradoHydroBaseRestDataStore();
        	if ( Message.isDebugOn ) {
        		Message.printStatus(2, routine, "Panel datastore name is \"" + datastore.getName() + "\"");
        	}
            if ( datastore.getName().equalsIgnoreCase(selectedDataStoreName) && datastore.isClimateStationTimeSeriesDataType(selectedDataType)) {
                // Have a match in the datastore name so return the panel.
            	if ( Message.isDebugOn ) {
            		Message.printStatus(2, routine, "Matched datastore and climate station input panel.");
            	}
                return panel;
            }
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Did not match datastore and climate station input panel.");
           	}
        }
        else if ( (panel instanceof ColoradoHydroBaseRest_Structure_InputFilter_JPanel) ) {
            // This type of filter uses a DataStore.
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Checking ColoradoHydroBaseRest structure input panel...");
           	}
            ColoradoHydroBaseRestDataStore datastore =
                ((ColoradoHydroBaseRest_Structure_InputFilter_JPanel)panel).getColoradoHydroBaseRestDataStore();
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Panel datastore name is \"" + datastore.getName() + "\"");
           	}
            if ( datastore.getName().equalsIgnoreCase(selectedDataStoreName) && datastore.isStructureTimeSeriesDataType(selectedDataType) ) {
                // Have a match in the datastore name so return the panel.
            	Message.printStatus(2, routine, "Matched datastore and structure input panel...");
                return panel;
            }
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Did not match datastore and structure input panel.");
           	}
        }
        else if ( (panel instanceof ColoradoHydroBaseRest_SurfaceWaterStation_InputFilter_JPanel) ) {
            // This type of filter uses a DataStore.
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Checking ColoradoHydroBaseRest surface water station input panel...");
           	}
            ColoradoHydroBaseRestDataStore datastore =
                ((ColoradoHydroBaseRest_SurfaceWaterStation_InputFilter_JPanel)panel).getColoradoHydroBaseRestDataStore();
            Message.printStatus(2, routine, "Panel datastore name is \"" + datastore.getName() + "\"");
            if ( datastore.getName().equalsIgnoreCase(selectedDataStoreName) && datastore.isSurfaceWaterStationTimeSeriesDataType(selectedDataType) ) {
                // Have a match in the datastore name so return the panel.
            	if ( Message.isDebugOn ) {
            		Message.printStatus(2, routine, "Matched datastore and station input panel.");
            	}
                return panel;
            }
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Did not match datastore and station input panel.");
           	}
        }
        else if ( (panel instanceof ColoradoHydroBaseRest_TelemetryStation_InputFilter_JPanel) ) {
            // This type of filter uses a DataStore.
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Checking ColoradoHydroBaseRest telemetry station input panel...");
           	}
            ColoradoHydroBaseRestDataStore datastore =
                ((ColoradoHydroBaseRest_TelemetryStation_InputFilter_JPanel)panel).getColoradoHydroBaseRestDataStore();
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Panel datastore name is \"" + datastore.getName() + "\"");
           	}
            if ( datastore.getName().equalsIgnoreCase(selectedDataStoreName) && datastore.isTelemetryStationTimeSeriesDataType(selectedDataType)) {
                // Have a match in the datastore name so return the panel.
            	if ( Message.isDebugOn ) {
            		Message.printStatus(2, routine, "Matched datastore and telemetry station input panel.");
            	}
                return panel;
            }
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Did not match datastore and telemetry station input panel.");
           	}
        }
        else if ( (panel instanceof ColoradoHydroBaseRest_Well_InputFilter_JPanel) ) {
            // This type of filter uses a DataStore.
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Checking ColoradoHydroBaseRest well input panel...");
           	}
        	ColoradoHydroBaseRestDataStore datastore =
                ((ColoradoHydroBaseRest_Well_InputFilter_JPanel)panel).getColoradoHydroBaseRestDataStore();
        	if ( Message.isDebugOn ) {
        		Message.printStatus(2, routine, "Panel datastore name is \"" + datastore.getName() + "\"");
        	}
            if ( datastore.getName().equalsIgnoreCase(selectedDataStoreName) && datastore.isWellTimeSeriesDataType(selectedDataType)) {
                // Have a match in the datastore name so return the panel.
            	if ( Message.isDebugOn ) {
            		Message.printStatus(2, routine, "Matched datastore and well input panel.");
            	}
                return panel;
            }
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2, routine, "Did not match datastore and well input panel.");
           	}
        }
        // Start GenericDatabaseDataStore direct database connection.
        else if ( panel instanceof GenericDatabaseDataStore_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((GenericDatabaseDataStore_TimeSeries_InputFilter_JPanel)panel).getDataStore();
           	if ( Message.isDebugOn ) {
           		Message.printStatus(2,routine,"Selected data store is \"" + selectedDataStoreName +
           			"\" checking filter panel data store name \"" + dataStore.getName() );
           	}
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        // Start HydroBase datastore.
        else if ( panel instanceof HydroBase_GUI_StationGeolocMeasType_InputFilter_JPanel ) {
            // HydroBase station time series.
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            HydroBase_GUI_StationGeolocMeasType_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_StationGeolocMeasType_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            // Do not want to match the legacy DMI.
            if ( hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                !hbpanel.getDataStore().getIsLegacyDMI() ) {
                if ( HydroBase_Util.isGroundWaterWellTimeSeriesDataType ( hbdmi, hbMeasType) &&
                    selectedTimeStep.equalsIgnoreCase("Irregular")) {
                    //Message.printStatus(2, routine, "Setting station (groundwater) input filter panel visible.");
                    return panel;
                }
                else if ( HydroBase_Util.isStationTimeSeriesDataType ( hbdmi, hbMeasType) ) {
                    //Message.printStatus(2, routine, "Setting station input filter panel visible.");
                    return panel;
                }
            }
        }
        else if ( panel instanceof HydroBase_GUI_StructureGeolocStructMeasType_InputFilter_JPanel ) {
            // HydroBase structure time series (no SFUT).
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            HydroBase_GUI_StructureGeolocStructMeasType_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_StructureGeolocStructMeasType_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            if ( hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                //Message.printStatus(2, routine, "Panel includSFUT=" + hbpanel.getIncludeSFUT());
                if ( !hbpanel.getIncludeSFUT() && HydroBase_Util.isStructureTimeSeriesDataType ( hbdmi, hbMeasType) &&
                    !HydroBase_Util.isStructureSFUTTimeSeriesDataType ( hbdmi, hbMeasType) ) {
                    // Normal structure time series (not SFUT).
                    //Message.printStatus(2, routine, "Setting structure (no SFUT) input filter panel visible.");
                    return panel;
                }
                else if ( hbpanel.getIncludeSFUT() && HydroBase_Util.isStructureSFUTTimeSeriesDataType ( hbdmi, hbMeasType) ) {
                    // SFUT time series.
                    //Message.printStatus(2, routine, "Setting structure SFUT input filter panel visible.");
                    return panel;
                }
            }
        }
        else if ( panel instanceof HydroBase_GUI_AgriculturalCASSCropStats_InputFilter_JPanel ) {
            // CASS crop time series.
            HydroBase_GUI_AgriculturalCASSCropStats_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_AgriculturalCASSCropStats_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isAgriculturalCASSCropStatsTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                // Message.printStatus(2, routine, "Setting CASS crop stats input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof HydroBase_GUI_AgriculturalCASSLivestockStats_InputFilter_JPanel ) {
            // CASS livestock time series.
            HydroBase_GUI_AgriculturalCASSLivestockStats_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_AgriculturalCASSLivestockStats_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isAgriculturalCASSLivestockStatsTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                // Message.printStatus(2, routine, "Setting CASS livestock stats input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof HydroBase_GUI_CUPopulation_InputFilter_JPanel ) {
            // CU population time series.
            HydroBase_GUI_CUPopulation_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_CUPopulation_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isCUPopulationTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                //Message.printStatus(2, routine, "Setting CU population input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof HydroBase_GUI_AgriculturalNASSCropStats_InputFilter_JPanel ) {
            // NASS time series.
            HydroBase_GUI_AgriculturalNASSCropStats_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_AgriculturalNASSCropStats_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isAgriculturalNASSCropStatsTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI() ) {
                //Message.printStatus(2, routine, "Setting NASS crop stats input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof HydroBase_GUI_StructureIrrigSummaryTS_InputFilter_JPanel ) {
            // Irrig summary time series.
            HydroBase_GUI_StructureIrrigSummaryTS_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_StructureIrrigSummaryTS_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isIrrigSummaryTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                //Message.printStatus(2, routine, "Setting irrig summary input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof HydroBase_GUI_GroundWater_InputFilter_JPanel ) {
            // Groundwater wells time series.
            // Note that irregular data are matched under the station time series above.
            HydroBase_GUI_GroundWater_InputFilter_JPanel hbpanel =
                (HydroBase_GUI_GroundWater_InputFilter_JPanel)panel;
            HydroBaseDMI hbdmi = (HydroBaseDMI)hbpanel.getDataStore().getDMI();
            String [] hb_mt = HydroBase_Util.convertToHydroBaseMeasType( selectedDataType, selectedTimeStep );
            String hbMeasType = hb_mt[0];
            if (hbpanel.getDataStore().getName().equalsIgnoreCase(selectedDataStoreName) &&
                HydroBase_Util.isGroundWaterWellTimeSeriesDataType ( hbdmi, hbMeasType) &&
                !hbpanel.getDataStore().getIsLegacyDMI()) {
                // Message.printStatus(2, routine, "Setting groundwater wells input filter panel visible.");
                return panel;
            }
        }
        else if ( panel instanceof RccAcis_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((RccAcis_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        else if ( panel instanceof ReclamationHDB_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((ReclamationHDB_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        else if ( panel instanceof ReclamationPisces_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((ReclamationPisces_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        // Start USGS NWIS REST datastores.
        else if ( panel instanceof UsgsNwisDaily_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((UsgsNwisDaily_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        else if ( panel instanceof UsgsNwisGroundwater_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((UsgsNwisGroundwater_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        else if ( panel instanceof UsgsNwisInstantaneous_TimeSeries_InputFilter_JPanel ) {
            // This type of filter uses a DataStore.
            DataStore dataStore = ((UsgsNwisInstantaneous_TimeSeries_InputFilter_JPanel)panel).getDataStore();
            if ( dataStore.getName().equalsIgnoreCase(selectedDataStoreName) ) {
                // Have a match in the datastore name so return the panel.
                return panel;
            }
        }
        else {
        	// Figure out if the panel is associated with a plugin datastore.
        	// The panel class is generally specific to the datastore, such as Test1DataStore_TimeSeries_InputFilter_JPanel.
        	DataStore ds = ui_GetSelectedDataStore();
        	if ( (ds != null) && (ds instanceof PluginDataStore) ) {
        		// The panel will have had its name set to:
        		//     ds.getClass().getSimpleName() + "." + ds.getName() + ".InputFilterPanel"
        		if ( panel.getName().equals(ds.getClass().getSimpleName() + "." + ds.getName() + ".InputFilterPanel") ) {
        			return panel;
        		}
        	}
        }
    }
    // Input filter panel does not match the requested datastore.
    return null;
}

/**
Return the input name JComboBox, used for datastore integration.
@return the input name JComboBox.
*/
public SimpleJComboBox ui_GetInputNameJComboBox() {
    return this.__inputName_JComboBox;
}

/**
Return the input type JComboBox, used for datastore integration.
@return the input name JComboBox.
*/
public SimpleJComboBox ui_GetInputTypeJComboBox() {
    return this.__inputType_JComboBox;
}

/**
Return the query input panel;
This used by datastore UI code.
*/
public JPanel ui_GetQueryInputJPanel () {
    return this.__queryInput_JPanel;
}

/**
Return the datastore for the selected datastore name.
If the datastore name is a substitute, return the original datastore to which it refers.
@return the datastore for the selected datastore name, or null if the selected name is blank
(or for some reason is not in the processor - should not happen if data are being kept consistent).
*/
public DataStore ui_GetSelectedDataStore () {
    // TODO smalers 2010-09-02 How to ensure that name is unique until datastores are handled consistently?
    String dataStoreName = this.__dataStore_JComboBox.getSelected();
    if ( Message.isDebugOn ) {
    	Message.printDebug(2, "ui_GetSelectedDataStore", "Getting datastore for selected name \"" +
    		dataStoreName + "\"" );
    }
    if ( (dataStoreName == null) || dataStoreName.equals("") ) {
        // No need to request from processor.
        return null;
    }
    // TODO smalers 2023-02-02 evalaute whether needed.
    //boolean isActive = true;
    // Want to interact with the specified datastore:
    // - do not process substitutes
    // - only return the original datastore when processing commands
    // TODO smalers 2023-02-02 evalaute whether needed.
    //boolean checkSubstitutes = false;
    //return this.__tsProcessor.getDataStoreForName ( dataStoreName, null, isActive, checkSubstitutes );
    return this.__tsProcessor.getDataStoreForName ( dataStoreName, null );
}

/**
Return the selected data type as a short string.
For some input types, data types have additional label-only information
because the types are grouped in the GUI due to the list length.
StateCUB has a lot of types but currently they are not grouped (AND THEY MAY INCLUDE "-" so don't do anything special).
*/
public String ui_GetSelectedDataType () {
    // First set the default for no special handling of data type in GUI.
	// This applies to many of the data types, including DateValue, HEC-DSS, MODSIM, NWSCard, NWSRFS ESP trace ensemble,
    // RiverWare, StateCU, StateCUB, StateMod, StateModB (New - just use data types in files), USGS NWIS
    DataStore selectedDataStore = ui_GetSelectedDataStore();
    String selectedInputType = ui_GetSelectedInputType(); // OK if null or blank.
    String selectedDataTypeFull = ui_GetSelectedDataTypeFull();
    String selectedDataType = selectedDataTypeFull;
    // The displayed data type may not be the actual due to some annotation.
    // Check some specific input types and strip off the labels:
    // - TODO smalers 2022-03-17 need to move this into each datastores code since TSTool should not care
    if ( ((selectedDataStore != null) && ((selectedDataStore instanceof HydroBaseDataStore))) ||
        selectedInputType.equals(TSToolConstants.INPUT_TYPE_HydroBase) || selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateModB) ) {
        // Data type group is first and data type second.
        // HydroBase:  "Climate - Precip"
        // StateModB (old, group the types to help user):  "Water Supply - Total_Supply"
        if ( selectedDataTypeFull.indexOf('-') >= 0 ) {
            selectedDataType = StringUtil.getToken( selectedDataTypeFull, "-", 0, 1).trim();
            int pos = selectedDataType.indexOf(' ');
            if ( pos >= 0 ) {
                // Special case "Well - WellLevel (phasing out)".
                selectedDataType = selectedDataType.substring(0,pos).trim();
            }
        }
    }
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files) ) {
        // Data type is first and explanation second, for example.
        // NWSRFS FS5 Files: "MAP - Mean Areal Precipitation"
        if ( selectedDataTypeFull.indexOf('-') >= 0 ) {
            selectedDataType = StringUtil.getToken( selectedDataTypeFull, "-", 0, 0).trim();
        }
    }
    return selectedDataType;
}

/**
Return the selected data type full string, which may include a note.
*/
private String ui_GetSelectedDataTypeFull () {
    return this.__dataType_JComboBox.getSelected();
}

/**
Return the selected input filter.
@return the selected input filter.
*/
public InputFilter_JPanel ui_GetSelectedInputFilterJPanel() {
    return this.__selectedInputFilter_JPanel;
}

/**
Return the selected input name.
This is the visible name shown in the UI.
If a shortened name is shown, it needs to be looked up from the visible name.
@return the selected input name.
*/
public String ui_GetSelectedInputName() {
    return this.__inputName_JComboBox.getSelected();
}

/**
Return the selected input type.  Use this to ensure that operations are based on the current setting.
*/
public String ui_GetSelectedInputType() {
    return this.__inputType_JComboBox.getSelected();
}

/**
Return the selected time step.
*/
public String ui_GetSelectedTimeStep() {
    return this.__timeStep_JComboBox.getSelected();
}

/**
 * Return the time series catalog table model.
 * This is called by code that populates the time series catalog.
 * @return the time series catalog table model.
 */
public JWorksheet_AbstractRowTableModel ui_GetTimeSeriesCatalogTableModel () {
	return this.__query_TableModel;
}

/**
 * Return the time series catalog worksheet.
 * This is called by code that populates the time series catalog.
 * @return the time series catalog worksheet.
 */
public JWorksheet ui_GetTimeSeriesCatalogWorksheet () {
	return this.__query_JWorksheet;
}

/**
Return the input name JComboBox, used for datastore integration.
@return the time step JComboBox.
*/
public SimpleJComboBox ui_GetTimeStepJComboBox() {
    return this.__timeStep_JComboBox;
}

/**
 * Get the modifier to use for the title, used with --ui-title program option.
 * This string can be appended directly after "TSTool" in the title,
 * for example setTitle ( "Title" + ui_GetTitleMod + " - other text" );
 */
private String ui_GetTitleMod () {
	if ( (this.titleMod == null) || (this.titleMod.length() == 0) ) {
		return "";
	}
	else {
		return " - " + this.titleMod;
	}
}

/**
Initialize the graphical user interface (GUI).
@param initProps initial properties, from TSTool command line
*/
private void ui_InitGUI ( PropList initProps ) {
	String routine = getClass().getSimpleName() + ".ui_InitGUI";
	try {	// To catch layout problems.
	int y;

	try {
	    String propval = TSToolMain.getPropValue("TSTool.UILookAndFeel" );
	    if ( propval != null ) {
	        // Use the look and feel that is in the TSTool configuration file, useful for Linux.
	        try {
	            Message.printStatus(2,routine,"Setting UI look and feel to: " + propval );
	            UIManager.setLookAndFeel(propval);
	        }
	        catch ( Exception e ) {
	            // Default to the system look and feel.
	            JGUIUtil.setSystemLookAndFeel(true);
	        }
	    }
	    else {
	        JGUIUtil.setSystemLookAndFeel(true);
	    }
	}
	catch (Exception e) {
		Message.printWarning ( 2, routine, e );
	}

	// Set the help viewer handler.
	HelpViewer.getInstance().setUrlFormatter(this);

	// TODO smalers 2013-11-16 Old note: need this even if no main GUI (why? secondary windows?).

	JGUIUtil.setIcon(this, JGUIUtil.getIconImage());

	ui_InitGUIMenus ();
    ui_InitToolbar ();

	// Remainder of main window.

	// objects used throughout the GUI layout.
	int buffer = 3;
	Insets insetsNLNR = new Insets(0,buffer,0,buffer);
	Insets insetsNNNR = new Insets(0,0,0,buffer);
	Insets insetsNLNN = new Insets(0,buffer,0,0);
    Insets insetsNLBR = new Insets(0,buffer,buffer,buffer);
	Insets insetsTLNR = new Insets(buffer,buffer,0,buffer);
	Insets insetsNNNN = new Insets(0,0,0,0);
    GridBagLayout gbl = new GridBagLayout();

	// Panel to hold the query components, added to the top of the main content pane.

    JPanel query_JPanel = new JPanel();
    query_JPanel.setLayout(new BorderLayout());
    getContentPane().add("North", query_JPanel);

	// --------------------------------------------------------------------
	// Query input components.
	// --------------------------------------------------------------------

	this.__queryInput_JPanel = new JPanel();
	this.__queryInput_JPanel.setLayout(gbl);
	ui_SetInputPanelTitle (null, Color.black );

    query_JPanel.add("West", this.__queryInput_JPanel);

    y=-1;

    this.__dataStore_JTabbedPane = new JTabbedPane ();
    this.__dataStore_JTabbedPane.setVisible(false); // Let the initializing panel show first.
    JGUIUtil.addComponent(this.__queryInput_JPanel, this.__dataStore_JTabbedPane,
        0, ++y, 2, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);
    // The following will display during startup to wait for datastores to initialize, and will then be set not visible.
    this.__dataStoreInitializing_JPanel = new JPanel();
    this.__dataStoreInitializing_JPanel.setLayout(gbl);
    this.__dataStoreInitializing_JLabel = new JLabel("<html><b>Wait...initializing data connections...</html>");
    JGUIUtil.addComponent(__dataStoreInitializing_JPanel, __dataStoreInitializing_JLabel,
        0, 0, 1, 2, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    // Add at same location and __dataStore_JTabbedPane, which is not visible at start.
    JGUIUtil.addComponent(this.__queryInput_JPanel, this.__dataStoreInitializing_JPanel,
        0, y, 2, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);

    JPanel dataStore_JPanel = new JPanel();
    dataStore_JPanel.setLayout(gbl);
    int yDataStore = -1;
    this.__dataStore_JLabel = new JLabel("Datastore:");
    JGUIUtil.addComponent(dataStore_JPanel, this.__dataStore_JLabel,
        0, ++yDataStore, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__dataStore_JComboBox = new SimpleJComboBox(false);
    this.__dataStore_JComboBox.setMaximumRowCount ( 20 );
    String tooltip = "<html>Configured database and web service datastores - select a datastore OR input type.  See <b><i>View / Datastores</i></b> for status and errors.</html>";
    this.__dataStore_JLabel.setToolTipText(tooltip);
    this.__dataStore_JComboBox.setToolTipText ( tooltip );
    this.__dataStore_JComboBox.addItemListener( this );
    JGUIUtil.addComponent(dataStore_JPanel, this.__dataStore_JComboBox,
        1, yDataStore, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    __dataStore_JTabbedPane.addTab ( "Datastore", dataStore_JPanel );

    JPanel inputType_JPanel = new JPanel();
    inputType_JPanel.setLayout(gbl);
    int yInputType = -1;
    JLabel label = new JLabel("Input type:");
    JGUIUtil.addComponent(inputType_JPanel, label,
		0, ++yInputType, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__inputType_JComboBox = new SimpleJComboBox(false);
    this.__inputType_JComboBox.setMaximumRowCount ( 20 );
    tooltip = "<html>The input type is the file/database format being read - select an input type OR datastore.</html>";
    label.setToolTipText ( tooltip );
    this.__inputType_JComboBox.setToolTipText ( tooltip );
	this.__inputType_JComboBox.addItemListener( this );
        JGUIUtil.addComponent(inputType_JPanel, this.__inputType_JComboBox,
		1, yInputType, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    this.__dataStore_JTabbedPane.addTab ( "Input type", inputType_JPanel );

    this.__inputName_JLabel = new JLabel("Input name:" );
    JGUIUtil.addComponent(inputType_JPanel, this.__inputName_JLabel,
		0, ++yInputType, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__inputName_JComboBox = new SimpleJComboBox(false);
    this.__inputName_JComboBox.setMaximumRowCount ( 20 );
    // Set a blank entry to work with datastore handling.
    this.__inputName_JComboBox.add ( "" );
    tooltip = "<html>The input name is the name of the file or database" +
    " being read.<br>It will default or be prompted for after selecting the input type.</html>";
    label.setToolTipText ( tooltip );
    this.__inputName_JComboBox.setToolTipText ( tooltip );
	this.__inputName_JComboBox.addItemListener( this );
        JGUIUtil.addComponent(inputType_JPanel, this.__inputName_JComboBox,
		1, yInputType, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);

    label = new JLabel("Data type:");
    JGUIUtil.addComponent(this.__queryInput_JPanel, label,
		0, ++y, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
	this.__dataType_JComboBox = new SimpleJComboBox(false);
    this.__dataType_JComboBox.setMaximumRowCount ( 20 );
    tooltip = "<html>The data type is used to filter the list of time series.</html>";
    label.setToolTipText ( tooltip );
	this.__dataType_JComboBox.setToolTipText ( tooltip );
	this.__dataType_JComboBox.addItemListener( this );
    JGUIUtil.addComponent(this.__queryInput_JPanel, this.__dataType_JComboBox,
		1, y++, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);

    label = new JLabel("Time step:");
    JGUIUtil.addComponent(this.__queryInput_JPanel, label,
		0, y, 1, 1, 0.0, 0.0, insetsNLNN, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__timeStep_JComboBox = new SimpleJComboBox(false);
    tooltip = "<html>The time step is used to filter the list of time series.</html>";
    label.setToolTipText ( tooltip );
	this.__timeStep_JComboBox.setToolTipText ( tooltip );
	this.__timeStep_JComboBox.addItemListener( this );
    JGUIUtil.addComponent(this.__queryInput_JPanel, this.__timeStep_JComboBox,
		1, y++, 2, 1, 1.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.WEST);

	// Save the position for the input filters, which will be added after database connections are made.

	this.__inputFilterY = y;
	++y;	// Increment for GUI features below.

	// Force the choices to assume some reasonable values.

	ui_SetInputTypeChoices();

    this.__get_ts_list_JButton = new SimpleJButton(TSToolConstants.BUTTON_TOP_GET_TIME_SERIES,this);
	this.__get_ts_list_JButton.setToolTipText (
		"<html>Get a list of time series but not the full time " +
		"series data.<br>Time series can then be selected for processing.</html>" );
    JGUIUtil.addComponent(__queryInput_JPanel, this.__get_ts_list_JButton,
		2, y++, 1, 1, 0, 0, insetsTLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);

	// --------------------------------------------------------------------
	// Query results components.
	// --------------------------------------------------------------------

	this.__query_results_JPanel = new JPanel();
    this.__query_results_JPanel.setLayout(gbl);
	this.__query_results_JPanel.setBorder(
		BorderFactory.createTitledBorder (BorderFactory.createLineBorder(Color.black),"Time Series List"));

    // Set the minimum size for the panel based on the default size
    // used for HydroBase, which seems to be an acceptable size.
    this.__query_results_JPanel.setPreferredSize(new Dimension( 460, 200 ));

    query_JPanel.add("Center", this.__query_results_JPanel);

	// Add the table for time series list:
    // - the worksheet is only created once and is cleared out and repopulated as necessary,
    //   which ensures that UI setup and refresh issues are minimized in other components

	y = 0;
	try {
    	PropList props = new PropList ( "QueryList" );
    	props.add("JWorksheet.ShowRowHeader=true");
    	props.add("JWorksheet.AllowCopy=true");
    	JScrollWorksheet sjw = new JScrollWorksheet ( 0, 0, props );
    	this.__query_JWorksheet = sjw.getJWorksheet ();
    	this.__query_JWorksheet.setPreferredScrollableViewportSize(null);
    	// Listen for mouse events to enable the buttons in the Time Series area.
    	this.__query_JWorksheet.addMouseListener ( this );
    	this.__query_JWorksheet.addJWorksheetListener ( this );
        JGUIUtil.addComponent(this.__query_results_JPanel, sjw,
		0, y++, 3, 7, 1.0, 1.0, insetsNLBR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
	}
	catch ( Exception e ) {
		// Absorb the exception in most cases - print if developing to see if this issue can be resolved.
		if ( Message.isDebugOn && IOUtil.testing()  ) {
			Message.printWarning ( 3, routine, "For developers:  caught exception initializing time series list JWorksheet at setup." );
			Message.printWarning ( 3, routine, e );
		}
	}

	// Add the button to select all the time series.

	y = 7;
    this.__CopySelectedToCommands_JButton = new SimpleJButton( TSToolConstants.BUTTON_TOP_COPY_SELECTED_TO_COMMANDS,this);
	this.__CopySelectedToCommands_JButton.setToolTipText (
		"<html>Copy selected time series from above to the Commands list as time series identifiers.<br/>" +
		"Insert AFTER last selected command or at end if no commands are selected.</html>" );
    JGUIUtil.addComponent ( __query_results_JPanel,	this.__CopySelectedToCommands_JButton,
		1, y, 1, 1, 0.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.EAST );
    this.__CopyAllToCommands_JButton = new SimpleJButton( TSToolConstants.BUTTON_TOP_COPY_ALL_TO_COMMANDS,this);
	this.__CopyAllToCommands_JButton.setToolTipText (
		"<html>Copy all time series from above to the Commands list as time series identifiers.<br />" +
		"Insert AFTER last selected command or at end if no commands are selected.</html>" );
    JGUIUtil.addComponent ( this.__query_results_JPanel, this.__CopyAllToCommands_JButton,
		2, y, 1, 1, 0.0, 0.0, insetsNNNR, GridBagConstraints.NONE, GridBagConstraints.EAST );

	// --------------------------------------------------------------------
	// Command components.
	// --------------------------------------------------------------------

	// Use a panel to include both the commands and time series panels and place in the center, to allow resizing.

	JPanel center_JPanel = new JPanel ();
    center_JPanel.setLayout(gbl);
    getContentPane().add("Center", center_JPanel);

    // Commands JPanel - 8 columns wide for grid bag layout.
    this.__commands_JPanel = new JPanel();
    this.__commands_JPanel.setLayout(gbl);
	this.__commands_JPanel.setBorder(
		BorderFactory.createTitledBorder ( BorderFactory.createLineBorder(Color.black), "Commands" ));
	JGUIUtil.addComponent(center_JPanel, this.__commands_JPanel,
		0, 0, 1, 1, 1.0, 1.0, insetsNNNN, GridBagConstraints.BOTH, GridBagConstraints.CENTER);

	// Initialize the command processor to interact with the GUI.
	// The initial working directory will be the software startup directory.
	this.__tsProcessor = new TSCommandProcessor( initProps );
	ui_SetInitialWorkingDir( System.getProperty("user.dir") );
	commandProcessor_SetInitialWorkingDir ( ui_GetInitialWorkingDir(), true );
	// FIXME smalers 2007-08-28 Need to set a WindowListener for -nomaingui calls?
	//__ts_processor.setTSCommandProcessorUI ( this );
	this.__tsProcessor.addCommandProcessorListener ( this );
	this.__commands_JListModel = new TSCommandProcessorListModel(this.__tsProcessor);
	this.__commands_JListModel.addListDataListener ( this );

	// The following provides indicators of problems:
	// - change to the command list (via change to the command processor) will update the AnnotatedCommandList
	this.__commands_AnnotatedCommandJList = new AnnotatedCommandJList ( this.__commands_JListModel );
	JList command_JList = this.__commands_AnnotatedCommandJList.getJList();
	// Set the font to fixed font so that similar command text lines up, especially for comments.
    // This looks like crap on Linux. Try using Lucida Console on windows and Linux to get some feedback.
    if ( IOUtil.isUNIXMachine() ) {
        command_JList.setFont ( new Font(TSToolConstants.COMMANDS_FONT, Font.PLAIN, 12 ) );
    }
    else {
        // __commands_JList.setFont ( new Font("Courier", Font.PLAIN, 11 ) );
        command_JList.setFont ( new Font(TSToolConstants.COMMANDS_FONT, Font.PLAIN, 12 ) );
    }
	// Handling the ellipsis is dealt with in the annotated list.

	// Listen for events on the list so the GUI can respond to selections.

	command_JList.addListSelectionListener ( this );
	command_JList.addKeyListener ( this );
	command_JList.addMouseListener ( this );

	JGUIUtil.addComponent(this.__commands_JPanel, this.__commands_AnnotatedCommandJList,
		0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);

	// Popup menu for the commands list.

	ui_InitGUIMenus_CommandsPopup ();

	// Popup menu for the input name field.
	this.__input_name_JPopupMenu = new JPopupMenu("Input Name Actions");

	// Buttons that correspond to the command list.

	// Put on left because user is typically working in that area.
	this.__Run_SelectedCommands_JButton =
		new SimpleJButton(TSToolConstants.Button_RunSelectedCommands_String, TSToolConstants.Run_SelectedCommandsCreateOutput_String, this);
	this.__Run_SelectedCommands_JButton.setToolTipText (
		"<html>Run selected commands from above to generate time series and other results," +
		"<br>which will be shown in the Results tabs below.</html>" );
	JGUIUtil.addComponent(__commands_JPanel, __Run_SelectedCommands_JButton,
		5, 5, 1, 1, 0.0, 0.0, insetsTLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);
	this.__Run_AllCommands_JButton =
		new SimpleJButton(TSToolConstants.Button_RunAllCommands_String, TSToolConstants.Run_AllCommandsCreateOutput_String, this);
	__Run_AllCommands_JButton.setToolTipText (
		"<html>Run all commands from above to generate time series and other results," +
		"<br>which will be shown in the Results tabs below.</html>" );
	JGUIUtil.addComponent(this.__commands_JPanel, this.__Run_AllCommands_JButton,
		6, 5, 1, 1, 0.0, 0.0, insetsTLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);
	// Put on right because we want it to be a decision to clear.
	this.__ClearCommands_JButton = new SimpleJButton(TSToolConstants.Button_ClearCommands_String, this);
	this.__ClearCommands_JButton.setToolTipText (
		"<html>Clear selected commands from above.<br>Clear all commands if none are selected.</html>" );
	JGUIUtil.addComponent(this.__commands_JPanel, this.__ClearCommands_JButton,
		7, 5, 1, 1, 0.0, 0.0, insetsTLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);

	// --------------------------------------------------------------------
	// Results components (listed alphabetically by label).
	// --------------------------------------------------------------------

    this.__results_JTabbedPane = new JTabbedPane ();
    this.__results_JTabbedPane.setBorder(
            BorderFactory.createTitledBorder ( BorderFactory.createLineBorder(Color.black), "Results" ));
    JGUIUtil.addComponent(center_JPanel, this.__results_JTabbedPane,
            0, 1, 1, 1, 1.0, 1.0, insetsNNNN, GridBagConstraints.BOTH, GridBagConstraints.CENTER);

    // Results: Ensembles.

    this.__resultsTSEnsembles_JPanel = new JPanel();
    this.__resultsTSEnsembles_JPanel.setLayout(gbl);
    /*
    __results_tsensembles_JPanel.setBorder(
        BorderFactory.createTitledBorder (
        BorderFactory.createLineBorder(Color.black),
        "Results: Ensembles of Time Series" ));
        */
    this.__resultsTSEnsembles_JListModel = new DefaultListModel<String>();
    this.__resultsTSEnsembles_JList = new JList<> ( this.__resultsTSEnsembles_JListModel );
    this.__resultsTSEnsembles_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    this.__resultsTSEnsembles_JList.addKeyListener ( this );
    this.__resultsTSEnsembles_JList.addListSelectionListener ( this );
    this.__resultsTSEnsembles_JList.addMouseListener ( this );
    JScrollPane results_tsensembles_JScrollPane = new JScrollPane ( __resultsTSEnsembles_JList );
    JGUIUtil.addComponent(this.__resultsTSEnsembles_JPanel, results_tsensembles_JScrollPane,
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Ensembles", this.__resultsTSEnsembles_JPanel );

    // Row at the bottom includes actions that can be taken on the time series list,
    // in particular the graph templates
	this.__resultsTSEnsemblesGraphTemplates_JButton = new SimpleJButton("Graph with template:",
            "GraphTSEnsembleWithTemplate",
            "Select a graph template to use to graph the selected time series ensemble.",
            insetsNLNR, false, this);
	JGUIUtil.addComponent(this.__resultsTSEnsembles_JPanel, new JLabel(""), // Use to fill space.
		0, 5, 1, 1, 1.0, 0.0, insetsNLNR, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);
	this.__resultsTSEnsemblesGraphTemplates_JButton.setEnabled(false); // Disable until command processed and >0 time series ensembles available.
	JGUIUtil.addComponent(this.__resultsTSEnsembles_JPanel, this.__resultsTSEnsemblesGraphTemplates_JButton,
		6, 5, 1, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);
	this.__resultsTSEnsemblesGraphTemplates_JComboBox = new SimpleJComboBox(false);
	List<File> templateFileList = this.session.getGraphTemplateFileList();
	List<String> templateFileList2 = new ArrayList<>();
	for ( File f : templateFileList ) {
		templateFileList2.add(f.getName());
	}
	this.__resultsTSEnsemblesGraphTemplates_JComboBox.setMaximumRowCount ( 20 );
	this.__resultsTSEnsemblesGraphTemplates_JComboBox.setData(templateFileList2);
	// Select graph template from the UI state.
	String uiStateEnsembleGraphTemplate = this.session.getUIStateProperty("Results.Ensembles.GraphTemplate");
	try {
		this.__resultsTSEnsemblesGraphTemplates_JComboBox.select(uiStateEnsembleGraphTemplate);
	}
	catch ( Exception e ) {
		// OK - previous state no longer a valid template so leave default selection.
	}
	this.__resultsTSEnsemblesGraphTemplates_JComboBox.addItemListener( this );
	JGUIUtil.addComponent(__resultsTSEnsembles_JPanel, this.__resultsTSEnsemblesGraphTemplates_JComboBox,
		7, 5, 1, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
	this.__resultsTSEnsemblesGraphTemplates_JComboBox.setEnabled(false); // Disable until command processed and >0 time series available.

    // Results: networks.

    JPanel results_networks_JPanel = new JPanel();
    results_networks_JPanel.setLayout(gbl);
    JGUIUtil.addComponent(results_networks_JPanel, new JLabel ("Networks:"),
        0, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__resultsNetworks_JListModel = new DefaultListModel<>();
    this.__resultsNetworks_JList = new JList<> ( this.__resultsNetworks_JListModel );
    this.__resultsNetworks_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    this.__resultsNetworks_JList.addKeyListener ( this );
    this.__resultsNetworks_JList.addListSelectionListener ( this );
    this.__resultsNetworks_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_networks_JPanel, new JScrollPane ( this.__resultsNetworks_JList ),
        0, 15, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Networks", results_networks_JPanel );

    // Results: objects.

    JPanel results_objects_JPanel = new JPanel();
    results_objects_JPanel.setLayout(gbl);
    JGUIUtil.addComponent(results_objects_JPanel, new JLabel ("Objects:"),
        0, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__resultsObjects_JListModel = new DefaultListModel<>();
    this.__resultsObjects_JList = new JList<> ( this.__resultsObjects_JListModel );
    this.__resultsObjects_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    this.__resultsObjects_JList.addKeyListener ( this );
    this.__resultsObjects_JList.addListSelectionListener ( this );
    this.__resultsObjects_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_objects_JPanel, new JScrollPane ( this.__resultsObjects_JList ),
        0, 15, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Objects", results_objects_JPanel );

    // Results: output files.

    JPanel results_files_JPanel = new JPanel();
    results_files_JPanel.setLayout(gbl);
    JGUIUtil.addComponent(center_JPanel, results_files_JPanel,
        0, 3, 1, 1, 1.0, 0.0, insetsNNNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
    this.__resultsOutputFiles_JLabel = new JLabel ( "Output files:");
    JGUIUtil.addComponent(results_files_JPanel, this.__resultsOutputFiles_JLabel,
        0, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__resultsOutputFiles_JListModel = new DefaultListModel<>();
    this.__resultsOutputFiles_JList = new JList<String> ( this.__resultsOutputFiles_JListModel );
    this.__resultsOutputFiles_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    this.__resultsOutputFiles_JList.addKeyListener ( this );
    this.__resultsOutputFiles_JList.addListSelectionListener ( this );
    this.__resultsOutputFiles_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_files_JPanel, new JScrollPane ( this.__resultsOutputFiles_JList ),
        0, 15, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Output Files", results_files_JPanel );

    // Results - problems.

    JPanel results_problems_JPanel = new JPanel();
    results_problems_JPanel.setLayout(gbl);
    CommandLog_TableModel tableModel = null;
    try {
        tableModel = new CommandLog_TableModel(new Vector<>());
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
    this.__resultsProblems_JWorksheet = sjw.getJWorksheet ();
    this.__resultsProblems_JWorksheet.setColumnWidths (cellRenderer.getColumnWidths(), getGraphics() );
    this.__resultsProblems_JWorksheet.setPreferredScrollableViewportSize(null);
    // Listen for mouse events to ?
    //__problems_JWorksheet.addMouseListener ( this );
    //__problems_JWorksheet.addJWorksheetListener ( this );
    // TODO smalers 2015-07-09 Need the worksheet to fill the panel.
    JGUIUtil.addComponent(results_problems_JPanel, sjw,
        0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Problems", results_problems_JPanel );

    // Results - properties.

    JPanel resultsProperties_JPanel = new JPanel();
    resultsProperties_JPanel.setLayout(gbl);
    PropList_TableModel propsTableModel = null;
    try {
        propsTableModel = new PropList_TableModel(new PropList("processor"),false,false);
        propsTableModel.setKeyColumnName("Property Name");
        propsTableModel.setTypeColumnName("Property Type");
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
    this.__resultsProperties_JWorksheet = psjw.getJWorksheet ();
    this.__resultsProperties_JWorksheet.setColumnWidths (cellRenderer.getColumnWidths(), getGraphics() );
    this.__resultsProperties_JWorksheet.setPreferredScrollableViewportSize(null);
    // Listen for mouse events to ?
    //__problems_JWorksheet.addMouseListener ( this );
    //__problems_JWorksheet.addJWorksheetListener ( this );
    JGUIUtil.addComponent(resultsProperties_JPanel, new JLabel("Processor properties control processing and can be used in " +
        "some command parameters using ${Property} notation (see command documentation)."),
        0, 0, 8, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
    JGUIUtil.addComponent(resultsProperties_JPanel, psjw,
        0, 1, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Properties", resultsProperties_JPanel );

    // Results: tables.

    JPanel results_tables_JPanel = new JPanel();
    results_tables_JPanel.setLayout(gbl);
	this.__resultsTables_JLabel = new JLabel ("Tables:");
    JGUIUtil.addComponent(results_tables_JPanel, this.__resultsTables_JLabel,
        0, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.EAST);
    this.__resultsTables_JListModel = new DefaultListModel<>();
    this.__resultsTables_JList = new JList<> ( this.__resultsTables_JListModel );
    this.__resultsTables_JList.setSelectionMode ( ListSelectionModel.SINGLE_SELECTION );
    this.__resultsTables_JList.addKeyListener ( this );
    this.__resultsTables_JList.addListSelectionListener ( this );
    this.__resultsTables_JList.addMouseListener ( this );
    JGUIUtil.addComponent(results_tables_JPanel, new JScrollPane ( this.__resultsTables_JList ),
        0, 15, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Tables", results_tables_JPanel );

	// Results: time series.

    this.__resultsTS_JPanel = new JPanel();
    this.__resultsTS_JPanel.setLayout(gbl);
    // Most of the space is occupied by the list of time series.
    this.__results_JTabbedPane.addTab ( "Time Series", __resultsTS_JPanel );
	this.__resultsTS_JListModel = new DefaultListModel<>();
	this.__resultsTS_JList = new JList<> ( __resultsTS_JListModel );
	this.__resultsTS_JList.addKeyListener ( this );
	this.__resultsTS_JList.addListSelectionListener ( this );
	this.__resultsTS_JList.addMouseListener ( this );
	JScrollPane results_ts_JScrollPane = new JScrollPane ( __resultsTS_JList );
	// The following is 8 units wide and 5 high (y=0 to 4).
	JGUIUtil.addComponent(this.__resultsTS_JPanel, results_ts_JScrollPane,
		0, 0, 8, 5, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    // Row at the bottom includes actions that can be taken on the time series list, in particular the graph templates.
	this.__resultsTSGraphTemplates_JButton = new SimpleJButton("Graph with template:",
            "GraphTSWithTemplate",
            "Select a graph template to use to graph the selected time series.",
            insetsNLNR, false, this);
	JGUIUtil.addComponent(this.__resultsTS_JPanel, new JLabel(""), // Use to fill space.
		0, 5, 1, 1, 1.0, 0.0, insetsNLNR, GridBagConstraints.HORIZONTAL, GridBagConstraints.EAST);
	this.__resultsTSGraphTemplates_JButton.setEnabled(false); // Disable until command processed and >0 time series available.
	JGUIUtil.addComponent(this.__resultsTS_JPanel, this.__resultsTSGraphTemplates_JButton,
		6, 5, 1, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.EAST);
	this.__resultsTSGraphTemplates_JComboBox = new SimpleJComboBox(false);
	templateFileList = this.session.getGraphTemplateFileList();
	templateFileList2 = new ArrayList<>();
	for ( File f : templateFileList ) {
		templateFileList2.add(f.getName());
	}
	this.__resultsTSGraphTemplates_JComboBox.setMaximumRowCount ( 20 );
	this.__resultsTSGraphTemplates_JComboBox.setData(templateFileList2);
	// Select graph template from the UI state.
	String uiStateTSGraphTemplate = this.session.getUIStateProperty("Results.TimeSeries.GraphTemplate");
	try {
		this.__resultsTSGraphTemplates_JComboBox.select(uiStateTSGraphTemplate);
	}
	catch ( Exception e ) {
		// OK - previous state no longer a valid template so leave default selection.
	}
	this.__resultsTSGraphTemplates_JComboBox.addItemListener( this );
	JGUIUtil.addComponent(this.__resultsTS_JPanel, this.__resultsTSGraphTemplates_JComboBox,
		7, 5, 1, 1, 0.0, 0.0, insetsNLNR, GridBagConstraints.NONE, GridBagConstraints.WEST);
	this.__resultsTSGraphTemplates_JComboBox.setEnabled(false); // Disable until command processed and >0 time series available.

    // Results: views.

    this.__resultsViews_JPanel = new JPanel();
    this.__resultsViews_JPanel.setLayout(gbl);
    JGUIUtil.addComponent(center_JPanel, this.__resultsViews_JPanel,
        0, 3, 1, 1, 1.0, 0.0, insetsNNNN, GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER);
    this.__resultsViews_JTabbedPane = new JTabbedPane();
    JGUIUtil.addComponent(this.__resultsViews_JPanel, this.__resultsViews_JTabbedPane,
        0, 0, 1, 1, 1.0, 1.0, insetsNLNR, GridBagConstraints.BOTH, GridBagConstraints.WEST);
    this.__results_JTabbedPane.addTab ( "Views", this.__resultsViews_JPanel );

    // Default to time series selected since that is what most people have seen with previous TSTool versions.

    this.__results_JTabbedPane.setSelectedComponent ( this.__resultsTS_JPanel );

	// Popup menu for the time series, tables, and other results lists.
	ui_InitGUIMenus_ResultsPopup ();

	// --------------------------------------------------------------------
	// Status messages.
	// --------------------------------------------------------------------

	// Bottom panel for the information TextFields.
	// Add this as the south panel of the main interface since it is not resizable.

	JPanel bottom_JPanel = new JPanel();
	bottom_JPanel.setLayout (gbl);

	this.__message_JTextField = new JTextField();
	this.__message_JTextField.setEditable(false);
	JGUIUtil.addComponent(bottom_JPanel, this.__message_JTextField,
		0, 0, 5, 1, 1.0, 0.0, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST);
	this.__processor_JProgressBar = new JProgressBar ();
	this.__processor_JProgressBar.setToolTipText ( "Indicates progress in processing all commands.");
	this.__processor_JProgressBar.setStringPainted ( true );
	JGUIUtil.addComponent(bottom_JPanel, this.__processor_JProgressBar,
		5, 0, 2, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
	this.__command_JProgressBar = new JProgressBar ();
	this.__command_JProgressBar.setToolTipText ( "Indicates progress in processing the current command that is running.");
	this.__command_JProgressBar.setStringPainted ( true );
	JGUIUtil.addComponent(bottom_JPanel, this.__command_JProgressBar,
		7, 0, 2, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);
	this.__status_JTextField = new JTextField ( 7 );
	this.__status_JTextField.setEditable(false);
	JGUIUtil.addComponent(bottom_JPanel, this.__status_JTextField,
		9, 0, 1, 1, 0.0, 0.0, GridBagConstraints.NONE, GridBagConstraints.WEST);

	getContentPane().add ("South", bottom_JPanel);

	ui_UpdateStatusTextFields ( -1, "TSTool_JFrame.initGUI",
			null, "Open a command file or add new commands.",
			TSToolConstants.STATUS_READY );
	ui_UpdateStatus ( false );
	// Set the initial window size to 2/3 of the screen:
	// - TODO smalers 2019-07-12 need to remember this in the UIState file
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    int screenWidth = (int)screenSize.getWidth();
    int screenHeight = (int)screenSize.getHeight();
    if ( Message.isDebugOn ) {
    	Message.printStatus(2, routine, "Screen size is " + screenWidth + "x" + screenHeight);
    }
    // Size the screen to be at least 900x750 (legacy value), up to 2/3 of screen size.
    int tstoolWidth = screenWidth*2/3;
    int tstoolHeight = screenHeight*2/3;
    if ( tstoolWidth < 900 ) {
    	// Increase to size that has been used historically.
    	tstoolWidth = 900;
    }
    if ( tstoolHeight < 750 ) {
    	// Increase to size that has been used historically.
    	tstoolHeight = 750;
    }
    if ( Message.isDebugOn ) {
    	Message.printStatus(2, routine, "TSTool size is " + tstoolWidth + "x" + tstoolHeight);
    }
	setPreferredSize ( new Dimension(tstoolWidth, tstoolHeight) );
    pack();
    //this.setLocationRelativeTo(null);
	JGUIUtil.center ( this );
	// TODO smalers 2008-01-11 Need to evaluate whether server mode controls the GUI or only a command processor.
	if ( !TSToolMain.isRestServer() ) {
       	setVisible ( true );
	}
	}
	catch ( Exception e ) {
	    Message.printWarning ( 2, routine, "Error initializing UI (" + e + ")." );
		Message.printWarning ( 2, routine, e );
	}
	this.__guiInitialized = true;
	// Select an input type to get the UI to a usable initial state.
	if ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() != null ) {
		// Select HydroBase for CDSS use.
		this.__inputType_JComboBox.select( null );
		this.__inputType_JComboBox.select( TSToolConstants.INPUT_TYPE_HydroBase );
		// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
		this.__dataStore_JTabbedPane.setSelectedIndex(0);
	}
	else {
		// Select DateValue, which is a simple general file format.
        this.__inputType_JComboBox.select( null );
		this.__inputType_JComboBox.select( TSToolConstants.INPUT_TYPE_DateValue );
		// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
		this.__dataStore_JTabbedPane.setSelectedIndex(0);
	}
}

/**
Initialize the input filters.
An input filter is defined and added for each enabled input type but only one is set visible at a time.
Later, as an input type is selected, the appropriate input filter is made visible.
This method is called at GUI startup.  Individual helper methods can be called as necessary to reset the
filters for a specific input time (e.g., when File...Open...HydroBase is used).
@param y layout position to add the input filters.
*/
private void ui_InitGUIInputFilters ( final int y ) {
	// Define and add specific input filters.
	String routine = getClass().getSimpleName() + ".ui_InitGUIInputFilters";
    Message.printStatus ( 2, routine, "Initializing input filters." );

    // Local reference that can be used in the calls below because "this" conflicts with Runnable instance.
    TSTool_JFrame ui = this;
    Runnable r = new Runnable() {
        public void run() {
        	// Encapsulated environment so need to reinitialize some data.
        	String routine = "TSTool_JFrame.ui_InitGUIInputFilters";
        	// TODO smalers 2012-09-27 Want user to see something to cause them to wait while input filters are initialized,
        	// but this does not seem to do anything.
            ui_SetInputPanelTitle ("Initializing Input/Query Options...", Color.red );
        	int buffer = 3;
        	Insets insets = new Insets(0,buffer,0,0);
        	// Remove all the current input filters.
        	// Remove from the layout.
        	for ( int i = 0; i < __inputFilterJPanelList.size(); i++ ) {
                __queryInput_JPanel.remove( (Component)__inputFilterJPanelList.get(i));
        	}
        	// Remove from the list of filter panels.
        	__inputFilterJPanelList.clear();
        	// Now add the input filters for input types that are enabled, all on top of each other.
        	// Will set visible the one that is appropriate for the selections.
            if ( __source_ColoradoHydroBaseRest_enabled &&
                (__tsProcessor.getDataStoresByType(ColoradoHydroBaseRestDataStore.class).size() > 0) ) {
                try {
                    TSTool_HydroBaseRest.getInstance(ui).initGUIInputFilters(
                        __tsProcessor.getDataStoresByType(ColoradoHydroBaseRestDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the web service cannot initialize.
                    Message.printWarning(1, routine, "Error initializing ColoradoHydroBaseRest input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __tsProcessor.getDataStoresByType(GenericDatabaseDataStore.class).size() > 0 ) {
                try {
                    TSTool_Generic.getInstance(ui).initGUIInputFilters(__tsProcessor.getDataStoresByType(GenericDatabaseDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing GenericDatabaseDataStore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_HECDSS_enabled ) {
                // Add input filters for HEC-DSS files.
                TSTool_HecDss.getInstance(ui).initGUIInputFilters(insets, y);
            }
        	if ( __source_HydroBase_enabled && (TSTool_HydroBase.getInstance(ui).getHydroBaseDataStoreLegacy() != null) ) {
        	    try {
        	        TSTool_HydroBase.getInstance(ui).initGUIInputFiltersLegacy(TSTool_HydroBase.getInstance(ui).getHydroBaseDataStoreLegacy(), y );
        	    }
                catch ( Throwable e ) {
                    // This may happen if the web service static code cannot initialize.
                	// Just catch and let a blank panel be used for input filters.
                    Message.printWarning(3, routine, "Error initializing legacy HydroBase input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
        	}
            if ( __source_HydroBase_enabled && (__tsProcessor.getDataStoresByType(HydroBaseDataStore.class).size() > 0) ) {
                try {
                    TSTool_HydroBase.getInstance(ui).initGUIInputFilters(__tsProcessor.getDataStoresByType(HydroBaseDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing HydroBase datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
         	if ( __source_NWSRFS_FS5Files_enabled ) {
        		// Add input filters for NWSRFS FS5 files.
        		try {
        	        TSTool_FS5Files.getInstance(ui).initGUIInputFiltersLegacy(__queryInput_JPanel, __inputFilterJPanelList, insets, y);
        		}
        		catch ( Throwable e ) {
        			Message.printWarning ( 2, routine, "Unable to initialize input filter for NWSRFS FS5Files.");
        			Message.printWarning ( 2, routine, e );
        		}
        	}
            if ( __source_RCCACIS_enabled && (__tsProcessor.getDataStoresByType(RccAcisDataStore.class).size() > 0) ) {
                try {
                	TSTool_RccAcis.getInstance(ui).initGUIInputFilters ( __tsProcessor.getDataStoresByType(RccAcisDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing RCC ACIS datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_ReclamationHDB_enabled && (__tsProcessor.getDataStoresByType(ReclamationHDBDataStore.class).size() > 0) ) {
                try {
                    TSTool_HDB.getInstance(ui).initGUIInputFilters(__tsProcessor.getDataStoresByType(ReclamationHDBDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing Reclamation HDB datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_ReclamationPisces_enabled && (__tsProcessor.getDataStoresByType(ReclamationPiscesDataStore.class).size() > 0) ) {
                try {
                    TSTool_Pisces.getInstance(ui).initGUIInputFilters(__tsProcessor.getDataStoresByType(ReclamationPiscesDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing Reclamation Pisces datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_UsgsNwisDaily_enabled && (__tsProcessor.getDataStoresByType(UsgsNwisDailyDataStore.class).size() > 0) ) {
                try {
                    TSTool_UsgsNwis.getInstance(ui).initGUIInputFiltersUsgsNwisDaily(
                        __tsProcessor.getDataStoresByType(UsgsNwisDailyDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing USGS NWIS daily datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_UsgsNwisGroundwater_enabled && (__tsProcessor.getDataStoresByType(UsgsNwisGroundwaterDataStore.class).size() > 0) ) {
                try {
                    TSTool_UsgsNwis.getInstance(ui).initGUIInputFiltersUsgsNwisGroundwater(
                        __tsProcessor.getDataStoresByType(UsgsNwisGroundwaterDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing USGS NWIS groundwater datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            if ( __source_UsgsNwisInstantaneous_enabled && (__tsProcessor.getDataStoresByType(UsgsNwisInstantaneousDataStore.class).size() > 0) ) {
                try {
                    TSTool_UsgsNwis.getInstance(ui).initGUIInputFiltersUsgsNwisInstantaneous(
                        __tsProcessor.getDataStoresByType(UsgsNwisInstantaneousDataStore.class), y );
                }
                catch ( Throwable e ) {
                    // This may happen if the database is unavailable or inconsistent with expected design.
                    Message.printWarning(3, routine, "Error initializing USGS NWIS instantaneous datastore input filters (" + e + ").");
                    Message.printWarning(3, routine, e);
                }
            }
            // Loop through all the plug-in datastores and initialize input filters if they provide.
            for ( DataStore ds : __tsProcessor.getDataStores() ) {
            	if ( ds == null ) {
            		continue;
            	}
            	else if ( ds instanceof PluginDataStore ) {
            		PluginDataStore pds = (PluginDataStore)ds;
            		if ( pds.providesTimeSeriesListInputFilterPanel() ) {
            			// Plugin provides an input filter panel.
            			try {
            				TSTool_Plugin.getInstance(ui).initGUIInputFilters ( pds, __queryInput_JPanel, __inputFilterJPanelList, insets, y);
            			}
            			catch ( Throwable e ) {
                            // This may happen if the database is unavailable or inconsistent with expected design.
                            Message.printWarning(3, routine, "Error initializing " + ds.getName() + " plugin datastore input filters (" + e + ").");
                            Message.printWarning(3, routine, e);
            			}
            		}
            	}
            }

            // For troubleshooting, list out the input filters that have been initialized.
            if ( Message.isDebugOn ) {
            	for ( InputFilter_JPanel panel: __inputFilterJPanelList ) {
                	Message.printStatus(2, routine, "After initialization have input filter panel:  " + panel.getName() );
            	}
            }

        	// Always add a generic input filter JPanel that is shared by input
        	// types that do not have filter capabilities and when database connections are not set up.
            // Note that this is not associated only with GenericDatabaseDataStore.

           	JGUIUtil.addComponent(__queryInput_JPanel, __inputFilterGeneric_JPanel = new InputFilter_JPanel (),
    			0, y, 3, 1, 1.0, 0.0, insets, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST );
        	__inputFilterGeneric_JPanel.setToolTipText ( "The selected input type does not support input filters." );
        	__inputFilterGeneric_JPanel.setName( "GenericDefault.InputFilterPanel" );
        	__inputFilterJPanelList.add ( __inputFilterGeneric_JPanel );

            // Always add a message input filter JPanel that can be used to display a message,
        	// such as an instruction that a database connection is not available.

            JGUIUtil.addComponent(__queryInput_JPanel, __inputFilterMessage_JPanel = new InputFilter_JPanel (""),
                0, y, 3, 1, 1.0, 0.0, insets, GridBagConstraints.HORIZONTAL, GridBagConstraints.WEST );
            __inputFilterMessage_JPanel.setName ( "Message.InputFilterPanel" );
            __inputFilterJPanelList.add ( __inputFilterMessage_JPanel );

        	// The appropriate JPanel will be set visible later based on the input type that is selected.
        	// Because a component is added to the original GUI, need to refresh the GUI layout.
        	ui_SetInputFilterForSelections();
            ui_SetInputPanelTitle (null, Color.black );
            ui_ClearDataStoreInitializing();
            __dataStore_JTabbedPane.setVisible(true); // This should now be visible.
        	validate();
        	repaint();
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
Initialize the GUI menus.
*/
private void ui_InitGUIMenus () {
	JMenuBar menu_bar = new JMenuBar();
	ui_InitGUIMenus_File ( menu_bar );
	ui_InitGUIMenus_Edit ( menu_bar );
	ui_InitGUIMenus_View ( menu_bar );
	ui_InitGUIMenus_Commands ( menu_bar );
	ui_InitGUIMenus_CommandsGeneral ( menu_bar );
	ui_InitGUIMenus_Run ( menu_bar );
	ui_InitGUIMenus_Results ( menu_bar );
	ui_InitGUIMenus_Tools ( menu_bar );
	ui_InitGUIMenus_Help ( menu_bar );
	setJMenuBar ( menu_bar );
}

/**
Initialize the GUI "Commands" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_Commands ( JMenuBar menuBar ) {
	// "Commands...TS Create/Convert/Read Time Series"...

	menuBar.add( TSToolMenus.Commands_JMenu = new JMenu( TSToolConstants.Commands_String, true ) );
	TSToolMenus.Commands_JMenu.setToolTipText("Insert command into commands list (above first selected command, or at end).");

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_SelectTimeSeries_JMenu = new JMenu(TSToolConstants.Commands_SelectTimeSeries_String) );
	//TSToolMenus.Commands_SelectTimeSeries_JMenu.setToolTipText("Select, free, and sort time series results.");
    TSToolMenus.Commands_SelectTimeSeries_JMenu.add ( TSToolMenus.Commands_Select_DeselectTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Select_DeselectTimeSeries_String, this ) );
	TSToolMenus.Commands_Select_DeselectTimeSeries_JMenuItem.setToolTipText("Deselect time series for processing (use with command parameter TSList=SelectedTS).");
    TSToolMenus.Commands_SelectTimeSeries_JMenu.add ( TSToolMenus.Commands_Select_SelectTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Select_SelectTimeSeries_String, this ) );
	TSToolMenus.Commands_Select_SelectTimeSeries_JMenuItem.setToolTipText("Select time series for processing (use with command parameter TSList=SelectedTS).");
    TSToolMenus.Commands_SelectTimeSeries_JMenu.addSeparator();
    TSToolMenus.Commands_SelectTimeSeries_JMenu.add ( TSToolMenus.Commands_Select_Free_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Select_Free_String, this ) );
	TSToolMenus.Commands_Select_Free_JMenuItem.setToolTipText("Delete time series in results and free memory, useful for large workflows.");
    TSToolMenus.Commands_SelectTimeSeries_JMenu.addSeparator();
    TSToolMenus.Commands_SelectTimeSeries_JMenu.add ( TSToolMenus.Commands_Select_SortTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Select_SortTimeSeries_String, this ) );
	TSToolMenus.Commands_Select_SortTimeSeries_JMenuItem.setToolTipText("Sort time series in results.");
    TSToolMenus.Commands_JMenu.addSeparator();

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_CreateTimeSeries_JMenu = new JMenu(TSToolConstants.Commands_CreateTimeSeries_String) );
	//TSToolMenus.Commands_CreateTimeSeries_JMenu.setToolTipText("Create time series from supplied values or other time series.");

	// Create (break into logical groups).
	// Commands that create new simple data (maybe add functions or random).

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add ( TSToolMenus.Commands_Create_NewPatternTimeSeries_JMenuItem =
       new SimpleJMenuItem(TSToolConstants.Commands_Create_NewPatternTimeSeries_String, this ) );
	TSToolMenus.Commands_Create_NewPatternTimeSeries_JMenuItem.setToolTipText("Create time series and initialize with a pattern of values.");
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_NewTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_NewTimeSeries_String, this ) );
	TSToolMenus.Commands_Create_NewTimeSeries_JMenuItem.setToolTipText("Create time series and initialize with values.");
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_TSID_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_TSID_String, this ) );
	TSToolMenus.Commands_Create_TSID_JMenuItem.setToolTipText("Create time series identifier (TSID) command, which will cause a read based on the TSID.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.addSeparator();
	// Commands that perform other processing and create new time series.
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_ChangeInterval_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_ChangeInterval_String, this) );
	TSToolMenus.Commands_Create_ChangeInterval_JMenuItem.setToolTipText("Create time series by changing the interval time series, handles small<->large, irregular/regular, etc.");
    // TODO smalers 2017-04-24 need to enable these commands when they work
    //TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_ChangeIntervalToLarger_JMenuItem =
    //    new SimpleJMenuItem(TSToolMenus.Commands_Create_ChangeIntervalToLarger_String, this) );
    //TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_ChangeIntervalToSmaller_JMenuItem =
    //    new SimpleJMenuItem(TSToolMenus.Commands_Create_ChangeIntervalToSmaller_String, this) );
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_ChangeIntervalIrregularToRegular_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_ChangeIntervalIrregularToRegular_String, this) );
    //TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_ChangeIntervalRegularToIrregular_JMenuItem =
    //    new SimpleJMenuItem(TSToolMenus.Commands_Create_ChangeIntervalRegularToIrregular_String, this) );

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_Copy_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_Copy_String, this) );
	TSToolMenus.Commands_Create_Copy_JMenuItem.setToolTipText("Create time series by copying a time series.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add( TSToolMenus.Commands_Create_Delta_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_Delta_String, this) );
	TSToolMenus.Commands_Create_Delta_JMenuItem.setToolTipText("Create a time series by calculating each input time series' interval delta.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add( TSToolMenus.Commands_Create_Disaggregate_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_Disaggregate_String, this) );
	TSToolMenus.Commands_Create_Disaggregate_JMenuItem.setToolTipText("Create a time series by disaggregating a large interval to small interval.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add( TSToolMenus.Commands_Create_LookupTimeSeriesFromTable_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_LookupTimeSeriesFromTable_String, this) );
	TSToolMenus.Commands_Create_LookupTimeSeriesFromTable_JMenuItem.setToolTipText("Create a time series by looking up values from a table.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_NewDayTSFromMonthAndDayTS_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_NewDayTSFromMonthAndDayTS_String, this) );
	TSToolMenus.Commands_Create_NewDayTSFromMonthAndDayTS_JMenuItem.setToolTipText("Create a day interval time series from daily time series (pattern) and monthly time series (amount).");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_NewEndOfMonthTSFromDayTS_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_NewEndOfMonthTSFromDayTS_String, this ) );
	TSToolMenus.Commands_Create_NewEndOfMonthTSFromDayTS_JMenuItem.setToolTipText("Create an end-of-month time series from daily time series by searching for values near the end of each month.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add(TSToolMenus.Commands_Create_Normalize_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_Normalize_String, this ) );
	TSToolMenus.Commands_Create_Normalize_JMenuItem.setToolTipText("Create a time series by normalizing input time series to range of valus (e.g., 0.0 to 1.0).");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add ( TSToolMenus.Commands_Create_RelativeDiff_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Create_RelativeDiff_String, this ) );
	TSToolMenus.Commands_Create_RelativeDiff_JMenuItem.setToolTipText("Create a time series as relative difference of two input time series values.");

    TSToolMenus.Commands_CreateTimeSeries_JMenu.add( TSToolMenus.Commands_Create_ResequenceTimeSeriesData_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_ResequenceTimeSeriesData_String, this ) );
	TSToolMenus.Commands_Create_ResequenceTimeSeriesData_JMenuItem.setToolTipText("Create a time series by resequencing the years in the input time series.");

    // Statistic commands.
    TSToolMenus.Commands_CreateTimeSeries_JMenu.addSeparator();
	TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_NewStatisticTimeSeries_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Create_NewStatisticTimeSeries_String, this ) );
	TSToolMenus.Commands_Create_NewStatisticTimeSeries_JMenuItem.setToolTipText("Create a time series as statistic of each interval's historical data (e.g, mean of all January 1 values).");
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_NewStatisticMonthTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_NewStatisticMonthTimeSeries_String, this ) );
	TSToolMenus.Commands_Create_NewStatisticMonthTimeSeries_JMenuItem.setToolTipText("Create a month interval time series as statistic of each month's data values.");
	TSToolMenus.Commands_CreateTimeSeries_JMenu.add (TSToolMenus.Commands_Create_NewStatisticYearTS_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Create_NewStatisticYearTS_String, this ) );
	TSToolMenus.Commands_Create_NewStatisticYearTS_JMenuItem.setToolTipText("Create a year interval time series as statistic of each year's data values.");
    TSToolMenus.Commands_CreateTimeSeries_JMenu.add ( TSToolMenus.Commands_Create_RunningStatisticTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_RunningStatisticTimeSeries_String, this ) );
	TSToolMenus.Commands_Create_RunningStatisticTimeSeries_JMenuItem.setToolTipText("Create a time series as statistic of values from a moving window in the input time series.");

	// Read commands.

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_ReadTimeSeries_JMenu=	new JMenu(TSToolConstants.Commands_ReadTimeSeries_String) );
	//TSToolMenus.Commands_ReadTimeSeries_JMenu.setToolTipText("Read time series from files, databases, and web services.");

	TSToolMenus.Commands_ReadTimeSeries_JMenu.add (TSToolMenus.Commands_Read_SetIncludeMissingTS_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Read_SetIncludeMissingTS_String, this ) );
	TSToolMenus.Commands_Read_SetIncludeMissingTS_JMenuItem.setToolTipText("Indicate whether missing time series should be included in results, with minimal properties.");

	TSToolMenus.Commands_ReadTimeSeries_JMenu.add (TSToolMenus.Commands_Read_SetInputPeriod_JMenuItem=
        new SimpleJMenuItem(TSToolConstants.Commands_Read_SetInputPeriod_String, this ) );
	TSToolMenus.Commands_Read_SetInputPeriod_JMenuItem.setToolTipText("Set the default input period for queries/reads, will impact calculations.  See also SetOutputPeriod.");

	TSToolMenus.Commands_ReadTimeSeries_JMenu.addSeparator ();

	TSToolMenus.Commands_ReadTimeSeries_JMenu.add( TSToolMenus.Commands_Read_CreateFromList_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Create_CreateFromList_String, this) );
	TSToolMenus.Commands_Read_CreateFromList_JMenuItem.setToolTipText("Read time series using a delimited file for the list.  Replaced by ReadTimeSeriesList command.");

    TSToolMenus.Commands_ReadTimeSeries_JMenu.addSeparator ();

    if ( this.__source_ColoradoHydroBaseRest_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadColoradoHydroBaseRest_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadColoradoHydroBaseRest_String, this) );
			TSToolMenus.Commands_Read_ReadColoradoHydroBaseRest_JMenuItem.setToolTipText("Read time series from Colorado HydroBase REST web services datastore.");
	}
	if ( this.__source_DateValue_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadDateValue_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadDateValue_String, this) );
			TSToolMenus.Commands_Read_ReadDateValue_JMenuItem.setToolTipText("Read time series from a DateValue time series text file.");
	}
	if ( this.__source_DelftFews_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadDelftFewsPiXml_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadDelftFewsPiXml_String, this) );
			TSToolMenus.Commands_Read_ReadDelftFewsPiXml_JMenuItem.setToolTipText("Read time series from Delft FEWS software PiXml text file.");
	}
    TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadDelimitedFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadDelimitedFile_String, this) );
	TSToolMenus.Commands_Read_ReadDelimitedFile_JMenuItem.setToolTipText("Read time series from a delimited text file (CSV, tab-delimited, etc.).");
    if ( this.__source_HECDSS_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadHecDss_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadHecDss_String, this) );
        TSToolMenus.Commands_Read_ReadHecDss_JMenuItem.setToolTipText("Read time series from US Army Corps HEC-DSS binary database file.");
    }
    if ( this.__source_HydroBase_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadHydroBase_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadHydroBase_String, this) );
        TSToolMenus.Commands_Read_ReadHydroBase_JMenuItem.setToolTipText("Read time series from Colorado HydroBase database.");
	}
	if ( this.__source_MODSIM_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadMODSIM_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadMODSIM_String, this) );
        TSToolMenus.Commands_Read_ReadMODSIM_JMenuItem.setToolTipText("Read time series from MODSIM modeling software text file.");
	}
    if ( this.__source_NrcsAwdb_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadNrcsAwdb_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadNrcsAwdb_String, this) );
        TSToolMenus.Commands_Read_ReadNrcsAwdb_JMenuItem.setToolTipText("Read time series from US Natural Resources Conservation Service (NRCS) web service.");
    }
	if ( this.__source_NWSCard_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadNwsCard_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadNwsCard_String, this) );
        TSToolMenus.Commands_Read_ReadNwsCard_JMenuItem.setToolTipText("Read time series from US National Weather Service (NWS) \"card\" format text file.");
	}
    if ( this.__source_NWSRFS_FS5Files_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadNwsrfsFS5Files_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadNwsrfsFS5Files_String, this) );
        TSToolMenus.Commands_Read_ReadNwsrfsFS5Files_JMenuItem.setToolTipText("Read time series from US National Weather Service (NWS) River Forecast System (RFS) binary files.");
    }
    if ( this.__source_RCCACIS_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadRccAcis_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadRccAcis_String, this) );
        TSToolMenus.Commands_Read_ReadRccAcis_JMenuItem.setToolTipText("Read time series from US Reginal Climate Center (RCC) Applied Climate Information System (ACIS) web service.");
    }
    if ( this.__source_ReclamationHDB_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadReclamationHDB_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadReclamationHDB_String, this) );
        TSToolMenus.Commands_Read_ReadReclamationHDB_JMenuItem.setToolTipText("Read time series from US Bureau of Reclamation HDB database.");
    }
    if ( this.__source_ReclamationPisces_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadReclamationPisces_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadReclamationPisces_String, this) );
        TSToolMenus.Commands_Read_ReadReclamationPisces_JMenuItem.setToolTipText("Read time series from US Bureau of Reclamation Pisces database.");
    }
    if ( this.__source_RiverWare_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadRiverWare_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadRiverWare_String, this) );
        TSToolMenus.Commands_Read_ReadRiverWare_JMenuItem.setToolTipText("Read time series from RiverWare modeling software text files.");
    }
	if ( this.__source_StateCU_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadStateCU_JMenuItem =
			new SimpleJMenuItem( TSToolConstants.Commands_Read_ReadStateCU_String, this) );
        TSToolMenus.Commands_Read_ReadStateCU_JMenuItem.setToolTipText("Read time series from StateCU (consumptive use modeling software) text input files.");
	}
    if ( this.__source_StateCUB_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadStateCUB_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadStateCUB_String, this) );
        TSToolMenus.Commands_Read_ReadStateCUB_JMenuItem.setToolTipText("Read time series from StateCU (consumptive use modeling software) binary output files.");
    }
	if ( this.__source_StateMod_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadStateMod_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadStateMod_String, this) );
        TSToolMenus.Commands_Read_ReadStateMod_JMenuItem.setToolTipText("Read time series from StateMod (water allocation modeling software) text input files.");
	}
	if ( this.__source_StateModB_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadStateModB_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadStateModB_String, this) );
        TSToolMenus.Commands_Read_ReadStateModB_JMenuItem.setToolTipText("Read time series from StateMod (water allocation modeling software) binary output files.");
	}
    TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadTimeSeries_String, this) );
    TSToolMenus.Commands_Read_ReadTimeSeries_JMenuItem.setToolTipText("Read time series given a time series identifier (TSID).");
    // Duplicate this menu from the Datastore menus because of common use.
    TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadTimeSeriesFromDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_ReadTimeSeriesFromDataStore_String, this) );
    TSToolMenus.Commands_Read_ReadTimeSeriesFromDataStore_JMenuItem.setToolTipText("Read time series from a database datastore.");
    TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadTimeSeriesList_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadTimeSeriesList_String, this) );
	TSToolMenus.Commands_Read_ReadTimeSeriesList_JMenuItem.setToolTipText("Read time series list using table to provide time series identifier information.");
    if ( this.__source_UsgsNwisDaily_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadUsgsNwisDaily_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadUsgsNwisDaily_String, this) );
        TSToolMenus.Commands_Read_ReadUsgsNwisDaily_JMenuItem.setToolTipText("Read daily time series from United States Geological Survey (USGS) National Water Information System (NWIS) web service.");
    }
    if ( this.__source_UsgsNwisGroundwater_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadUsgsNwisGroundwater_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadUsgsNwisGroundwater_String, this) );
        TSToolMenus.Commands_Read_ReadUsgsNwisGroundwater_JMenuItem.setToolTipText("Read groundwater time series from United States Geological Survey (USGS) National Water Information System (NWIS) web service.");
    }
    if ( this.__source_UsgsNwisInstantaneous_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadUsgsNwisInstantaneous_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadUsgsNwisInstantaneous_String, this) );
        TSToolMenus.Commands_Read_ReadUsgsNwisInstantaneous_JMenuItem.setToolTipText("Read instantaneous time series from United States Geological Survey (USGS) National Water Information System (NWIS) web service.");
    }
    if ( this.__source_UsgsNwisRdb_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadUsgsNwisRdb_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadUsgsNwisRdb_String, this) );
        TSToolMenus.Commands_Read_ReadUsgsNwisRdb_JMenuItem.setToolTipText("Read time series from United States Geological Survey (USGS) National Water Information System (NWIS) RDB text file.");
    }
    if ( this.__source_WaterML_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadWaterML_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadWaterML_String, this) );
        TSToolMenus.Commands_Read_ReadWaterML_JMenuItem.setToolTipText("Read time series from WaterML XML text file.  See ReadWaterML2.");
    }
    if ( this.__source_WaterML_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadWaterML2_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadWaterML2_String, this) );
        TSToolMenus.Commands_Read_ReadWaterML2_JMenuItem.setToolTipText("Read time series from WaterML 2 XML text file.");
    }
    if ( this.__source_WaterOneFlow_enabled ) {
        TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_ReadWaterOneFlow_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Read_ReadWaterOneFlow_String, this) );
        TSToolMenus.Commands_Read_ReadWaterOneFlow_JMenuItem.setToolTipText("Read time series from WaterOneFlow web service.");
    }
	if ( this.__source_StateMod_enabled ) {
		TSToolMenus.Commands_ReadTimeSeries_JMenu.addSeparator ();
		TSToolMenus.Commands_ReadTimeSeries_JMenu.add(TSToolMenus.Commands_Read_StateModMax_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Read_StateModMax_String, this) );
        TSToolMenus.Commands_Read_StateModMax_JMenuItem.setToolTipText("Create maximum of time series from two StateMod input files, for matching identifiers.");
	}

	// Menu: Commands / Fill Time Series

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_FillTimeSeries_JMenu = new JMenu(TSToolConstants.Commands_FillTimeSeries_String));
	//TSToolMenus.Commands_FillTimeSeries_JMenu.setToolTipText("Fill time series missing data values by estimating values.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillConstant_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillConstant_String, this ) );
    TSToolMenus.Commands_Fill_FillConstant_JMenuItem.setToolTipText("Fill time series missing data values using constant.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_String,this) );
    TSToolMenus.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_JMenuItem.setToolTipText(
    	"Fill day interval time series missing data values using day interval time series (pattern) and month interval time series (value).");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillFromTS_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillFromTS_String,this) );
    TSToolMenus.Commands_Fill_FillFromTS_JMenuItem.setToolTipText("Fill time series missing data values using data from another time series.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add(TSToolMenus.Commands_Fill_FillHistMonthAverage_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Commands_Fill_FillHistMonthAverage_String, this ) );
    TSToolMenus.Commands_Fill_FillHistMonthAverage_JMenuItem.setToolTipText("Fill month interval time series missing data values using historical monthly average values.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillHistYearAverage_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Commands_Fill_FillHistYearAverage_String, this ) );
    TSToolMenus.Commands_Fill_FillHistYearAverage_JMenuItem.setToolTipText("Fill year interval time series missing data values using historical yearly average values.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillInterpolate_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillInterpolate_String, this ) );
    TSToolMenus.Commands_Fill_FillInterpolate_JMenuItem.setToolTipText("Fill time series missing data values using interpolation.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillMixedStation_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillMixedStation_String, this ) );
    TSToolMenus.Commands_Fill_FillMixedStation_JMenuItem.setToolTipText("Fill time series missing data values using Mixed Station Analysis (best regression relationships).");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillMOVE2_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillMOVE2_String, this ) );
    TSToolMenus.Commands_Fill_FillMOVE2_JMenuItem.setToolTipText("Fill time series missing data values using Maintenance of Variation approach.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillPattern_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillPattern_String, this ) );
    TSToolMenus.Commands_Fill_FillPattern_JMenuItem.setToolTipText("Fill time series missing data values using Wet/Dry/Average historical average pattern.");

    TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_ReadPatternFile_JMenuItem=
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_ReadPatternFile_String, this ) );
    TSToolMenus.Commands_Fill_ReadPatternFile_JMenuItem.setToolTipText("Read input file containing pattern for FillPattern command.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillProrate_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Fill_FillProrate_String, this ) );
    TSToolMenus.Commands_Fill_FillProrate_JMenuItem.setToolTipText("Fill time series missing data values by prorating values from another time series.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillRegression_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Fill_FillRegression_String, this ) );
    TSToolMenus.Commands_Fill_FillRegression_JMenuItem.setToolTipText("Fill time series missing data values using ordinary least squares (OLS) regression.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_FillRepeat_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Fill_FillRepeat_String, this ) );
    TSToolMenus.Commands_Fill_FillRepeat_JMenuItem.setToolTipText("Fill time series missing data values by repeating non-missing values.");

	if ( this.__source_HydroBase_enabled ) {
		TSToolMenus.Commands_FillTimeSeries_JMenu.add(TSToolMenus.Commands_Fill_FillUsingDiversionComments_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Fill_FillUsingDiversionComments_String,this ) );
			TSToolMenus.Commands_Fill_FillUsingDiversionComments_JMenuItem.setToolTipText("Fill time series missing data values with additional zeros using HydroBase diversion comments.");
	}

	TSToolMenus.Commands_FillTimeSeries_JMenu.addSeparator();

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_SetAutoExtendPeriod_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Fill_SetAutoExtendPeriod_String, this ) );
	TSToolMenus.Commands_Fill_SetAutoExtendPeriod_JMenuItem.setToolTipText(
		"Set whether the period for time series is automatically extended to OutputPeriod when reading data, used when creating model datasets.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add (TSToolMenus.Commands_Fill_SetAveragePeriod_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_SetAveragePeriod_String, this ) );
    TSToolMenus.Commands_Fill_SetAveragePeriod_JMenuItem.setToolTipText("Set the period used when computing historical averages, if full period is not to be used.");

	TSToolMenus.Commands_FillTimeSeries_JMenu.add(TSToolMenus.Commands_Fill_SetIgnoreLEZero_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Fill_SetIgnoreLEZero_String, this ) );
    TSToolMenus.Commands_Fill_SetIgnoreLEZero_JMenuItem.setToolTipText("Indicate whether values <= 0 should be ignored when computing historical averages.");

	// Menu: Commands / Set Time Series Contents

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_SetTimeSeries_JMenu=new JMenu(TSToolConstants.Commands_SetTimeSeries_String));
	//TSToolMenus.Commands_SetTimeSeries_JMenu.setToolTipText("Set time series properties and data values.");

	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_ReplaceValue_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Commands_Set_ReplaceValue_String, this));
    TSToolMenus.Commands_Set_ReplaceValue_JMenuItem.setToolTipText("Replace a range of time series data values with alternate values.");
	TSToolMenus.Commands_SetTimeSeries_JMenu.addSeparator();
	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetConstant_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Commands_Set_SetConstant_String, this ));
    TSToolMenus.Commands_Set_SetConstant_JMenuItem.setToolTipText("Set time series data values to constant values.");
	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetDataValue_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetDataValue_String, this ) );
    TSToolMenus.Commands_Set_SetDataValue_JMenuItem.setToolTipText("Set time series single data value to a constant value.");
	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetFromTS_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetFromTS_String, this ) );
    TSToolMenus.Commands_Set_SetFromTS_JMenuItem.setToolTipText("Set time series data values by using data in another time series.");
    TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetTimeSeriesValuesFromLookupTable_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetTimeSeriesValuesFromLookupTable_String, this ) );
    TSToolMenus.Commands_Set_SetTimeSeriesValuesFromLookupTable_JMenuItem.setToolTipText("Set time series data values using a lookup table.");
    TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetTimeSeriesValuesFromTable_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetTimeSeriesValuesFromTable_String, this ) );
    TSToolMenus.Commands_Set_SetTimeSeriesValuesFromTable_JMenuItem.setToolTipText("Set time series data values using values in a table.");
	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetToMax_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetToMax_String, this ) );
    TSToolMenus.Commands_Set_SetToMax_JMenuItem.setToolTipText("Set time series data values to the maximum values from a list of time series.");
	TSToolMenus.Commands_SetTimeSeries_JMenu.add (TSToolMenus.Commands_Set_SetToMin_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Set_SetToMin_String, this ) );
    TSToolMenus.Commands_Set_SetToMin_JMenuItem.setToolTipText("Set time series data values to the minimum values from a list of time series.");

    TSToolMenus.Commands_SetTimeSeries_JMenu.addSeparator ();
    TSToolMenus.Commands_SetTimeSeries_JMenu.add ( TSToolMenus.Commands_Set_SetTimeSeriesProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Set_SetTimeSeriesProperty_String, this ) );
    TSToolMenus.Commands_Set_SetTimeSeriesProperty_JMenuItem.setToolTipText("Set time series properties.");

	// Menu: Commands / Manipulate Time Series

	TSToolMenus.Commands_JMenu.add (TSToolMenus.Commands_ManipulateTimeSeries_JMenu=new JMenu("Manipulate Time Series"));
	//TSToolMenus.Commands_ManipulateTimeSeries_JMenu.setToolTipText("Manipulate time series data values.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Add_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_Add_String,this) );
    TSToolMenus.Commands_Manipulate_Add_JMenuItem.setToolTipText("Add 1+ time series values to another.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_AddConstant_JMenuItem=
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_AddConstant_String,this) );
    TSToolMenus.Commands_Manipulate_AddConstant_JMenuItem.setToolTipText("Add constant to time series values.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add(TSToolMenus.Commands_Manipulate_AdjustExtremes_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Manipulate_AdjustExtremes_String, this ) );
    TSToolMenus.Commands_Manipulate_AdjustExtremes_JMenuItem.setToolTipText("Adjust minimum/maxumum time series values by balancing neighboring values.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_ARMA_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_ARMA_String, this ) );
    TSToolMenus.Commands_Manipulate_ARMA_JMenuItem.setToolTipText("Calculate autoregressive moving average time series.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Blend_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_Blend_String, this ) );
    TSToolMenus.Commands_Manipulate_Blend_JMenuItem.setToolTipText("Blend periods of two time series.");

    TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_ChangePeriod_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_ChangePeriod_String, this ) );
    TSToolMenus.Commands_Manipulate_ChangePeriod_JMenuItem.setToolTipText("Change the period of time series by truncating or filling with missing data value.");

    TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_ChangeTimeZone_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_ChangeTimeZone_String, this ) );
    TSToolMenus.Commands_Manipulate_ChangeTimeZone_JMenuItem.setToolTipText("Change the time zone for time series date/times.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_ConvertDataUnits_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_ConvertDataUnits_String, this ) );
    TSToolMenus.Commands_Manipulate_ConvertDataUnits_JMenuItem.setToolTipText("Convert time series data units, including adjusting data values.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Cumulate_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Manipulate_Cumulate_String, this ) );
    TSToolMenus.Commands_Manipulate_Cumulate_JMenuItem.setToolTipText("Cumulate time series data values.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Divide_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_Divide_String, this ) );
    TSToolMenus.Commands_Manipulate_Divide_JMenuItem.setToolTipText("Divide one time series by another.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Multiply_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Manipulate_Multiply_String, this ) );
    TSToolMenus.Commands_Manipulate_Multiply_JMenuItem.setToolTipText("Multiply one time series by another.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Scale_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Manipulate_Scale_String, this ) );
    TSToolMenus.Commands_Manipulate_Scale_JMenuItem.setToolTipText("Scale time series data values by multiplying by a constant value.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_ShiftTimeByInterval_JMenuItem=
		new SimpleJMenuItem(TSToolConstants.Commands_Manipulate_ShiftTimeByInterval_String, this ) );
    TSToolMenus.Commands_Manipulate_ShiftTimeByInterval_JMenuItem.setToolTipText("Shift time series data values by date/time offset.");

	TSToolMenus.Commands_ManipulateTimeSeries_JMenu.add ( TSToolMenus.Commands_Manipulate_Subtract_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Manipulate_Subtract_String, this ) );
    TSToolMenus.Commands_Manipulate_Subtract_JMenuItem.setToolTipText("Subtract 1+ time series from a time series.");

	// Menu: Commands / Analyze Time Series

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_AnalyzeTimeSeries_JMenu= new JMenu(TSToolConstants.Commands_AnalyzeTimeSeries_String) );
	//TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.setToolTipText("Analyze time series data values.");
	TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.add ( TSToolMenus.Commands_Analyze_AnalyzePattern_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Analyze_AnalyzePattern_String, this ) );
    TSToolMenus.Commands_Analyze_AnalyzePattern_JMenuItem.setToolTipText("Analyze Wet/Dry/Average (or other categories) pattern to create input for FillPattern command.");
    TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.add ( TSToolMenus.Commands_Analyze_CalculateTimeSeriesStatistic_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Analyze_CalculateTimeSeriesStatistic_String, this ) );
    TSToolMenus.Commands_Analyze_CalculateTimeSeriesStatistic_JMenuItem.setToolTipText("Calculate a single statistic from time series data values.");
	TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.add (TSToolMenus.Commands_Analyze_CompareTimeSeries_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Analyze_CompareTimeSeries_String, this ) );
    TSToolMenus.Commands_Analyze_CompareTimeSeries_JMenuItem.setToolTipText("Compare time series to identify differences.");

	TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.addSeparator ();
	TSToolMenus.Commands_AnalyzeTimeSeries_JMenu.add (TSToolMenus.Commands_Analyze_ComputeErrorTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Analyze_ComputeErrorTimeSeries_String, this ) );
    TSToolMenus.Commands_Analyze_ComputeErrorTimeSeries_JMenuItem.setToolTipText("Create time series as the difference (error) between input time series, useful for simulation.");

	// Menu: Commands / Models - Routing

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_Models_Routing_JMenu = new JMenu(TSToolConstants.Commands_Models_Routing_String) );
	//TSToolMenus.Commands_Models_Routing_JMenu.setToolTipText("Route time series (lag and attenuate over time).");
	TSToolMenus.Commands_Models_Routing_JMenu.add ( TSToolMenus.Commands_Models_Routing_LagK_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Models_Routing_LagK_String, this ) );
    TSToolMenus.Commands_Models_Routing_LagK_JMenuItem.setToolTipText("Route (lag and attenuate) a time series using LagK approach.");
    TSToolMenus.Commands_Models_Routing_JMenu.add ( TSToolMenus.Commands_Models_Routing_VariableLagK_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Models_Routing_VariableLagK_String, this ) );
    TSToolMenus.Commands_Models_Routing_VariableLagK_JMenuItem.setToolTipText("Route (lag and attenuate) a time series using variable LagK approach.");

	// Menu: Commands / Output Time Series

	TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_OutputTimeSeries_JMenu=new JMenu(TSToolConstants.Commands_OutputTimeSeries_String) );
	//TSToolMenus.Commands_OutputTimeSeries_JMenu.setToolTipText("Output (write) time series to files and databases.");

	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_SetOutputDetailedHeaders_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Output_SetOutputDetailedHeaders_String, this ) );
    TSToolMenus.Commands_Output_SetOutputDetailedHeaders_JMenuItem.setToolTipText("Indicate whether to output detailed headers in summary reports.");
	TSToolMenus.Commands_OutputTimeSeries_JMenu.add( TSToolMenus.Commands_Output_SetOutputPeriod_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Output_SetOutputPeriod_String, this ) );
    TSToolMenus.Commands_Output_SetOutputPeriod_JMenuItem.setToolTipText("Set the default output period (can be overridden by specific commands parameters).");
	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_SetOutputYearType_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Output_SetOutputYearType_String, this ) );
    TSToolMenus.Commands_Output_SetOutputYearType_JMenuItem.setToolTipText("Set the default output year type (can be overridden by specific command parameters).");

	TSToolMenus.Commands_OutputTimeSeries_JMenu.addSeparator ();

	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteDateValue_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteDateValue_String, this ) );
    TSToolMenus.Commands_Output_WriteDateValue_JMenuItem.setToolTipText("Write time series to DateValue text file.");
    //if ( __source_DelftFews_enabled ) {
    //	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteDelftFewsPiXml_JMenuItem =
    //		new SimpleJMenuItem(TSToolMenus.Commands_Output_WriteDelftFewsPiXml_String, this ) );
    //}
    TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteDelimitedFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteDelimitedFile_String, this ) );
    TSToolMenus.Commands_Output_WriteDelimitedFile_JMenuItem.setToolTipText("Write time series to delimited text file (CSV, tab-delimited, etc.).");

    if ( this.__source_HECDSS_enabled ) {
        TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteHecDss_JMenuItem =
            new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteHecDss_String, this ) );
        TSToolMenus.Commands_Output_WriteHecDss_JMenuItem.setToolTipText("Write time series to US Army Corps HEC-DSS binary database file.");
    }

	if ( this.__source_NWSCard_enabled ) {
		TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteNwsCard_JMenuItem =
			new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteNwsCard_String, this ) );
        TSToolMenus.Commands_Output_WriteNwsCard_JMenuItem.setToolTipText("Write time series to US National Weather Service (NWS) \"card\" format text file.");
	}

    if ( this.__source_ReclamationHDB_enabled ) {
        TSToolMenus.Commands_OutputTimeSeries_JMenu.add( TSToolMenus.Commands_Output_WriteReclamationHDB_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteReclamationHDB_String, this ) );
        TSToolMenus.Commands_Output_WriteReclamationHDB_JMenuItem.setToolTipText("Write time series to US Bureau of Reclamation HDB database.");
    }

	if ( this.__source_RiverWare_enabled ) {
		TSToolMenus.Commands_OutputTimeSeries_JMenu.add( TSToolMenus.Commands_Output_WriteRiverWare_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteRiverWare_String, this ) );
        TSToolMenus.Commands_Output_WriteRiverWare_JMenuItem.setToolTipText("Write time series to RiverWare modeling software text files.");
	}

	/* TODO smalers 2017-03-05 disable for now - need to work on in a branch in the processor library.
    if ( __source_SHEF_enabled ) {
        TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteSHEF_JMenuItem =
            new SimpleJMenuItem(  TSToolConstants.Commands_Output_WriteSHEF_String, this ) );
    }
    */

	if ( this.__source_StateCU_enabled ) {
		TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteStateCU_JMenuItem =
            new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteStateCU_String, this ) );
        TSToolMenus.Commands_Output_WriteStateCU_JMenuItem.setToolTipText("Write time series to StateCU (consumptive use modeling software) text input files.");
	}

	if ( this.__source_StateMod_enabled ) {
		TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteStateMod_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteStateMod_String, this ) );
        TSToolMenus.Commands_Output_WriteStateMod_JMenuItem.setToolTipText("Write time series to StateMod (water allocation modeling software) text input files.");
	}

	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteSummary_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteSummary_String, this ) );
    TSToolMenus.Commands_Output_WriteSummary_JMenuItem.setToolTipText("Write time series to summary text file.");
    TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteTimeSeriesToDataStore_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_WriteTimeSeriesToDataStore_String, this ) );
    TSToolMenus.Commands_Output_WriteTimeSeriesToDataStore_JMenuItem.setToolTipText("Write time series to datastore.");
    TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteTimeSeriesToDataStream_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteTimeSeriesToDataStream_String, this ) );
    TSToolMenus.Commands_Output_WriteTimeSeriesToDataStream_JMenuItem.setToolTipText("Write time series to data stream text file.");
    TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteTimeSeriesToHydroJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteTimeSeriesToHydroJSON_String, this ) );
    TSToolMenus.Commands_Output_WriteTimeSeriesToHydroJSON_JMenuItem.setToolTipText("Write time series to HydroJSON text file.");
    TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteTimeSeriesToJson_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Output_WriteTimeSeriesToJson_String, this ) );
    TSToolMenus.Commands_Output_WriteTimeSeriesToJson_JMenuItem.setToolTipText("Write time series to JSON text file.");

    if ( this.__source_WaterML_enabled ) {
        TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteWaterML_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteWaterML_String, this ) );
        TSToolMenus.Commands_Output_WriteWaterML_JMenuItem.setToolTipText("Write time series to WaterML XML text file.  See WriteWaterML2.");
        TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteWaterML2_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Output_WriteWaterML2_String, this ) );
        TSToolMenus.Commands_Output_WriteWaterML2_JMenuItem.setToolTipText("Write time series to WaterML 2 XML text file.");
    }

	TSToolMenus.Commands_OutputTimeSeries_JMenu.addSeparator ();

	TSToolMenus.Commands_OutputTimeSeries_JMenu.add ( TSToolMenus.Commands_Output_WriteTimeSeriesPropertiesToFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_String, this ) );
    TSToolMenus.Commands_Output_WriteTimeSeriesPropertiesToFile_JMenuItem.setToolTipText("Write time series properties to text file.");

    // Check time series and other data.

    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Check_CheckTimeSeries_JMenu = new JMenu( TSToolConstants.Commands_Check_CheckingResults_String, true ) );
    //TSToolMenus.Commands_Check_CheckTimeSeries_JMenu.setToolTipText("Check time series against criteria.");
    TSToolMenus.Commands_Check_CheckTimeSeries_JMenu.add ( TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeries_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeries_String, this ) );
    TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeries_JMenuItem.setToolTipText("Check time series values against criteria.");
    TSToolMenus.Commands_Check_CheckTimeSeries_JMenu.add ( TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_String, this ) );
    TSToolMenus.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_JMenuItem.setToolTipText("Check time series statistic against criteria.");
    TSToolMenus.Commands_Check_CheckTimeSeries_JMenu.add ( TSToolMenus.Commands_Check_CheckingResults_WriteCheckFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Check_CheckingResults_WriteCheckFile_String, this ) );
    TSToolMenus.Commands_Check_CheckingResults_WriteCheckFile_JMenuItem.setToolTipText("Write check result to file.");
}

/**
Initialize the GUI "Commands...General" and Commands/Table (top level).
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_CommandsGeneral ( JMenuBar menuBar ) {
	TSToolMenus.Commands_JMenu.addSeparator(); // Results in double separator.

    // Menu: Commands / Datastore processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_Datastore_JMenu = new JMenu(TSToolConstants.Commands_Datastore_String) );
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_NewAccessDatabase_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_NewAccessDatabase_String, this) );
    TSToolMenus.Commands_Datastore_NewAccessDatabase_JMenuItem.setToolTipText("Create a new Microsoft Access database.");
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_NewDerbyDatabase_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_NewDerbyDatabase_String, this) );
    TSToolMenus.Commands_Datastore_NewDerbyDatabase_JMenuItem.setToolTipText("Create a new Derby (built-in Java) database.");
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_NewSQLiteDatabase_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_NewSQLiteDatabase_String, this) );
    TSToolMenus.Commands_Datastore_NewSQLiteDatabase_JMenuItem.setToolTipText("Create a new SQLite database.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_OpenDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_OpenDataStore_String, this) );
    TSToolMenus.Commands_Datastore_OpenDataStore_JMenuItem.setToolTipText("Open a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_ReadTableFromDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_ReadTableFromDataStore_String, this) );
    TSToolMenus.Commands_Datastore_ReadTableFromDataStore_JMenuItem.setToolTipText("Read a table from a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_WriteTableToDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_WriteTableToDataStore_String, this) );
    TSToolMenus.Commands_Datastore_WriteTableToDataStore_JMenuItem.setToolTipText("Write a table to a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add( TSToolMenus.Commands_Datastore_RunSql_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_RunSql_String, this ) );
    TSToolMenus.Commands_Datastore_RunSql_JMenuItem.setToolTipText("Run an Structured Query Language (SQL) statement on a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.add( TSToolMenus.Commands_Datastore_DeleteDataStoreTableRows_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_DeleteDataStoreTableRows_String, this ) );
    TSToolMenus.Commands_Datastore_DeleteDataStoreTableRows_JMenuItem.setToolTipText("Delete datastore table rows.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_ReadTimeSeriesFromDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_ReadTimeSeriesFromDataStore_String, this) );
    TSToolMenus.Commands_Datastore_ReadTimeSeriesFromDataStore_JMenuItem.setToolTipText("Read time series from database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_WriteTimeSeriesToDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_WriteTimeSeriesToDataStore_String, this) );
    TSToolMenus.Commands_Datastore_WriteTimeSeriesToDataStore_JMenuItem.setToolTipText("Write time series to database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_CloseDataStore_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_CloseDataStore_String, this) );
    TSToolMenus.Commands_Datastore_CloseDataStore_JMenuItem.setToolTipText("Close a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add(TSToolMenus.Commands_Datastore_CreateDataStoreDataDictionary_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Datastore_CreateDataStoreDataDictionary_String, this) );
    TSToolMenus.Commands_Datastore_CreateDataStoreDataDictionary_JMenuItem.setToolTipText("Create an HTML database dictionary for a database datastore.");
    TSToolMenus.Commands_Datastore_JMenu.addSeparator();
    TSToolMenus.Commands_Datastore_JMenu.add (TSToolMenus.Commands_Datastore_SetPropertyFromDataStore_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_SetPropertyFromDataStore_String,this));
    TSToolMenus.Commands_Datastore_SetPropertyFromDataStore_JMenuItem.setToolTipText(
    	"Set a processor property from a datastore, to use as ${Property} in commands parameters.");

    // Menu: Commands / Ensemble processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add ( TSToolMenus.Commands_Ensemble_JMenu = new JMenu(TSToolConstants.Commands_Ensemble_String) );
    //TSToolMenus.Commands_Ensemble_JMenu.setToolTipText("Process ensembles (groups of related time series).");
    TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_String, this) );
    TSToolMenus.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_JMenuItem.setToolTipText("Create a time series ensemble from one time series.");
    TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_CopyEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_CopyEnsemble_String, this) );
    TSToolMenus.Commands_Ensemble_CopyEnsemble_JMenuItem.setToolTipText("Copy a time series ensemble to a new ensemble.");
    TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_NewEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_NewEnsemble_String, this) );
    TSToolMenus.Commands_Ensemble_NewEnsemble_JMenuItem.setToolTipText("Create a new time series ensemble.");

    if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
        TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_ReadNwsrfsEspTraceEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_ReadNwsrfsEspTraceEnsemble_String, this) );
        TSToolMenus.Commands_Ensemble_ReadNwsrfsEspTraceEnsemble_JMenuItem.setToolTipText(
        	"Read time series ensemble from National Weather Service (NWS) River Forecast System (RFS) " +
            "ensemble stremaflow prediction binary format file.");
    }

    TSToolMenus.Commands_Ensemble_JMenu.addSeparator();
    TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_String, this) );
    TSToolMenus.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_JMenuItem.setToolTipText("Insert time series into a time series ensemble.");
    TSToolMenus.Commands_Ensemble_JMenu.add( TSToolMenus.Commands_Ensemble_SetEnsembleProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_SetEnsembleProperty_String, this) );
    TSToolMenus.Commands_Ensemble_SetEnsembleProperty_JMenuItem.setToolTipText("Set time series ensemble property.");

    TSToolMenus.Commands_Ensemble_JMenu.addSeparator();
    TSToolMenus.Commands_Ensemble_JMenu.add ( TSToolMenus.Commands_Ensemble_NewStatisticEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_NewStatisticEnsemble_String, this ) );
    TSToolMenus.Commands_Ensemble_NewStatisticEnsemble_JMenuItem.setToolTipText(
    	"Create a new time series ensemble where each time series in the ensemble is a statistic time series.");
    TSToolMenus.Commands_Ensemble_JMenu.add ( TSToolMenus.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_String, this ) );
    TSToolMenus.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_JMenuItem.setToolTipText(
    	"Create a new time series as a statistic computed from input ensemble.");

    TSToolMenus.Commands_Ensemble_JMenu.add ( TSToolMenus.Commands_Ensemble_WeightTraces_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Ensemble_WeightTraces_String, this ) );
    TSToolMenus.Commands_Ensemble_WeightTraces_JMenuItem.setToolTipText("Create a time series by weighting ensemble trace time series.");
    if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
        TSToolMenus.Commands_Ensemble_JMenu.addSeparator();
        TSToolMenus.Commands_Ensemble_JMenu.add ( TSToolMenus.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_JMenuItem =
            new SimpleJMenuItem(TSToolConstants.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_String,this ));
        TSToolMenus.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_JMenuItem.setToolTipText(
        	"Write time series ensemble to National Weather Service (NWS) River Forecast System (RFS)" +
        	" Ensemble Streamflow Prediction (ESP) binary file.");
    }

    // Menu: Commands / Network Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Network_JMenu = new JMenu( TSToolConstants.Commands_Network_String, true ) );
    //TSToolMenus.Commands_Network_JMenu.setToolTipText("Process time series associated with network of nodes and links.");
    TSToolMenus.Commands_Network_JMenu.add( TSToolMenus.Commands_Network_CreateNetworkFromTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Network_CreateNetworkFromTable_String, this ) );
    TSToolMenus.Commands_Network_CreateNetworkFromTable_JMenuItem.setToolTipText("Create a network from data in a table.");
    TSToolMenus.Commands_Network_JMenu.addSeparator();
    TSToolMenus.Commands_Network_JMenu.add( TSToolMenus.Commands_Network_AnalyzeNetworkPointFlow_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Network_AnalyzeNetworkPointFlow_String, this ) );
    TSToolMenus.Commands_Network_AnalyzeNetworkPointFlow_JMenuItem.setToolTipText(
    	"Analyze a network point flow model and create output time series at each network node.");

    // Menu: Commands / Object Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Object_JMenu = new JMenu( TSToolConstants.Commands_Object_String, true ) );
    //TSToolMenus.Commands_Object_JMenu.setToolTipText("Process objects.");
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_NewObject_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_NewObject_String, this ) );
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_FreeObject_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_FreeObject_String, this ) );
    TSToolMenus.Commands_Object_JMenu.addSeparator();
    // Command is also in table read commands.
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_ReadTableFromJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromJSON_String, this ) );
    TSToolMenus.Commands_Object_JMenu.addSeparator();
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_SetObjectProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_SetObjectProperty_String, this ) );
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_SetObjectPropertiesFromTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_SetObjectPropertiesFromTable_String, this ) );
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_SetPropertyFromObject_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_SetPropertyFromObject_String, this ) );
    TSToolMenus.Commands_Object_JMenu.addSeparator();
    TSToolMenus.Commands_Object_JMenu.add( TSToolMenus.Commands_Object_WriteObjectToJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Object_WriteObjectToJSON_String, this ) );

    // Menu: Commands / Spatial Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Spatial_JMenu = new JMenu( TSToolConstants.Commands_Spatial_String, true ) );
    //TSToolMenus.Commands_Spatial_JMenu.setToolTipText("Process spatial data).");
    TSToolMenus.Commands_Spatial_JMenu.add( TSToolMenus.Commands_Spatial_WriteTableToGeoJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spatial_WriteTableToGeoJSON_String, this ) );
    TSToolMenus.Commands_Spatial_WriteTableToGeoJSON_JMenuItem.setToolTipText("Write a table with coordinate data to a GeoJSON file.");
    TSToolMenus.Commands_Spatial_JMenu.add( TSToolMenus.Commands_Spatial_WriteTableToKml_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spatial_WriteTableToKml_String, this ) );
    TSToolMenus.Commands_Spatial_WriteTableToKml_JMenuItem.setToolTipText("Write a table with coordinate data to a KML file.");
    TSToolMenus.Commands_Spatial_JMenu.add( TSToolMenus.Commands_Spatial_WriteTableToShapefile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spatial_WriteTableToShapefile_String, this ) );
    TSToolMenus.Commands_Spatial_WriteTableToShapefile_JMenuItem.setToolTipText("Write a table with coordinate data to a shapefile.");
    TSToolMenus.Commands_Spatial_JMenu.addSeparator();
    TSToolMenus.Commands_Spatial_JMenu.add( TSToolMenus.Commands_Spatial_WriteTimeSeriesToGeoJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spatial_WriteTimeSeriesToGeoJSON_String, this ) );
    TSToolMenus.Commands_Spatial_WriteTimeSeriesToGeoJSON_JMenuItem.setToolTipText("Write time series with coordinate properties to a GeoJSON file.");
    TSToolMenus.Commands_Spatial_JMenu.add( TSToolMenus.Commands_Spatial_WriteTimeSeriesToKml_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spatial_WriteTimeSeriesToKml_String, this ) );
    TSToolMenus.Commands_Spatial_WriteTimeSeriesToKml_JMenuItem.setToolTipText("Write time series with coordinate properties to a KML file.");

    // Menu: Commands / Spreadsheet Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Spreadsheet_JMenu = new JMenu( TSToolConstants.Commands_Spreadsheet_String, true ) );
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_NewExcelWorkbook_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_NewExcelWorkbook_String, this ) );
    TSToolMenus.Commands_Spreadsheet_NewExcelWorkbook_JMenuItem.setToolTipText("Create a new Excel workbook file.");
    TSToolMenus.Commands_Spreadsheet_JMenu.addSeparator();
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_ReadExcelWorkbook_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_ReadExcelWorkbook_String, this ) );
    TSToolMenus.Commands_Spreadsheet_ReadExcelWorkbook_JMenuItem.setToolTipText("Read an Excel workbook file into TSTool memory.");
    TSToolMenus.Commands_Spreadsheet_JMenu.addSeparator();
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_ReadTableFromExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_ReadTableFromExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_ReadTableFromExcel_JMenuItem.setToolTipText("Read a table from an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_ReadTableCellsFromExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_ReadTableCellsFromExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_ReadTableCellsFromExcel_JMenuItem.setToolTipText("Read table cells from an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_ReadPropertiesFromExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_ReadPropertiesFromExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_ReadPropertiesFromExcel_JMenuItem.setToolTipText("Read processor properties from an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.addSeparator();
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_SetExcelCell_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_SetExcelCell_String, this ) );
    TSToolMenus.Commands_Spreadsheet_SetExcelCell_JMenuItem.setToolTipText("Set a specific Excel worksheet's cell's values.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_SetExcelWorksheetViewProperties_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_SetExcelWorksheetViewProperties_String, this ) );
    TSToolMenus.Commands_Spreadsheet_SetExcelWorksheetViewProperties_JMenuItem.setToolTipText("Set an Excel worksheet's view properties, such as freeze panes.");
    TSToolMenus.Commands_Spreadsheet_JMenu.addSeparator();
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_WriteTableToExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_WriteTableToExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_WriteTableToExcel_JMenuItem.setToolTipText("Write a table to an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_WriteTableCellsToExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_WriteTableCellsToExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_WriteTableCellsToExcel_JMenuItem.setToolTipText("Write specific table cells to an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_WriteTimeSeriesToExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcel_String, this ) );
    TSToolMenus.Commands_Spreadsheet_WriteTimeSeriesToExcel_JMenuItem.setToolTipText("Write time series to an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String, this ) );
    TSToolMenus.Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_JMenuItem.setToolTipText("Write time series to a block of cells in an Excel worksheet.");
    TSToolMenus.Commands_Spreadsheet_JMenu.addSeparator();
    TSToolMenus.Commands_Spreadsheet_JMenu.add( TSToolMenus.Commands_Spreadsheet_CloseExcelWorkbook_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_CloseExcelWorkbook_String, this ) );
    TSToolMenus.Commands_Spreadsheet_CloseExcelWorkbook_JMenuItem.setToolTipText("Close an Excel workbook.");

    // Menu: Commands / Table Processing

    ui_InitGUIMenus_CommandsTable(menuBar);

    // Menu: Commands(Plugin)

    TSTool_Plugin.getInstance(this).initGUIMenus_Commands(menuBar);

    // Menu: Commands / Template Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Template_JMenu = new JMenu( TSToolConstants.Commands_Template_String, true ) );
    //TSToolMenus.Commands_Template_JMenu.setToolTipText("Process templates (to handle dynamic logic and data).");
    TSToolMenus.Commands_Template_JMenu.add( TSToolMenus.Commands_Template_ExpandTemplateFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Template_ExpandTemplateFile_String, this ) );
    TSToolMenus.Commands_Template_ExpandTemplateFile_JMenuItem.setToolTipText("Expand a template file by providing processing properties and other data.");
    TSToolMenus.Commands_Template_JMenu.addSeparator();
    TSToolMenus.Commands_Template_JMenu.add (TSToolMenus.Commands_Template_Comments_Template_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_TemplateComment_String, this ) );
    TSToolMenus.Commands_Template_Comments_Template_JMenuItem.setToolTipText("Insert a comment indicating that the commmand file is a template.");

    // Menu: Commands / Visualization Processing

    TSToolMenus.Commands_JMenu.addSeparator();
    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Visualization_JMenu = new JMenu( TSToolConstants.Commands_Visualization_String, true ) );
    //TSToolMenus.Commands_Visualization_JMenu.setToolTipText("Automate creation of data visualization products.");
    TSToolMenus.Commands_Visualization_JMenu.add ( TSToolMenus.Commands_Visualization_ProcessTSProduct_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Visualization_ProcessTSProduct_String, this ) );
    TSToolMenus.Commands_Visualization_ProcessTSProduct_JMenuItem.setToolTipText("Process a time series product (*.tsp) file into a data product file (e.g., graph image).");
    TSToolMenus.Commands_Visualization_JMenu.add ( TSToolMenus.Commands_Visualization_ProcessRasterGraph_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Visualization_ProcessRasterGraph_String, this ) );
    TSToolMenus.Commands_Visualization_ProcessRasterGraph_JMenuItem.setToolTipText("Process time series into a raster graph (heat map) data product file (e.g., graph image).");
    TSToolMenus.Commands_Visualization_JMenu.addSeparator();
    TSToolMenus.Commands_Visualization_JMenu.add( TSToolMenus.Commands_Visualization_NewTreeView_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Visualization_NewTreeView_String, this ) );
    TSToolMenus.Commands_Visualization_NewTreeView_JMenuItem.setToolTipText("Create a new tree view in the Results / View tab with hierarchy organizing time series.");

    // Menu: Commands / General - Comments

	TSToolMenus.Commands_JMenu.addSeparator(); // Separate general commands from others.
	TSToolMenus.Commands_JMenu.addSeparator(); // Results in double separator.

    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_General_Comments_JMenu = new JMenu( TSToolConstants.Commands_General_Comments_String, true ) );
    //TSToolMenus.Commands_General_Comments_JMenu.setToolTipText("Insert comments.");
    TSToolMenus.Commands_General_Comments_JMenu.add ( TSToolMenus.Commands_General_Comments_Comment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_Comment_String, this ) );
    TSToolMenus.Commands_General_Comments_Comment_JMenuItem.setToolTipText("Insert a # comment.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_StartComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_StartComment_String, this ) );
    TSToolMenus.Commands_General_Comments_StartComment_JMenuItem.setToolTipText("Insert a /* (start comment).");
    TSToolMenus.Commands_General_Comments_JMenu.add( TSToolMenus.Commands_General_Comments_EndComment_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Comments_EndComment_String, this ) );
    TSToolMenus.Commands_General_Comments_EndComment_JMenuItem.setToolTipText("Insert a */ (end comment).");
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_AuthorComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_AuthorComment_String, this ) );
    TSToolMenus.Commands_General_Comments_AuthorComment_JMenuItem.setToolTipText("Insert an #@author comment - used for attribution.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_VersionComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_VersionComment_String, this ) );
    TSToolMenus.Commands_General_Comments_VersionComment_JMenuItem.setToolTipText("Insert a #@version comment.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_VersionDateComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_VersionDateComment_String, this ) );
    TSToolMenus.Commands_General_Comments_VersionDateComment_JMenuItem.setToolTipText("Insert a #@versionDate comment.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_SourceUrlComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_SourceUrlComment_String, this ) );
    TSToolMenus.Commands_General_Comments_SourceUrlComment_JMenuItem.setToolTipText("Insert a #@sourceUrl comment - location of the maintained command file.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_DocUrlComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_DocUrlComment_String, this ) );
    TSToolMenus.Commands_General_Comments_DocUrlComment_JMenuItem.setToolTipText("Insert a #@docUrl comment - documentation for the command file.");
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_ReadOnlyComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_ReadOnlyComment_String, this ) );
    TSToolMenus.Commands_General_Comments_ReadOnlyComment_JMenuItem.setToolTipText("Insert a #@readOnly comment - TSTool will not allow saving over the file.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_RunDiscoveryFalseComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_RunDiscoveryFalseComment_String, this ) );
    TSToolMenus.Commands_General_Comments_RunDiscoveryFalseComment_JMenuItem.setToolTipText("Insert a #@runDiscovery False comment - TSTool will not run discovery when loading the file.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_TemplateComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_TemplateComment_String, this ) );
    TSToolMenus.Commands_General_Comments_TemplateComment_JMenuItem.setToolTipText("Insert a #@template comment - TSTool will treat the command file as a template to be expanded.");
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_EnabledComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_EnabledComment_String, this ) );
    TSToolMenus.Commands_General_Comments_EnabledComment_JMenuItem.setToolTipText("Insert a #@enabled True|False comment - if False, TSTool will ignore when running as a test.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_EnabledIfApplicationComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_EnabledIfApplicationComment_String, this ) );
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_EnabledIfDatastoreComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_EnabledIfDatastoreComment_String, this ) );
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_ExpectedStatusFailureComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_ExpectedStatusFailureComment_String, this ) );
    TSToolMenus.Commands_General_Comments_ExpectedStatusFailureComment_JMenuItem.setToolTipText("Insert a #@expectedStatus Failure comment - used with testing to indicate expected status.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_ExpectedStatusWarningComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_ExpectedStatusWarningComment_String, this ) );
    TSToolMenus.Commands_General_Comments_ExpectedStatusWarningComment_JMenuItem.setToolTipText("Insert a #@expectedStatus Warning comment - used with testing to indicate expected status.");
    /* TODO smalers 2021-06-13 add if CheckFile does not do enough needed
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_FileModTimeComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_FileModTimeComment_String, this ) );
    TSToolMenus.Commands_General_Comments_FileModTimeComment_JMenuItem.setToolTipText("Insert a #@fileModTime file1 > file2 comment - compare file modification times.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_FileSizeComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_FileSizeComment_String, this ) );
    TSToolMenus.Commands_General_Comments_FileSizeComment_JMenuItem.setToolTipText("Insert a #@fileSize file1 > size comment - compare file size.");
    */
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_IdComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_IdComment_String, this ) );
    TSToolMenus.Commands_General_Comments_IdComment_JMenuItem.setToolTipText("Insert an #@id CommandFileId comment - identify the command file.");
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_OrderComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_OrderComment_String, this ) );
    TSToolMenus.Commands_General_Comments_OrderComment_JMenuItem.setToolTipText("Insert an #@order CommandFileId comment - used to order tests.");
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_RequireApplicationComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_RequireApplicationComment_String, this ) );
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_RequireDatastoreComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_RequireDatastoreComment_String, this ) );
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_RequireUserComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_RequireUserComment_String, this ) );
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_FixMeComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_FixMeComment_String, this ) );
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_ToDoComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_ToDoComment_String, this ) );
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_DocExampleComment_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_DocExampleComment_String, this ) );
    // ---------
    TSToolMenus.Commands_General_Comments_JMenu.addSeparator();
    TSToolMenus.Commands_General_Comments_JMenu.add (TSToolMenus.Commands_General_Comments_Empty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Comments_Empty_String, this ) );
    TSToolMenus.Commands_General_Comments_Empty_JMenuItem.setToolTipText("Insert a empty (blank) line, to improve readability of the command file.");

    // Menu: Commands / General - File Handling

    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_General_FileHandling_JMenu = new JMenu( TSToolConstants.Commands_General_FileHandling_String, true ) );
    //TSToolMenus.Commands_General_FileHandling_JMenu.setToolTipText("Manipulate files.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_FTPGet_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_FTPGet_String, this ) );
    TSToolMenus.Commands_General_FileHandling_FTPGet_JMenuItem.setToolTipText("Retrieve a file from an FTP site and save as a local file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_WebGet_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_WebGet_String, this ) );
    TSToolMenus.Commands_General_FileHandling_WebGet_JMenuItem.setToolTipText("Retrieve a file from an web site URL and save as a local file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.addSeparator();
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_CreateFolder_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_CreateFolder_String, this ) );
    TSToolMenus.Commands_General_FileHandling_CreateFolder_JMenuItem.setToolTipText("Create a file and optionally all parent folders.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_RemoveFolder_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_RemoveFolder_String, this ) );
    TSToolMenus.Commands_General_FileHandling_RemoveFolder_JMenuItem.setToolTipText("Remove a folder and all of its contents.");
    TSToolMenus.Commands_General_FileHandling_JMenu.addSeparator();
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_AppendFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_AppendFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_AppendFile_JMenuItem.setToolTipText("Append a file to another file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_CheckFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_CheckFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_CheckFile_JMenuItem.setToolTipText("Check a file's contents.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_CopyFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_CopyFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_CopyFile_JMenuItem.setToolTipText("Copy a file to a new file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_FormatFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_FormatFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_FormatFile_JMenuItem.setToolTipText("Format a file, for example for web output.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_ListFiles_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_ListFiles_String, this ) );
    TSToolMenus.Commands_General_FileHandling_ListFiles_JMenuItem.setToolTipText("List files in a folder and save in a table.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_RemoveFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_RemoveFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_RemoveFile_JMenuItem.setToolTipText("Remove a file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_TextEdit_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_TextEdit_String, this ) );
    TSToolMenus.Commands_General_FileHandling_TextEdit_JMenuItem.setToolTipText("Edit a file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.addSeparator();
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_PDFMerge_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_PDFMerge_String, this ) );
    TSToolMenus.Commands_General_FileHandling_PDFMerge_JMenuItem.setToolTipText("Merge PDF files.");
    TSToolMenus.Commands_General_FileHandling_JMenu.addSeparator();
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_UnzipFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_UnzipFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_UnzipFile_JMenuItem.setToolTipText("Unzip a zip file.");
    TSToolMenus.Commands_General_FileHandling_JMenu.addSeparator();
    TSToolMenus.Commands_General_FileHandling_JMenu.add ( TSToolMenus.Commands_General_FileHandling_PrintTextFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_FileHandling_PrintTextFile_String, this ) );
    TSToolMenus.Commands_General_FileHandling_PrintTextFile_JMenuItem.setToolTipText("Print a text file to a printer.");

    // Menu: Commands / General - Logging and Messaging

	TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_General_Logging_JMenu = new JMenu( TSToolConstants.Commands_General_Logging_String, true ) );
	//TSToolMenus.Commands_General_Logging_JMenu.setToolTipText("Control logging (tracking).");
	TSToolMenus.Commands_General_Logging_JMenu.add(TSToolMenus.Commands_General_Logging_ConfigureLogging_JMenuItem =
	    new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_ConfigureLogging_String, this ) );
    TSToolMenus.Commands_General_Logging_ConfigureLogging_JMenuItem.setToolTipText("Configure logging properties, useful for testing.");
	TSToolMenus.Commands_General_Logging_JMenu.add(TSToolMenus.Commands_General_Logging_StartLog_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_StartLog_String, this ) );
    TSToolMenus.Commands_General_Logging_StartLog_JMenuItem.setToolTipText("(Re)start the log file.");
	TSToolMenus.Commands_General_Logging_JMenu.add (TSToolMenus.Commands_General_Logging_SetDebugLevel_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_SetDebugLevel_String, this ) );
    TSToolMenus.Commands_General_Logging_SetDebugLevel_JMenuItem.setToolTipText("Set the logging level for debug messages.");
	TSToolMenus.Commands_General_Logging_JMenu.add ( TSToolMenus.Commands_General_Logging_SetWarningLevel_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_SetWarningLevel_String, this ) );
    TSToolMenus.Commands_General_Logging_SetWarningLevel_JMenuItem.setToolTipText("Set the logging level for warning messages.");
	TSToolMenus.Commands_General_Logging_JMenu.addSeparator();
    TSToolMenus.Commands_General_Logging_JMenu.add ( TSToolMenus.Commands_General_Logging_Message_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_Message_String, this ) );
    TSToolMenus.Commands_General_Logging_Message_JMenuItem.setToolTipText(
    	"Output a message to the logging system, including log file, and set command status.");
    TSToolMenus.Commands_General_Logging_JMenu.add ( TSToolMenus.Commands_General_Logging_SendEmailMessage_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Logging_SendEmailMessage_String, this ) );
    TSToolMenus.Commands_General_Logging_SendEmailMessage_JMenuItem.setToolTipText("Send an email message.");

    // Menu: Commands / General - Running and Properties

    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_General_Running_JMenu = new JMenu( TSToolConstants.Commands_General_Running_String, true ) );
    //TSToolMenus.Commands_General_Running_JMenu.setToolTipText("Run external programs, command files, Python.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_ReadPropertiesFromFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_ReadPropertiesFromFile_String, this ) );
    TSToolMenus.Commands_General_Running_ReadPropertiesFromFile_JMenuItem.setToolTipText("Read processor properties from a file, various formats are supported.");
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_SetProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_SetProperty_String,this));
    TSToolMenus.Commands_General_Running_SetProperty_JMenuItem.setToolTipText("Set a processor property to use as ${Property} in commands parameters.");
    if ( this.__source_NWSRFS_FS5Files_enabled ) {
        TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_SetPropertyFromNwsrfsAppDefault_JMenuItem =
        	new SimpleJMenuItem( TSToolConstants.Commands_General_Running_SetPropertyFromNwsrfsAppDefault_String,this));
        TSToolMenus.Commands_General_Running_SetPropertyFromNwsrfsAppDefault_JMenuItem.setToolTipText(
        	"Set a processor property from National Weather Service (NWS) River Forecast System (RFS) application default property.");
    }
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_SetPropertyFromEnsemble_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_SetPropertyFromEnsemble_String,this));
    TSToolMenus.Commands_General_Running_SetPropertyFromEnsemble_JMenuItem.setToolTipText(
    	"Set a processor property from a time series ensemble, to use as ${Property} in commands parameters.");
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_SetPropertyFromTimeSeries_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_SetPropertyFromTimeSeries_String,this));
    TSToolMenus.Commands_General_Running_SetPropertyFromTimeSeries_JMenuItem.setToolTipText(
    	"Set a processor property from a time series, to use as ${Property} in commands parameters.");
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_FormatDateTimeProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_FormatDateTimeProperty_String,this));
    TSToolMenus.Commands_General_Running_FormatDateTimeProperty_JMenuItem.setToolTipText("Format a date/time property to use as ${Property} in command parameters.");
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_FormatStringProperty_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_FormatStringProperty_String,this));
    TSToolMenus.Commands_General_Running_FormatStringProperty_JMenuItem.setToolTipText("Format a string property to use as ${Property} in command parameters.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_WritePropertiesToFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_WritePropertiesToFile_String, this ) );
    TSToolMenus.Commands_General_Running_WritePropertiesToFile_JMenuItem.setToolTipText("Write processor properties to a file.");
    TSToolMenus.Commands_General_Running_JMenu.addSeparator();
    TSToolMenus.Commands_General_Running_JMenu.add (TSToolMenus.Commands_General_Running_RunCommands_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_RunCommands_String,this));
    TSToolMenus.Commands_General_Running_RunCommands_JMenuItem.setToolTipText("Run a command file, useful for testing and implementing modular workflows.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_RunProgram_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_RunProgram_String,this));
    TSToolMenus.Commands_General_Running_RunProgram_JMenuItem.setToolTipText("Run a program given the command line.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_RunPython_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_RunPython_String,this));
    TSToolMenus.Commands_General_Running_RunPython_JMenuItem.setToolTipText("Run a Python program.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_RunR_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_RunR_String,this));
    TSToolMenus.Commands_General_Running_RunR_JMenuItem.setToolTipText("Run an R script.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_RunDSSUTL_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_RunDSSUTL_String,this));
    TSToolMenus.Commands_General_Running_RunDSSUTL_JMenuItem.setToolTipText("Run the US Army Corps DSSUTL program.");
    TSToolMenus.Commands_General_Running_JMenu.addSeparator();
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_If_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_If_String, this ) );
    TSToolMenus.Commands_General_Running_If_JMenuItem.setToolTipText("Insert If block start.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_EndIf_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_EndIf_String, this ) );
    TSToolMenus.Commands_General_Running_EndIf_JMenuItem.setToolTipText("Insert If block end.");
    TSToolMenus.Commands_General_Running_JMenu.addSeparator();
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_For_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_For_String, this ) );
    TSToolMenus.Commands_General_Running_For_JMenuItem.setToolTipText("Insert For block start.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_EndFor_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_EndFor_String, this ) );
    TSToolMenus.Commands_General_Running_EndFor_JMenuItem.setToolTipText("Insert For block end.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_Break_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_Break_String, this ) );
    TSToolMenus.Commands_General_Running_EndFor_JMenuItem.setToolTipText("Insert For block break.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_Continue_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_Continue_String, this ) );
    TSToolMenus.Commands_General_Running_EndFor_JMenuItem.setToolTipText("Insert For block continue.");
    TSToolMenus.Commands_General_Running_JMenu.addSeparator();
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_Exit_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_Exit_String, this ) );
    TSToolMenus.Commands_General_Running_Exit_JMenuItem.setToolTipText("Exit command processing.");
    TSToolMenus.Commands_General_Running_JMenu.add ( TSToolMenus.Commands_General_Running_Wait_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_Running_Wait_String, this ) );
    TSToolMenus.Commands_General_Running_Wait_JMenuItem.setToolTipText("Wait for a time before resuming running the workflow.");
    TSToolMenus.Commands_General_Running_JMenu.addSeparator();
	TSToolMenus.Commands_General_Running_JMenu.add(TSToolMenus.Commands_General_Running_SetWorkingDir_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_SetWorkingDir_String, this ) );
    TSToolMenus.Commands_General_Running_SetWorkingDir_JMenuItem.setToolTipText("Set the working directory - PHASING OUT.");
    TSToolMenus.Commands_General_Running_JMenu.add(TSToolMenus.Commands_General_Running_ProfileCommands_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_Running_ProfileCommands_String, this ) );
    TSToolMenus.Commands_General_Running_ProfileCommands_JMenuItem.setToolTipText(
    	"Save additional information about each command's run time, to optimize software and workflows.");

    // Menu: Commands / General - Test Processing

    TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_General_TestProcessing_JMenu = new JMenu( TSToolConstants.Commands_General_TestProcessing_String, true ) );
    //TSToolMenus.Commands_General_TestProcessing_JMenu.setToolTipText("Test the software and processes.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_String, this ) );
    TSToolMenus.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_JMenuItem.setToolTipText("Write time series properties to a file, facilitates testing.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_WriteTimeSeriesProperty_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesProperty_String, this ) );
    TSToolMenus.Commands_General_TestProcessing_WriteTimeSeriesProperty_JMenuItem.setToolTipText("Write time series property to a file, facilitates testing - PHASING OUT.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.addSeparator();
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_CompareFiles_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_General_TestProcessing_CompareFiles_String, this ) );
    // The following menu is also in Tables menu
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_CompareTables_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_TableAnalyze_CompareTables_String, this ) );
    // The following menu is also in Time Series menu
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_CompareTimeSeries_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Commands_Analyze_CompareTimeSeries_String, this ) );
    TSToolMenus.Commands_General_TestProcessing_CompareFiles_JMenuItem.setToolTipText("Compare two files, used in testing.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.addSeparator();
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_CreateRegressionTestCommandFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_TestProcessing_CreateRegressionTestCommandFile_String, this ) );
    TSToolMenus.Commands_General_TestProcessing_CreateRegressionTestCommandFile_JMenuItem.setToolTipText("Create test suite to run multiple testing command files.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.add (TSToolMenus.Commands_General_TestProcessing_StartRegressionTestResultsReport_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_TestProcessing_StartRegressionTestResultsReport_String,this));
    TSToolMenus.Commands_General_TestProcessing_StartRegressionTestResultsReport_JMenuItem.setToolTipText("Start the regression test report, used to save test results.");
    TSToolMenus.Commands_General_TestProcessing_JMenu.add ( TSToolMenus.Commands_General_TestProcessing_TestCommand_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_General_TestProcessing_TestCommand_String, this ) );
    TSToolMenus.Commands_General_TestProcessing_TestCommand_JMenuItem.setToolTipText("Command to test user interface features.");

    boolean includeDeprecated = false;
    if ( includeDeprecated ) {
    	// Add the deprecated menu if any datastores are enabled that have deprecated commands.
    	TSToolMenus.Commands_JMenu.addSeparator();
    	TSToolMenus.Commands_JMenu.addSeparator();

    	// Menu: Commands / General - Deprecated Commands

    	TSToolMenus.Commands_JMenu.add( TSToolMenus.Commands_Deprecated_JMenu = new JMenu( TSToolConstants.Commands_Deprecated_String, true ) );
    	// Handle each datastore type separately under the main menu.
    	if ( this.__source_HydroBase_enabled ) {
        	TSToolMenus.Commands_Deprecated_JMenu.setToolTipText("Commands that are slated for removal.");
        	TSToolMenus.Commands_Deprecated_JMenu.add (TSToolMenus.Commands_Deprecated_OpenHydroBase_JMenuItem =
            	new SimpleJMenuItem(TSToolConstants.Commands_Deprecated_OpenHydroBase_String, this ) );
        	TSToolMenus.Commands_Deprecated_OpenHydroBase_JMenuItem.setToolTipText(
        		"Open a HydroBase database connection.  Use datastores to configure database connections.");
    	}
    	TSToolMenus.Commands_Deprecated_JMenu.add ( TSToolMenus.Commands_Deprecated_RunningAverage_JMenuItem =
        	new SimpleJMenuItem(TSToolConstants.Commands_Deprecated_RunningAverage_String, this ) );
    	TSToolMenus.Commands_Deprecated_RunningAverage_JMenuItem.setToolTipText(
    		"Calculate a running average time series.  Replaced by the RunningStatisticTimeSeries command.");
    }
}

/**
Initialize the GUI "Commands(Table)" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_CommandsTable ( JMenuBar menuBar ) {
    menuBar.add( TSToolMenus.Commands_Table_JMenu = new JMenu( TSToolConstants.Commands_Table_String, true ) );
	TSToolMenus.Commands_Table_JMenu.setToolTipText("Insert command into commands list (above first selected command, or at end).");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableCreate_JMenu = new JMenu( TSToolConstants.Commands_TableCreate_String, true ) );
    //TSToolMenus.Commands_TableCreate_JMenu.setToolTipText("Create new tables.");
    TSToolMenus.Commands_TableCreate_JMenu.add( TSToolMenus.Commands_TableCreate_NewTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableCreate_NewTable_String, this ) );
    TSToolMenus.Commands_TableCreate_NewTable_JMenuItem.setToolTipText("Create a new table by defining column names and data types.");
    TSToolMenus.Commands_TableCreate_JMenu.add( TSToolMenus.Commands_TableCreate_CopyTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableCreate_CopyTable_String, this ) );
    TSToolMenus.Commands_TableCreate_CopyTable_JMenuItem.setToolTipText("Copy a table, with filters to copy a subset of columns and rows.");
    TSToolMenus.Commands_TableCreate_JMenu.addSeparator();
    TSToolMenus.Commands_TableCreate_JMenu.add( TSToolMenus.Commands_TableCreate_FreeTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableCreate_FreeTable_String, this ) );
    TSToolMenus.Commands_TableCreate_FreeTable_JMenuItem.setToolTipText("Delete a table and free memory used by the table.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableRead_JMenu = new JMenu( TSToolConstants.Commands_TableRead_String, true ) );
    //TSToolMenus.Commands_TableRead_JMenu.setToolTipText("Read tables.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromDataStore_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_ReadTableFromDataStore_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromDataStore_JMenuItem.setToolTipText("Read a table from a database datastore.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromDBF_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromDBF_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromDBF_JMenuItem.setToolTipText(
    	"Read a table from a dBASE database binary file, with column properties take from database.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromDelimitedFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromDelimitedFile_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromDelimitedFile_JMenuItem.setToolTipText(
    	"Read a table from a delimited file (CSV, tab-delimited, etc.).");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_ReadTableFromExcel_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromExcel_JMenuItem.setToolTipText("Read a table from an Excel worksheet, using Excel data types.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromFixedFormatFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromFixedFormatFile_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromFixedFormatFile_JMenuItem.setToolTipText("Read a table from a fixed-format text file with constant column widths.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromJSON_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromJSON_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromJSON_JMenuItem.setToolTipText("Read a table from a JSON text file.");
    TSToolMenus.Commands_TableRead_JMenu.add( TSToolMenus.Commands_TableRead_ReadTableFromXML_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableRead_ReadTableFromXML_String, this ) );
    TSToolMenus.Commands_TableRead_ReadTableFromXML_JMenuItem.setToolTipText("Read a table from an XML text file.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableJoin_JMenu = new JMenu( TSToolConstants.Commands_TableJoin_String, true ) );
    //TSToolMenus.Commands_TableJoin_JMenu.setToolTipText("Append/join tables.");
    TSToolMenus.Commands_TableJoin_JMenu.add( TSToolMenus.Commands_TableJoin_AppendTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableJoin_AppendTable_String, this ) );
    TSToolMenus.Commands_TableJoin_AppendTable_JMenuItem.setToolTipText("Append one table to another (add rows from one to the other).");
    TSToolMenus.Commands_TableJoin_JMenu.add( TSToolMenus.Commands_TableJoin_JoinTables_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableJoin_JoinTables_String, this ) );
    TSToolMenus.Commands_TableJoin_JoinTables_JMenuItem.setToolTipText("Join one table to another (add columns from one table to the other).");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableTimeSeries_JMenu = new JMenu( TSToolConstants.Commands_TableTimeSeries_String, true ) );
    //TSToolMenus.Commands_TableTimeSeries_JMenu.setToolTipText("Processing tables to/from time series.");
    TSToolMenus.Commands_TableTimeSeries_JMenu.add( TSToolMenus.Commands_TableTimeSeries_TimeSeriesToTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableTimeSeries_TimeSeriesToTable_String, this ) );
    TSToolMenus.Commands_TableTimeSeries_TimeSeriesToTable_JMenuItem.setToolTipText("Convert time series to a table.");
    TSToolMenus.Commands_TableTimeSeries_JMenu.add( TSToolMenus.Commands_TableTimeSeries_TableToTimeSeries_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableTimeSeries_TableToTimeSeries_String, this ) );
    TSToolMenus.Commands_TableTimeSeries_TableToTimeSeries_JMenuItem.setToolTipText("Convert a table to time series.");
    TSToolMenus.Commands_TableTimeSeries_JMenu.addSeparator();
    TSToolMenus.Commands_TableTimeSeries_JMenu.add( TSToolMenus.Commands_TableTimeSeries_CreateTimeSeriesEventTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableTimeSeries_CreateTimeSeriesEventTable_String, this ) );
    TSToolMenus.Commands_TableTimeSeries_CreateTimeSeriesEventTable_JMenuItem.setToolTipText("Create a table listing events from time series.");
    TSToolMenus.Commands_TableTimeSeries_JMenu.addSeparator();
    TSToolMenus.Commands_TableTimeSeries_JMenu.add( TSToolMenus.Commands_TableTimeSeries_SetTimeSeriesPropertiesFromTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableTimeSeries_SetTimeSeriesPropertiesFromTable_String, this ) );
    TSToolMenus.Commands_TableTimeSeries_SetTimeSeriesPropertiesFromTable_JMenuItem.setToolTipText("Set time series properties from values in a table.");
    TSToolMenus.Commands_TableTimeSeries_JMenu.add( TSToolMenus.Commands_TableTimeSeries_CopyTimeSeriesPropertiesToTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableTimeSeries_CopyTimeSeriesPropertiesToTable_String, this ) );
    TSToolMenus.Commands_TableTimeSeries_CopyTimeSeriesPropertiesToTable_JMenuItem.setToolTipText("Copy time series properties to values in a table.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableManipulate_JMenu = new JMenu( TSToolConstants.Commands_TableManipulate_String, true ) );
    //TSToolMenus.Commands_TableManipulate_JMenu.setToolTipText("Manipulate table contents.");
    // Add commands that manipulate table columns.
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_DeleteTableColumns_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_DeleteTableColumns_String, this ) );
    TSToolMenus.Commands_TableManipulate_DeleteTableColumns_JMenuItem.setToolTipText("Delete columns from a table.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_InsertTableColumn_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_InsertTableColumn_String, this ) );
    TSToolMenus.Commands_TableManipulate_InsertTableColumn_JMenuItem.setToolTipText("Insert a column into a table.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_RenameTableColumns_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_RenameTableColumns_String, this ) );
    TSToolMenus.Commands_TableManipulate_RenameTableColumns_JMenuItem.setToolTipText("Rename a table's columns.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_SplitTableColumn_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_SplitTableColumn_String, this ) );
    TSToolMenus.Commands_TableManipulate_SplitTableColumn_JMenuItem.setToolTipText("Split a table's column into multiple columns.");
    TSToolMenus.Commands_TableManipulate_JMenu.addSeparator();
    // Add commands that manipulate table rows.
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_DeleteTableRows_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_DeleteTableRows_String, this ) );
    TSToolMenus.Commands_TableManipulate_DeleteTableRows_JMenuItem.setToolTipText("Delete a table's rows based on criteria.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_InsertTableRow_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_InsertTableRow_String, this ) );
    TSToolMenus.Commands_TableManipulate_InsertTableRow_JMenuItem.setToolTipText("Insert a row into a table.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_SortTable_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_SortTable_String, this ) );
    TSToolMenus.Commands_TableManipulate_SortTable_JMenuItem.setToolTipText("Sort a table's rows.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_SplitTableRow_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_SplitTableRow_String, this ) );
    TSToolMenus.Commands_TableManipulate_SplitTableRow_JMenuItem.setToolTipText("Split a table's row into multiple rows.");
    // Manipulation of data.
    TSToolMenus.Commands_TableManipulate_JMenu.addSeparator();
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_FormatTableDateTime_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_FormatTableDateTime_String, this ) );
    TSToolMenus.Commands_TableManipulate_FormatTableDateTime_JMenuItem.setToolTipText("Format table date/time column, for example based on precision of date/time.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_FormatTableString_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_FormatTableString_String, this ) );
    TSToolMenus.Commands_TableManipulate_FormatTableString_JMenuItem.setToolTipText("Format a table string column values, for example format width and number of digits.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_ManipulateTableString_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_ManipulateTableString_String, this ) );
    TSToolMenus.Commands_TableManipulate_ManipulateTableString_JMenuItem.setToolTipText("Manipulate a table string column, for example concatenate string column values.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_SetTableColumnProperties_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_SetTableColumnProperties_String, this ) );
    TSToolMenus.Commands_TableManipulate_SetTableColumnProperties_JMenuItem.setToolTipText("Set table column properties.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_SetTableValues_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_SetTableValues_String, this ) );
    TSToolMenus.Commands_TableManipulate_SetTableValues_JMenuItem.setToolTipText("Set table data values.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_TableMath_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_TableMath_String, this ) );
    TSToolMenus.Commands_TableManipulate_TableMath_JMenuItem.setToolTipText("Perform table math, for example adding column values.");
    TSToolMenus.Commands_TableManipulate_JMenu.add( TSToolMenus.Commands_TableManipulate_TableTimeSeriesMath_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableManipulate_TableTimeSeriesMath_String, this ) );
    TSToolMenus.Commands_TableManipulate_TableTimeSeriesMath_JMenuItem.setToolTipText("Perform table math involving column values and time series values.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableAnalyze_JMenu = new JMenu( TSToolConstants.Commands_TableAnalyze_String, true ) );
    //TSToolMenus.Commands_TableAnalyze_JMenu.setToolTipText("Analyze table.");
    TSToolMenus.Commands_TableAnalyze_JMenu.add( TSToolMenus.Commands_TableAnalyze_CompareTables_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableAnalyze_CompareTables_String, this ) );
    TSToolMenus.Commands_TableAnalyze_CompareTables_JMenuItem.setToolTipText("Compare tables, useful for testing.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableOutput_JMenu = new JMenu( TSToolConstants.Commands_TableOutput_String, true ) );
    //TSToolMenus.Commands_TableOutput_JMenu.setToolTipText("Output table.");
    TSToolMenus.Commands_TableOutput_JMenu.add( TSToolMenus.Commands_TableOutput_WriteTableToDataStore_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Datastore_WriteTableToDataStore_String, this ) );
    TSToolMenus.Commands_TableOutput_WriteTableToDataStore_JMenuItem.setToolTipText("Write a table to a database datastore.");
    TSToolMenus.Commands_TableOutput_JMenu.add( TSToolMenus.Commands_TableOutput_WriteTableToDelimitedFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableOutput_WriteTableToDelimitedFile_String, this ) );
    TSToolMenus.Commands_TableOutput_WriteTableToDelimitedFile_JMenuItem.setToolTipText("Write a table to a delimited file (CSV, tab-delimited, etc.).");
    TSToolMenus.Commands_TableOutput_JMenu.add( TSToolMenus.Commands_TableOutput_WriteTableToExcel_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_Spreadsheet_WriteTableToExcel_String, this ) );
    TSToolMenus.Commands_TableOutput_WriteTableToExcel_JMenuItem.setToolTipText("Write a table to an Excel worksheet.");
    TSToolMenus.Commands_TableOutput_JMenu.add( TSToolMenus.Commands_TableOutput_WriteTableToMarkdown_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableOutput_WriteTableToMarkdown_String, this ) );
    TSToolMenus.Commands_TableOutput_WriteTableToMarkdown_JMenuItem.setToolTipText("Write a table to an Markdown text file, for web data visualization.");
    TSToolMenus.Commands_TableOutput_JMenu.add( TSToolMenus.Commands_TableOutput_WriteTableToHTML_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Commands_TableOutput_WriteTableToHTML_String, this ) );
    TSToolMenus.Commands_TableOutput_WriteTableToHTML_JMenuItem.setToolTipText("Write a table to an HTML text file, for web data visualization.");

    TSToolMenus.Commands_Table_JMenu.add( TSToolMenus.Commands_TableRunning_JMenu = new JMenu( TSToolConstants.Commands_TableRunning_String, true ) );
    //TSToolMenus.Commands_TableRunning_JMenu.setToolTipText("Commands to integrate table data with processor properties.");
    TSToolMenus.Commands_TableRunning_JMenu.add( TSToolMenus.Commands_TableRunning_SetPropertyFromTable_JMenuItem =
         new SimpleJMenuItem( TSToolConstants.Commands_TableRunning_SetPropertyFromTable_String, this ) );
    TSToolMenus.Commands_TableRunning_SetPropertyFromTable_JMenuItem.setToolTipText("Set a processor property from a table to use ${Property} in command parameters.");
    TSToolMenus.Commands_TableRunning_JMenu.add( TSToolMenus.Commands_TableRunning_CopyPropertiesToTable_JMenuItem =
         new SimpleJMenuItem( TSToolConstants.Commands_TableRunning_CopyPropertiesToTable_String, this ) );
    TSToolMenus.Commands_TableRunning_CopyPropertiesToTable_JMenuItem.setToolTipText("Copy processor properties to a table.");
}

/**
Define the popup menu for the commands area.
In some cases the words that are shown are different from the corresponding menu because the popup mixes submenus
from different menus and also popup menus are typically more abbreviated.
*/
private void ui_InitGUIMenus_CommandsPopup () {
	// Pop-up menu to manipulate commands.
	TSToolMenus.Commands_JPopupMenu = new JPopupMenu("Command Actions");
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_ShowCommandStatus_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.CommandsPopup_ShowCommandStatus_String, TSToolConstants.CommandsPopup_ShowCommandStatus_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_IndentRight_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.CommandsPopup_IndentRight_String, TSToolConstants.CommandsPopup_IndentRight_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_IndentLeft_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.CommandsPopup_IndentLeft_String, TSToolConstants.CommandsPopup_IndentLeft_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Edit_CommandWithErrorChecking_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Edit_String, TSToolConstants.Edit_CommandWithErrorChecking_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Edit_CommandAsText_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.CommandsPopup_Edit_AsText_String, TSToolConstants.CommandsPopup_Edit_AsText_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Cut_JMenuItem =
        new SimpleJMenuItem( "Cut", TSToolConstants.Edit_CutCommands_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Copy_JMenuItem =
        new SimpleJMenuItem ( "Copy", TSToolConstants.Edit_CopyCommands_String,this));
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Paste_JMenuItem=
        new SimpleJMenuItem("Paste (after last selected)", TSToolConstants.Edit_PasteCommands_String,this));
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add(TSToolMenus.CommandsPopup_Delete_JMenuItem=
		new SimpleJMenuItem( TSToolConstants.Edit_DeleteCommands_String, TSToolConstants.Edit_DeleteCommands_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_FindCommands_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.CommandsPopup_FindCommands_String, this));
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_SelectAll_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.Edit_SelectAllCommands_String, TSToolConstants.Edit_SelectAllCommands_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_DeselectAll_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Edit_DeselectAllCommands_String, TSToolConstants.Edit_DeselectAllCommands_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_ConvertSelectedCommandsToComments_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.Edit_ConvertSelectedCommandsToComments_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_ConvertSelectedCommandsFromComments_JMenuItem =
		new SimpleJMenuItem ( TSToolConstants.Edit_ConvertSelectedCommandsFromComments_String, this ) );
    TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadTimeSeries_JMenuItem =
        new SimpleJMenuItem ( TSToolConstants.Edit_ConvertTSIDTo_ReadTimeSeries_String, this ) );
    TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_ConvertTSIDTo_ReadCommand_JMenuItem =
        new SimpleJMenuItem ( TSToolConstants.Edit_ConvertTSIDTo_ReadCommand_String, this ) );
	TSToolMenus.Commands_JPopupMenu.addSeparator();
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Run_AllCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + TSToolConstants.Run_AllCommandsCreateOutput_String,
			TSToolConstants.Run_AllCommandsCreateOutput_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Run_AllCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + TSToolConstants.Run_AllCommandsIgnoreOutput_String,
			TSToolConstants.Run_AllCommandsIgnoreOutput_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Run_SelectedCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + TSToolConstants.Run_SelectedCommandsCreateOutput_String,
			TSToolConstants.Run_SelectedCommandsCreateOutput_String, this ) );
	TSToolMenus.Commands_JPopupMenu.add( TSToolMenus.CommandsPopup_Run_SelectedCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem ( "Run " + TSToolConstants.Run_SelectedCommandsIgnoreOutput_String,
			TSToolConstants.Run_SelectedCommandsIgnoreOutput_String, this ) );
}

/**
Initialize the GUI "Edit" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_Edit ( JMenuBar menuBar ) {
	TSToolMenus.Edit_JMenu = new JMenu( "Edit", true);
	menuBar.add( TSToolMenus.Edit_JMenu );

	TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_CutCommands_JMenuItem = new SimpleJMenuItem( TSToolConstants.Edit_CutCommands_String, this ) );
    TSToolMenus.Edit_CutCommands_JMenuItem.setToolTipText("Cut (delete) selected commands, will be able to paste elsewhere in the commands.");
	TSToolMenus.Edit_CutCommands_JMenuItem.setEnabled ( false );

	TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_CopyCommands_JMenuItem = new SimpleJMenuItem( TSToolConstants.Edit_CopyCommands_String, this ) );
    TSToolMenus.Edit_CopyCommands_JMenuItem.setToolTipText("Copy selected commands, will be able to paste elsewhere in the commands.");
	TSToolMenus.Edit_CopyCommands_JMenuItem.setEnabled ( false );

	TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_PasteCommands_JMenuItem = new SimpleJMenuItem( TSToolConstants.Edit_PasteCommands_String, this ) );
    TSToolMenus.Edit_PasteCommands_JMenuItem.setToolTipText("Paste selected commands after last selected command.");
	TSToolMenus.Edit_PasteCommands_JMenuItem.setEnabled ( false );

	TSToolMenus.Edit_JMenu.addSeparator( );

	TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_DeleteCommands_JMenuItem = new SimpleJMenuItem(TSToolConstants.Edit_DeleteCommands_String, this) );
    TSToolMenus.Edit_DeleteCommands_JMenuItem.setToolTipText("Delete selected commands.");
	TSToolMenus.Edit_DeleteCommands_JMenuItem.setEnabled ( false );

	TSToolMenus.Edit_JMenu.addSeparator( );

	TSToolMenus.Edit_JMenu.add(TSToolMenus.Edit_SelectAllCommands_JMenuItem = new SimpleJMenuItem( TSToolConstants.Edit_SelectAllCommands_String, this ) );
    TSToolMenus.Edit_SelectAllCommands_JMenuItem.setToolTipText("Select all commands.");
	TSToolMenus.Edit_JMenu.add(TSToolMenus.Edit_DeselectAllCommands_JMenuItem = new SimpleJMenuItem( TSToolConstants.Edit_DeselectAllCommands_String, this ) );
    TSToolMenus.Edit_DeselectAllCommands_JMenuItem.setToolTipText("Deselect all commands.");

	TSToolMenus.Edit_JMenu.addSeparator( );

	TSToolMenus.Edit_JMenu.add(TSToolMenus.Edit_CommandWithErrorChecking_JMenuItem = new SimpleJMenuItem(TSToolConstants.Edit_CommandWithErrorChecking_String, this ) );
    TSToolMenus.Edit_CommandWithErrorChecking_JMenuItem.setToolTipText("Edit the command using the command editor.");

	TSToolMenus.Edit_JMenu.addSeparator( );
	TSToolMenus.Edit_JMenu.add(TSToolMenus.Edit_ConvertSelectedCommandsToComments_JMenuItem=
		new SimpleJMenuItem (TSToolConstants.Edit_ConvertSelectedCommandsToComments_String, this ) );
    TSToolMenus.Edit_ConvertSelectedCommandsToComments_JMenuItem.setToolTipText("Convert selected commands to # commments.");
	TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_ConvertSelectedCommandsFromComments_JMenuItem =
		new SimpleJMenuItem (TSToolConstants.Edit_ConvertSelectedCommandsFromComments_String, this ) );
    TSToolMenus.Edit_ConvertSelectedCommandsFromComments_JMenuItem.setToolTipText("Convert selected # comments to commands.");
    TSToolMenus.Edit_JMenu.add(TSToolMenus.Edit_ConvertTSIDTo_ReadTimeSeries_JMenuItem=
        new SimpleJMenuItem (TSToolConstants.Edit_ConvertTSIDTo_ReadTimeSeries_String, this ) );
    TSToolMenus.Edit_ConvertTSIDTo_ReadTimeSeries_JMenuItem.setToolTipText("Convert selected TSID command to ReadTimeSeries command, provides more options.");
    TSToolMenus.Edit_JMenu.add( TSToolMenus.Edit_ConvertTSIDTo_ReadCommand_JMenuItem =
        new SimpleJMenuItem (TSToolConstants.Edit_ConvertTSIDTo_ReadCommand_String, this ) );
    TSToolMenus.Edit_ConvertTSIDTo_ReadCommand_JMenuItem.setToolTipText("Convert selected TSID command to corresponding read command - UNDER DEVELOPMENT.");
}

/**
Initialize the GUI "File" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_File ( JMenuBar menuBar ) {
 	TSToolMenus.File_JMenu = new JMenu( TSToolConstants.File_String, true );
	menuBar.add( TSToolMenus.File_JMenu );

	TSToolMenus.File_JMenu.add( TSToolMenus.File_New_JMenu=new JMenu(TSToolConstants.File_New_String,true));
    TSToolMenus.File_New_JMenu.add( TSToolMenus.File_New_CommandFile_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.File_New_CommandFile_String, this ) );
    TSToolMenus.File_New_CommandFile_JMenuItem.setToolTipText("Create a new command file by clearing current commands.");

	TSToolMenus.File_JMenu.add( TSToolMenus.File_Open_JMenu=new JMenu(TSToolConstants.File_Open_String,true));

	TSToolMenus.File_Open_JMenu.add( TSToolMenus.File_Open_CommandFile_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.File_Open_CommandFile_String, this ) );
    TSToolMenus.File_Open_CommandFile_JMenuItem.setToolTipText("Open a command file, starting in the folder of the previously opened command file.");
    TSToolMenus.File_Open_JMenu.add( TSToolMenus.File_Open_CommandFileNoDiscovery_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.File_Open_CommandFileNoDiscovery_String, this ) );
    TSToolMenus.File_Open_CommandFileNoDiscovery_JMenuItem.setToolTipText(
        "Open a command file for faster loading ... use for large command files that will not be interactively edited.");
    TSToolMenus.File_Open_JMenu.addSeparator();
    TSToolMenus.File_Open_CommandFileRecent_JMenuItem = new JMenuItem[TSToolConstants.MAX_RECENT_FILES];
    for ( int i = 0; i < TSToolConstants.MAX_RECENT_FILES; i++ ) {
	    TSToolMenus.File_Open_JMenu.add( TSToolMenus.File_Open_CommandFileRecent_JMenuItem[i] = new SimpleJMenuItem( "", this ) );
    }
    ui_InitGUIMenus_File_OpenRecentFiles();

	boolean separator_added = false;
	if ( __source_HydroBase_enabled ) {
		if ( !separator_added ) {
			TSToolMenus.File_Open_JMenu.addSeparator( );
			separator_added = true;
		}
		TSToolMenus.File_Open_JMenu.add (
			TSToolMenus.File_Open_HydroBase_JMenuItem = new SimpleJMenuItem( TSToolConstants.File_Open_HydroBase_String, this ) );
		TSToolMenus.File_Open_HydroBase_JMenuItem.setToolTipText(
			"Open a State of Colorado HydroBase database connection (legacy input type rather than datastore).");
	}
	if ( this.__source_ReclamationHDB_enabled ) {
		if ( !separator_added ) {
			TSToolMenus.File_Open_JMenu.addSeparator( );
			separator_added = true;
		}
		TSToolMenus.File_Open_JMenu.add (
			TSToolMenus.File_Open_ReclamationHDB_JMenuItem = new SimpleJMenuItem( TSToolConstants.File_Open_ReclamationHDB_String, this ) );
		TSToolMenus.File_Open_ReclamationHDB_JMenuItem.setToolTipText("Open a Reclamation HDB database datastore connection");
	}

	TSToolMenus.File_JMenu.add( TSToolMenus.File_Save_JMenu=new JMenu(TSToolConstants.File_Save_String,true));
	//TSToolMenus.File_Save_Commands_JMenuItem = new SimpleJMenuItem(
		//TSToolMenus.File_Save_Commands_String,TSToolMenus.File_Save_Commands_ActionString,this );
	TSToolMenus.File_Save_JMenu.add ( TSToolMenus.File_Save_Commands_JMenuItem = new SimpleJMenuItem( TSToolConstants.File_Save_Commands_String, this ) );
    TSToolMenus.File_Save_Commands_JMenuItem.setToolTipText("Save commands using the same name as the original.");
	TSToolMenus.File_Save_JMenu.add ( TSToolMenus.File_Save_CommandsAs_JMenuItem = new SimpleJMenuItem( TSToolConstants.File_Save_CommandsAs_String, this ) );
    TSToolMenus.File_Save_CommandsAs_JMenuItem.setToolTipText("Save commands using a new file name.");
    /*
	// TODO smalers 2023-02-19 remove ASAP since not used.
	TSToolMenus.File_Save_JMenu.add ( TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem =
	   new SimpleJMenuItem( TSToolConstants.File_Save_CommandsAsVersion9_String, this ) );
    TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem.setToolTipText("Save commands using a new file name, using Version 9 syntax.");
	TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem.setToolTipText ( "Save commands using a new file name, using old TS Alias = Command(...) syntax" );
    */
	TSToolMenus.File_Save_JMenu.addSeparator();
	TSToolMenus.File_Save_JMenu.add ( TSToolMenus.File_Save_TimeSeriesAs_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.File_Save_TimeSeriesAs_String, this ) );
    TSToolMenus.File_Save_TimeSeriesAs_JMenuItem.setToolTipText("Save time series results in a file, for commonly-used formats.");

	TSToolMenus.File_JMenu.add( TSToolMenus.File_CheckForUpdate_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.File_CheckForUpdate_String, this ) );

	TSToolMenus.File_JMenu.addSeparator( );

	TSToolMenus.File_JMenu.add( TSToolMenus.File_Print_JMenu=new JMenu(TSToolConstants.File_Print_String,true));
    TSToolMenus.File_Print_JMenu.add ( TSToolMenus.File_Print_Commands_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.File_Print_Commands_String,TSToolConstants.File_Print_Commands_String, this ) );
    TSToolMenus.File_Print_Commands_JMenuItem.setToolTipText("Print the commands.");

	TSToolMenus.File_JMenu.addSeparator( );

	TSToolMenus.File_JMenu.add( TSToolMenus.File_Properties_JMenu=new JMenu(TSToolConstants.File_Properties_String,true));

	TSToolMenus.File_Properties_JMenu.add(TSToolMenus.File_Properties_CommandsRun_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.File_Properties_CommandsRun_String, this ) );
    TSToolMenus.File_Properties_CommandsRun_JMenuItem.setToolTipText("View properties for the most recent command file run.");
	TSToolMenus.File_Properties_JMenu.add( TSToolMenus.File_Properties_TSToolSession_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.File_Properties_TSToolSession_String, this ) );
    TSToolMenus.File_Properties_TSToolSession_JMenuItem.setToolTipText("View properties for the current TSTool session.");

	boolean seperator_added = false;

	if ( this.__source_HydroBase_enabled ) {
		if ( !seperator_added ) {
			TSToolMenus.File_Properties_JMenu.addSeparator ();
			seperator_added = true;
		}
		TSToolMenus.File_Properties_JMenu.add ( TSToolMenus.File_Properties_HydroBase_JMenuItem =
			new SimpleJMenuItem( TSToolConstants.File_Properties_HydroBase_String, this ) );
		TSToolMenus.File_Properties_HydroBase_JMenuItem.setToolTipText("View Colorado HydroBae properties.");
	}

	TSToolMenus.File_JMenu.addSeparator( );
	TSToolMenus.File_JMenu.add ( TSToolMenus.File_SetWorkingDirectory_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.File_SetWorkingDirectory_String, this ));
	TSToolMenus.File_SetWorkingDirectory_JMenuItem.setToolTipText("Set working directory (folder) - PHASING OUT.");

	// Add a test menu.

	String args[] = IOUtil.getProgramArguments();
	int argc = 0;
	if ( args != null ) {
		argc = args.length;
	}
	for ( int i = 0; i < argc; i++ ) {
		if ( args[i].equalsIgnoreCase("-test") ) {
			IOUtil.testing(true);
			// Add a menu for testing.
			args = null;
			TSToolMenus.File_JMenu.add ( new SimpleJMenuItem( "Test", "Test",	this ) );
			break;
		}
	}
	args = null;

	TSToolMenus.File_JMenu.addSeparator( );
	TSToolMenus.File_JMenu.add( TSToolMenus.File_Exit_JMenuItem = new SimpleJMenuItem( TSToolConstants.File_Exit_String, this ) );
	TSToolMenus.File_Exit_JMenuItem.setToolTipText("Exit TSTool, with option to save unsaved work.");
}

/**
Reset the File / Open / Command Files (Recent) menu items to recent files.
*/
private void ui_InitGUIMenus_File_OpenRecentFiles () {
	List<String> history = this.session.readHistory();
	for ( int i = 0; i < TSToolConstants.MAX_RECENT_FILES; i++ ) {
		String filename = "";
		if ( i >= history.size() ) {
			filename = "";
		}
		else {
			// Long filenames will make the menu unwieldy so show the front and the back.
			// TODO smalers 2014-12-19 Find a way to replace parts of the path with "..." to shorten the menu.
			// Maybe add as an IOUtil method.
			filename = history.get(i);
		}
		TSToolMenus.File_Open_CommandFileRecent_JMenuItem[i].setText(filename);
		TSToolMenus.File_Open_CommandFileRecent_JMenuItem[i].setToolTipText(filename);
	}
}

/**
Initialize the GUI "Help" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_Help ( JMenuBar menuBar ) {
	TSToolMenus.Help_JMenu = new JMenu ( TSToolConstants.Help_String );
	menuBar.add ( TSToolMenus.Help_JMenu );
	// TODO - not implemented by Java?
	//menu_bar.setHelpMenu ( _help_JMenu );
	TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_AboutTSTool_JMenuItem = new SimpleJMenuItem(TSToolConstants.Help_AboutTSTool_String,this));
	TSToolMenus.Help_JMenu.addSeparator();
	File docFile = new File(IOUtil.verifyPathForOS(IOUtil.getApplicationHomeDir() + "/doc/UserManual/TSTool.pdf",true));
	if ( docFile.exists() ) {
	    // Old single-PDF help document:
	    // - TODO smalers 2013-01-08 Remove this when CDSS is only version of TSTool
		// - TODO smalers 2021-12-20 will probably never go back to local documentation
	    TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_JMenuItem = new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_String,this));
	}
	else {
	    // Newer convention where documents are split apart.
	    TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_ReleaseNotes_JMenuItem =
	       new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_ReleaseNotes_String,this));
       TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_UserManual_JMenuItem =
           new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_UserManual_String,this));
       TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_CommandReference_JMenuItem =
           new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_CommandReference_String,this));
       TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_DatastoreReference_JMenuItem =
           new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_DatastoreReference_String,this));
       TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ViewDocumentation_Troubleshooting_JMenuItem =
           new SimpleJMenuItem(TSToolConstants.Help_ViewDocumentation_Troubleshooting_String,this));

       TSToolMenus.Help_JMenu.addSeparator();
       TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_View_TrainingMaterials_JMenuItem =
           new SimpleJMenuItem(TSToolConstants.Help_View_TrainingMaterials_String,this));
	}
    TSToolMenus.Help_JMenu.addSeparator();
    TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_CheckForUpdates_JMenuItem = new SimpleJMenuItem(TSToolConstants.Help_CheckForUpdates_String,this));
    TSToolMenus.Help_JMenu.add ( TSToolMenus.Help_ImportConfiguration_JMenuItem = new SimpleJMenuItem(TSToolConstants.Help_ImportConfiguration_String,this));
}

/**
Initialize the GUI "Results" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_Results ( JMenuBar menuBar ) {
	menuBar.add( TSToolMenus.Results_JMenu = new JMenu( "Results", true ) );

	/* TODO smalers 2004-08-04 Add later?
	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_AnnualTraces_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Results_Graph_AnnualTraces_String, this));
	TSToolMenus.Results_Graph_AnnualTraces_JMenuItem.setEnabled ( false );
	*/

    TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_Area_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Graph_Area_String, this ) );

    TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_AreaStacked_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Graph_AreaStacked_String, this ) );

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_BarsLeft_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_BarsLeft_String, this ) );

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_BarsCenter_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_BarsCenter_String, this ));

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_BarsRight_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_BarsRight_String, this ));

	/* TODO smalers 2004-08-04 Add later?
	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_DoubleMass_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_DoubleMass_String, this));
	TSToolMenus.Results_Graph_DoubleMass_JMenuItem.setEnabled ( false );
	*/

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_Duration_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_Duration_String, this ));

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_Ensemble_JMenuItem =
		new SimpleJMenuItem( TSToolConstants.Results_Graph_Ensemble_String, this ));

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_Line_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Graph_Line_String, this ) );

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_LineLogY_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Graph_LineLogY_String, this ) );

	/* SAMX Not enabled
	_view_graph_percent_exceed_JMenuItem = new SimpleJMenuItem(
	"Percent Exceedance Curve", "GraphPercentExceed", this );
	_Results_JMenu.add( _view_graph_percent_exceed_JMenuItem );
	_view_graph_percent_exceed.setEnabled ( false );
	*/

	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Graph_PeriodOfRecord_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Results_Graph_PeriodOfRecord_String, this ) );

	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Graph_Point_JMenuItem=
        new SimpleJMenuItem( TSToolConstants.Results_Graph_Point_String, this ) );

	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Graph_PredictedValue_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Results_Graph_PredictedValue_String, this ) );

	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Graph_PredictedValueResidual_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Results_Graph_PredictedValueResidual_String, this ) );

    TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Graph_Raster_JMenuItem =
	    new SimpleJMenuItem(TSToolConstants.Results_Graph_Raster_String, this ) );

	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Graph_XYScatter_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Results_Graph_XYScatter_String, this ) );

	TSToolMenus.Results_JMenu.addSeparator();
	TSToolMenus.Results_JMenu.add( TSToolMenus.Results_Table_JMenuItem = new SimpleJMenuItem( TSToolConstants.Results_Table_String, this ) );

	TSToolMenus.Results_JMenu.addSeparator();
    TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Report_Summary_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Report_Summary_Html_String, this ) );
	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_Report_Summary_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_Report_Summary_Text_String, this ) );

	TSToolMenus.Results_JMenu.addSeparator();
    TSToolMenus.Results_JMenu.add(TSToolMenus.Results_TimeSeries_FindTimeSeries_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_TimeSeries_FindTimeSeries_String, this ) );
    TSToolMenus.Results_JMenu.add(TSToolMenus.Results_SelectAllForOutput_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_SelectAllForOutput_String, this ) );
    TSToolMenus.Results_JMenu.add(TSToolMenus.Results_DeselectAll_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_DeselectAll_String, this ) );

	TSToolMenus.Results_JMenu.addSeparator();
	TSToolMenus.Results_JMenu.add(TSToolMenus.Results_TimeSeriesProperties_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Results_TimeSeriesProperties_String, this ) );
}

/**
Define the popup menus for results.
*/
private void ui_InitGUIMenus_ResultsPopup () {
	this.__resultsTS_JPopupMenu = new JPopupMenu("TS Results Actions");
    this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Area_String, this ) );
    this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_AreaStacked_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_BarsLeft_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_BarsCenter_String,this));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_BarsRight_String, this ));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Duration_String, this ));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Ensemble_String, this ));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Line_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_LineLogY_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_PeriodOfRecord_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Point_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_PredictedValue_String, this));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_PredictedValueResidual_String, this));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_Raster_String, this));
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Graph_XYScatter_String, this));
	this.__resultsTS_JPopupMenu.addSeparator();
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Table_String, this ) );
	this.__resultsTS_JPopupMenu.addSeparator();
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Report_Summary_Html_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Report_Summary_Text_String, this ) );
	this.__resultsTS_JPopupMenu.addSeparator();
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_TimeSeries_FindTimeSeries_String, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.BUTTON_TS_SELECT_ALL, this ) );
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.BUTTON_TS_DESELECT_ALL, this ) );
	this.__resultsTS_JPopupMenu.addSeparator();
	this.__resultsTS_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_TimeSeriesProperties_String, this ) );

    ActionListener_ResultsEnsembles ens_l = new ActionListener_ResultsEnsembles(this);
    this.__resultsTSEnsembles_JPopupMenu = new JPopupMenu("Ensembles Results Actions");
    this.__resultsTSEnsembles_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Ensemble_Graph_Line_String, ens_l ) );
    this.__resultsTSEnsembles_JPopupMenu.addSeparator();
    this.__resultsTSEnsembles_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Ensemble_Table_String, ens_l ) );
    this.__resultsTSEnsembles_JPopupMenu.addSeparator();
    this.__resultsTSEnsembles_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Ensemble_Properties_String, ens_l ) );

    ActionListener_ResultsNetworks networks_l = new ActionListener_ResultsNetworks();
    this.__resultsNetworks_JPopupMenu = new JPopupMenu("Network Results Actions");
    this.__resultsNetworks_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Network_Properties_String, networks_l ) );

    ActionListener_ResultsObjects objects_l = new ActionListener_ResultsObjects();
    this.__resultsObjects_JPopupMenu = new JPopupMenu("Object Results Actions");
    this.__resultsObjects_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Object_Properties_String, objects_l ) );

    ActionListener_ResultsOutputFiles outputFiles_l = new ActionListener_ResultsOutputFiles();
    this.__resultsOutputFiles_JPopupMenu = new JPopupMenu("Output Files Results Actions");
    this.__resultsOutputFiles_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_OutputFile_FindOutputFiles_String, outputFiles_l ) );

    ActionListener_ResultsTables tables_l = new ActionListener_ResultsTables();
    this.__resultsTables_JPopupMenu = new JPopupMenu("Table Results Actions");
    this.__resultsTables_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Table_Properties_String, tables_l ) );
    this.__resultsTables_JPopupMenu.addSeparator();
    this.__resultsTables_JPopupMenu.add( new SimpleJMenuItem ( TSToolConstants.Results_Table_FindTables_String, tables_l ) );
}

/**
Initialize the GUI "Run" menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_Run ( JMenuBar menuBar ) {
 	TSToolMenus.Run_JMenu = new JMenu( "Run", true);
	TSToolMenus.Run_JMenu.setToolTipText("Run commands.  See also Run Selected Commands and Run All Commands buttons.");
	menuBar.add ( TSToolMenus.Run_JMenu );
	TSToolMenus.Run_JMenu.add( TSToolMenus.Run_AllCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_AllCommandsCreateOutput_String,this));
	TSToolMenus.Run_AllCommandsCreateOutput_JMenuItem.setToolTipText("Run all commands and create output files.");
	TSToolMenus.Run_JMenu.add( TSToolMenus.Run_AllCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_AllCommandsIgnoreOutput_String,this));
	TSToolMenus.Run_AllCommandsIgnoreOutput_JMenuItem.setToolTipText("Run all commands and ignore creating output files.");
	TSToolMenus.Run_JMenu.add( TSToolMenus.Run_SelectedCommandsCreateOutput_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_SelectedCommandsCreateOutput_String,this));
	TSToolMenus.Run_SelectedCommandsCreateOutput_JMenuItem.setToolTipText("Run selected commands and create output files.");
	TSToolMenus.Run_JMenu.add( TSToolMenus.Run_SelectedCommandsIgnoreOutput_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_SelectedCommandsIgnoreOutput_String,this));
	TSToolMenus.Run_SelectedCommandsIgnoreOutput_JMenuItem.setToolTipText("Run selected commands and ignore creating output files.");
	TSToolMenus.Run_JMenu.add ( TSToolMenus.Run_CancelCommandProcessing_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_CancelCommandProcessing_String,this));
	TSToolMenus.Run_CancelCommandProcessing_JMenuItem.setToolTipText("Stop processing commands after the current command completes running.");
	TSToolMenus.Run_JMenu.add ( TSToolMenus.Run_CancelCommandProcessingKill_JMenuItem =
	new SimpleJMenuItem(TSToolConstants.Run_CancelCommandProcessingKill_String,this));
	TSToolMenus.Run_CancelCommandProcessingKill_JMenuItem.setToolTipText("Interrupt processing immediately, may result in lost data.");
	/* TODO smalers 2009-04-10 Evaluate whether to allow this - the problem is that although the command processor
	 * is run on a thread, the individual commands are not and therefore if a process hangs,
	 * it is hung in the processor and the Process instances cannot be retrieved
    TSToolMenus.Run_JMenu.add ( TSToolMenus.Run_CancelAllCommandProcesses_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Run_CancelAllCommandProcesses_String,this));
             */
	TSToolMenus.Run_JMenu.addSeparator();
	TSToolMenus.Run_JMenu.add(TSToolMenus.Run_CommandsFromFile_JMenuItem =
	    new SimpleJMenuItem ( TSToolConstants.Run_CommandsFromFile_String, this ));
	TSToolMenus.Run_CommandsFromFile_JMenuItem.setToolTipText("Run commands in selected commmand file (will not load into TSTool main window).");
	TSToolMenus.Run_JMenu.addSeparator();
	TSToolMenus.Run_JMenu.add ( TSToolMenus.Run_ProcessTSProductPreview_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_ProcessTSProductPreview_String,this));
	TSToolMenus.Run_ProcessTSProductPreview_JMenuItem.setToolTipText("Process a time series product file (*.tsp) and preview the resulting product).");
	TSToolMenus.Run_JMenu.add ( TSToolMenus.Run_ProcessTSProductOutput_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Run_ProcessTSProductOutput_String,this));
	TSToolMenus.Run_ProcessTSProductOutput_JMenuItem.setToolTipText("Process a time series product file (*.tsp) to create output, but do not preview).");
}

/**
Initialize the GUI "Tools" menu.
@param menuBar menu bar to add menus
*/
private void ui_InitGUIMenus_Tools ( JMenuBar menuBar ) {
	TSToolMenus.Tools_JMenu = new JMenu();
	menuBar.add( TSToolMenus.Tools_JMenu = new JMenu( TSToolConstants.Tools_String, true ) );

	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_Analysis_JMenu = new JMenu(TSToolConstants.Tools_Analysis_String, true ) );

	TSToolMenus.Tools_Analysis_JMenu.add ( TSToolMenus.Tools_Analysis_MixedStationAnalysis_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_Analysis_MixedStationAnalysis_String, this ) );

	TSToolMenus.Tools_Analysis_JMenu.add ( TSToolMenus.Tools_Analysis_PrincipalComponentAnalysis_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_Analysis_PrincipalComponentAnalysis_String, this ) );

	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_Datastore_JMenu = new JMenu(TSToolConstants.Tools_Datastore_String, true ) );
	TSToolMenus.Tools_Datastore_JMenu.add(TSToolMenus.Tools_Datastore_ERDiagram_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_Datastore_ERDiagram_String, this ) );

	TSToolMenus.Tools_JMenu.add(TSToolMenus.Tools_DateTimeTools_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_DateTimeTools_String, this ) );

	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_Report_JMenu = new JMenu(TSToolConstants.Tools_Report_String, true ) );

	TSToolMenus.Tools_Report_JMenu.add(TSToolMenus.Tools_Report_DataCoverageByYear_JMenuItem=
        new SimpleJMenuItem(TSToolConstants.Tools_Report_DataCoverageByYear_String, this ) );

	TSToolMenus.Tools_Report_JMenu.add (TSToolMenus.Tools_Report_DataLimitsSummary_JMenuItem =
        new SimpleJMenuItem(TSToolConstants.Tools_Report_DataLimitsSummary_String, this ) );

	TSToolMenus.Tools_Report_JMenu.add (TSToolMenus.Tools_Report_MonthSummaryDailyMeans_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_Report_MonthSummaryDailyMeans_String, this ) );

	TSToolMenus.Tools_Report_JMenu.add (TSToolMenus.Tools_Report_MonthSummaryDailyTotals_JMenuItem =
		new SimpleJMenuItem(TSToolConstants.Tools_Report_MonthSummaryDailyTotals_String, this ) );

	TSToolMenus.Tools_Report_JMenu.add (TSToolMenus.Tools_Report_YearToDateTotal_JMenuItem =
        new SimpleJMenuItem( TSToolConstants.Tools_Report_YearToDateTotal_String, this ) );

	if ( this.__source_NWSRFS_FS5Files_enabled || this.__source_NWSCard_enabled || this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
		// Add NWSRFS-related tools (check all above because on non-UNIX system only card type may be enabled).
		TSToolMenus.Tools_JMenu.addSeparator ();
		TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_NWSRFS_JMenu = new JMenu(TSToolConstants.Tools_NWSRFS_String, true ) );

		TSToolMenus.Tools_NWSRFS_JMenu.add( TSToolMenus.Tools_NWSRFS_ConvertNWSRFSESPTraceEnsemble_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Tools_NWSRFS_ConvertNWSRFSESPTraceEnsemble_String,this ) );
		TSToolMenus.Tools_NWSRFS_JMenu.add( TSToolMenus.Tools_NWSRFS_ConvertJulianHour_JMenuItem =
			new SimpleJMenuItem(TSToolConstants.Tools_NWSRFS_ConvertJulianHour_String, this ) );
	}

	// Options menu.

	TSToolMenus.Tools_JMenu.addSeparator ();
	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_SelectOnMap_JMenuItem=new SimpleJMenuItem( TSToolConstants.Tools_SelectOnMap_String, this));

	TSToolMenus.Tools_JMenu.addSeparator ();
	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_Options_JMenuItem=new SimpleJMenuItem( TSToolConstants.Tools_Options_String, this ) );

	// View Log File.

	TSToolMenus.Tools_JMenu.addSeparator ();
	// Create the diagnostics GUI, specifying the key for the help
	// button.  Events are handled from within the diagnostics GUI.
	DiagnosticsJFrame diagnostics_JFrame = new DiagnosticsJFrame (this);
	// TODO smalers 2005-04-05 some day need to enable on-line help. ("TSTool.PreferencesMenu");
	diagnostics_JFrame.attachMainMenu ( TSToolMenus.Tools_JMenu );
	Message.addMessageLogListener ( this );
	// "View Log File (Startup)" menu is handled here and the "View Log File" uses utility setup code
	TSToolMenus.Tools_JMenu.add ( TSToolMenus.Tools_ViewLogFile_Startup_JMenuItem =
		new SimpleJMenuItem (TSToolConstants.Tools_ViewLogFile_Startup_String, this ));
}

/**
Initialize the View menu.
@param menuBar the menu bar to add menus
*/
private void ui_InitGUIMenus_View ( JMenuBar menuBar ) {
	TSToolMenus.View_JMenu = new JMenu (TSToolConstants.View_String, true);
	menuBar.add (TSToolMenus.View_JMenu);

    TSToolMenus.View_JMenu.add ( TSToolMenus.View_CommandFileDiff_JMenuItem=new SimpleJMenuItem( TSToolConstants.View_CommandFileDiff_String, this));
    TSToolMenus.View_CommandFileDiff_JMenuItem.setToolTipText("Use visual diff program to compare current commands with last saved version.");
    TSToolMenus.View_JMenu.add ( TSToolMenus.View_CommandFileSourceDiff_JMenuItem=new SimpleJMenuItem( TSToolConstants.View_CommandFileSourceDiff_String, this));
    TSToolMenus.View_CommandFileSourceDiff_JMenuItem.setToolTipText("Use visual diff program to compare current commands with original source version from #@sourceUrl.");
    TSToolMenus.View_JMenu.addSeparator();
    TSToolMenus.View_JMenu.add ( TSToolMenus.View_DataStores_JMenuItem=new SimpleJMenuItem( TSToolConstants.View_DataStores_String, this));
    TSToolMenus.View_DataStores_JMenuItem.setToolTipText("View a list of datastores, with status and connection errors.");
    TSToolMenus.View_JMenu.addSeparator();
	TSToolMenus.View_JMenu.add ( TSToolMenus.View_DataUnits_JMenuItem=new SimpleJMenuItem( TSToolConstants.View_DataUnits_String, this));
    TSToolMenus.View_DataUnits_JMenuItem.setToolTipText("View a list of data units, used to convert units.");
    TSToolMenus.View_JMenu.addSeparator();
    TSToolMenus.View_JMenu.add ( TSToolMenus.View_MapInterface_JCheckBoxMenuItem=new JCheckBoxMenuItem(TSToolConstants.View_Map_String) );
    TSToolMenus.View_MapInterface_JCheckBoxMenuItem.setToolTipText("Toggle the map view.");
    TSToolMenus.View_MapInterface_JCheckBoxMenuItem.setState ( false );
    TSToolMenus.View_MapInterface_JCheckBoxMenuItem.addItemListener ( this );
    TSToolMenus.View_JMenu.addSeparator();
    TSToolMenus.View_JMenu.add ( TSToolMenus.View_CloseAllViewWindows_JMenuItem=new SimpleJMenuItem( TSToolConstants.View_CloseAllViewWindows_String, this));
    TSToolMenus.View_CloseAllViewWindows_JMenuItem.setToolTipText("Close all graphs and other views.");
}

/**
Initialize the toolbar.
*/
private void ui_InitToolbar () {
    JToolBar toolbar = new JToolBar("TSTool Control Buttons");

    Insets none = new Insets(0, 0, 0, 0);
    URL url = null;
    /* TODO smalers 2007-12-04 Enable when decide how to handle blank file better - /tmp, etc.
    url = this.getClass().getResource( __TOOL_ICON_PATH + "/icon_newFile.gif" );
    String New_CommandFile_String = "New command file";
    if (url != null) {
        __toolbarNew_JButton = new SimpleJButton(new ImageIcon(url),
            New_CommandFile_String,
            New_CommandFile_String,
            none, false, this);
    }

    if ( __toolbarNew_JButton != null ) {
        // Might be null if no files are found.
        __toolbarNew_JButton.setToolTipText ( "<html>" + New_CommandFile_String + "</html>" );
        toolbar.add(__toolbarNew_JButton);
    }
    */

    url = this.getClass().getResource( TSToolConstants.TOOL_ICON_PATH + "/icon_openFile.gif");
    String Open_CommandFile_String = "Open command file";
    if (url != null) {
        this.__toolbarOpen_JButton = new SimpleJButton(new ImageIcon(url),
            Open_CommandFile_String,
            Open_CommandFile_String,
            none, false, this);
    }

    if ( this.__toolbarOpen_JButton != null ) {
        // Might be null if no files are found.
        this.__toolbarOpen_JButton.setToolTipText ( "<html>" + Open_CommandFile_String + "/html>" );
        toolbar.add(this.__toolbarOpen_JButton);
    }

    url = this.getClass().getResource( TSToolConstants.TOOL_ICON_PATH + "/icon_saveFile.gif");
    String Save_CommandFile_String = "Save command file";
    if (url != null) {
        this.__toolbarSave_JButton = new SimpleJButton(new ImageIcon(url),
            Save_CommandFile_String,
            Save_CommandFile_String,
            none, false, this);
    }

    if ( this.__toolbarSave_JButton != null ) {
        // Might be null if no files are found.
        this.__toolbarSave_JButton.setToolTipText ( "<html>" + Save_CommandFile_String + "/html>" );
        toolbar.add(this.__toolbarSave_JButton);
    }
    // FIXME smalers 2007-12-04 Add when some of the other layout changes - adding split pane to separate commands and results, etc.
    // Right now this conflicts with the query panel.
    //getContentPane().add ("North", toolbar);
}

/**
Load a command file and display in the command list.
@param commandFile full path to command file to load
@param runOnLoad if true, the commands will be run after loading
@param runDiscoveryOnLoad if true, run discovery on the commands as they are loaded (the normal case);
if false (may be useful for very large command files), do not run discovery when loading commands
*/
private void ui_LoadCommandFile ( String commandFile, boolean runOnLoad, boolean runDiscoveryOnLoad ) {
    String routine = getClass().getSimpleName() + ".ui_LoadCommandFile";
    int numAutoChanges = 0; // Number of lines automatically changed during load.
    try {
        ui_UpdateStatusTextFields ( 2, null, null, "Reading the selected command file.", TSToolConstants.STATUS_BUSY );
        ui_StartWaitCursor();
        
        // Read the command file into the command processor.
        numAutoChanges = commandProcessor_ReadCommandFile ( commandFile, runDiscoveryOnLoad );

        // Add progress listeners to the commands so that the UI can listen for progress within commands.
        for ( Command command : this.__tsProcessor.getCommands() ) {
            // Connect the command to the UI to handle progress when the command is run.
            // TODO smalers 2009-03-23 Evaluate whether to define an interface rather than rely on
            // AbstractCommand here - too much overhead as is when only some commands implement.
            if ( command instanceof AbstractCommand ) {
                ((AbstractCommand)command).addCommandProgressListener ( this );
            }
        }
        // Repaint the list to reflect the status of the commands.
        ui_ShowCurrentCommandListStatus(CommandPhaseType.DISCOVERY);
    }
    catch ( FileNotFoundException e ) {
        Message.printWarning ( 1, routine, "Command file \"" + commandFile + "\" does not exist." );
        Message.printWarning ( 3, routine, e );
        // Previous contents will remain.
        return;
    }
    catch ( IOException e ) {
        Message.printWarning ( 1, routine, "Error reading command file \"" + commandFile + "\".  List of commands may be incomplete." );
        Message.printWarning ( 3, routine, e );
        // Previous contents will remain.
        return;
    }
    catch ( Exception e ) {
        // FIXME smalers 2007-10-09 Perhaps should revert to previous.
        // data model contents?  For now allow partial contents to be displayed.
        //
        // Error opening the file (should not happen but maybe a read permissions problem).
        Message.printWarning ( 1, routine,
        "Unexpected error reading command file \"" + commandFile + "\".  Displaying commands that could be read." );
        Message.printWarning ( 3, routine, e );
    }
    finally {
        ui_StopWaitCursor();
    }

    // If successful, the TSCommandProcessor, as the data model, will have fired actions to make the JList update.

    commandList_SetCommandFileName(commandFile);
    if ( numAutoChanges == 0 ) {
        commandList_SetDirty(false);
    }

    // Check the comments for annotations that need to be handled.
    commandList_CheckComments();

    // Clear the old results.
    results_Clear();
    ui_UpdateStatusTextFields ( 2, null, null, "Use the Run menu/buttons to run the commands.", TSToolConstants.STATUS_READY );
    this.__processor_JProgressBar.setValue ( 0 );
    this.__command_JProgressBar.setValue ( 0 );

    // If requested, run the commands after loading.

    if ( runOnLoad ) {
        // Run all commands and create output.
        uiAction_RunCommands ( true, true );
        // This will update the status text fields
    }
}

/**
Indicate whether running commands should occur in a thread.
The default if not specified is true.
@return true if the commands should be run in a thread, false if not.
*/
private boolean ui_Property_RunCommandProcessorInThread() {
	String RunCommandProcessorInThread_String = this.__props.getValue ( TSTool_Options_JDialog.TSTool_RunCommandProcessorInThread );
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
 * Set the table model used to list time series.
 * This is called from datastore integration code.
 * @param query_TableModel the table model created elsewhere, which needs to be set as the active table model
 */
public void ui_SetTimeSeriesCatalogTableModel ( JWorksheet_AbstractRowTableModel query_TableModel ) {
	this.__query_TableModel = query_TableModel;
}

/**
Set the directory for the last "File...Open Command File".
@param Dir_LastCommandFileOpened Directory for last command file opened.
*/
private void ui_SetDir_LastCommandFileOpened ( String Dir_LastCommandFileOpened ) {
	this.__Dir_LastCommandFileOpened = Dir_LastCommandFileOpened;
	// Also set the last directory opened by a dialog.
	JGUIUtil.setLastFileDialogDirectory(Dir_LastCommandFileOpened);
}

/**
Set the last directory for "Run Command File", which runs an external command file but does not show the results.
@param Dir_LastExternalCommandFileRun Directory for last command file open
*/
private void ui_SetDir_LastExternalCommandFileRun ( String Dir_LastExternalCommandFileRun ) {
	this.__Dir_LastExternalCommandFileRun = Dir_LastExternalCommandFileRun;
	// Also set the last directory opened by a dialog.
	JGUIUtil.setLastFileDialogDirectory(Dir_LastExternalCommandFileRun);
}

/**
Set whether ActionEvents should be ignored (or not).
In general they should not be ignored but in some cases when programmatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
private void ui_SetIgnoreActionEvent ( boolean ignore ) {
	this.__ignoreActionEvent = ignore;
}

/**
Set whether ItemEvents should be ignored (or not).
In general they should not be ignored but in some cases when programmatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
public void ui_SetIgnoreItemEvent ( boolean ignore ) {
	this.__ignoreItemEvent = ignore;
}

/**
Set whether ListSelectionEvents should be ignored (or not).
In general they should not be ignored but in some cases when programmatically modifying data models
the spurious events do not need to trigger other actions.
@param ignore whether to ignore ActionEvents.
*/
private void ui_SetIgnoreListSelectionEvent ( boolean ignore ) {
	this.__ignoreListSelectionEvent = ignore;
}

/**
Set the initial working directory,
which will be the software startup home or the location where the command file has been read/saved.
@param initialWorkingDir The initial working directory (should be non-null).
*/
private void ui_SetInitialWorkingDir ( String initialWorkingDir ) {
	String routine = getClass().getSimpleName() + ".ui_SetInitialWorkingDir";
	Message.printStatus(2, routine, "Setting the initial working directory to \"" + initialWorkingDir + "\"" );
	this.__initialWorkingDir = initialWorkingDir;
	// Also set in the processor.
	commandProcessor_SetInitialWorkingDir ( initialWorkingDir, true );
}

/**
Set the input filters based on the current settings (input type and name, datastore name, data type).
This sets the appropriate input filter visible since all input filters are created at startup or when a datastore is opened.
*/
public void ui_SetInputFilterForSelections() {
	String routine = getClass().getSimpleName() + ".ui_SetInputFilterForSelections";
    String selectedDataStoreName = null;
    // Get the selected datastore from the user selections.
    DataStore selectedDataStore = ui_GetSelectedDataStore();
    if ( selectedDataStore != null ) {
        selectedDataStoreName = selectedDataStore.getName();
    }
    InputFilter_JPanel selectedInputFilter_JPanel = null; // If not set at end, will use generic panel.
    String selectedInputType = ui_GetSelectedInputType();
    String selectedDataType = ui_GetSelectedDataType();
    String selectedTimeStep = ui_GetSelectedTimeStep();
    if ( Message.isDebugOn ) {
    	Message.printStatus(2, routine, "Setting the input filter based on selected datastore \"" +
        	selectedDataStoreName + "\", input type \"" + selectedInputType +
        	"\", and data type \"" + selectedDataType + "\"" );
    }
    try {
    if ( selectedDataStore != null ) {
        // This handles input filters associated with datastores, including plugin datastores.
        selectedInputFilter_JPanel = ui_GetInputFilterPanelForDataStoreName(selectedDataStoreName, selectedDataType, selectedTimeStep);
        if ( Message.isDebugOn ) {
        	Message.printStatus(2, routine,
           	"Unable to determine input panel to use for selected datastore \"" + selectedDataStoreName +
           	"\" using datastore name \"" + selectedDataStoreName + "\" data type \"" + selectedDataType +
           	"\" time step \"" + selectedTimeStep + "\"." );
        }
    }
    else if(selectedInputType.equals(TSToolConstants.INPUT_TYPE_HECDSS) &&
    	(TSTool_HecDss.getInstance(this).getInputFilterJPanel() != null) ) {
    	// One input filter panel is reused among different HEC-DSS files:
    	// - the previously-selected filter choices will still be selected
        selectedInputFilter_JPanel = TSTool_HecDss.getInstance(this).getInputFilterJPanel();
    }
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_HydroBase) ) {
        selectedInputFilter_JPanel = TSTool_HydroBase.getInstance(this).setInputFilterForSelections(selectedDataType, selectedTimeStep,
        	this.__inputFilterGeneric_JPanel);
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files) ) {
        selectedInputFilter_JPanel = TSTool_FS5Files.getInstance(this).setInputFilterForSelections();
	}
	else {
        // Currently no other input types support filtering - this may also be used if HydroBase input
        // filters were not set up due to a missing database connection.
		selectedInputFilter_JPanel = null;
	}
    if ( selectedInputFilter_JPanel == null ) {
        if ( selectedDataStore != null ) {
            // Dealing with datastore.
            Message.printStatus(2, routine,
                "Unable to determine input panel to use for datastore \"" + selectedDataStoreName + "\".  Using blank panel." );
        }
        else {
            // Dealing with input type.
            Message.printStatus(2, routine,
                "Unable to determine input panel to use for input type \"" + selectedInputType + "\".  Using blank panel." );
        }
        selectedInputFilter_JPanel = this.__inputFilterGeneric_JPanel;
    }
    }
    catch ( Throwable e ) {
        Message.printStatus(2, routine,
            "Error selecting the input panel for input type\"" + selectedInputType + "\".  Using blank panel." );
        Message.printWarning(3,routine,e);
        selectedInputFilter_JPanel = __inputFilterGeneric_JPanel;
    }
    this.__selectedInputFilter_JPanel = selectedInputFilter_JPanel;
	// Loop through the available input filter panels and set not visible all others.
    if ( this.__selectedInputFilter_JPanel != null ) {
        this.__selectedInputFilter_JPanel.setVisible ( true );
        if ( Message.isDebugOn ) {
        	Message.printStatus(2, routine, "Set input filter panel \"" + this.__selectedInputFilter_JPanel.getName() +
        		"\" visible TRUE." );
        }
    }
    int i = -1;
	for ( JPanel input_filter_JPanel: this.__inputFilterJPanelList ) {
		++i;
	    if ( input_filter_JPanel == this.__selectedInputFilter_JPanel ) {
	    	if ( Message.isDebugOn ) {
	    		Message.printStatus(2, routine, "Set input filter panel [" + i + "] \"" + input_filter_JPanel.getName() +
	            	"\" visible TRUE." );
	    	}
	    }
	    else {
		    input_filter_JPanel.setVisible ( false );
	    	if ( Message.isDebugOn ) {
	    		Message.printStatus(2, routine, "Set input filter panel [" + i + "] \"" + input_filter_JPanel.getName() +
	    			"\" visible FALSE." );
	    	}
		}
	}
}

/**
Set the "Input name" label and choices visible.
This is called when a datastore or input type is selected because input name is only used by some.
@param isVisible whether the "Input name" label and choices should be visible
*/
public void ui_SetInputNameVisible(boolean isVisible ) {
    this.__inputName_JLabel.setVisible(isVisible);
    this.__inputName_JComboBox.setVisible(isVisible);
}

/**
Set the title of the input panel.
@param title the title for the input/query panel.
If null, use the default of "Input/Query Options..." with a black border.
@param color color of the line border.
*/
private void ui_SetInputPanelTitle ( String title, Color color ) {
    if ( title == null ) {
        title = "Input/Query Options";
        color = Color.black;
    }
    this.__queryInput_JPanel.setBorder( BorderFactory.createTitledBorder ( BorderFactory.createLineBorder(color),title ));
}

/**
Set the __inputType_JComboBox contents based on the configuration information.
If an input type is a database, only add if a non-null connection is available.
Later, database connections may also be named, in which case more checks will need to be done.
*/
public void ui_SetInputTypeChoices () {
	//Message.printStatus ( 1, "", "SAMX - setting input type choices..." );
	// Ignore item events while manipulating.  This should prevent unnecessary error-handling at startup.
	ui_SetIgnoreItemEvent ( true );
	if ( this.__inputType_JComboBox.getItemCount() > 0 ) {
		this.__inputType_JComboBox.removeAll ();
	}
	// Add a blank choice to allow working with datastores.
	this.__inputType_JComboBox.add ( "" );
	if ( this.__source_DateValue_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_DateValue );
	}
    if ( this.__source_HECDSS_enabled ) {
        this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_HECDSS );
    }
	if ( this.__source_HydroBase_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_HydroBase );
	}
	if ( this.__source_MODSIM_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_MODSIM );
	}
	if ( this.__source_NWSCard_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_NWSCARD );
	}
	if ( this.__source_NWSRFS_FS5Files_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files );
	}
	if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_NWSRFS_ESPTraceEnsemble );
	}
	if ( this.__source_RiverWare_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_RiverWare );
	}
	// TODO - don't know how to parse SHEF yet.
	//if ( this.__source_SHEF_enabled ) {
		//this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_SHEF );
	//}
	if ( this.__source_StateCU_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_StateCU );
	}
    if ( this.__source_StateCUB_enabled ) {
        this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_StateCUB );
    }
	if ( this.__source_StateMod_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_StateMod );
	}
	if ( this.__source_StateModB_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_StateModB );
	}
	if ( this.__source_UsgsNwisRdb_enabled ) {
		this.__inputType_JComboBox.add( TSToolConstants.INPUT_TYPE_UsgsNwisRdb );
	}

	// Enable item events again so the events will cascade.

	ui_SetIgnoreItemEvent ( false );

	if ( this.__source_HydroBase_enabled && (TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() != null) ) {
		// If enabled and available, select it because the users probably want it as the choice.
		this.__inputType_JComboBox.select( null );
		this.__inputType_JComboBox.select( TSToolConstants.INPUT_TYPE_HydroBase );
		// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
		this.__dataStore_JTabbedPane.setSelectedIndex(0);
	}
	else {
        // Select the DateValue format, which is generic.
		this.__inputType_JComboBox.select ( null );
		this.__inputType_JComboBox.select ( TSToolConstants.INPUT_TYPE_DateValue );
		// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
		this.__dataStore_JTabbedPane.setSelectedIndex(0);
	}
}

/**
Set the message text field.
*/
private void ui_SetMessageText ( String message ) {
    this.__message_JTextField.setText (message);
}

/**
Update the command list to show the current status.
This is called after all commands have been processed in run mode(),
when a command has been edited(), and when loading commands from a file.
@param lastCommandPhase the last command phase run,
provided as a hint to the annotated command list so earlier warnings like discovery are not shown after running
*/
private void ui_ShowCurrentCommandListStatus (CommandPhaseType lastCommandPhase) {
	this.__commands_AnnotatedCommandJList.setLastCommandPhase(lastCommandPhase);
    this.__commands_AnnotatedCommandJList.repaint();
}

/**
Display the wait cursor above everything else.
*/
private void ui_StartWaitCursor() {
    RootPaneContainer root = (RootPaneContainer)this.getRootPane().getTopLevelAncestor();
    root.getGlassPane().setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
    root.getGlassPane().setVisible(true);
}

/**
Stop displaying the wait cursor above everything else.
*/
private void ui_StopWaitCursor() {
    RootPaneContainer root = (RootPaneContainer)this.getRootPane().getTopLevelAncestor();
    root.getGlassPane().setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
    root.getGlassPane().setVisible(false);
}

/**
Update the main status information when the list contents have changed.
This method should be called after any change to the query, command, or time series results list.
Interface tasks include:
<ol>
<li>
	Set the title bar.
	If no command file has been read, the title will be:  "TSTool - no commands saved".
	If a command file has been read but not modified, the title will be:  "TSTool - "filename"".
	If a command file has been read and modified, the title will be: "TSTool - "filename" (modified)".
	</li>
<li>
	Call updateTextFields() to indicate the number of selected and total
	commands and set the general status to "Ready".
	</li>
<li>.
	Call checkGUIState() to reset menus, etc.  Note this should be called
	independently when the list appearance changes (selections, etc.).
	</li>
</ol>
@param check_gui_state If true, then the checkGUIState() method is also called,
which checks many interface settings.
*/
public void ui_UpdateStatus ( boolean check_gui_state ) {
	// Title bar (command file).

	if ( this.__commandFileName == null ) {
		setTitle ( "TSTool" + this.ui_GetTitleMod() + " - no commands saved");
	}
	else {
        if ( this.__commandsDirty ) {
			setTitle ( "TSTool" + this.ui_GetTitleMod() + " - \"" + this.__commandFileName + "\" (modified)");
		}
		else {
            setTitle ( "TSTool" + this.ui_GetTitleMod() + " - \"" + this.__commandFileName + "\"");
		}
	}

	// Variables that are reused below.
	int selectedSize = 0;
	int selectedIndices[] = null;

	// Query results.

	if ( this.__query_results_JPanel != null ) {
		int size = 0;
		if ( this.__query_JWorksheet != null ) {
			try {
                size = this.__query_JWorksheet.getRowCount();
				selectedSize = this.__query_JWorksheet.getSelectedRowCount();
			}
			catch ( Exception e ) {
				// Absorb the exception in most cases - print if developing to see if this issue can be resolved.
				if ( Message.isDebugOn && IOUtil.testing()  ) {
					String routine = "TSTool_JFrame.updateStatus";
					Message.printWarning ( 3, routine,
					"For developers:  caught exception in clearQueryList JWorksheet at setup." );
					Message.printWarning ( 3, routine, e );
				}
			}
		}
        this.__query_results_JPanel.setBorder( BorderFactory.createTitledBorder (
    		BorderFactory.createLineBorder(Color.black),
    		"Time Series List (" + size + " time series, " + selectedSize + " selected)") );
	}

	// Commands.

	selectedIndices = ui_GetCommandJList().getSelectedIndices();
	selectedSize = 0;
	if ( selectedIndices != null ) {
		selectedSize = selectedIndices.length;
	}
	if ( this.__commands_JPanel != null ) {
    	this.__commands_JPanel.setBorder( BorderFactory.createTitledBorder (
		BorderFactory.createLineBorder(Color.black),
		"Commands (" + this.__commands_JListModel.size() + " commands, " + selectedSize + " selected, " +
			commandList_GetFailureCount() + " with failures, " + commandList_GetWarningCount() + " with warnings, " +
			commandList_GetNotificationCount() + " with notifications)") );
	}

	// Results: Output Files.

	int numOutputFiles = 0;
	if ( this.__resultsOutputFiles_JListModel != null ) {
	    numOutputFiles = this.__resultsOutputFiles_JListModel.size();
	}
	selectedIndices = this.__resultsOutputFiles_JList.getSelectedIndices();
	selectedSize = 0;
	if ( selectedIndices != null ) {
		selectedSize = selectedIndices.length;
	}
	this.__resultsOutputFiles_JLabel.setText ( "" + numOutputFiles + " output files, " + selectedSize + " selected");

	// Results: Tables.

	int numTables = 0;
	if ( this.__resultsTables_JListModel != null ) {
	    numTables = this.__resultsTables_JListModel.size();
	}
	selectedIndices = this.__resultsTables_JList.getSelectedIndices();
	selectedSize = 0;
	if ( selectedIndices != null ) {
		selectedSize = selectedIndices.length;
	}
	this.__resultsTables_JLabel.setText ( "" + numTables + " tables, " + selectedSize + " selected");

	// Results: Time Series.

	selectedIndices = this.__resultsTS_JList.getSelectedIndices();
	selectedSize = 0;
	if ( selectedIndices != null ) {
		selectedSize = selectedIndices.length;
	}

	int noDataCount = 0;
	int size = commandProcessor_GetTimeSeriesResultsListSize();
	TS ts = null;
	for ( int i = 0; i < size; i++ ) {
        ts = commandProcessor_GetTimeSeries(i);
        if ( ts == null ) {
        	// Should not happen because only non-null time series should be in the list.
        	++noDataCount;
        }
        else if ( !ts.hasData() ) {
        	// Could be because time series was not found (therefore minimal metadata populated),
        	// or time series was found by no data are available in the input period.
        	++noDataCount;
        }
	}

	if ( this.__resultsTS_JPanel != null ) {
		if ( noDataCount == 0 ) {
			this.__resultsTS_JPanel.setBorder(BorderFactory.createTitledBorder (
				BorderFactory.createLineBorder(Color.black),
				//"Results: Time Series (" +
				"" + this.__resultsTS_JListModel.size() + " time series, " + selectedSize + " selected") );
		}
		else {
			// Show how many time series have no data (will be highlighted in red in the list).
			this.__resultsTS_JPanel.setBorder(BorderFactory.createTitledBorder (
				BorderFactory.createLineBorder(Color.black),
				//"Results: Time Series (" +
				"" + this.__resultsTS_JListModel.size() + " time series, " + selectedSize + " selected, " +
				noDataCount + " with no data"));
		}
	}
	// TODO smalers 2007-08-31 Evaluate call here - probably should call elsewhere
	//ui_UpdateStatusTextFields ( -1, "TSTool_JFrame.updateStatus", null, __STATUS_READY );
	// FIXME smalers 2008-11-11 Why is this called no matter what is passed in for the parameter?
	ui_CheckGUIState ();
}

/**
Update the text fields at the bottom of the main interface.
This does NOT update all text fields like the number of commands, etc.
@param level Message level.  If > 0 and the message is not null, call Message.printStatus() to record a message.
@param routine Routine name used if Message.printStatus() is called.
@param commandPanelStatus currently ignored (intended that if not null set the status for the text in the command panel border)
@param message If not null, update the __message_JTextField to contain this text.
If null, leave the contents as previously shown.  Specify "" to clear the text.
@param status If not null, update the __status_JTextField to contain this text.
If null, leave the contents as previously shown.  Specify "" to clear the text.
*/
private void ui_UpdateStatusTextFields ( int level, String routine, String commandPanelStatus, String message, String status ) {
	if ( (level > 0) && (message != null) ) {
		// Print a status message to the messaging system.
		Message.printStatus ( 1, routine, message );
	}
	if ( message != null ) {
		ui_SetMessageText ( message );
	}
	if ( status != null ) {
		this.__status_JTextField.setText (status);
	}
}

/**
Handle a group of UI actions, for the main actions.
@param event Event to handle.
*/
private void uiAction_ActionPerformed01_MainActions (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();
	Object o = event.getSource();

	// Next list menus or commands.
	if (command.equals(TSToolConstants.BUTTON_TOP_GET_TIME_SERIES) ) {
		uiAction_GetTimeSeriesListClicked();
	}
	else if ( o == __CopySelectedToCommands_JButton ) {
		// Transfer from the time series list to the commands.
		uiAction_TransferSelectedQueryResultsToCommandList();
	}
	else if ( o == __CopyAllToCommands_JButton ) {
		// Transfer from the time series list to the commands.
		uiAction_TransferAllQueryResultsToCommandList();
	}
	else if (command.equals(TSToolConstants.Button_RunSelectedCommands_String) ) {
		// Can be a button or a menu?
		uiAction_RunCommands ( false, true );
	}
	else if (command.equals(TSToolConstants.Button_RunAllCommands_String) ) {
		// Can be a button or a menu?
		uiAction_RunCommands ( true, true );
	}
	else if (command.equals(TSToolConstants.Button_ClearCommands_String) ) {
		commandList_RemoveCommandsBasedOnUI();
	}
	else if (command.equals(TSToolConstants.BUTTON_TS_SELECT_ALL) ) {
		JGUIUtil.selectAll ( __resultsTS_JList );
	}
	else if (command.equals(TSToolConstants.BUTTON_TS_DESELECT_ALL) ) {
		this.__resultsTS_JList.clearSelection();
	}
	else {
        // Chain to the next method.
		uiAction_ActionPerformed02_FileMenu(event);
	}
}

/**
Handle a group of actions for the File menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed02_FileMenu (ActionEvent event)
throws Exception {
	Object o = event.getSource();
	String command = event.getActionCommand();
	String routine = "FileMenu";

	// File Menu actions.
    if ( o == TSToolMenus.File_New_CommandFile_JMenuItem ) {
        uiAction_NewCommandFile();
    }
	else if ( o == TSToolMenus.File_Open_CommandFile_JMenuItem ) {
		try {
            uiAction_OpenCommandFile ( null, true );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error reading command file (" + e + ")." );
			Message.printWarning( 3, "", e);
		}
	}
    else if ( o == TSToolMenus.File_Open_CommandFileNoDiscovery_JMenuItem ) {
        try {
            uiAction_OpenCommandFile ( null, false );
        }
        catch ( Exception e ) {
            Message.printWarning ( 1, routine, "Error reading command file (" + e + ")." );
            Message.printWarning( 3, "", e);
        }
    }
	else if ( command.equals ( TSToolConstants.File_Open_HydroBase_String )) {
		TSTool_HydroBase.getInstance(this).openHydroBase ( false, TSToolMenus.File_Properties_HydroBase_JMenuItem ); // False means not opening at startup.
		// Update the HydroBase input filters.
		if ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() != null ) {
		    TSTool_HydroBase.getInstance(this).initGUIInputFiltersLegacy ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy(), __inputFilterY );
		}
		// Force the choices to refresh.
		if ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() != null ) {
			this.__inputType_JComboBox.select ( null );
			this.__inputType_JComboBox.select ( TSToolConstants.INPUT_TYPE_HydroBase);
			// As of TSTool 14.6.1 default to the datastore tab (previously defaulted to "Input Type" tab).
			this.__dataStore_JTabbedPane.setSelectedIndex(0);
		}
	}
	else if ( command.equals ( TSToolConstants.File_Open_ReclamationHDB_String )) {
		// This is used only to re-login to an existing data store.
		// The datastore with server, database, etc. must be configured in a datastore configuration file.
		TSTool_HDB.getInstance(this).openDatabase();
	}
	else if ( o == TSToolMenus.File_Save_Commands_JMenuItem ) {
		try {
            if ( this.__commandFileName != null ) {
				// Use the existing name.
                int x = ResponseJDialog.OK;
                if ( this.__tsProcessor.getReadOnly() ) {
                    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                        "The commands are marked read-only (#@readOnly comment).\n" +
                        "Press Cancel and save to a new name if desired.  Press OK to update the read-only file.",
                        ResponseJDialog.OK|ResponseJDialog.CANCEL).response();
                }
                else if ( this.__tsProcessor.areCommandsTemplate() ) {
                    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                        "The commands are marked as a template (#@template comment).\n" +
                        "TSTool does not currently support editing template command files.  You must use a text editor.\n" +
                        "Functionality is being evaluated and may be enabled in the future to allow editing template command files.\n" +
                        "Press CANCEL to ensure that the template is not modified in unexpected ways by TSTool.",
                        ResponseJDialog.CANCEL).response();
                }
                if ( x == ResponseJDialog.OK ) {
                    // Save most recent version.
                    uiAction_WriteCommandFile ( __commandFileName, false, false );
                }
			}
			else {
                // No command file has been saved - prompt for the name.
				uiAction_WriteCommandFile ( this.__commandFileName, true, false );
			}
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error writing command file (" + e + ")." );
		}
	}
	else if ( o == TSToolMenus.File_Save_CommandsAs_JMenuItem ) {
		try {
            // Prompt for the name.
			uiAction_WriteCommandFile ( this.__commandFileName, true, false );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error writing command file (" + e + ")." );
		}
	}
    /*
	// TODO smalers 2023-02-19 remove ASAP since not used.
    else if ( o == TSToolMenus.File_Save_CommandsAsVersion9_JMenuItem ) {
        try {
            // Prompt for the name.
            uiAction_WriteCommandFile ( __commandFileName, true, true );
        }
        catch ( Exception e ) {
            Message.printWarning ( 1, routine, "Error writing command file in version 9 format (" + e + ")." );
        }
    }
    */
    else if ( command.equals(TSToolConstants.File_Save_TimeSeriesAs_String) ) {
		// Can save in a number of formats.  Allow the user to pick using a file chooser.
		uiAction_SaveTimeSeries ();
	}
	else if ( o == TSToolMenus.File_CheckForUpdate_JMenuItem ) {
		// Check for an update to the command file:
		// - use the @sourceUrl to retrieve the source copy
		// - then use the @version and @versionDate in source and local copy to compare versions
		try {
			uiAction_CheckForCommandFileUpdate();
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error checking for command file update (" + e + ")." );
			Message.printWarning ( 3, routine, e );
		}
	}
    else if (command.equals(TSToolConstants.File_Print_Commands_String) ) {
        // Get all commands as strings for printing.
        try {
            new TextPrinterJob ( commandList_GetCommandStrings(true), "TSTool Commands",
                null, // Printer name.
                "na-letter", // Paper size.
                null, // Paper source.
                "Landscape", // Page orientation.
                .75, // Left margin.
                .75, // Right margin.
                .6, // Top margin.
                .6, // Bottom margin.
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
	else if ( command.equals(TSToolConstants.File_Properties_CommandsRun_String) ) {
		// Simple text display of last commands run data from TSEngine.
		uiAction_ShowProperties_CommandsRun();
	}
    else if ( command.equals(TSToolConstants.File_Properties_TSToolSession_String) ) {
        uiAction_ShowProperties_TSToolSession( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() );
	}
    else if ( command.equals(TSToolConstants.File_Properties_HydroBase_String) ) {
		// Simple text display of HydroBase properties.
		PropList reportProp = new PropList ("HydroBase Properties");
		reportProp.set ( "TotalWidth", "600" );
		reportProp.set ( "TotalHeight", "300" );
		reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
		reportProp.set ( "DisplaySize", "11" );
		reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
		reportProp.set ( "PrintSize", "7" );
		reportProp.set ( "Title", "HydroBase Properties" );
		List<String> v = null;
		if ( TSTool_HydroBase.getInstance(this).getHydroBaseDMILegacy() == null ) {
		    v = new ArrayList<>(3);
			v.add ( "HydroBase Properties" );
			v.add ( "" );
			v.add ( "No HydroBase database is available." );
		}
		else {
            v = TSTool_HydroBase.getInstance(this).getHydroBaseDMILegacy().getDatabaseProperties();
		}
		reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
		new ReportJFrame ( v, reportProp );
	}
    else if ( command.equals(TSToolConstants.File_Properties_NWSRFSFS5Files_String) ) {
		PropList reportProp = new PropList ("NWSRFSFS5Files.props");
		// Too big (make this big when we have more stuff).
		reportProp.set ( "TotalWidth", "600" );
		reportProp.set ( "TotalHeight", "300" );
		reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
		reportProp.set ( "DisplaySize", "11" );
		reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
		reportProp.set ( "PrintSize", "7" );
		reportProp.set ( "Title", "NWSRFS FS5Files Properties" );
		List<String> v = null;
		if ( TSTool_FS5Files.getInstance(this).getNwsrfsFS5FilesDMI() == null ) {
			v = new ArrayList<>( 1 );
			v.add ( "The NWSRFS FS5Files connection is not open." );
		}
		else {
            v = TSTool_FS5Files.getInstance(this).getNwsrfsFS5FilesDMI().getDatabaseProperties ( 3 );
		}
		reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
		new ReportJFrame ( v, reportProp );
	}
    else if ( o == TSToolMenus.File_SetWorkingDirectory_JMenuItem ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser ( JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle( "Set the Working Directory (normally only use if a command file was not opened or saved)");
		fc.setFileSelectionMode (JFileChooser.DIRECTORIES_ONLY );
		if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
			String directory = fc.getSelectedFile().getPath();
			IOUtil.setProgramWorkingDir(directory);
			// TODO - is this needed with Swing?
			// Reset to make sure the ending delimiter is removed.
			this.__props.set("WorkingDir",IOUtil.getProgramWorkingDir());
			ui_SetInitialWorkingDir (__props.getValue ("WorkingDir"));
			JGUIUtil.setLastFileDialogDirectory(directory);
		}
	}
    else if (command.equals(TSToolConstants.Run_ProcessTSProductPreview_String) ) {
		try {
            uiAction_ProcessTSProductFile ( null, true );
		}
		catch ( Exception te ) {
			Message.printWarning ( 1, "", "Error processing TSProduct file (" + te + ")." );
			Message.printWarning ( 3, "", te );
		}
	}
    else if ( command.equals(TSToolConstants.File_Exit_String) ) {
		uiAction_FileExitClicked();
    }
    else if ( command.toUpperCase().endsWith(".TSTOOL")) {
    	// TSTool command file in recent files, treat as open.
    	uiAction_OpenCommandFile ( command, true );
    }
	else if (command.equals("Test") ) {
		// Test code.
		try {
            uiAction_Test();
		}
		catch ( Exception te ) {
			Message.printWarning ( 1, "", "Error running test" );
			Message.printWarning ( 3, "", te );
		}
	}
    else {
    	// Chain to the next action handler.
    	uiAction_ActionPerformed03_EditMenu ( event );
    }
}

/**
Handle a group of actions for the Edit menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed03_EditMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	// Edit menu actions (in order of menu).

    if ( command.equals(TSToolConstants.CommandsPopup_IndentRight_String) ) {
		// Indent selected commands.
		uiAction_IndentCommands( 1 );
	}
    else if ( command.equals(TSToolConstants.CommandsPopup_IndentLeft_String) ) {
		// Indent selected commands.
		uiAction_IndentCommands( -1 );
	}
    else if ( command.equals(TSToolConstants.Edit_CutCommands_String) ) {
		// Need to think whether this should work for the time series list or only the commands.  Copy to the buffer.
		uiAction_CopyFromCommandListToCutBuffer( true );
	}
    else if ( command.equals(TSToolConstants.Edit_CopyCommands_String) ) {
		// Copy to the buffer.
		uiAction_CopyFromCommandListToCutBuffer( false );
	}
    else if ( command.equals(TSToolConstants.Edit_PasteCommands_String) ) {
		// Copy the buffer to the final list.
		uiAction_PasteFromCutBufferToCommandList();
	}
    else if ( command.equals(TSToolConstants.Edit_DeleteCommands_String) ) {
		// The commands WILL NOT remain in the cut buffer.  Now clear the list of selected commands.
		commandList_RemoveCommandsBasedOnUI();
	}
    else if ( command.equals(TSToolConstants.Edit_SelectAllCommands_String) ) {
    	uiAction_SelectAllCommands();
	}
    else if ( command.equals(TSToolConstants.Edit_DeselectAllCommands_String) ) {
		uiAction_DeselectAllCommands();
	}
	else if ( command.equals(TSToolConstants.Edit_CommandWithErrorChecking_String) ) {
		// Edit the first selected item, unless a comment, in which case all are edited.
		uiAction_EditCommand ();
	}
	else if ( command.equals(TSToolConstants.CommandsPopup_Edit_AsText_String) ) {
		// Edit the first selected item, unless a comment, in which case all are edited.
		uiAction_EditCommandAsText ();
	}
	else if (command.equals(TSToolConstants.Edit_ConvertSelectedCommandsToComments_String) ) {
		uiAction_ConvertCommandsToComments ( true );
	}
	else if (command.equals(TSToolConstants.Edit_ConvertSelectedCommandsFromComments_String) ) {
		uiAction_ConvertCommandsToComments ( false );
	}
	else if (command.equals(TSToolConstants.CommandsPopup_FindCommands_String) ) {
		// Popup only.
		new FindInJListJDialog(this,ui_GetCommandJList(),"Find Command(s)");
		ui_UpdateStatus ( true );
	}
	else if (command.equals(TSToolConstants.CommandsPopup_ShowCommandStatus_String) ) {
		// Popup only.
		uiAction_ShowCommandStatus();
	}
	else {
		// Chain to next set of actions.
		uiAction_ActionPerformed04_ViewMenu ( event );
	}
}

/**
Handle a group of actions for the Run menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed04_ViewMenu (ActionEvent event)
throws Exception {
    String command = event.getActionCommand();
    //String routine = getClass().getSimpleName() + ".uiAction_ActionPerformed3b_ViewMenu";

    if ( command.equals(TSToolConstants.View_CommandFileDiff_String) ) {
        // Show visual diff of current command file and saved version.
        uiAction_ViewCommandFileDiff();
    }
    else if ( command.equals(TSToolConstants.View_CommandFileSourceDiff_String) ) {
		// Compare the current command file with the source:
		// - this is similar to comparing the in-memory commands with file version,
		//   but use the @sourceUrl to determine the source
		try {
			uiAction_ViewCommandFileSourceDiff();
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, "", "Error comparing commands with source (" + e + ")." );
			Message.printWarning ( 3, "", e );
		}
	}
    else if ( command.equals(TSToolConstants.View_DataStores_String) ) {
        // Show the datastores.
        uiAction_ShowDataStores();
    }
    else if ( command.equals(TSToolConstants.View_DataUnits_String) ) {
        // Show the data units.
        uiAction_ShowDataUnits();
    }
    else if ( command.equals(TSToolConstants.View_CloseAllViewWindows_String) ) {
        // Show the datastores.
        TSViewJFrame.getTSViewWindowManager().closeAll();
    }
    else {
        // Chain to next set of actions.
        uiAction_ActionPerformed04b_CommandsSelectMenu(event);
    }
}

/**
Handle a group of actions for the Commands...Select... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed04b_CommandsSelectMenu (ActionEvent event)
throws Exception {
    String command = event.getActionCommand();

    if (command.equals( TSToolConstants.Commands_Select_DeselectTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Select_DeselectTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Select_SelectTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Select_SelectTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Select_Free_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Select_Free_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Select_SortTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Select_SortTimeSeries_String, null, CommandEditType.INSERT );
    }
    else {
        // Chain to next actions.
        uiAction_ActionPerformed05_CommandsCreateMenu ( event );
    }
}

/**
Handle a group of actions for the Commands...Create... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed05_CommandsCreateMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	// TODO smalers 2006-05-02 Why is all of this needed?  Should rely on the command factory for commands.
	// Evaluate this when all commands are in the factory.

	if (command.equals( TSToolConstants.Commands_Create_CreateFromList_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_CreateFromList_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_Delta_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Create_Delta_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Create_ResequenceTimeSeriesData_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Create_ResequenceTimeSeriesData_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Create_RunningStatisticTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Create_RunningStatisticTimeSeries_String, null, CommandEditType.INSERT );
    }

	// Convert TS Identifier to read command.

	else if ( command.equals(TSToolConstants.Edit_ConvertTSIDTo_ReadTimeSeries_String) ) {
		commandList_EditCommand ( TSToolConstants.Edit_ConvertTSIDTo_ReadTimeSeries_String,
		    commandList_GetCommandsBasedOnUI(), CommandEditType.CONVERT );
	}
    else if ( command.equals(TSToolConstants.Edit_ConvertTSIDTo_ReadCommand_String) ) {
        commandList_EditCommand ( TSToolConstants.Edit_ConvertTSIDTo_ReadCommand_String,
            commandList_GetCommandsBasedOnUI(), CommandEditType.CONVERT );
    }
	/*
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_readDateValue_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_readDateValue_String, getCommand(), __UPDATE_COMMAND );
	}
    else if ( o == TSToolConstants.Commands_ConvertTSIDTo_readDateDelimitedFile_JMenuItem ) {
        commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_readDelimitedFile_String, getCommand(), __UPDATE_COMMAND );
    }
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_ReadHydroBase_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_ReadHydroBase_String, getCommand(), __UPDATE_COMMAND );
	}
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_readMODSIM_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_readMODSIM_String, getCommand(), __UPDATE_COMMAND );
	}
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_ReadNwsCard_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_ReadNwsCard_String, getCommand(), __UPDATE_COMMAND );
	}
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_readRiverWare_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_readRiverWare_String, getCommand(), __UPDATE_COMMAND );
	}
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_ReadStateMod_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_ReadStateMod_String, getCommand(), __UPDATE_COMMAND );
	}
	else if ( o == TSToolConstants.Commands_ConvertTSIDTo_ReadStateModB_JMenuItem ) {
		commandList_EditCommand ( TSToolConstants.Commands_ConvertTSIDTo_ReadStateModB_String, getCommand(), __UPDATE_COMMAND );
	}
	*/
	else if (command.equals( TSToolConstants.Commands_Create_ChangeInterval_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_ChangeInterval_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_ChangeIntervalToLarger_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_ChangeIntervalToLarger_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_ChangeIntervalToSmaller_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_ChangeIntervalToSmaller_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_ChangeIntervalIrregularToRegular_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_ChangeIntervalIrregularToRegular_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_ChangeIntervalRegularToIrregular_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_ChangeIntervalRegularToIrregular_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_Copy_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_Copy_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_Disaggregate_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_Disaggregate_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Create_LookupTimeSeriesFromTable_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Create_LookupTimeSeriesFromTable_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Create_NewDayTSFromMonthAndDayTS_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewDayTSFromMonthAndDayTS_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Create_NewEndOfMonthTSFromDayTS_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewEndOfMonthTSFromDayTS_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_NewPatternTimeSeries_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewPatternTimeSeries_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Create_NewStatisticTimeSeries_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewStatisticTimeSeries_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Create_NewStatisticMonthTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Create_NewStatisticMonthTimeSeries_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Create_NewStatisticYearTS_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewStatisticYearTS_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_NewTimeSeries_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_NewTimeSeries_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_Normalize_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_Normalize_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_RelativeDiff_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_RelativeDiff_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Create_TSID_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Create_TSID_String, null, CommandEditType.INSERT );
	}
	else {
		// Chain to next actions.
		uiAction_ActionPerformed06_CommandsReadMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Read... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed06_CommandsReadMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	// Read Time Series.

    if (command.equals(TSToolConstants.Commands_Read_SetIncludeMissingTS_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_SetIncludeMissingTS_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_SetInputPeriod_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Read_SetInputPeriod_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadColoradoHydroBaseRest_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadColoradoHydroBaseRest_String,	null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadDateValue_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadDateValue_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadDelftFewsPiXml_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadDelftFewsPiXml_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadDelimitedFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadDelimitedFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadHecDss_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadHecDss_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadHydroBase_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadHydroBase_String,	null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Read_ReadMODSIM_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadMODSIM_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Read_ReadNwsCard_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadNwsCard_String, null, CommandEditType.INSERT );
	}
    else if (command.equals(TSToolConstants.Commands_Read_ReadNrcsAwdb_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadNrcsAwdb_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadRccAcis_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadRccAcis_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadReclamationHDB_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadReclamationHDB_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadReclamationPisces_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadReclamationPisces_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadStateCU_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadStateCU_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadStateCUB_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadStateCUB_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadStateModB_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadStateModB_String,	null, CommandEditType.INSERT );
	}
	// Put after longer versions.
	else if (command.equals( TSToolConstants.Commands_Read_ReadStateMod_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadStateMod_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Read_ReadNwsrfsFS5Files_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadNwsrfsFS5Files_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Read_ReadRiverWare_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadRiverWare_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadTimeSeriesList_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadTimeSeriesList_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadUsgsNwisDaily_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadUsgsNwisDaily_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadUsgsNwisGroundwater_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadUsgsNwisGroundwater_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadUsgsNwisInstantaneous_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadUsgsNwisInstantaneous_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Read_ReadUsgsNwisRdb_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Read_ReadUsgsNwisRdb_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Read_ReadWaterML_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadWaterML_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadWaterML2_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadWaterML2_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_ReadWaterOneFlow_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_ReadWaterOneFlow_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Read_StateModMax_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Read_StateModMax_String, null, CommandEditType.INSERT );
    }
	else {
		// Chain to next menus.
		uiAction_ActionPerformed07_CommandsFillMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Fill... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed07_CommandsFillMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

    if (command.equals( TSToolConstants.Commands_Fill_FillConstant_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillConstant_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillDayTSFrom2MonthTSAnd1DayTS_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillFromTS_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillFromTS_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillHistMonthAverage_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillHistMonthAverage_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillHistYearAverage_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillHistYearAverage_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillInterpolate_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillInterpolate_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillMixedStation_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillMixedStation_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillMOVE1_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillMOVE1_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillMOVE2_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillMOVE2_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillPattern_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillPattern_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Fill_ReadPatternFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Fill_ReadPatternFile_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Fill_FillProrate_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillProrate_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillRegression_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillRegression_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_FillRepeat_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_FillRepeat_String, null, CommandEditType.INSERT );
	}
	else if(command.equals( TSToolConstants.Commands_Fill_FillUsingDiversionComments_String)){
		commandList_EditCommand (TSToolConstants.Commands_Fill_FillUsingDiversionComments_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Fill_SetAutoExtendPeriod_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Fill_SetAutoExtendPeriod_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_SetAveragePeriod_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_SetAveragePeriod_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Fill_SetIgnoreLEZero_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Fill_SetIgnoreLEZero_String, null, CommandEditType.INSERT );
	}
	else {
		// Chain to other menus.
		uiAction_ActionPerformed08_CommandsSetMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Set... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed08_CommandsSetMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	if (command.equals( TSToolConstants.Commands_Set_ReplaceValue_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_ReplaceValue_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Set_SetConstant_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_SetConstant_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Set_SetDataValue_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_SetDataValue_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Set_SetFromTS_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_SetFromTS_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Set_SetTimeSeriesValuesFromLookupTable_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Set_SetTimeSeriesValuesFromLookupTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Set_SetTimeSeriesValuesFromTable_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Set_SetTimeSeriesValuesFromTable_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Set_SetToMax_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_SetToMax_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Set_SetToMin_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Set_SetToMin_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Set_SetTimeSeriesProperty_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Set_SetTimeSeriesProperty_String, null, CommandEditType.INSERT );
    }
	else {
		uiAction_ActionPerformed09_CommandsManipulateMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Manipulate... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed09_CommandsManipulateMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	if (command.equals( TSToolConstants.Commands_Manipulate_Add_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Add_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Manipulate_AddConstant_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_AddConstant_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Manipulate_AdjustExtremes_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_AdjustExtremes_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Manipulate_ARMA_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_ARMA_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Manipulate_Blend_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Blend_String, null, CommandEditType.INSERT );
	}
    else if (command.equals(TSToolConstants.Commands_Manipulate_ChangePeriod_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Manipulate_ChangePeriod_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Manipulate_ChangeTimeZone_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Manipulate_ChangeTimeZone_String, null, CommandEditType.INSERT );
    }
	else if (command.equals(TSToolConstants.Commands_Manipulate_ConvertDataUnits_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_ConvertDataUnits_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Manipulate_Cumulate_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Cumulate_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Manipulate_Divide_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Divide_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Manipulate_Multiply_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Multiply_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Manipulate_Scale_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Scale_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_Manipulate_ShiftTimeByInterval_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_ShiftTimeByInterval_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Manipulate_Subtract_String)) {
		commandList_EditCommand ( TSToolConstants.Commands_Manipulate_Subtract_String, null, CommandEditType.INSERT );
	}
	else {
		// Chain to next actions.
		uiAction_ActionPerformed10_CommandsAnalyzeMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Analyze... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed10_CommandsAnalyzeMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	if (command.equals( TSToolConstants.Commands_Analyze_AnalyzePattern_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Analyze_AnalyzePattern_String,	null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Analyze_CalculateTimeSeriesStatistic_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Analyze_CalculateTimeSeriesStatistic_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Analyze_CompareTimeSeries_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Analyze_CompareTimeSeries_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Analyze_ComputeErrorTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Analyze_ComputeErrorTimeSeries_String, null, CommandEditType.INSERT );
    }
	else {
		// Chain to other actions.
		uiAction_ActionPerformed11_CommandsModelsMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Models*... menus.
@param event Event to handle.
*/
private void uiAction_ActionPerformed11_CommandsModelsMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

	if (command.equals( TSToolConstants.Commands_Models_Routing_LagK_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Models_Routing_LagK_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Models_Routing_VariableLagK_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Models_Routing_VariableLagK_String, null, CommandEditType.INSERT );
    }
	else {
		// Chain to other actions.
		uiAction_ActionPerformed12_CommandsEnsembleMenu ( event );
	}
}

/**
Handle a group of actions for the Commands...Ensemble... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed12_CommandsEnsembleMenu (ActionEvent event)
throws Exception {
   String command = event.getActionCommand();

    if (command.equals( TSToolConstants.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_CreateEnsembleFromOneTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_CopyEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_CopyEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_NewEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_NewEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_ReadNwsrfsEspTraceEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_ReadNwsrfsEspTraceEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_InsertTimeSeriesIntoEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_SetEnsembleProperty_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_SetEnsembleProperty_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Ensemble_NewStatisticEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_NewStatisticEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_NewStatisticTimeSeriesFromEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Ensemble_WeightTraces_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_WeightTraces_String, null, CommandEditType.INSERT );
    }
    else if(command.equals( TSToolConstants.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Ensemble_WriteNwsrfsEspTraceEnsemble_String, null, CommandEditType.INSERT );
    }
    else {
        // Chain to other actions.
        uiAction_ActionPerformed13_CommandsOutputMenu ( event );
    }
}

/**
Handle a group of actions for the Commands...Output... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed13_CommandsOutputMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

    if (command.equals(TSToolConstants.Commands_Output_SetOutputDetailedHeaders_String) ) {
		commandList_EditCommand (TSToolConstants.Commands_Output_SetOutputDetailedHeaders_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Output_SetOutputPeriod_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_Output_SetOutputPeriod_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Output_SetOutputYearType_String) ){
		commandList_EditCommand ( TSToolConstants.Commands_Output_SetOutputYearType_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Output_WriteDateValue_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteDateValue_String, null, CommandEditType.INSERT );
	}
	//else if (command.equals( TSToolConstants.Commands_Output_WriteDelftFewsPiXml_String)){
	//	commandList_EditCommand ( TSToolConstants.Commands_Output_WriteDelftFewsPiXml_String, null, CommandEditType.INSERT );
	//}
    else if (command.equals( TSToolConstants.Commands_Output_WriteDelimitedFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteDelimitedFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Output_WriteHecDss_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteHecDss_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Output_WriteNwsCard_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteNwsCard_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Output_WriteReclamationHDB_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteReclamationHDB_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Output_WriteRiverWare_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteRiverWare_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_Output_WriteSHEF_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteSHEF_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_Output_WriteStateCU_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteStateCU_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Output_WriteStateMod_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteStateMod_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_Output_WriteSummary_String)){
		commandList_EditCommand ( TSToolConstants.Commands_Output_WriteSummary_String, null, CommandEditType.INSERT );
	}
    // See also TSToolConstants.Commands_Datastore_WriteTimeSeriesToDataStore which duplicates the output menu
    else if (command.equals( TSToolConstants.Commands_Output_WriteTimeSeriesToDataStream_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteTimeSeriesToDataStream_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Output_WriteTimeSeriesToHydroJSON_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteTimeSeriesToHydroJSON_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Output_WriteTimeSeriesToJson_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteTimeSeriesToJson_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Output_WriteWaterML_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteWaterML_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Output_WriteWaterML2_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Output_WriteWaterML2_String, null, CommandEditType.INSERT );
    }
    // TSToolConstants.Commands_Output_WriteTimeSeriesPropertiesToFile handled in testing commands.
	else {
		// Chain to next list of commands.
		uiAction_ActionPerformed14_CommandsGeneralMenu ( event );
	}
}

/**
Handle a group of actions for the "Commands...Network Processing", "Commands...Spatial Processing",
"Commands...Spreadsheet Processing",
"Commands...Table Processing" and "Commands...General..." menu.
Also include a couple of special open commands for input types.
@param event Event to handle.
*/
private void uiAction_ActionPerformed14_CommandsGeneralMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

    // Datastore commands.

    if (command.equals( TSToolConstants.Commands_Datastore_NewAccessDatabase_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_NewAccessDatabase_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_NewDerbyDatabase_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_NewDerbyDatabase_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_NewSQLiteDatabase_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_NewSQLiteDatabase_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_OpenDataStore_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_OpenDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_ReadTableFromDataStore_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_ReadTableFromDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_WriteTableToDataStore_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_WriteTableToDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_DeleteDataStoreTableRows_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_DeleteDataStoreTableRows_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_RunSql_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_RunSql_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_ReadTimeSeriesFromDataStore_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_ReadTimeSeriesFromDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_WriteTimeSeriesToDataStore_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_WriteTimeSeriesToDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_CloseDataStore_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_CloseDataStore_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_CreateDataStoreDataDictionary_String)) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_CreateDataStoreDataDictionary_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Datastore_SetPropertyFromDataStore_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Datastore_SetPropertyFromDataStore_String, null, CommandEditType.INSERT );
    }

    // Network commands.

    else if (command.equals( TSToolConstants.Commands_Network_CreateNetworkFromTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Network_CreateNetworkFromTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Network_AnalyzeNetworkPointFlow_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Network_AnalyzeNetworkPointFlow_String, null, CommandEditType.INSERT );
    }

    // Object commands.

    else if (command.equals( TSToolConstants.Commands_Object_NewObject_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_NewObject_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Object_FreeObject_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_FreeObject_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Object_SetObjectProperty_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_SetObjectProperty_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Object_SetObjectPropertiesFromTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_SetObjectPropertiesFromTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Object_SetPropertyFromObject_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_SetPropertyFromObject_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Object_WriteObjectToJSON_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Object_WriteObjectToJSON_String, null, CommandEditType.INSERT );
    }

    // Spatial commands.

    else if (command.equals( TSToolConstants.Commands_Spatial_WriteTableToGeoJSON_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spatial_WriteTableToGeoJSON_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spatial_WriteTableToKml_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spatial_WriteTableToKml_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spatial_WriteTableToShapefile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spatial_WriteTableToShapefile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spatial_WriteTimeSeriesToGeoJSON_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spatial_WriteTimeSeriesToGeoJSON_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spatial_WriteTimeSeriesToKml_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spatial_WriteTimeSeriesToKml_String, null, CommandEditType.INSERT );
    }

    // Spreadsheet commands.

    else if (command.equals( TSToolConstants.Commands_Spreadsheet_NewExcelWorkbook_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_NewExcelWorkbook_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_ReadExcelWorkbook_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_ReadExcelWorkbook_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_ReadTableFromExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_ReadTableFromExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_ReadTableCellsFromExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_ReadTableCellsFromExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_ReadPropertiesFromExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_ReadPropertiesFromExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_SetExcelCell_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_SetExcelCell_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_SetExcelWorksheetViewProperties_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_SetExcelWorksheetViewProperties_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_WriteTableToExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_WriteTableToExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_WriteTableCellsToExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_WriteTableCellsToExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcel_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcel_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_WriteTimeSeriesToExcelBlock_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Spreadsheet_CloseExcelWorkbook_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Spreadsheet_CloseExcelWorkbook_String, null, CommandEditType.INSERT );
    }

    // Table commands.

    else if (command.equals( TSToolConstants.Commands_TableCreate_NewTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableCreate_NewTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableCreate_CopyTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableCreate_CopyTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableJoin_AppendTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableJoin_AppendTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableJoin_JoinTables_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableJoin_JoinTables_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_SortTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_SortTable_String, null, CommandEditType.INSERT );
    }
    // See TSToolConstants.Commands_Tble_ReadTableFromDataStore, which is duplicated in Table menu
    else if (command.equals( TSToolConstants.Commands_TableRead_ReadTableFromDelimitedFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRead_ReadTableFromDelimitedFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRead_ReadTableFromDBF_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRead_ReadTableFromDBF_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRead_ReadTableFromFixedFormatFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRead_ReadTableFromFixedFormatFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRead_ReadTableFromJSON_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRead_ReadTableFromJSON_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRead_ReadTableFromXML_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRead_ReadTableFromXML_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableTimeSeries_SetTimeSeriesPropertiesFromTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableTimeSeries_SetTimeSeriesPropertiesFromTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableTimeSeries_CopyTimeSeriesPropertiesToTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableTimeSeries_CopyTimeSeriesPropertiesToTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableTimeSeries_TimeSeriesToTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableTimeSeries_TimeSeriesToTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableTimeSeries_TableToTimeSeries_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableTimeSeries_TableToTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableTimeSeries_CreateTimeSeriesEventTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableTimeSeries_CreateTimeSeriesEventTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_FormatTableDateTime_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_FormatTableDateTime_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_FormatTableString_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_FormatTableString_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_ManipulateTableString_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_ManipulateTableString_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_InsertTableColumn_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_InsertTableColumn_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_DeleteTableColumns_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_DeleteTableColumns_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_DeleteTableRows_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_DeleteTableRows_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_InsertTableRow_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_InsertTableRow_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_RenameTableColumns_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_RenameTableColumns_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_SetTableColumnProperties_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_SetTableColumnProperties_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_SetTableValues_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_SetTableValues_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_SplitTableColumn_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_SplitTableColumn_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_SplitTableRow_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_SplitTableRow_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_TableMath_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_TableMath_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableManipulate_TableTimeSeriesMath_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableManipulate_TableTimeSeriesMath_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableAnalyze_CompareTables_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableAnalyze_CompareTables_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableOutput_WriteTableToDelimitedFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableOutput_WriteTableToDelimitedFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableOutput_WriteTableToHTML_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableOutput_WriteTableToHTML_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableOutput_WriteTableToMarkdown_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableOutput_WriteTableToMarkdown_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableCreate_FreeTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableCreate_FreeTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRunning_SetPropertyFromTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRunning_SetPropertyFromTable_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_TableRunning_CopyPropertiesToTable_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_TableRunning_CopyPropertiesToTable_String, null, CommandEditType.INSERT );
    }

	// Template commands.

    else if (command.equals( TSToolConstants.Commands_Template_ExpandTemplateFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Template_ExpandTemplateFile_String, null, CommandEditType.INSERT );
    }

    // Data visualization commands.

    if (command.equals( TSToolConstants.Commands_Visualization_ProcessTSProduct_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Visualization_ProcessTSProduct_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Visualization_ProcessRasterGraph_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Visualization_ProcessRasterGraph_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_Visualization_NewTreeView_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Visualization_NewTreeView_String, null, CommandEditType.INSERT );
    }

	// General commands.
    // General - Logging commands.
	else if (command.equals( TSToolConstants.Commands_General_Logging_ConfigureLogging_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Logging_ConfigureLogging_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_Logging_StartLog_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Logging_StartLog_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_Logging_SetDebugLevel_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Logging_SetDebugLevel_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_Logging_SetWarningLevel_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Logging_SetWarningLevel_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_General_Logging_Message_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Logging_Message_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Logging_SendEmailMessage_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Logging_SendEmailMessage_String, null, CommandEditType.INSERT );
    }
    // General - Running commands.
	else if (command.equals( TSToolConstants.Commands_General_Running_SetWorkingDir_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Running_SetWorkingDir_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_General_Running_ProfileCommands_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_ProfileCommands_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeries_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Check_CheckingResults_CheckTimeSeriesStatistic_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Check_CheckingResults_WriteCheckFile_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Check_CheckingResults_WriteCheckFile_String, null, CommandEditType.INSERT );
    }
	else if (command.equals(TSToolConstants.Commands_General_Comments_Comment_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Comments_Comment_String, null, CommandEditType.INSERT );
	}
    else if (command.equals(TSToolConstants.Commands_General_Comments_AuthorComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@author insert name, organization, contact, etc.",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_AuthorComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_DocExampleComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@docExample - command file is used as an example in the command's documentation", true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_DocExampleComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_DocUrlComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@docUrl https://path/to/command-file-documentation/",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_DocUrlComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_EnabledComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@enabled False",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_EnabledComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_EnabledIfApplicationComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@enabledif application TSTool version >= X.YY.ZZ",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_EnabledIfApplicationComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_EnabledIfDatastoreComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@enabledif datastore HydroBase version >= YYYYMMDD",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_EnabledIfDatastoreComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_ExpectedStatusFailureComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@expectedStatus Failure",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_ExpectedStatusFailureComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_ExpectedStatusWarningComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@expectedStatus Warning",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_ExpectedStatusWarningComment_String, comments, CommandEditType.INSERT );
    }
    /*
    else if (command.equals(TSToolConstants.Commands_General_Comments_FileModTimeComment_String) ) {
        // Most inserts let the editor format the command.
        // However, in this case the specific comment needs to be supplied.
        // Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@fileModTime File1Path > File2Path",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_FileModTimeComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_FileSizeComment_String) ) {
        // Most inserts let the editor format the command.
        // However, in this case the specific comment needs to be supplied.
        // Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@fileSize File1Path > File1Bytes",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_FileSizeComment_String, comments, CommandEditType.INSERT );
    }
    */
    else if (command.equals(TSToolConstants.Commands_General_Comments_FixMeComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
    	DateTime now = new DateTime ( DateTime.DATE_CURRENT );
        comments.add ( commandList_NewCommand("#@fixme " + IOUtil.getProgramUser() + " " +
        	now.toString(DateTime.FORMAT_YYYY_MM_DD) + " Add text here", true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_FixMeComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_ToDoComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
    	DateTime now = new DateTime ( DateTime.DATE_CURRENT );
        comments.add ( commandList_NewCommand("#@todo " + IOUtil.getProgramUser() + " " +
        	now.toString(DateTime.FORMAT_YYYY_MM_DD) + " Add text here", true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_ToDoComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_IdComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@id CommandFileId",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_IdComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_OrderComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@order before/after CommandFileId",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_OrderComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_RequireApplicationComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@require application TSTool version >= X.YY.ZZ",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_RequireApplicationComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_RequireDatastoreComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@require datastore HydroBase version >= YYYYMMDD",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_RequireDatastoreComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_RequireUserComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
    	List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@require user == username",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_RequireUserComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_ReadOnlyComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@readOnly - command file is not intended to be saved from within TSTool",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_ReadOnlyComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_RunDiscoveryFalseComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@runDiscovery False",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_RunDiscoveryFalseComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_SourceUrlComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@sourceUrl https://path/to/command-file.tstool",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_SourceUrlComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_TemplateComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@template - command file is not intended to be saved from within TSTool - use a text editor to edit",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_TemplateComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_VersionComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@version 1.2.3 or YYYY-MM-DD, etc., use a @versionDate comment for date",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_VersionComment_String, comments, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Comments_VersionDateComment_String) ) {
        // Most inserts let the editor format the command.
    	// However, in this case the specific comment needs to be supplied.
    	// Otherwise, the comment will be blank or the string from the menu, which has too much text.
        List<Command> comments = new ArrayList<>(1);
        comments.add ( commandList_NewCommand("#@versionDate YYYY-MM-DD or YYYY-MM-DDThh:mm, etc.",true) );
        commandList_EditCommand ( TSToolConstants.Commands_General_Comments_VersionDateComment_String, comments, CommandEditType.INSERT );
    }
	else if (command.equals(TSToolConstants.Commands_General_Comments_StartComment_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Comments_StartComment_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_General_Comments_EndComment_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Comments_EndComment_String,	null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_General_Comments_Empty_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Comments_Empty_String,	null, CommandEditType.INSERT );
	}
    else if (command.equals(TSToolConstants.Commands_General_Running_If_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_If_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Running_EndIf_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_EndIf_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Running_For_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_For_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Running_EndFor_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_EndFor_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Running_Break_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_Break_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_General_Running_Continue_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_Continue_String, null, CommandEditType.INSERT );
    }
	else if (command.equals(TSToolConstants.Commands_General_Running_Exit_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Running_Exit_String, null, CommandEditType.INSERT );
	}
	else if (command.equals(TSToolConstants.Commands_General_Running_Wait_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Running_Wait_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_General_TestProcessing_StartRegressionTestResultsReport_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_StartRegressionTestResultsReport_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_ReadPropertiesFromFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_ReadPropertiesFromFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_SetProperty_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_SetProperty_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_SetPropertyFromNwsrfsAppDefault_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_SetPropertyFromNwsrfsAppDefault_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_SetPropertyFromEnsemble_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_SetPropertyFromEnsemble_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_SetPropertyFromTimeSeries_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_SetPropertyFromTimeSeries_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_FormatDateTimeProperty_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_FormatDateTimeProperty_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_FormatStringProperty_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_FormatStringProperty_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_WritePropertiesToFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_WritePropertiesToFile_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_General_Running_RunCommands_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Running_RunCommands_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_Running_RunProgram_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_Running_RunProgram_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_General_Running_RunPython_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_RunPython_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_RunR_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_RunR_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_Running_RunDSSUTL_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_General_Running_RunDSSUTL_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_FTPGet_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_FTPGet_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_WebGet_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_WebGet_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_CreateFolder_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_CreateFolder_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_RemoveFolder_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_RemoveFolder_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_AppendFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_AppendFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_CheckFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_CheckFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_CopyFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_CopyFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_FormatFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_FormatFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_ListFiles_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_ListFiles_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_RemoveFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_RemoveFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_TextEdit_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_TextEdit_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_PDFMerge_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_PDFMerge_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_UnzipFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_UnzipFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_FileHandling_PrintTextFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_FileHandling_PrintTextFile_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_General_TestProcessing_CompareFiles_String)){
		commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_CompareFiles_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_TestProcessing_WriteProperty_String)){
		commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_WriteProperty_String, null, CommandEditType.INSERT );
	}
    else if (command.equals( TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesPropertiesToFile_String, null, CommandEditType.INSERT );
    }
    else if (command.equals( TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesProperty_String)){
        commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_WriteTimeSeriesProperty_String, null, CommandEditType.INSERT );
    }
	else if (command.equals( TSToolConstants.Commands_General_TestProcessing_TestCommand_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_TestCommand_String, null, CommandEditType.INSERT );
	}
	else if (command.equals( TSToolConstants.Commands_General_TestProcessing_CreateRegressionTestCommandFile_String) ) {
		commandList_EditCommand ( TSToolConstants.Commands_General_TestProcessing_CreateRegressionTestCommandFile_String, null, CommandEditType.INSERT );
	}

    // Deprecated commands.

	else if (command.equals(TSToolConstants.Commands_Deprecated_OpenHydroBase_String)){
        commandList_EditCommand ( TSToolConstants.Commands_Deprecated_OpenHydroBase_String, null, CommandEditType.INSERT );
    }
    else if (command.equals(TSToolConstants.Commands_Deprecated_RunningAverage_String) ) {
        commandList_EditCommand ( TSToolConstants.Commands_Deprecated_RunningAverage_String, null, CommandEditType.INSERT );
    }
	else {
		// Chain to other actions.
		uiAction_ActionPerformed15_RunMenu ( event );
	}
}

/**
Handle a group of actions for the Run menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed15_RunMenu (ActionEvent event)
throws Exception {
    String command = event.getActionCommand();
    String routine = getClass().getSimpleName() + ".uiAction_ActionPerformed4_RunMenu";

    // Run menu (order in menu).

    if ( command.equals(TSToolConstants.Run_AllCommandsCreateOutput_String) ) {
        // Process time series and create all output from Write* commands.
        uiAction_RunCommands ( true, true );
    }
    else if ( command.equals(TSToolConstants.Run_AllCommandsIgnoreOutput_String) ) {
        // Process time series but ignore write* commands.
        uiAction_RunCommands ( true, false );
    }
    else if ( command.equals(TSToolConstants.Run_SelectedCommandsCreateOutput_String) ) {
        // Process selected commands and create all output from Write* commands.
        uiAction_RunCommands ( false, true );
    }
    else if ( command.equals(TSToolConstants.Run_SelectedCommandsIgnoreOutput_String) ) {
        // Process selected commands but ignore write* commands.
        uiAction_RunCommands ( false, false );
    }
    else if (command.equals(TSToolConstants.Run_CancelCommandProcessing_String) ) {
        // Cancel the current processor.  This may take awhile to occur if the current command is doing a lot of work.
        ui_UpdateStatusTextFields ( 1, routine, "Processing is being canceled...", null, TSToolConstants.STATUS_CANCELING );
        ui_UpdateStatus ( true );
        __tsProcessor.setCancelProcessingRequested ( true );
    }
    else if (command.equals(TSToolConstants.Run_CancelCommandProcessesExternal_String) ) {
        // Cancel all processes being run by commands - to fix hung processes.
        commandProcessor_CancelCommandProcessesExternal ();
    }
    else if (command.equals(TSToolConstants.Run_CancelCommandProcessingKill_String) ) {
        // Kill the current processor thread.
        Thread thread =  commandProcessor_GetCommandProcessorThread();
        Message.printStatus(1, routine, "Request to cancel processing, thread=" + thread);
        if ( thread != null ) {
            ui_UpdateStatusTextFields ( 1, routine, "Processing is being canceled...", null, TSToolConstants.STATUS_CANCELING );
            try {
            	// This may cause a cascade of InterruptedException:
            	// - more tricky if in a wait() or sleep, such as Wait() command
            	thread.interrupt();
            	// Indicate that the process is done running.
            }
            catch ( SecurityException e ) {
            	Message.printStatus(1, routine, "Exception canceling processing (" + e + ")." );
            }
            ui_UpdateStatus ( true );
	        commandProcessor_SetCommandProcessorThread(null);
	        ui_UpdateStatusTextFields ( 1, routine, "Processing has been canceled.", null, TSToolConstants.STATUS_CANCELED );
	        // Set the state on the run buttons so can run again:
	        ui_CheckGUIState();
        }
    }
    else if ( command.equals(TSToolConstants.Run_CommandsFromFile_String) ) {
        // Get the name of the file to run and then execute a TSCommandProcessor as if in batch mode.
        uiAction_RunCommandFile ();
    }
    else if (command.equals(TSToolConstants.Run_ProcessTSProductOutput_String) ) {
        // Test code.
        try {
            uiAction_ProcessTSProductFile ( null, false );
        }
        catch ( Exception te ) {
            Message.printWarning ( 1, "", "Error processing TSProduct file." );
            Message.printWarning ( 2, "", te );
        }
    }
    else {
        // Chain to the next method.
        uiAction_ActionPerformed16_ResultsMenu ( event );
    }
}

/**
Handle a group of actions for the View menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed16_ResultsMenu (ActionEvent event)
throws Exception {
	String command = event.getActionCommand();

    if ( command.equals(TSToolConstants.Results_Graph_AnnualTraces_String) ) {
		// Only do if data are selected.
		String response = new TextResponseJDialog (
			this, "Graph Annual Traces", "Enter the 4-digit year to use as a reference.",
			ResponseJDialog.OK|ResponseJDialog.CANCEL ).response();
		if ( response == null ) {
			return;
		}
		uiAction_GraphTimeSeriesResults("-oannual_traces_graph " + StringUtil.atoi(response) );
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Area_String) ) {
        uiAction_GraphTimeSeriesResults("-oarea_graph");
    }
    else if ( command.equals(TSToolConstants.Results_Graph_AreaStacked_String) ) {
        uiAction_GraphTimeSeriesResults("-oarea_stacked_graph");
    }
    else if ( command.equals(TSToolConstants.Results_Graph_BarsLeft_String) ) {
    	uiAction_GraphTimeSeriesResults("-obar_graph", "BarsLeftOfDate");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_BarsCenter_String) ) {
    	uiAction_GraphTimeSeriesResults("-obar_graph", "BarsCenteredOnDate");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_BarsRight_String) ) {
    	uiAction_GraphTimeSeriesResults("-obar_graph", "BarsRightOfDate");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_DoubleMass_String) ) {
    	uiAction_GraphTimeSeriesResults("-odoublemassgraph");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Duration_String) ) {
		// Only do if data are selected.
    	uiAction_GraphTimeSeriesResults("-oduration_graph " );
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Ensemble_String) ) {
    	// This event corresponds to:
    	// 1) a time series is selected in results
    	// 2) Graph - Ensemble
    	// Display the dialog to confirm how to convert the time series to ensemble and graph.
    	boolean isDialogForTS = true;
    	EnsembleGraph_JDialog dialog = new EnsembleGraph_JDialog(this, this.session, isDialogForTS, new PropList(""));
    	String userOutputYearType = dialog.getOutputYearType();
    	String userReferenceDateTime = dialog.getReferenceDate().trim();
    	String userStatistics = dialog.getStatistics().trim();
    	String userGraphTemplate = dialog.getGraphTemplate().trim();
    	String[] statisticsArray = new String[0];
    	if ( !userStatistics.isEmpty() ) {
    		statisticsArray = userStatistics.split(",");
    		for ( int istat = 0; istat < statisticsArray.length; istat++ ) {
    			statisticsArray[istat] = statisticsArray[istat].trim();
    		}
    	}
    	boolean ok = dialog.ok();
    	if ( ok ) {
	    	// Create the ensemble from the single time series based on the properties from the dialog.
	    	// This is the same code called by the CreateEnsembleFromOneTimeSeries() command.
	    	TSUtil_CreateTracesFromTimeSeries util = new TSUtil_CreateTracesFromTimeSeries();
	    	String alias = null;
	    	String descriptionFormat = "%D"; // Just the main description rather than including trace ID.
	    	String traceLength = "1Year";
	    	boolean createData = true;
	    	String shiftDataHow = "ShiftToReference";
	    	YearType outputYearType = YearType.CALENDAR; // Default.
	    	if ( (userOutputYearType != null) && !userOutputYearType.isEmpty() ) {
	    		outputYearType = YearType.valueOfIgnoreCase(userOutputYearType);
	    	}
	    	// Default reference is the start of the current year type.
	    	DateTime referenceDateTime = null;
	    	if ( (userReferenceDateTime != null) && !userReferenceDateTime.isEmpty() ) {
	    		referenceDateTime = DateTime.parse(userReferenceDateTime);
	    	}
	    	else {
	    		// Default is to use start of current year for output year type.
	    		referenceDateTime = outputYearType.getStartDateTimeForCurrentYear();
	    	}
	    	Message.printStatus(2, "", "referenceDateTime=" + referenceDateTime);
	    	DateTime inputStart = null;
	    	DateTime inputEnd = null;
	    	// Time series is the first selected time series in the results.
	    	int pos = -1;
	    	if ( JGUIUtil.selectedSize(__resultsTS_JList) == 0 ) {
				pos = 0;
			}
			else {
	            pos = JGUIUtil.selectedIndex(__resultsTS_JList,0);
			}
	    	List<TS> tslist = new ArrayList<>();
	    	TS ts = null;
			if ( pos >= 0 ) {
				ts = commandProcessor_GetTimeSeries(pos);
			}
			// Get the time series for the ensemble.
			String propVal = null;
			File userGraphTemplateFile = null;
			if ( (userGraphTemplate != null) && !userGraphTemplate.isEmpty() ) {
				userGraphTemplateFile = this.session.getGraphTemplateFile(userGraphTemplate);
				TSProduct tsp0 = new TSProduct(userGraphTemplateFile.getAbsolutePath(),new PropList(""));
				propVal = tsp0.getLayeredPropValue("TemplatePreprocessCommandFile", -1, -1);
				Message.printStatus(2,"","Value of TemplatePreprocessCommandFile = \"" + propVal + "\"");
			}
			// Ensemble is necessary when processing statistics.
			TSEnsemble tsensemble = null;
			TSCommandFileRunner runner = null;
			if ( (propVal != null) && !propVal.isEmpty() ) {
				// Get the time series by processing the specified command file.
				// Command file in template is relative to the template folder.
				String preprocessCommandFile = IOUtil.verifyPathForOS(
				    IOUtil.toAbsolutePath(userGraphTemplateFile.getParent(),propVal) );
				runner = new TSCommandFileRunner(
					this.__tsProcessor.getInitialPropList(),
					this.__tsProcessor.getPluginCommandClasses());
				Message.printStatus(2,"","Preprocess command file for graph template is \"" + preprocessCommandFile + "\"");
				runner.readCommandFile(preprocessCommandFile, false);
				// Have to seed the processor with the time series from the original processor
				// so it can be found for subsequent processing.
				Message.printStatus(2,"","Running internal processor to preprocess time series into ensemble");
				@SuppressWarnings("unchecked")
				List<TS> tslist0 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist0.add(ts);
				runner.getProcessor().setPropContents("Recursive","true");
				runner.runCommands(null);
				// Now get the time series out and use for the graphing.
				@SuppressWarnings("unchecked")
				List<TS> tslist1 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist = tslist1;
				Message.printStatus(2,"","After running internal processor have " + tslist.size() + " time series.");
			}
			else {
				// Process the single time series from above into ensemble.
				TransferDataHowType transferDataHowType = TransferDataHowType.SEQUENTIALLY;
		        tslist = util.getTracesFromTS ( ts, traceLength, referenceDateTime,
			        outputYearType, shiftDataHow, transferDataHowType,
			        inputStart, inputEnd, alias, descriptionFormat, createData );
		        // Create a new list for the ensemble because when statistic time series are computed and
		        // added below the should not be added to the original list.
		        List<TS> tslist2 = new ArrayList<>();
		        tslist2.addAll(tslist);
		        tsensemble = new TSEnsemble (ts.getLocation() + "_Ensemble", ts.getDescription(), tslist2);
			}
			// If any statistics were requested, process and add to the list, but not in the ensemble itself.
	        // This is similar to the NewStatisticTimeSeriesFromEnsemble() command functionality.
			for ( int istat = 0; istat < statisticsArray.length; istat++ ) {
				TSStatisticType statType = TSStatisticType.valueOfIgnoreCase(statisticsArray[istat]);
				DateTime analysisStart = null;
				DateTime analysisEnd = null;
				DateTime outputStart = null;
				DateTime outputEnd = null;
				String description = ts.getDescription() + ", " + statType;
				Integer allowMissingCount = null;
				Integer minimumSampleSize = null;
				Double value1 = null;
				// The newTSID is not critical, but want to make sure the alias and sequence ID is properly set.
				TSIdent tsident = new TSIdent(ts.getIdentifier());
				tsident.setSequenceID("");
				tsident.setInputName("");
				tsident.setInputType("");
				tsident.setType(tsident.getType() + "-" + statType);
				String newTSID = tsident.toString();
				// Important - the tsensemble was created with a separate time series list,
				// so it is OK to add statistic time series to the list below (won't be the same list in the ensemble).
			    TSUtil_NewStatisticTimeSeriesFromEnsemble tsu = new TSUtil_NewStatisticTimeSeriesFromEnsemble (
				    tsensemble, analysisStart, analysisEnd, outputStart, outputEnd,
				    newTSID, description, statType, value1, allowMissingCount, minimumSampleSize );
				TS stat_ts = tsu.newStatisticTimeSeriesFromEnsemble ( createData );
				stat_ts.setAlias(ts.getLocation() + "_" + statType);
				stat_ts.getIdentifier().setSequenceID(""+ statType); // So %z legend will show statistic
				tslist.add(stat_ts);
			}
			if ( (userGraphTemplate != null) && !userGraphTemplate.isEmpty() ) {
				// If a graph template was specified, expand it with properties that are relevant
				// and then graph using similar logic to ProcessTSProduct() command,
				// but pass the time series in directly rather than searching in the processor results.
				// Determine whether a command file should be run to preprocess the time series for the template.
				String tempTSPFile = IOUtil.tempFileName() + "-TSTool-template.tsp";
				GraphTemplateProcessor graphTemplateProcessor = new GraphTemplateProcessor (
					this.session.getGraphTemplateFile(userGraphTemplate) );
				// Create a model.
				CommandProcessor runnerProcessor = null;
				if ( runner != null ) {
					runnerProcessor = runner.getProcessor();
				}
				List<TSEnsemble> tsensembleList = new ArrayList<>();
				tsensembleList.add(tsensemble);
				graphTemplateProcessor.expandTemplate (tslist, tsensembleList, commandProcessor_GetCommandProcessor(),
					runnerProcessor, new File(tempTSPFile));
				Message.printStatus(2, "", "Expanded temporary graph template to \"" + tempTSPFile + "\"");
				TSProcessor p = new TSProcessor();
				PropList overrideProps = new PropList ( "OverrideProps" );
				overrideProps.set ( "InitialView", "Graph" ); // Initial view when display opened.
				overrideProps.set ( "PreviewOutput", "True" ); // Display a view window (not just file output).
	 			overrideProps.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
				TSProduct tsp = new TSProduct ( tempTSPFile, overrideProps );
				// Now process the product.
				p.addTSSupplier(graphTemplateProcessor);
				p.processProduct ( tsp );
			}
			else {
				// No graph template so use the normal graphing approach.
		    	// Display the graph using the created list of time series from the ensemble:
		        // - rather than using the time series in the processor, use the supplied list
				PropList graphProps = new PropList("GraphProps");
				// TODO smalers 2017-04-08 there is currently no way to pass these properties:
				// - alternative is to use the template
				// - need to figure out how to pass in properties that goes to the TSProduct
				// - currently the following does nothing
				graphProps.set("Subproduct 1.LegendPosition","Left");
				graphProps.set("Subproduct 1.LegendFormat","%z"); // Would require setting the statistic as the sequence ID.
		    	uiAction_GraphEnsembleResults(tslist,"-olinegraph",graphProps);
			}
    	}
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Line_String) ) {
    	uiAction_GraphTimeSeriesResults("-olinegraph");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_LineLogY_String) ) {
        uiAction_GraphTimeSeriesResults("-olinelogygraph");
	}
/* Not enabled.
        else if ( command.equals("GraphPercentExceed") ) {
		// Because Visualize can only handle grid-based data, only allow
		// one time series to be graphed to ensure that the data set is
		// nice.
		if ( _final__commands_JList != 1 ) {
			Message.printWarning ( 1, rtn, "Only one time " +
			"series can be graphed for Percent Exceedance Curve." );
		}
		else {	// OK to do the graph...
			graphTS("-opercentexceedgraph");
		}
	}
*/
    else if ( command.equals(TSToolConstants.Results_Graph_PeriodOfRecord_String) ) {
		uiAction_GraphTimeSeriesResults("-oporgraph");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Point_String) ) {
    	uiAction_GraphTimeSeriesResults("-opointgraph");
	}
    else if ( command.equals(TSToolConstants.Results_Graph_PredictedValue_String) ) {
    	uiAction_GraphTimeSeriesResults("-oPredictedValue_graph" );
	}
    else if (command.equals(TSToolConstants.Results_Graph_PredictedValueResidual_String)){
    	uiAction_GraphTimeSeriesResults("-oPredictedValueResidual_graph" );
	}
    else if ( command.equals(TSToolConstants.Results_Graph_Raster_String) ) {
    	// Do checks here rather than trying to handle low-level exceptions:
    	// - if a single time series is selected, it must be day or month interval
    	// - if multiple time series are selected, the interval must be the same
    	List<TS> tslist = results_TimeSeries_GetList ( true );
    	// Make sure that no time series are irregular interval.
   		if ( TSUtil.areAnyTimeSeriesIrregular(tslist) ) {
   			Message.printWarning(1, "", "Raster graphs cannot be created for irregular interval time series.");
   			return;
   		}
    	// Time series are regular interval so do additional checks.
    	if ( tslist.size() == 1 ) {
    		// Single time series:
    		// - must be N-minute, 1-hour, 1-day, 1-month, or 1-year interval
    		TS ts = tslist.get(0);
    		int intervalBase = ts.getDataIntervalBase();
    		int intervalMult = ts.getDataIntervalMult();
    		if ( (intervalBase == TimeInterval.MINUTE)
    			|| ((intervalBase == TimeInterval.HOUR) && (intervalMult == 1))
    			|| ((intervalBase == TimeInterval.DAY) && (intervalMult == 1))
    			|| ((intervalBase == TimeInterval.MONTH) && (intervalMult == 1))
    			|| ((intervalBase == TimeInterval.YEAR) && (intervalMult == 1)) ) {
    			// OK
    		}
    		else {
    			Message.printWarning(1, "",
    				"A single time series raster graph can only be created for N-minute, 1-hour, day, month, or year interval time series.");
    			return;
    		}
    	}
    	else {
    		// Multiple time series:
    		// - all the time series must have the same interval
    		if ( !TSUtil.areIntervalsSame(tslist) ) {
    			Message.printWarning(1, "",
    				"A multiple time series raster graph can only be created for time series with the same regular interval.");
    			return;
    		}
    	}
    	// OK to graph.
        uiAction_GraphTimeSeriesResults("-oraster_graph" );
    }
    else if ( command.equals(TSToolConstants.Results_Graph_XYScatter_String) ) {
    	uiAction_GraphTimeSeriesResults("-oxyscatter_graph" );
	}
    else if ( command.equals(TSToolConstants.Results_Table_String) ) {
		// For now handle similar to the summary report, forcing a preview.
    	uiAction_ExportTimeSeriesResults("-otable", "-preview" );
	}
    else if ( command.equals(TSToolConstants.Results_Report_Summary_Html_String) ) {
        // SAM.  Let the ReportJFrame prompt for this.
    	// This is different from the StateMod output in that when a summary is exported in the GUI,
    	// the user views first and then saves to disk.
        uiAction_ExportTimeSeriesResults("-osummaryhtml", "-preview" );
    }
    else if ( command.equals(TSToolConstants.Results_Report_Summary_Text_String) ) {
		// SAM.  Let the ReportJFrame prompt for this.
    	// This is different from the StateMod output in that when a summary is exported in the GUI,
    	// the user views first and then saves to disk.
		uiAction_ExportTimeSeriesResults("-osummary", "-preview" );
	}
	else if (command.equals(TSToolConstants.Results_TimeSeries_FindTimeSeries_String) ) {
		// Find time series in the time series results list.
		new FindInJListJDialog ( this, false, __resultsTS_JList, "Find Time Series" );
	}
    else if ( command.equals(TSToolConstants.Results_TimeSeriesProperties_String) ) {
		// Get the first time series selected in the view window.
		if ( __tsProcessor != null ) {
			int pos = 0;
			if ( JGUIUtil.selectedSize(__resultsTS_JList) == 0 ) {
				pos = 0;
			}
			else {
                pos = JGUIUtil.selectedIndex(__resultsTS_JList,0);
			}
			// Now display the properties.
			if ( pos >= 0 ) {
				PropList props = new PropList ( "" );
				props.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
				new TSPropertiesJFrame ( this, commandProcessor_GetTimeSeries(pos), props );
			}
		}
	}
    // Graph time series ensemble using template.
    else if ( command.equals("GraphTSEnsembleWithTemplate") ) {
    	// The "Graph with template" button was pressed for a selected ensemble so there is no intervening dialog.
    	// Go straight to processing the template file.
    	Message.printStatus(2,"","Graphing ensemble using template (no dialog).");
	    try {
			String userGraphTemplate = __resultsTSEnsemblesGraphTemplates_JComboBox.getSelected();
			// Save state for next TSTool session.
			this.session.setUIStateProperty("Results.Ensembles.GraphTemplate",userGraphTemplate);
			File userGraphTemplateFile = this.session.getGraphTemplateFile(userGraphTemplate);
			// Determine whether a command file should be run to preprocess the time series for the template.
			TSProduct tsp0 = new TSProduct(userGraphTemplateFile.getAbsolutePath(),new PropList(""));
			String preprocessCommandFile = tsp0.getLayeredPropValue("TemplatePreprocessCommandFile", -1, -1);
			Message.printStatus(2,"","Value of *tsp TemplatePreprocessCommandFile=\"" + preprocessCommandFile + "\"");
			List<TS> tslist = new ArrayList<>();
			// Time series is the first selected time series in the results.
	    	int pos = -1;
	    	TSEnsemble tsensemble = null;
	    	if ( JGUIUtil.selectedSize(this.__resultsTSEnsembles_JList) == 0 ) {
				pos = 0;
			}
			else {
	            pos = JGUIUtil.selectedIndex(this.__resultsTSEnsembles_JList,0);
			}
			if ( pos >= 0 ) {
				tsensemble = commandProcessor_GetEnsembleAt(pos);
				tslist = tsensemble.getTimeSeriesList(true);
				Message.printStatus(2, "", "Ensemble to graph: " + tsensemble.getEnsembleID());
			}
			TSCommandFileRunner runner = null;
			List<TSEnsemble> tsensembleList = new ArrayList<>();
			if ( (preprocessCommandFile != null) && !preprocessCommandFile.isEmpty() ) {
				// Have a command file specified by TemplatePreprocessCommandFile property in the tsp
				// so run the command file to preprocess the time series and use for the graph.
				preprocessCommandFile = IOUtil.verifyPathForOS(
					IOUtil.toAbsolutePath(userGraphTemplateFile.getParent(),preprocessCommandFile) );
				Message.printStatus(2,"","Preprocess command file for graph template is \"" + preprocessCommandFile + "\"");
				runner = new TSCommandFileRunner(
					this.__tsProcessor.getInitialPropList(),
					this.__tsProcessor.getPluginCommandClasses());
				runner.readCommandFile(preprocessCommandFile, false);
				// Have to seed the processor with the ensemble and time series from the original processor
				// so they can be found for subsequent processing.
				Message.printStatus(2,"","Running internal processor to preprocess time series for graphing");
				@SuppressWarnings("unchecked")
				List<TSEnsemble> tsensembleList0 = (List<TSEnsemble>)runner.getProcessor().getPropContents("EnsembleResultsList");
				tsensembleList0.add(tsensemble);
				@SuppressWarnings("unchecked")
				List<TS> tslist0 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist0.addAll(tsensemble.getTimeSeriesList(true));
				PropList runProps = new PropList ( "run");
				runProps.set("AppendResults","true");
				runner.runCommands(runProps);
				// Now get the time series out and use for the graphing.
				@SuppressWarnings("unchecked")
				List<TSEnsemble> tsensembleList1 = (List<TSEnsemble>)runner.getProcessor().getPropContents("EnsembleResultsList");
				tsensembleList = tsensembleList1;
				@SuppressWarnings("unchecked")
				List<TS> tslist1 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist = tslist1;
				Message.printStatus(2,"","After running internal processor have " + tslist.size() + " time series.");
			}
			else {
				// No preprocessor specified so process the time series directly.
				// Original ensemble and time series list from above are OK
				// tslist was set above.
				tsensembleList.add(tsensemble);
			}
			String tempTSPFile = IOUtil.tempFileName() + "-TSTool-template.tsp";
			GraphTemplateProcessor graphTemplateProcessor = new GraphTemplateProcessor (userGraphTemplateFile);
			// Create a model.
			CommandProcessor processorFromRunner = null;
			if ( runner != null ) {
				processorFromRunner = runner.getProcessor();
			}
			// Pass empty ensemble list.
			graphTemplateProcessor.expandTemplate (tslist, tsensembleList, commandProcessor_GetCommandProcessor(), processorFromRunner, new File(tempTSPFile));
			Message.printStatus(2, "", "Expanded temporary graph template to \"" + tempTSPFile + "\"");
			TSProcessor p = new TSProcessor();
			PropList overrideProps = new PropList ( "OverrideProps" );
			overrideProps.set ( "InitialView", "Graph" ); // Initial view when display opened.
			overrideProps.set ( "PreviewOutput", "True" ); // Display a view window (not just file output).
			TSProduct tsp = new TSProduct ( tempTSPFile, overrideProps );
			// Now process the product.
			p.addTSSupplier(graphTemplateProcessor);
			p.processProduct ( tsp );
		}
		catch ( Exception te ) {
			Message.printWarning ( 1, "", "Error processing TSProduct file (" + te + ")." );
			Message.printWarning ( 3, "", te );
		}
    }
    // Graph time series using template.
    else if ( command.equals("GraphTSWithTemplate") ) {
    	// The "Graph with template" button was pressed for the selected time series so there is no intervening dialog.
    	// Go straight to processing the template file.
	    try {
			String userGraphTemplate = this.__resultsTSGraphTemplates_JComboBox.getSelected();
			// Save state for next TSTool session.
			this.session.setUIStateProperty("Results.TimeSeries.GraphTemplate",userGraphTemplate);
			File userGraphTemplateFile = this.session.getGraphTemplateFile(userGraphTemplate);
			// Determine whether a command file should be run to preprocess the time series for the template.
			TSProduct tsp0 = new TSProduct(userGraphTemplateFile.getAbsolutePath(),new PropList(""));
			String preprocessCommandFile = tsp0.getLayeredPropValue("TemplatePreprocessCommandFile", -1, -1);
			List<TS> tslist = new ArrayList<>();
			TS ts = null;
			// Ensemble is the first selected ensemble in the results.
	    	int pos = -1;
	    	if ( JGUIUtil.selectedSize(this.__resultsTS_JList) == 0 ) {
				pos = 0;
			}
			else {
	            pos = JGUIUtil.selectedIndex(this.__resultsTS_JList,0);
			}
			if ( pos >= 0 ) {
				ts = commandProcessor_GetTimeSeries(pos);
				Message.printStatus(2, "", "Time series to process into ensemble: " + ts.getIdentifierString());
			}
			TSCommandFileRunner runner = null;
			if ( (preprocessCommandFile != null) && !preprocessCommandFile.isEmpty() ) {
				// Have a command file specified by TemplatePreprocessCommandFile property in the tsp
				// so run the command file to preprocess the ensemble and associated time series and use output for the graph.
				preprocessCommandFile = IOUtil.verifyPathForOS(
					IOUtil.toAbsolutePath(userGraphTemplateFile.getParent(),preprocessCommandFile) );
				Message.printStatus(2,"","Preprocess command file for ensemble graph template is \"" + preprocessCommandFile + "\"");
				runner = new TSCommandFileRunner(
					this.__tsProcessor.getInitialPropList(),
					this.__tsProcessor.getPluginCommandClasses());
				runner.readCommandFile(preprocessCommandFile, false);
				// Have to seed the processor with the time series from the original processor
				// so it can be found for subsequent processing.
				Message.printStatus(2,"","Running internal processor to preprocess time series for graphing");
				// First get the empty time series list.
				@SuppressWarnings("unchecked")
				List<TS> tslist0 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist0.add(ts);
				PropList runProps = new PropList ( "run");
				runProps.set("AppendResults","true");
				runner.runCommands(runProps);
				// Now get the time series out and use for the graphing.
				@SuppressWarnings("unchecked")
				List<TS> tslist1 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
				tslist = tslist1;
				Message.printStatus(2,"","After running internal processor have " + tslist.size() + " time series.");
			}
			else {
				// No preprocessor specified so process the time series directly.
				tslist.add(ts);
			}
			String tempTSPFile = IOUtil.tempFileName() + "-TSTool-template.tsp";
			GraphTemplateProcessor graphTemplateProcessor = new GraphTemplateProcessor (userGraphTemplateFile);
			// Create a model.
			CommandProcessor processorFromRunner = null;
			if ( runner != null ) {
				processorFromRunner = runner.getProcessor();
			}
			// Pass empty ensemble list.
			List<TSEnsemble> tsensembleList = new ArrayList<>();
			graphTemplateProcessor.expandTemplate (tslist, tsensembleList, commandProcessor_GetCommandProcessor(), processorFromRunner, new File(tempTSPFile));
			Message.printStatus(2, "", "Expanded temporary graph template to \"" + tempTSPFile + "\"");
			TSProcessor p = new TSProcessor();
			PropList overrideProps = new PropList ( "OverrideProps" );
			overrideProps.set ( "InitialView", "Graph" ); // Initial view when display opened.
			overrideProps.set ( "PreviewOutput", "True" ); // Display a view window (not just file output).
			TSProduct tsp = new TSProduct ( tempTSPFile, overrideProps );
			// Now process the product.
			p.addTSSupplier(graphTemplateProcessor);
			p.processProduct ( tsp );
		}
		catch ( Exception te ) {
			Message.printWarning ( 1, "", "Error processing TSProduct file (" + te + ")." );
			Message.printWarning ( 3, "", te );
		}
    }

    // Tables.

    else if (command.equals(TSToolConstants.Results_Table_Properties_String) ) {
        uiAction_ShowTableProperties ();
    }
    else {
    	// Chain to next actions.
    	uiAction_ActionPerformed17_ToolsMenu ( event );
    }
}

/**
Handle a group of actions for the Tools menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed17_ToolsMenu (ActionEvent event)
throws Exception {
	Object o = event.getSource();
	String command = event.getActionCommand();
	String routine = "ToolsMenu";

	if ( o == TSToolMenus.Tools_Analysis_MixedStationAnalysis_JMenuItem ) {
		// Create the dialog using the available time series results (accessed by the processor).
		try {
		    // TODO smalers 2013-08-17 MixedStationAnalysis tool is no longer available - only command is available. Need to remove this.
			// new FillMixedStation_JDialog ( this, commandProcessor_GetCommandProcessor(), this );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error in Mixed Station Analysis tool (" + e + ")." );
			Message.printWarning ( 3, routine, e );
		}
	}
	else if ( o == TSToolMenus.Tools_Datastore_ERDiagram_JMenuItem ) {
		// Create the dialog using the available time series results (accessed by the processor).
		try {
			// TODO smalers 2015-02-14 need to pick the DMI to use - for now hard-code to HydroBase.
			DMI dmi = commandProcessor_GetHydroBaseDMIList().get(0);
			String tablesTableName = null; // Table in database containing the list of tables - need to switch to DataTable or list?
			String tableNameField = null; // Column in tablesTableName that has the name of the tables.
			String erdXField = null; // Column in tablesTableName that contains ER Diagram x-coordinate.
			String erdYField = null; // Column in tablesTableName that contains ER Diagram y-coordinate.
			List<String> referenceTables = null; // List of tables in tablesTableName that are reference tables.
			PageFormat pageFormat = new PageFormat();
			Paper paper = new Paper();
			double w = 72*17.0;
			double h = 72*11.0;
			paper.setSize(w,h);
			pageFormat.setPaper(paper);
			pageFormat.setOrientation(PageFormat.LANDSCAPE);
			boolean debug = true;
		    new ERDiagram_JFrame(dmi, tablesTableName, tableNameField,
		    		erdXField, erdYField, referenceTables,
		    		pageFormat, debug);
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error in Enity Relationship Diagram tool (" + e + ")." );
			Message.printWarning ( 3, routine, e );
		}
	}
	else if ( o == TSToolMenus.Tools_DateTimeTools_JMenuItem ) {
		// Create Date/time conversion tool dialog.
		new DateTimeToolsJDialog(this);
	}
    else if ( o == TSToolMenus.Tools_Analysis_PrincipalComponentAnalysis_JMenuItem ) {
		// Create the dialog using the available time series.
		try {
			new FillPrincipalComponentAnalysis_JDialog ( this, commandProcessor_GetCommandProcessor(), this );
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Error in Principal Component Analysis tool (" + e + ")." );
			Message.printWarning ( 3, routine, e );
		}
	}
	else if (command.equals(TSToolConstants.Tools_Report_DataCoverageByYear_String) ) {
		// Use graph TS because it does not take an output file.
		uiAction_GraphTimeSeriesResults ( "-odata_coverage_report " );
	}
	else if (command.equals(TSToolConstants.Tools_Report_DataLimitsSummary_String) ) {
		// Use graph TS because it does not take an output file.
		uiAction_GraphTimeSeriesResults ( "-odata_limits_report " );
	}
	else if (command.equals(TSToolConstants.Tools_Report_MonthSummaryDailyMeans_String)) {
		// Use graph TS because it does not take an output file.
		uiAction_GraphTimeSeriesResults ( "-omonth_mean_summary_report " );
	}
	else if (command.equals(TSToolConstants.Tools_Report_MonthSummaryDailyTotals_String)){
		// Use graph TS because it does not take an output file.
		uiAction_GraphTimeSeriesResults ( "-omonth_total_summary_report " );
	}
	else if (command.equals(TSToolConstants.Tools_Report_YearToDateTotal_String) ) {
		// Set the averaging end date.
		PropList props = new PropList( "DateBuilder properties" );
		props.set ( "DatePrecision", "Day" );
		props.set ( "DateFormat", "US" );
		props.set ( "EnableYear", "false" );
		props.set ( "DateLabel", "Enter Ending Date for Annual Total:" );
		props.set ( "Title", "Enter Ending Date for Annual Total" );
		DateTime to = new DateTime ( DateTime.DATE_CURRENT | DateTime.PRECISION_DAY );
		try {
            JTextField tmpJTextField = new JTextField();
			new DateTimeBuilderJDialog ( this, tmpJTextField, to, props );
			to = DateTime.parse ( tmpJTextField.getText() );
		}
		catch ( Exception ex ) {
			Message.printWarning ( 1, "TSTool_JFrame", "There was an error processing the date for the report." );
		}
		// Use graph TS because it does not take an output file.
		uiAction_GraphTimeSeriesResults ( "-oyear_to_date_report ",	to.toString(DateTime.FORMAT_MM_SLASH_DD) );
	}
	else if ( o == TSToolMenus.Tools_NWSRFS_ConvertNWSRFSESPTraceEnsemble_JMenuItem ){
		TSTool_NwsrfsEsp.getInstance(this).convertTraceFile();
	}
	else if ( o == TSToolMenus.Tools_NWSRFS_ConvertJulianHour_JMenuItem ) {
		// Display the NWSRFS dialog.
		new NWSRFS_ConvertJulianHour_JDialog(this);
	}
	else if ( o == TSToolMenus.Tools_SelectOnMap_JMenuItem ) {
		try {
            uiAction_SelectOnMap ();
		}
		catch ( Exception e ) {
			JGUIUtil.setWaitCursor ( this, false );
			Message.printWarning ( 1, routine, "Unable to select locations on map." );
			Message.printWarning ( 3, routine, e );
		}
	}
	else if ( o == TSToolMenus.Tools_Options_JMenuItem ) {
		new TSTool_Options_JDialog ( this, this.session, TSToolMain.getConfigFile(), this.__props );
		// Reset as necessary.
		if ( this.__query_TableModel instanceof TSTool_HydroBase_StructureGeolocStructMeasType_TableModel){
			((TSTool_HydroBase_StructureGeolocStructMeasType_TableModel)__query_TableModel).setWDIDLength(
			    StringUtil.atoi( __props.getValue("HydroBase.WDIDLength")));
		}
		else if ( this.__query_TableModel instanceof TSTool_HydroBase_GroundWaterWellsView_TableModel){
            ((TSTool_HydroBase_GroundWaterWellsView_TableModel)this.__query_TableModel).setWDIDLength(
                StringUtil.atoi( __props.getValue("HydroBase.WDIDLength")));
        }
		else if ( this.__query_TableModel instanceof TSTool_HydroBase_WellLevel_Day_TableModel){
			((TSTool_HydroBase_WellLevel_Day_TableModel)
			this.__query_TableModel).setWDIDLength(StringUtil.atoi(__props.getValue("HydroBase.WDIDLength")));
		}
	}
	else if ( o == TSToolMenus.Tools_ViewLogFile_Startup_JMenuItem ) {
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
	else {
		// Chain to remaining actions.
		uiAction_ActionPerformed18_HelpMenu ( event );
	}
}

/**
Handle a group of actions for the Tools menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed18_HelpMenu (ActionEvent event)
throws Exception {
	//Object o = event.getSource();
	String command = event.getActionCommand();

	// Help menu (order of GUI).

	if ( command.equals ( TSToolConstants.Help_AboutTSTool_String )) {
		uiAction_ShowHelpAbout ();
	}
	else if (
		command.equals ( TSToolConstants.Help_ViewDocumentation_String ) ||
	    command.equals(TSToolConstants.Help_ViewDocumentation_ReleaseNotes_String) ||
        command.equals(TSToolConstants.Help_ViewDocumentation_UserManual_String) ||
        command.equals(TSToolConstants.Help_ViewDocumentation_CommandReference_String) ||
        command.equals(TSToolConstants.Help_ViewDocumentation_DatastoreReference_String) ||
        command.equals(TSToolConstants.Help_ViewDocumentation_Troubleshooting_String) ) {
        uiAction_ViewDocumentation ( command );
    }
    else if ( command.equals ( TSToolConstants.Help_View_TrainingMaterials_String )) {
        uiAction_ViewTrainingMaterials ();
    }
	else if ( command.equals ( TSToolConstants.Help_CheckForUpdates_String )) {
        uiAction_CheckForUpdates ();
    }
	else if ( command.equals ( TSToolConstants.Help_ImportConfiguration_String )) {
        uiAction_ImportConfiguration ( IOUtil.getApplicationHomeDir() + File.separator + "system" +
            File.separator + "TSTool.cfg");
    }
	else {
		// Chain
		uiAction_ActionPerformed19_CommandsPluginMenu(event);
	}
}

/**
Handle a group of actions for the Commands...Output... menu.
@param event Event to handle.
*/
private void uiAction_ActionPerformed19_CommandsPluginMenu (ActionEvent event)
throws Exception {
	String commandMenu = event.getActionCommand();
	int pos0 = commandMenu.indexOf("()...");
	if ( pos0 > 0 ) {
		// Have a command CommandName()... menu.
		String commandNameFromMenu = commandMenu.substring(0, pos0);
		for ( @SuppressWarnings("rawtypes") Class c : TSTool_Plugin.getInstance(this).getPluginCommandClassList() ) {
			// For now use the class name to determine the menu.
			String name = c.getSimpleName();
			int pos = name.indexOf("_Command");
			if ( pos > 0 ) {
			   String commandNameFromPlugin = name.substring(0,pos);
			   if ( commandNameFromMenu.equalsIgnoreCase(commandNameFromPlugin) ) {
				   // Plugin command name matches menu that was selected.
				   commandList_EditCommand (commandMenu, null, CommandEditType.INSERT );
			   }
			}
		}
	}
}

/**
 * Check for newer command file.
 * Retrieve the remote copy from #@sourceUrl.
 * Check the @version from local and remote copies.
 * Provide feedback if there is a newer version
 */
private void uiAction_CheckForCommandFileUpdate() {
	// Get the remote file:
	// - time out is 5 seconds
	String tempFolder = System.getProperty("java.io.tmpdir");
	String file1Path = tempFolder + File.separator + "TSTool-commands-source.tstool";
	// Get the annotation values from the local command file.
	List<Command> commands = TSCommandProcessorUtil.getAnnotationCommands(commandProcessor_GetCommandProcessor(),"sourceUrl");
	StringBuilder warning = new StringBuilder();
	String sourceUrl = "";
	String localVersion = "";
	String localVersionDate = "";
	String sourceVersion = "";
	String sourceVersionDate = "";

	// Get the local command file information.
	if ( commands.size() == 0 ) {
		// Don't have any @sourceUrl annotations.
		warning.append ( "The commands have no #@sourceUrl annotation - can't get command file source.\n" );
	}
	else if ( commands.size() > 1 ) {
		// Have more than one @sourceUrl annotations:
		// - therefore ambiguous
		warning.append ( "The commands have multiple #@sourceUrl annotations - can't get command file source.\n" );
	}
	else {
		// Have exactly one @sourceUrl annotations:
		// - therefore unambiguous
		// - set the URL from the command
		sourceUrl = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);
	}
	commands = TSCommandProcessorUtil.getAnnotationCommands(commandProcessor_GetCommandProcessor(),"version");
	if ( commands.size() == 0 ) {
		// OK, checked below - must have version and/or versionDate.
	}
	else if ( commands.size() > 1 ) {
		warning.append ( "The commands have multiple #@version annotations - can't check for updates.\n" );
	}
	else {
		localVersion = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);
	}
	commands = TSCommandProcessorUtil.getAnnotationCommands(commandProcessor_GetCommandProcessor(),"versionDate");
	if ( commands.size() == 0 ) {
		// OK, checked below - must have version and/or versionDate.
	}
	else if ( commands.size() > 1 ) {
		warning.append ( "The commands have multiple #@versionDate annotations - can't check for updates.\n" );
	}
	else {
		localVersionDate = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);
	}

	if ( localVersion.isEmpty() && localVersionDate.isEmpty() ) {
		warning.append ( "The commands have no #@version or #@versionDate annotation - can't check for updates.\n" );
	}

	// Retrieve the source file and get the properties.
	if ( !sourceUrl.isEmpty() ) {
		if ( IOUtil.getUriContent(sourceUrl, file1Path, null, 5000, 5000) != 200 ) {
			Message.printWarning(1, "", "Error retrieving command file source from: " + sourceUrl + "\n");
		}
		else {
			// Get the version properties out of the source command file:
			// - use a second command processor
			TSCommandProcessor sourceProcessor = new TSCommandProcessor(null);
			try {
				sourceProcessor.readCommandFile ( file1Path, true, false, false );
				commands = TSCommandProcessorUtil.getAnnotationCommands(sourceProcessor,"version");
				if ( commands.size() == 0 ) {
					// OK, checked below - must have version and/or versionDate.
				}
				else if ( commands.size() > 1 ) {
					warning.append ( "The source commands have multiple #@version annotations - can't check for updates.\n" );
				}
				else {
					sourceVersion = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);
				}
				commands = TSCommandProcessorUtil.getAnnotationCommands(sourceProcessor,"versionDate");
				if ( commands.size() == 0 ) {
					// OK, checked below - must have version and/or versionDate.
				}
				else if ( commands.size() > 1 ) {
					warning.append ( "The source commands have multiple #@versionDate annotations - can't check for updates.\n" );
				}
				else {
					sourceVersionDate = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);
				}
			}
			catch ( Exception e ) {
				warning.append ( "Error reading source command file: " + file1Path + "\n");
			}
		}
	}

	// If there are any warnings with input, display and return.
	if ( warning.length() > 0 ) {
		Message.printWarning(1, "", warning.toString() );
		return;
	}

	// Do the version comparison and create a note for output:
	// - if 'version' is available for both use it
	// - else if 'versionDate' is available for both use it
	// - if both 'version' and 'versionDate' are available?

	StringBuilder note = new StringBuilder();
	boolean checkDate = false;
	if ( !localVersion.isEmpty() && !sourceVersion.isEmpty() ) {
		// Compare the versions:
		// - both must be either semantic versions or dates
		// - dates are redundant with @versionDate but may be used if semantic versions are not used
		int localPeriodCount = StringUtil.patternCount(localVersion,".");
		int sourcePeriodCount = StringUtil.patternCount(sourceVersion,".");
		int localDashCount = StringUtil.patternCount(localVersion,"-");
		int sourceDashCount = StringUtil.patternCount(sourceVersion,"-");
		if ( (localPeriodCount > 0) && (sourcePeriodCount > 0) ) {
			// Assume semantic versioning.
			if ( StringUtil.compareSemanticVersions(localVersion, "<", sourceVersion, 3) ) {
				note.append("The source commands (" + sourceVersion + ") has a newer @version than local commands (" + localVersion +
					") - need to update the local copy from the original source.\n");
			}
			else if ( StringUtil.compareSemanticVersions(localVersion, ">", sourceVersion, 3) ) {
				note.append("The source commands (" + sourceVersion + ") has an older @versionDate than local commands (" + localVersion +
					") - need to update the original source copy from the local copy.\n");
			}
			else {
				note.append("The source commands (" + sourceVersion + ") and local commands (" + localVersion +
					") have the same @version (to 3 parts).\n");
				// Also check the date as the tie-breaker.
				checkDate = true;
			}
		}
		else if ( (localDashCount > 0) && (sourceDashCount > 0) ) {
			// Compare the versions.
			DateTime localDate = null;
			DateTime sourceDate = null;
			try {
				localDate = DateTime.parse(localVersionDate);
			}
			catch ( Exception e ) {
				warning.append("The local commands @version seems to be a date/time but is invalid.\n");
			}
			try {
				sourceDate = DateTime.parse(sourceVersionDate);
			}
			catch ( Exception e ) {
				warning.append("The source commands @version seems to be a date/time but is invalid.\n");
			}
			if ( (localDate != null) && (sourceDate != null) ) {
				if ( sourceDate.greaterThan(localDate) ) {
					// The source is newer than local.
					note.append("The source commands (" + sourceVersion + ") has a newer @version than local commands (" + localVersion +
						") - need to update the local copy from the original source.");
				}
				else if ( sourceDate.lessThan(localDate) ) {
					// The source is newer than local.
					note.append("The source commands (" + sourceVersion + ") has an older @version than local commands (" + localVersion +
						") - need to update the original source copy from the local copy.");
				}
				else {
					note.append("The source commands (" + sourceVersion + ") and local commands (" + localVersion +
						") have the same @versionDate.");
				}
			}
		}
		else {
			warning.append("The source and local @version don't appear to be consistent semantic versions or dates - can't check the version.\n");
		}
	}
	else if ( !localVersionDate.isEmpty() && !sourceVersionDate.isEmpty() ) {
		checkDate = true;
	}
	if ( checkDate ) {
		// Compare the versions.
		DateTime localDate = null;
		DateTime sourceDate = null;
		try {
			localDate = DateTime.parse(localVersionDate);
		}
		catch ( Exception e ) {
			warning.append("The local commands @versionDate date/time is invalid.\n");
		}
		try {
			sourceDate = DateTime.parse(sourceVersionDate);
		}
		catch ( Exception e ) {
			warning.append("The source commands @versionDate date/time is invalid.\n");
		}
		if ( (localDate != null) && (sourceDate != null) ) {
			if ( sourceDate.greaterThan(localDate) ) {
				// The source is newer than local.
				note.append("The source commands (" + sourceVersionDate + ") has a newer @versionDate than local commands (" + localVersionDate +
					") - need to update the local copy from the original source.");
			}
			else if ( sourceDate.lessThan(localDate) ) {
				// The source is newer than local.
				note.append("The source commands (" + sourceVersionDate + ") has an older @versionDate than local commands (" + localVersionDate +
					") - need to update the original source copy from the local copy.");
			}
			else {
				note.append("The source commands (" + sourceVersionDate + ") and local commands (" + localVersionDate +
					") have the same @versionDate.");
			}
		}
	}

    new ResponseJDialog ( this, IOUtil.getProgramName(),
    "\nThe update check relies on the following comment annotations.\n\n" +
    "Local commands:  \n" +
    "  @sourceUrl: " + sourceUrl + "\n" +
    "  @version: " + localVersion + "\n" +
    "  @versionDate: " + localVersionDate + "\n" +
    "\nSource commands (using the URL from the above @sourceUrl):  \n" +
    "  @version: " + sourceVersion + "\n" +
    "  @versionDate: " + sourceVersionDate + "\n\n" + note,
    ResponseJDialog.OK).response();
    // TODO smalers 2022-11-17 could prompt to see if download/update is requested.
}

/**
 * Check for TSTool software update.
 */
private void uiAction_CheckForUpdates ( ) {
	// Read the available TSTool versions from the OpenCDSS website.
	String latestVersion = "unable to determine";
	String message = "A newer development version may be available on the OpenCDSS website.\n\n";
	try {
	    String currentVersionNum = IOUtil.getProgramVersion().split(" ")[0].trim();
        String versionUri = "https://opencdss.state.co.us/tstool/index.csv";
        String versionFile = IOUtil.tempFileName();
		int code = IOUtil.getUriContent(versionUri, versionFile, null, -1, -1);
		if ( code == 200 ) {
			// Success - determine the version from the file:
			// - read into a DataTable since a csv with headers
	        PropList props = new PropList ("");
	        props.set ( "Delimiter=," ); // See existing prototype.
	        props.set ( "CommentLineIndicator=#" );	// New - skip lines that start with this.
	        props.set ( "TrimStrings=True" ); // If true, trim strings after reading.
	        DataTable table = DataTable.parseFile ( versionFile, props );
			// Versions are in column named 'Version' with first row being the newest:
			// - but don't check dev version because most users won't care
			int col = table.getFieldIndex("Version");
			TableRecord rec;
			String version;
			for ( int irec = 0; irec < table.getNumberOfRecords(); irec++ ) {
				rec = table.getRecord(irec);
				version = rec.getFieldValueString(col);
				if ( version.toUpperCase().indexOf("DEV") < 0 ) {
					// Not a development version.
					latestVersion = version;
					break;
				}
			}
			// Determine if latest version is newer than current:
			// - should be able to just do a string comparison
			if ( latestVersion.compareTo(currentVersionNum) > 0 ) {
			    message = "A newer version is available on the OpenCDSS website.\n\n";
			}
		}
	}
	catch ( Exception e ) {
		message = "A newer release or development version may be available on the OpenCDSS website.\n\n";
	}
	// Display the information and allow user to open the download website.
    int x = new ResponseJDialog ( this, IOUtil.getProgramName(),
    "\nTSTool version:  " + IOUtil.getProgramVersion() + "\n" +
    "Latest available release version:  " + latestVersion + "\n\n" +
    message +
    "Open the OpenCDSS TSTool download web page?",
    ResponseJDialog.YES|ResponseJDialog.NO).response();
    if ( x == ResponseJDialog.NO ) {
        return;
    }
    else {
    	// Open the OpenCDSS web page.
        String docUri = "http://opencdss.state.co.us/tstool/";
        try {
            Desktop desktop = Desktop.getDesktop();
            desktop.browse ( new URI(docUri) );
        }
        catch ( Exception e ) {
            Message.printWarning(2, "", "Unable to display documentation at \"" + docUri + "\" (" + e + ")." );
        }
    }
}

/**
Convert selected commands to/from comments.  When converting to commands:
Each Command instance is retrieved, its command string is taken from the Command,
and a new GenericCommand is create, and the original Command is replaced in the list.
When converting from commands, the GenericCommand is retrieved, a new Command instance is created,
the original Command is replaced.
@param to_comment If true, convert commands to comments, if false, from comments.
*/
private void uiAction_ConvertCommandsToComments ( boolean to_comment ) {
	int selected_indexes[] = ui_GetCommandJList().getSelectedIndices();
	int selected_size = JGUIUtil.selectedSize ( ui_GetCommandJList() );
	String old_command_string = null;
	Command old_command = null;
	Command new_command = null;
	// It is OK to loop through each item below.
	// Even though the items in the data model will change, if a command is replaced each time,
	// the indices will still be relevant.
	for ( int i = 0; i < selected_size; i++ ) {
		old_command = (Command)this.__commands_JListModel.get(selected_indexes[i]);
		old_command_string = (String)old_command.toString();
		if ( to_comment ) {
			// Replace the current command with a new string that has the comment character.
			new_command = commandList_NewCommand(
				"# " + old_command_string,	// New command as comment.
				true );	// Create the command even if not recognized.
			// Check the status so that it will have a valid status and not "unknown", which triggers
			// a decorator to be displayed (no reason to show decorator for comment).
	        try {
	            new_command.checkCommandParameters(null, "", 3);
	        }
	        catch ( Exception e ) {
	            // Should not happen.
	        }
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
	this.__commandsCutBuffer.clear();

	// Transfer Command instances to the cut buffer.
	Command command = null;	// Command instance to process.
	for ( int i = 0; i < size; i++ ) {
		command = (Command)this.__commands_JListModel.get(selected_indices[i]);
		this.__commandsCutBuffer.add ( (Command)command.clone() );
	}

	if ( remove_original ) {
		// If removing, delete the selected commands from the list.
		commandList_RemoveCommandsBasedOnUI();
	}
}

/**
The datastore choice has been clicked so process the event.
The only entry point to this method is if the user actually clicks on the choice.
In this case, the input type/name choices will be set to blank because the user has
made a decision to work with a datastore.
If they subsequently choose to work with an input type,
then they would select an input and the datastore choice would be blanked.
*/
private void uiAction_DataStoreChoiceClicked() {
    String routine = getClass().getSimpleName() + ".uiAction_DataStoreChoiceClicked";
    if ( this.__dataStore_JComboBox == null ) {
        if ( Message.isDebugOn ) {
            Message.printDebug ( 1, routine, "Datastore has been selected but GUI is not yet initialized - no action taken in response to datastore selection.");
        }
        return; // Not done initializing.
    }
    // Do the following to make sure the initial label is cleared.
    ui_ClearDataStoreInitializing();
    String selectedDataStoreName = this.__dataStore_JComboBox.getSelected();
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
            TSTool_HydroBaseRest.getInstance(this).selectDataStore ( (ColoradoHydroBaseRestDataStore)selectedDataStore, this.__props );
        }
        else if ( selectedDataStore instanceof GenericDatabaseDataStore ) {
            TSTool_Generic.getInstance(this).selectDataStore ( (GenericDatabaseDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof HydroBaseDataStore ) {
            TSTool_HydroBase.getInstance(this).selectDataStore ( (HydroBaseDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof RccAcisDataStore ) {
            TSTool_RccAcis.getInstance(this).selectDataStore ( (RccAcisDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ReclamationHDBDataStore ) {
            TSTool_HDB.getInstance(this).selectDataStore ( (ReclamationHDBDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof ReclamationPiscesDataStore ) {
            TSTool_Pisces.getInstance(this).selectDataStore ( (ReclamationPiscesDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisDailyDataStore ) {
            TSTool_UsgsNwis.getInstance(this).dataStoreSelected_Daily ( (UsgsNwisDailyDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisGroundwaterDataStore ) {
            TSTool_UsgsNwis.getInstance(this).dataStoreSelected_Groundwater ( (UsgsNwisGroundwaterDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof UsgsNwisInstantaneousDataStore ) {
            TSTool_UsgsNwis.getInstance(this).dataStoreSelected_Instantaneous ( (UsgsNwisInstantaneousDataStore)selectedDataStore );
        }
        else if ( selectedDataStore instanceof PluginDataStore ) {
        	// Handle plugin.
        	TSTool_Plugin.getInstance(this).selectDataStore ( selectedDataStore );
         }
        // The above does not select the input filter so do that next.
        ui_SetInputFilterForSelections();
    }
    catch ( Exception e ) {
        Message.printWarning( 2, routine, "Error selecting datastore \"" + selectedDataStore.getName() + "\"" );
        Message.printWarning ( 3, routine, e );
    }
}

/**
This function fills in appropriate selections for the time step and choices.
This will result in a call to timestepChoiceClicked(), which will display input filters if appropriate.
*/
private void uiAction_DataTypeChoiceClicked() {
	String rtn = getClass().getSimpleName() + ".uiAction_DataTypeChoiceClicked";
	if ( (this.__inputType_JComboBox == null) || (this.__dataType_JComboBox == null) ) {
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, rtn, "Data type has been selected but GUI is not initialized." );
		}
		return;	// Not done initializing.
	}
	String selectedInputType = ui_GetSelectedInputType();
	String selectedDataType = ui_GetSelectedDataType ();
	DataStore selectedDataStore = ui_GetSelectedDataStore();
	if ( selectedDataType == null ) {
		// Apparently this happens when setData() or similar is called on the JComboBox, and before select() is called.
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, rtn, "Data type has been selected:  null (select is ignored)" );
		}
		return;
	}

	if ( Message.isDebugOn ) {
		Message.printDebug ( 1, rtn, "Data type has been selected for read:  \"" + selectedDataType + "\"" );
	}

	// Set the appropriate settings for the current data input type and data type.

    if ( (selectedDataStore != null) && (selectedDataStore instanceof ColoradoHydroBaseRestDataStore) ) {
    	TSTool_HydroBaseRest.getInstance(this).dataTypeSelected ( selectedDataStore, selectedDataType );
    }
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_DateValue) ) {
		// DateValue file.
    	TSTool_DateValue.getInstance(this).dataTypeSelected();
	}
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_HECDSS) ) {
        // HEC-DSS database file - the time step is set when the input name is selected so do nothing here.
    }
	else if ( ((selectedDataStore != null) && (selectedDataStore instanceof HydroBaseDataStore)) ||
	    selectedInputType.equals(TSToolConstants.INPUT_TYPE_HydroBase) ) {
    	TSTool_HydroBase.getInstance(this).dataTypeSelected ( selectedDataStore, selectedDataType );
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_MODSIM) ) {
		// MODSIM file.
		TSTool_Modsim.getInstance(this).dataTypeSelected();
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_NWSCARD) ) {
		// NWSCard file.
		TSTool_NwsrfsCard.getInstance(this).dataTypeSelected();
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files) ) {
    	TSTool_FS5Files.getInstance(this).dataTypeSelected ( selectedDataType );
	}
	else if ( selectedInputType.equals( TSToolConstants.INPUT_TYPE_NWSRFS_ESPTraceEnsemble) ){
		// ESP Trace Ensemble file.
    	TSTool_NwsrfsEsp.getInstance(this).dataTypeSelected ();
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof RccAcisDataStore)) {
        // Set intervals for the data type and trigger a select to populate the input filters.
    	TSTool_RccAcis.getInstance(this).dataTypeSelected ();
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof ReclamationHDBDataStore)) {
        // Time steps are determined from the database based on the data type that is selected.
        // FIXME smalers 2010-10-19 Need to enable.
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof ReclamationPiscesDataStore)) {
        // Set intervals for the data type and trigger a select to populate the input filters.
    	TSTool_Pisces.getInstance(this).dataTypeSelected ( (ReclamationPiscesDataStore)selectedDataStore, selectedDataType );
    }
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_RiverWare) ) {
		// RiverWare file.
		TSTool_RiverWare.getInstance(this).dataTypeSelected ();
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateCU) ) {
		// StateCU files.
		TSTool_StateCU.getInstance(this).dataTypeSelected ();
	}
    else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateCUB) ) {
        // StateCU binary output file - the time step is set when the input name is selected so do nothing here.
    }
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateMod) ) {
		TSTool_StateMod.getInstance(this).dataTypeSelected ();
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_StateModB) ) {
		// StateMod binary output file - the time step is set when the input name is selected so do nothing here.
	}
	else if ( selectedInputType.equals(TSToolConstants.INPUT_TYPE_UsgsNwisRdb) ) {
		// USGS NWIS file.
    	TSTool_UsgsNwis.getInstance(this).dataTypeSelected_Rdb();
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisDailyDataStore)) {
    	TSTool_UsgsNwis.getInstance(this).dataTypeSelected_Daily( (UsgsNwisDailyDataStore)selectedDataStore, selectedDataType);
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisGroundwaterDataStore)) {
    	TSTool_UsgsNwis.getInstance(this).dataTypeSelected_Groundwater( (UsgsNwisGroundwaterDataStore)selectedDataStore, selectedDataType);
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof UsgsNwisInstantaneousDataStore)) {
    	TSTool_UsgsNwis.getInstance(this).dataTypeSelected_Instantaneous( (UsgsNwisInstantaneousDataStore)selectedDataStore, selectedDataType);
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof PluginDataStore) ) {
    	// Plugin datastore - call its method to get the intervals.
    	TSTool_Plugin.getInstance(this).dataTypeSelected( (PluginDataStore)selectedDataStore, selectedDataType );
    }

	// Set the filter where clauses based on the data type changing
    // (this only triggers a reset of the input filter for some input types/datastores,
    // like HydroBase, which has different input filters for different data types).

	ui_SetInputFilterForSelections();
}

/**
Deselect all commands in the commands list.  This occurs in response to a user selecting a menu choice.
*/
private void uiAction_DeselectAllCommands() {
	ui_GetCommandJList().clearSelection();
	// TODO smalers 2007-08-31 Should add list selection listener to handle updateStatus call.
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
	int selectedSize = 0;
	int [] selected = ui_GetCommandJList().getSelectedIndices();
	if ( selected != null ) {
		selectedSize = selected.length;
	}
	if ( selectedSize > 0 ) {
		Command command = (Command)this.__commands_JListModel.get(selected[0]);
		List<Command> commandsToEdit = null;
		if ( command instanceof Comment_Command ) {
			// Allow multiple lines to be edited in a comment.
			// This is handled in the called method, which brings up a multi-line editor for comments.
            // Only edit the contiguous # block. The first one is a # but stop adding when lines no longer start with #.
			commandsToEdit = new ArrayList<> ( selectedSize );
			for ( int i = 0; i < selectedSize; i++ ) {
				command = (Command)this.__commands_JListModel.get(selected[i]);
				if ( !(command instanceof Comment_Command) ) {
					break;
				}
				// Else add command to the list.
				commandsToEdit.add ( command );
			}
		}
		else {
            // Commands are one line.
			commandsToEdit = new ArrayList<> ( 1 );
			commandsToEdit.add ( command );
		}
		// Edit using the command dialog.
		commandList_EditCommand ( "", commandsToEdit, CommandEditType.UPDATE ); // No action event from menus
	}
}

/**
Carry out the edit command action, but use a text editor rather than command dialog, triggered by:
<ol>
<li>	Popup menu edit "as text" of a command on the command list.</li>
</ol>
This method will call the uiAction_EditCommand() method with a list of commands that were selected to be edited.
Multiple commands may be edited if a block of # delimited comments.
If all the lines start with #, then call the normal editor for comments.
*/
private void uiAction_EditCommandAsText () {
	// THIS CODE IS THE SAME AS uiAction_EditCommand() except that text editor is requested.
	int selectedSize = 0;
	int [] selected = ui_GetCommandJList().getSelectedIndices();
	if ( selected != null ) {
		selectedSize = selected.length;
	}
	if ( selectedSize > 0 ) {
		Command command = (Command)this.__commands_JListModel.get(selected[0]);
		List<Command> commandsToEdit = null;
		if ( command instanceof Comment_Command ) {
			// Allow multiple lines to be edited in a comment.
			// This is handled in the called method, which brings up a multi-line editor for comments.
	        // Only edit the contiguous # block. The first one is a # but stop adding when lines no longer start with #.
			commandsToEdit = new ArrayList<> ( selectedSize );
			for ( int i = 0; i < selectedSize; i++ ) {
				command = (Command)this.__commands_JListModel.get(selected[i]);
				if ( !(command instanceof Comment_Command) ) {
					break;
				}
				// Else add command to the list.
				commandsToEdit.add ( command );
			}
		}
		else {
	        // Commands are one line.
			commandsToEdit = new ArrayList<> ( 1 );
			commandsToEdit.add ( command );
		}
		boolean editAsText = true;
		commandList_EditCommand ( "", commandsToEdit, CommandEditType.UPDATE, editAsText ); // No action event from menus.
	}
}

/**
Export time series to a file.
Assume that if this is called, the state of the GUI is such that time series are available from the TSEngine.
@param format Format to export, as a tstool command line option.
@param filename Name of file to save as, as a tstool command line option (e.g., "-o filename").
If previewing output, this will be "-preview".
*/
private void uiAction_ExportTimeSeriesResults ( String format, String filename ) {
	String routine = getClass().getSimpleName() + ".uiAction_ExportTimeSeriesResults";
	if ( Message.isDebugOn ) {
		Message.printDebug ( 1, routine, "In export" );
	}

	// Get the time series list.

	PropList props = new PropList ( "SaveAsProps" );
	props.set ( "OutputFormat=" + format );
	props.set ( "OutputFile=" + filename );
	props.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
	// Final list is selected.
	if ( this.__tsProcessor != null ) {
		try {
            int selected_ts = JGUIUtil.selectedSize(this.__resultsTS_JList);
			if ( selected_ts == 0 ) {
				commandProcessor_ProcessTimeSeriesResultsList(null,props);
			}
			else {
                commandProcessor_ProcessTimeSeriesResultsList ( this.__resultsTS_JList.getSelectedIndices(), props );
			}
		}
		catch ( Exception e ) {
			Message.printWarning ( 1, routine, "Unable to save time series (" + e + ")." );
		}
	}
}

/**
Handle "File...Exit" and Window X actions.
*/
private void uiAction_FileExitClicked () {
	// If the commands are dirty, see if they want to save them.
	// This code is also in openCommandFile - might be able to remove copy once all actions are implemented.
	int x = ResponseJDialog.YES;	// Default for batch mode.
	boolean commandsAreTemplate = false;
	if ( !TSToolMain.isRestServer() && !IOUtil.isBatch() ) {
		if ( this.__commandsDirty ) {
			if ( this.__commandFileName == null ) {
				// Have not been saved before.
				x = ResponseJDialog.NO;
				if ( this.__commands_JListModel.size() > 0 ) {
					// Have at least one command.
	                if ( this.__tsProcessor.getReadOnly() ) {
	                    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
	                            "The command file is marked read-only (#@readOnly comment).\n" +
	                            "Press Cancel and then save to a new name if desired." +
	                            "Press YES to update the read-only file.",
	                            ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
	                }
	                else if ( commandsAreTemplate = this.__tsProcessor.areCommandsTemplate() ) {
	                    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
	                            "The commands are marked as a template (#@template comment).\n" +
	                            "TSTool does not currently support editing template command files.  You must use a text editor.\n" +
	                            "Functionality is being evaluated and may be enabled in the future to allow editing template command files.\n" +
	                            "Press OK to continue with exit without saving or Cancel to return to TSTool.",
	                            ResponseJDialog.OK|ResponseJDialog.CANCEL).response();
	                }
	                else {
	                     x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                             "Do you want to save the changes you made?\n\n" +
                             "To view differences, Cancel and use View / Command File Diff.",
                             ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
	                }
	            }
				if ( x == ResponseJDialog.CANCEL ) {
					// Want to return to editing.
					setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
					return;
				}
				else if ( (this.__commands_JListModel.size() > 0) && !commandsAreTemplate && (x == ResponseJDialog.YES) ) {
					// DO NOT let empty command file save because it is probably an accident where all old commands were cleared.
					// Prompt for the name and then save.
					uiAction_WriteCommandFile ( this.__commandFileName, true, false );
				}
				// No will continue without saving.
			}
			else {
                // A command file exists...  Warn the user.
				// They can save to the existing file name or can cancel and File...Save As... to a different name.
				// Have not been saved before.
				x = ResponseJDialog.NO;
				if ( this.__commands_JListModel.size() > 0 ) {
				    if ( this.__tsProcessor.getReadOnly() ) {
                        x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                                "The command file is marked read-only (#@readOnly comment).  Changes cannot be saved.\n" +
                                "Press Cancel and then save to a new name if desired.",
                                ResponseJDialog.OK|ResponseJDialog.CANCEL).response();
                    }
				    else if ( commandsAreTemplate = this.__tsProcessor.areCommandsTemplate() ) {
                        x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                        		"The commands are marked as a template (#@template comment).\n" +
	                            "TSTool does not currently support editing template command files.  You must use a text editor.\n" +
	                            "Functionality is being evaluated and may be enabled in the future to allow editing template command files.\n" +
	                            "Press Ok to exit without saving or Cancel to return to TSTool.",
                                ResponseJDialog.OK|ResponseJDialog.CANCEL).response();
                    }
                    else {
                        x = new ResponseJDialog ( this,
                                IOUtil.getProgramName(), "Do you want to save the changes made to the command file?\n"
                                + "    " + this.__commandFileName + "\n\n" +
                                "To view differences, Cancel and use View / Command File Diff.",
                                ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
                    }
				}
				if ( x == ResponseJDialog.CANCEL ) {
					setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
					return;
				}
				else if ( (this.__commands_JListModel.size() > 0) && !commandsAreTemplate && (x == ResponseJDialog.YES) ) {
					// DO NOT let empty commands get saved because it is likely an accident.
					uiAction_WriteCommandFile ( this.__commandFileName, false, false );
				}
				// Else if No will just exit below.
			}
		}
		// Now make sure the user wants to exit - they might have a lot of data processed.
		StringBuilder b = new StringBuilder("Are you sure you want to exit TSTool?");
		if ( (this.__commands_JListModel.size() == 0) && (this.__commandFileName != null) ) {
			// Only need to warn if an empty file with a name is being used.
			b.append("\nCurrent commands are empty.\nTSTool WILL NOT save an empty file.\nThe previous file contents will remain." );
		}
		x = new ResponseJDialog (this, "Exit TSTool", b.toString(), ResponseJDialog.YES| ResponseJDialog.NO).response();
	}
	if ( x == ResponseJDialog.YES ) {
		setDefaultCloseOperation(DISPOSE_ON_CLOSE);
		setVisible(false);
		try {
            dispose();
		}
		catch ( Exception e ) {
			// Why is this a problem?
		}
		// Close the currently opened log file.
		Message.closeLogFile();
		// Write the UI state so settings are remembered for the next session.
		this.session.writeUIState();
		// Exit with status 0 indicating normal exit
		System.exit(0);
		// Close global data connections - need to figure out where to put this to work for batch mode also.
		this.__tsProcessor.closeDataConnections(true);
	}
	else {
        // Cancel.
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
	}
}

/**
Find output file(s) in the results.
*/
private void uiAction_FindOutputFiles () {
   	new FindInJListJDialog ( this, false, __resultsOutputFiles_JList, "Find Output Files (selecting a file will open it)" );
}

/**
Find table(s) in the results.
*/
private void uiAction_FindTables () {
   	new FindInJListJDialog ( this, false, __resultsTables_JList, "Find Tables (selecting a table will open it)" );
}

/**
Respond to "Get Time Series List" being clicked.
*/
private void uiAction_GetTimeSeriesListClicked() {
	String message, routine = getClass().getSimpleName() + ".getTimeSeriesListClicked";
    String selectedInputType = ui_GetSelectedInputType();
    DataStore selectedDataStore = ui_GetSelectedDataStore();
    // Call the following to help clear out an initial message.
    ui_ClearDataStoreInitializing();
    if ( selectedDataStore != null ) {
        Message.printStatus ( 1, routine, "Getting time series list from " + selectedDataStore.getName() + " datastore..." );
    }
    else {
        Message.printStatus ( 1, routine, "Getting time series list from " + selectedInputType + " input type..." );
    }

	// Verify that the input filters have valid data:
    // - the following works for plugins also because the parent InputFilter_JPanel class implements the method
    //   so the method is always defined
	if ( this.__selectedInputFilter_JPanel != this.__inputFilterGeneric_JPanel ) {
		// Call the available check method:
		// - if the newer method is available that takes the selected data type and interval, call it
		// - otherwise, call the older method that does not have data type and interval
		String warning = null;
		Method newMethod = null;
		try {
			newMethod = this.__selectedInputFilter_JPanel.getClass().getMethod("checkInputFilters",
				new Class[] {
					String.class, // Data type.
					String.class, // Data interval.
					boolean.class } );  // Whether to display warnings.
		}
		catch ( NoSuchMethodException e ) {
			newMethod = null;
		}
		if ( newMethod != null ) {
			// Call the method with the new signature
			// (not built into the InputFilter_JPanel so should only be found in derived class).
			try {
				warning = (String)newMethod.invoke(this.__selectedInputFilter_JPanel, ui_GetSelectedDataType(), ui_GetSelectedTimeStep(), false);
			}
			catch ( IllegalAccessException e ) {
				// Call the built-in check method.
				Message.printWarning(2, routine, "Error calling check on input filters.");
				Message.printWarning(2, routine, e);
				warning = this.__selectedInputFilter_JPanel.checkInputFilters(false);
			}
			catch ( InvocationTargetException e ) {
				Message.printWarning(2, routine, "Error calling check on input filters.");
				Message.printWarning(2, routine, e);
				// Call the built-in check method.
				warning = this.__selectedInputFilter_JPanel.checkInputFilters(false);
			}
		}
		else {
			// Call the method with the old signature (the method is built into InputFilter_JPanel).
			warning = this.__selectedInputFilter_JPanel.checkInputFilters(false);
		}
		if ( (warning != null) && !warning.isEmpty() ) {
			// An input error was detected so don't get the time series.
			Message.printWarning(1, routine, warning);
			return;
		}
	}

	// Read the time series list and display in the Time Series List area.
	// Return if an error occurs because the message at the bottom should only be printed if successful.
	// To avoid unnecessary class loads, check whether a datastore or input type is enabled.
	// TODO smalers 2016-02-22 in the future this code will be split into separate classes

    if ( (selectedDataStore != null) && this.__source_ColoradoHydroBaseRest_enabled && (selectedDataStore instanceof ColoradoHydroBaseRestDataStore) ) {
        try {
            TSTool_HydroBaseRest.getInstance(this).getTimeSeriesListClicked_ReadColoradoHydroBaseRestCatalog ( this.__selectedInputFilter_JPanel );
        }
        catch ( Exception e ) {
            message = "Error reading ColoradoHydroBaseRest web service - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_DateValue)) {
		try {
            TSTool_DateValue.getInstance(this).getTimeSeriesListClicked_ReadDateValueCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading DateValue file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof GenericDatabaseDataStore) ) {
        try {
            TSTool_Generic.getInstance(this).getTimeSeriesListClicked_ReadGenericDatabaseDataStoreCatalog (
            	this.__selectedInputFilter_JPanel, selectedDataStore );
        }
        catch ( Exception e ) {
            message = "Error reading GenericDatabaseDataStore - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
    else if ( this.__source_HECDSS_enabled && selectedInputType.equals (TSToolConstants.INPUT_TYPE_HECDSS)) {
        try {
            TSTool_HecDss.getInstance(this).getTimeSeriesListClicked_ReadHecDssCatalog ();
        }
        catch ( Exception e ) {
            message = "Error reading HEC-DSS file - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( this.__source_HydroBase_enabled && selectedInputType.equals (TSToolConstants.INPUT_TYPE_HydroBase)) {
		try {
		    GRLimits limits = null;
            TSTool_HydroBase.getInstance(this).getTimeSeriesListClicked_ReadHydroBaseCatalog ( limits,
            		this.__selectedInputFilter_JPanel, this.__props);
		}
		catch ( Exception e ) {
			message = "Error reading HydroBase - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
    else if ( (selectedDataStore != null) && this.__source_HydroBase_enabled && (selectedDataStore instanceof HydroBaseDataStore) ) {
        try {
            GRLimits limits = null;
            TSTool_HydroBase.getInstance(this).getTimeSeriesListClicked_ReadHydroBaseCatalog( limits,
            		this.__selectedInputFilter_JPanel, this.__props );
        }
        catch ( Exception e ) {
            message = "Error reading time series from HydroBase \"" + selectedDataStore.getName() +
                "\" - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( this.__source_MODSIM_enabled && selectedInputType.equals (TSToolConstants.INPUT_TYPE_MODSIM)) {
		try {
            TSTool_Modsim.getInstance(this).getTimeSeriesListClicked_ReadModsimCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading MODSIM file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( this.__source_NWSCard_enabled && selectedInputType.equals (TSToolConstants.INPUT_TYPE_NWSCARD)) {
		try {
            TSTool_NwsrfsCard.getInstance(this).getTimeSeriesListClicked_ReadNwsCardCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading NWS CARD file - cannot display time series list )" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled && selectedInputType.equals( TSToolConstants.INPUT_TYPE_NWSRFS_ESPTraceEnsemble)) {
		try {
            TSTool_NwsrfsEsp.getInstance(this).getTimeSeriesListClicked_ReadNwsrfsEspTraceEnsembleCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading NWSRFS_ESPTraceEnsemble file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( this.__source_NWSRFS_FS5Files_enabled && selectedInputType.equals (TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files)) {
		try {
            // This reads the time series headers and displays the results in the list.
			TSTool_FS5Files.getInstance(this).getTimeSeriesListClicked_ReadNwsrfsFS5FilesCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading NWSRFS FS5Files time series list - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
    else if ( (selectedDataStore != null) && this.__source_RCCACIS_enabled && (selectedDataStore instanceof RccAcisDataStore) ) {
        try {
            TSTool_RccAcis.getInstance(this).getTimeSeriesListClicked_ReadRccAcisCatalog(this.__selectedInputFilter_JPanel);
        }
        catch ( Exception e ) {
            message = "Error reading RCC ACIS - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( (selectedDataStore != null) && this.__source_ReclamationHDB_enabled && (selectedDataStore instanceof ReclamationHDBDataStore) ) {
        try {
            TSTool_HDB.getInstance(this).getTimeSeriesListClicked_ReadReclamationHDBCatalog();
        }
        catch ( Exception e ) {
            message = "Error reading ReclamationHDB - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( (selectedDataStore != null) && this.__source_ReclamationPisces_enabled && (selectedDataStore instanceof ReclamationPiscesDataStore) ) {
        try {
            TSTool_Pisces.getInstance(this).getTimeSeriesListClicked_ReadReclamationPiscesCatalog();
        }
        catch ( Exception e ) {
            message = "Error reading ReclamationPisces - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
    else if ( (selectedDataStore != null) && this.__source_UsgsNwisDaily_enabled && (selectedDataStore instanceof UsgsNwisDailyDataStore) ) {
        try {
            TSTool_UsgsNwis.getInstance(this).getTimeSeriesListClicked_ReadUsgsNwisDailyCatalog();
        }
        catch ( Exception e ) {
            message = "Error reading USGS NWIS daily values - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
    else if ( (selectedDataStore != null) && this.__source_UsgsNwisGroundwater_enabled && (selectedDataStore instanceof UsgsNwisGroundwaterDataStore) ) {
        try {
            TSTool_UsgsNwis.getInstance(this).getTimeSeriesListClicked_ReadUsgsNwisGroundwaterCatalog();
        }
        catch ( Exception e ) {
            message = "Error reading USGS NWIS groundwater - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
    else if ( (selectedDataStore != null) && this.__source_UsgsNwisInstantaneous_enabled && (selectedDataStore instanceof UsgsNwisInstantaneousDataStore) ) {
        try {
            TSTool_UsgsNwis.getInstance(this).getTimeSeriesListClicked_ReadUsgsNwisInstantaneousCatalog();
        }
        catch ( Exception e ) {
            message = "Error reading USGS NWIS instantaneous values - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
    else if ( (selectedDataStore != null) && (selectedDataStore instanceof PluginDataStore) ) {
    	// Have a plugin datastore.
        try {
            TSTool_Plugin.getInstance(this).getTimeSeriesListClicked_ReadPluginTimeSeriesCatalog( this.__selectedInputFilter_JPanel );
        }
        catch ( Exception e ) {
            message = "Error reading time series from plugin datastore \"" + selectedDataStore.getName() +
            	"\" - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_RiverWare) && this.__source_RiverWare_enabled ) {
		try {
            TSTool_RiverWare.getInstance(this).getTimeSeriesListClicked_ReadRiverWareCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading RiverWare file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_StateCU) && this.__source_StateCU_enabled ) {
		try {
            TSTool_StateCU.getInstance(this).getTimeSeriesListClicked_ReadStateCUCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading StateCU file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
   else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_StateCUB) && this.__source_StateCUB_enabled ) {
        try {
            TSTool_StateCUB.getInstance(this).getTimeSeriesListClicked_ReadStateCUBCatalog ();
        }
        catch ( Exception e ) {
            message = "Error reading StateCU binary file - cannot display time series list (" + e + ").";
            Message.printWarning ( 1, routine, message );
            Message.printWarning ( 3, routine, e );
            return;
        }
    }
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_StateMod) && this.__source_StateMod_enabled ) {
		try {
            TSTool_StateMod.getInstance(this).getTimeSeriesListClicked_ReadStateModCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading StateMod file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_StateModB) && this.__source_StateModB_enabled ) {
		try {
            TSTool_StateModB.getInstance(this).getTimeSeriesListClicked_ReadStateModBCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading StateMod binary file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else if ( selectedInputType.equals (TSToolConstants.INPUT_TYPE_UsgsNwisRdb) && this.__source_UsgsNwisRdb_enabled ) {
		try {
            TSTool_UsgsNwis.getInstance(this).getTimeSeriesListClicked_ReadUsgsNwisRdbCatalog ();
		}
		catch ( Exception e ) {
			message = "Error reading USGS NWIS file - cannot display time series list (" + e + ").";
			Message.printWarning ( 1, routine, message );
			Message.printWarning ( 3, routine, e );
			return;
		}
	}
	else {
		if ( selectedDataStore != null ) {
		    Message.printWarning(1,routine,
			    "Getting time series list for datastore \"" + selectedDataStore.getName() + "\" is not implemented." );
		}
		else {
		    Message.printWarning(1,routine,
		        "Getting time series list for input type \"" + selectedInputType + "\" is not implemented." );
		}
	}
    if ( selectedDataStore != null ) {
    	Message.printStatus ( 1, routine,
    	    "Time series list from input type \"" + selectedDataStore.getName() + "\" are listed in Time Series List area." );
    }
    else {
        Message.printStatus ( 1, routine,
            "Time series list from input type \"" + selectedInputType + "\" are listed in Time Series List area." );
    }
}

/**
Graph ensemble results.
@param tslistFromUI list of time series from the UI to graph
(for example when one time series is graphed with Graph - Ensemble), or null if selected ensemble is graphed.
@param graphType Type of graph (same as TSTool legacy command line arguments),
typically will be "-o line" for ensembles.
@param graphProps properties to control the graph.
*/
private void uiAction_GraphEnsembleResults ( List<TS> tslistFromUI, String graphType, PropList graphProps ) {
   String routine = getClass().getSimpleName() + ".uiAction_GraphEnsembleResults";

	if ( graphProps == null ) {
        graphProps = new PropList ( "GraphProps" );
	}
    try {
        // Change the wait cursor here in the main GUI to indicate that the graph is being processed.
        JGUIUtil.setWaitCursor ( this, true );
        graphProps.set ( "OutputFormat=" + graphType );
        // Final list is selected.
        if ( this.__tsProcessor != null ) {
            try {
                int selected_tsensembles = JGUIUtil.selectedSize(this.__resultsTSEnsembles_JList);
            	TSEnsemble ensembleFromUI = null; // TODO smalers 2017-04-05 evaluate whether needed in called code.
                if ( selected_tsensembles == 0 ) {
                    commandProcessor_ProcessEnsembleResultsList ( ensembleFromUI, tslistFromUI, null, graphProps );
                }
                else {
                    commandProcessor_ProcessEnsembleResultsList ( ensembleFromUI, tslistFromUI, this.__resultsTSEnsembles_JList.getSelectedIndices(), graphProps );
                }
            }
            catch ( Exception e ) {
                Message.printWarning ( 1, routine, "Unable to graph time series from ensemble results." );
                Message.printWarning ( 3, routine, e );
            }
        }
    }
    finally {
        JGUIUtil.setWaitCursor ( this, false );
    }
}

/**
Graph time series that are in the final list.
@param graph_type Type of graph to create.
*/
private void uiAction_GraphTimeSeriesResults ( String type ) {
	uiAction_GraphTimeSeriesResults ( type, null );
}

/**
Graph time series that are in the final list.
@param graph_type Type of graph (same as tstool command line arguments).
*/
private void uiAction_GraphTimeSeriesResults ( String graph_type, String params ) {
	String routine = getClass().getSimpleName() + ".uiAction_GraphTimeSeriesResults";

	try {
		// Change the wait cursor here in the main GUI to indicate that the graph is being processed.
		JGUIUtil.setWaitCursor ( this, true );
		PropList props = new PropList ( "GraphProps" );
		props.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
		props.set ( "OutputFormat=" + graph_type );
		if ( params != null ) {
			props.set ( "Parameters=" + params );
		}
		// Final list is selected.
		if ( this.__tsProcessor != null ) {
			try {
                int selected_ts=JGUIUtil.selectedSize(this.__resultsTS_JList);
				if ( selected_ts == 0 ) {
					commandProcessor_ProcessTimeSeriesResultsList ( null, props );
				}
				else {
                    commandProcessor_ProcessTimeSeriesResultsList ( this.__resultsTS_JList.getSelectedIndices(), props );
				}
			}
			catch ( Exception e ) {
				Message.printWarning ( 1, routine, "Unable to graph time series." );
                Message.printWarning ( 3, routine, e );
			}
		}
		JGUIUtil.setWaitCursor ( this, false );
	}
	catch ( Exception e ) {
		JGUIUtil.setWaitCursor ( this, false );
	}
}

/**
Import a configuration file and merge with the existing configuration file.
@param configFilePath Path to the current configuration file.
*/
private void uiAction_ImportConfiguration ( String configFilePath ) {
    String routine = getClass().getSimpleName() + ".uiAction_ImportConfiguration";
    // Print an explanation before continuing.
    int x = ResponseJDialog.NO;
    x = new ResponseJDialog ( this, IOUtil.getProgramName(),
        "This functionality is being reviewed.  Refer to documentation instead of using this tool.\n\n" +
        "The current TSTool configuration information will be updated as follows:\n\n" +
        "1) You will select a configuration file to merge (e.g., containing old preferences).\n" +
        "2) The properties in the current configuration file will be updated to matching properties in the selected file.\n" +
        "3) You will need to restart the software in order for the new information to take effect.\n\n" +
        "Continue?",
        ResponseJDialog.YES| ResponseJDialog.NO).response();
    if ( x == ResponseJDialog.NO ) {
        return;
    }
    // Else continue the process.
    // Pick the configuration file.
    File currentConfigFile = new File ( configFilePath );
    JFileChooser fc = JFileChooserFactory.createJFileChooser ( currentConfigFile.getParent() );
    fc.setDialogTitle("Select New " + IOUtil.getProgramName() + " Configuration File");
    SimpleFileFilter sff = new SimpleFileFilter("cfg", "TSTool Configuration File");
    fc.addChoosableFileFilter(sff);
    fc.setFileFilter(sff);
    if (fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
        return;
    }
    // Else, continue and do the merge.
    try {
        license_MergeConfigFiles ( currentConfigFile, new File(fc.getSelectedFile().getPath()));
        x = new ResponseJDialog ( this, IOUtil.getProgramName(),
            "You must restart the software in order for the new configuration information to take effect.",
            ResponseJDialog.OK).response();
    }
    catch ( Exception e ) {
        Message.printWarning( 1, routine, "There was an error updating the configuration file.  Check permissions." );
        Message.printWarning(3, routine, e);
    }
}

/**
Indent the selected commands in the commands list.
@param indentDirection -1 to indent to the left, 1 to indent to the right
*/
private void uiAction_IndentCommands ( int indentDirection ) {
	//String routine = getClass().getSimpleName() + ".uiAction_IndentCommands";
	int size = 0;
	int [] selected_indices = ui_GetCommandJList().getSelectedIndices();
	if ( selected_indices != null ) {
		size = selected_indices.length;
	}
	if ( size == 0 ) {
		return;
	}

	Command command = null;
	// TODO smalers 2023-02-19 invalidation is apparently not needed.
	//boolean didChange = false;
	for ( int i = 0; i < size; i++ ) {
		command = (Command)this.__commands_JListModel.get(selected_indices[i]);
		if ( indentDirection < 0 ) {
			// Reduce indent if possible.
			if ( command.toString().startsWith(TSToolConstants.INDENT_SPACES) ) {
				//Message.printStatus(2, routine, "Decreasing command indent string to: \"" +
				//command.toString().substring(TSToolConstants.INDENT_SPACES.length()) + "\"");
				command.setCommandString(command.toString().substring(TSToolConstants.INDENT_SPACES.length()) );
				// Set the command list dirty so that "modified" is shown for the command file.
				commandList_SetDirty(true);
				//Message.printStatus(2, routine, "After decreasing command string indent: \"" + command.toString() + "\"");
				//didChange = true;
			}
		}
		else if ( indentDirection > 0 ) {
			// Increase indent.
			//Message.printStatus(2, routine, "Increasing command string indent to: \"" +
			//TSToolConstants.INDENT_SPACES + command + "\"");
			command.setCommandString(TSToolConstants.INDENT_SPACES + command );
			// Set the command list dirty so that "modified" is shown for the command file.
			commandList_SetDirty(true);
			//Message.printStatus(2, routine, "After increasing command string indent (" +
			//		((AbstractCommand)command).getIndentSpaceCount() +
			//		"): \"" + command.toString() + "\"");
			//didChange = true;
		}
		/*
		if ( didChange ) {
			Message.printStatus(2, routine, "Command string after indent change (" +
				((AbstractCommand)command).getIndentSpaceCount() +
			"): \"" + command + "\"");
		}
		*/
	}

	// Invalidate the list so that it shows the current contents:
	// - need to do this since the list contents were changed independent of the list model
	//if ( didChange ) {
		//this.__commands_AnnotatedCommandJList.invalidate();
	//}
}

/**
Reset the query options choices based on the selected input name.
Other method calls are cascaded to fully reset the choices.
@param selectedDataStore if not null, then the blank input name is selected;
if null, then the input name selection is processed
*/
public void uiAction_InputNameChoiceClicked(DataStore selectedDataStore) {
	String routine = getClass().getSimpleName() + "uiAction_InputNameChoiceClicked";
	if ( this.__inputName_JComboBox == null ) {
		return;
	}
	// Default is for selected name and visible name to be the same,
	// but phase in abbreviated visible names for some input types below.
	String selectedInputName = ui_GetSelectedInputName();
	String selectedInputNameVisible = selectedInputName;

    if ( selectedDataStore != null ) {
        Message.printStatus(2, routine, "Blanking out input type because datastore \"" +
            selectedDataStore.getName() + "\" has been selected." );
        // Set the input name to blank, adding the blank item if necessary.
        if ( this.__inputName_JComboBox.getItemCount() == 0 ) {
            this.__inputName_JComboBox.add("");
        }
        else if ( !this.__inputName_JComboBox.getItemAt(0).equals("") ) {
            this.__inputName_JComboBox.addAt("",0);
        }
        ui_SetIgnoreItemEvent(true);
        this.__inputName_JComboBox.select("");
        ui_SetIgnoreItemEvent(false);
        return;
    }

	//if ( Message.isDebugOn ) {
	//	Message.printDebug ( 1, routine, "Input name has been selected:  \"" + selectedInputName + "\"" );
	//}
	Message.printStatus ( 2, routine, "Input name has been selected:  \"" + selectedInputName + "\"" );

	// List alphabetically.
	try {
	    String selectedInputType = ui_GetSelectedInputType();
        if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HECDSS ) ) {
        	TSTool_HecDss.getInstance(this).inputNameSelected(selectedInputNameVisible);
        }
        else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files ) ) {
        	TSTool_FS5Files.getInstance(this).inputNameSelected();
    	}
	}
	catch ( Exception e ) {
		Message.printWarning ( 3, routine, e );
	}
}

/**
Reset the query options choices based on the selected input type.
Other method calls are cascaded to fully reset the choices.
This method also shows/hides columns in the query results multilist to be appropriate for the data input source.
@param selectedDataStore if not null, then the input type choice is being cascaded through from
a datastore selection and just needs to further cascade to the input type, setting both to blank.
If null, then input type and name are fully processed, ignoring the datastore.
*/
private void uiAction_InputTypeChoiceClicked ( DataStore selectedDataStore ) {
	String routine = getClass().getSimpleName() + ".uiAction_InputTypeChoiceClicked";
	if ( this.__inputType_JComboBox == null ) {
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, routine, "Input type has been selected but GUI is not yet initialized.");
		}
		return;	// Not done initializing.
	}
	if ( selectedDataStore != null ) {
	    Message.printStatus(2, routine, "Blanking out input type because datastore \"" +
	        selectedDataStore.getName() + "\" has been selected." );
	    // Set the input type to blank, adding the blank item if necessary.
        if ( this.__inputType_JComboBox.getItemCount() == 0 ) {
            this.__inputType_JComboBox.add("");
        }
        else if ( !this.__inputType_JComboBox.getItemAt(0).equals("") ) {
            this.__inputType_JComboBox.addAt("",0);
        }
        ui_SetIgnoreItemEvent(true);
        this.__inputType_JComboBox.select("");
        ui_SetIgnoreItemEvent(false);
	    // Now chain to selecting the input name - this will blank the input name selection.
	    uiAction_InputNameChoiceClicked(selectedDataStore);
	    return;
	}
	// Get the selected input type.
    String selectedInputType = ui_GetSelectedInputType();
	if ( selectedInputType == null ) {
		// Apparently this happens when setData() or similar is called on the JComboBox, and before select() is called.
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, routine, "Input type has been selected:  null (select is ignored)" );
		}
		return;
	}
	// If here, make sure to blank out the selection on the datastore so that the user is not confused by seeing both.
	ui_SetIgnoreItemEvent(true);
	this.__dataStore_JComboBox.select ( "" );
	ui_SetIgnoreItemEvent(false);

	if ( Message.isDebugOn ) {
		Message.printDebug ( 1, routine, "Input type has been selected:  \"" + selectedInputType + "\"" );
	}

	// List alphabetically.
	try {
	    if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_DateValue ) ) {
	    	TSTool_DateValue.getInstance(this).selectInputType();
    	}
        else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HECDSS ) ) {
            TSTool_HecDss.getInstance(this).selectInputType();
        }
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HydroBase )) {
    	    TSTool_HydroBase.getInstance(this).selectInputType();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_MODSIM ) ) {
    	    TSTool_Modsim.getInstance(this).selectInputType();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSCARD ) ) {
    	    TSTool_NwsrfsCard.getInstance(this).selectInputType();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSRFS_FS5Files)) {
    		TSTool_FS5Files.getInstance(this).selectInputType();
    	}
    	else if(selectedInputType.equals ( TSToolConstants.INPUT_TYPE_NWSRFS_ESPTraceEnsemble)) {
    		TSTool_NwsrfsEsp.getInstance(this).selectInputType();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_RiverWare ) ) {
    		TSTool_RiverWare.getInstance(this).selectInputType();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateCU ) ) {
    		// Prompt for a StateCU file and update choices.
    		TSTool_StateCU.getInstance(this).selectInputType ( true );
    	}
        else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateCUB ) ) {
            // Prompt for a StateCU binary file and update choices.
            TSTool_StateCUB.getInstance(this).selectInputType ( true );
        }
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateMod ) ) {
    	    TSTool_StateMod.getInstance(this).selectInputType ();
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_StateModB ) ) {
    		// Prompt for a StateMod binary file and update choices.
    		TSTool_StateModB.getInstance(this).selectInputType ( true );
    	}
    	else if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_UsgsNwisRdb ) ) {
    	    TSTool_UsgsNwis.getInstance(this).inputTypeSelected ();
    	}
    	else {
    	    // Not a recognized input source.
    		Message.printWarning ( 1, routine,"\"" + selectedInputType + "\" is not a recognized input type." );
    		return;
    	}
	}
	catch ( Exception e ) {
		Message.printWarning ( 1, routine, "Error setting up choices for " + selectedInputType + " input type (" + e + ")." );
		Message.printWarning ( 3, routine, e );
	}
}

/**
Create a new command file.
If any existing commands have been modified the user has the option of saving.
Then, the existing commands are cleared and the command file name is reset to null.
*/
private void uiAction_NewCommandFile () {
    // See whether the old commands need to be saved/cleared.
    if ( !uiAction_OpenCommandFile_CheckForSavingCommands() ) {
        return;
    }

    // Clear the commands reset the name to null.

    commandList_RemoveAllCommands ();
    // deleteCommands() sets to true but since are clearing the command file name, the commands are not dirty.
    commandList_SetDirty ( false );
    commandList_SetCommandFileName ( null );
    // Clear the old results.
    results_Clear();
    ui_UpdateStatusTextFields ( 2, null, null, "Use Commands menu to insert commands", TSToolConstants.STATUS_READY );
    this.__processor_JProgressBar.setValue ( 0 );
    this.__command_JProgressBar.setValue ( 0 );
}

/**
Open a command file and read into the list of commands.
A check is made to see if the list contains anything and if it does the user is prompted as to
whether need to save the previous commands.
@param commandFile command file to open, specified as null if file selector dialog should display,
or as the full path to the command file if a recent file from the history has been selected
@param runDiscoveryOnLoad if true, run discovery on the commands as they are loaded (the normal case);
if false (may be useful for very large command files), do not run discovery when loading commands
*/
private void uiAction_OpenCommandFile ( String commandFile, boolean runDiscoveryOnLoad ) {
	String routine = getClass().getSimpleName() + ".openCommandFile";
    // It is possible that the last command processor run is still processing commands.
    TSCommandProcessor processor = commandProcessor_GetCommandProcessor();
    if ( processor.getIsRunning() ) {
        // TODO smalers 2013 figure out status of processing (percent complete).
        int x = new ResponseJDialog ( this, IOUtil.getProgramName(),
        "The previous commands are still running (if commands were killed then ignore this warning).\n" +
        "Do you want to load a new command file?\n\n" +
        "Yes - load new command file - old commands will run in background until complete\n" +
        "No - continue working with current command file (also can cancel)",
        ResponseJDialog.YES|ResponseJDialog.NO).response();
        if ( x == ResponseJDialog.NO ) {
            return;
        }
    }

	// See whether the old commands need to be saved/cleared:
    // - a cancel will return false meaning the existing commands will remain in the command area
    if ( !uiAction_OpenCommandFile_CheckForSavingCommands() ) {
        return;
    }

	// Get the file.  Do not clear the list until the file has been chosen and is readable.

    if ( commandFile == null ) {
		String initial_dir = ui_GetDir_LastCommandFileOpened();
		Message.printStatus ( 2, routine, "Initial directory for browsing:  \"" + initial_dir + "\"" );
		JFileChooser fc = JFileChooserFactory.createJFileChooser ( initial_dir );
		fc.setDialogTitle("Open " + IOUtil.getProgramName() + " Command File");
		List<String> extensionList = new ArrayList<>();
		extensionList.add("tstool");
		extensionList.add("TSTool");
		SimpleFileFilter sff = new SimpleFileFilter(extensionList, "TSTool Command File");
		fc.addChoosableFileFilter(sff);
		fc.setFileFilter(sff);
		if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
			// If the user approves a selection do the following.
			String directory = fc.getSelectedFile().getParent();
			String path = fc.getSelectedFile().getPath();

			// Set the "WorkingDir" property, which will NOT contain a trailing separator.
			IOUtil.setProgramWorkingDir(directory);
			ui_SetDir_LastCommandFileOpened(directory);
			this.__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
			ui_SetInitialWorkingDir ( __props.getValue ( "WorkingDir" ) );
			Message.printStatus(2, routine,
			    "Working directory (and initial working directory) from the command file is \"" + IOUtil.getProgramWorkingDir() + "\".");
			// Save in the session.
			this.session.pushHistory(path);
			// Update the recent files in the File...Open menu, for the next menu access.
			ui_InitGUIMenus_File_OpenRecentFiles();
			// Load but do not automatically run.
			ui_LoadCommandFile ( path, false, runDiscoveryOnLoad );
		}
    }
    else {
    	// Command file has been selected from the history.
    	// Set some state information, similar to above, but no need to update menus since picking from visible choice.
    	// TODO smalers 2014-12-19 maybe this information should be saved in the TSToolSession instance.
    	File f = new File(commandFile);
    	String directory = f.getParent();
		IOUtil.setProgramWorkingDir(directory);
		ui_SetDir_LastCommandFileOpened(directory);
		this.__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
		ui_SetInitialWorkingDir ( __props.getValue ( "WorkingDir" ) );
		// Save in the session.
		this.session.pushHistory(commandFile);
		// Update the recent files in the File...Open menu, for the next menu access.
		ui_InitGUIMenus_File_OpenRecentFiles();
    	// Load but do not automatically run.
    	ui_LoadCommandFile ( commandFile, false, runDiscoveryOnLoad );
    }
	// New file has been opened or there was a cancel/error and the old list remains.
	//Message.printStatus ( 2, routine, "Done reading commands.  Calling ui_UpdateStatus...");
	ui_UpdateStatus ( true );
	//Message.printStatus ( 2, routine, "Back from update status." );
}

/**
Check whether existing commands need to be saved (called when loading or creating a new command file).
@return true if the operation (open or new) should continue, or false if user has canceled.
*/
private boolean uiAction_OpenCommandFile_CheckForSavingCommands() {
    if ( !this.__commandsDirty ) {
        // No need to do anything so return true that it is OK to continue with operation.
        return true;
    }
    if ( this.__commandFileName == null ) {
        // Have not been saved before.
        // Always allow save, even if read-only comment or template is set (since first save).
        int x = ResponseJDialog.NO; // Blank commands will not be saved.
        if ( this.__commands_JListModel.size() > 0 ) {
            x = new ResponseJDialog ( this, IOUtil.getProgramName(),
            "Do you want to save the changes you made?\n\n" +
            "To view differences, Cancel and use View / Command File Diff.",
            ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
        }
        if ( x == ResponseJDialog.CANCEL ) {
            return false;
        }
        else if ( x == ResponseJDialog.YES ) {
            // Prompt for the name and then save.
            uiAction_WriteCommandFile ( this.__commandFileName, true, false );
        }
    }
    else {
        // A command file exists...  Warn the user.
    	// They can save to the existing file name or can cancel and
        // File...Save As... to a different name.
        int x = ResponseJDialog.NO;
        boolean commandsAreTemplate = false;
        if ( this.__commands_JListModel.size() > 0 ) {
            if ( __tsProcessor.getReadOnly() ) {
                x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                    "Do you want to save the changes made to the command file?\n"
                    + "    " + this.__commandFileName + "\n\n" +
                    "The commands are marked read-only (#@readOnly comment).\n" +
                    "Press Yes to update the read-only file before opening a new file.\n" +
                    "Press No to discard edits before opening a new file.\n" +
                    "Press Cancel and then save to a new name if desired.\n" +
                    "To view differences, Cancel and use View / Command File Diff.",
                    ResponseJDialog.YES|ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
            }
            else if ( commandsAreTemplate = this.__tsProcessor.areCommandsTemplate() ) {
                x = new ResponseJDialog ( this, IOUtil.getProgramName(),
            		"The commands are marked as a template (#@template comment).\n" +
                    "TSTool does not currently support editing template command files.  You must use a text editor.\n" +
                    "Functionality is being evaluated and may be enabled in the future to allow editing template command files.\n" +
                    "Press Ok to continue without saving or Cancel to return to TSTool.",
                    ResponseJDialog.OK|ResponseJDialog.CANCEL).response();
            }
            else {
                x = new ResponseJDialog ( this, IOUtil.getProgramName(),
                "Do you want to save the changes made to the command file?\n"
                + "    " + this.__commandFileName + "\n\n" +
                "To view differences, Cancel and use View / Command File Diff.",
                ResponseJDialog.YES| ResponseJDialog.NO|ResponseJDialog.CANCEL).response();
            }
        }
        if ( x == ResponseJDialog.CANCEL ) {
            return false;
        }
        else if ( !commandsAreTemplate && (x == ResponseJDialog.YES) && (this.__commands_JListModel.size() > 0) ) {
        	// Only write command file if not zero commands (otherwise will blank out previous file).
            uiAction_WriteCommandFile ( this.__commandFileName, false, false );
        }
        // Else if No or OK will clear before opening the other file.
    }
    return true;
}

/**
Paste the cut buffer containing Command instances that were previously cut or copied, inserting after the selected item.
*/
private void uiAction_PasteFromCutBufferToCommandList () {
	// Default selected to zero (empty list).
	int last_selected = -1;
	int list_size = this.__commands_JListModel.size();

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

	int buffersize = this.__commandsCutBuffer.size();

	Command command = null;
	for ( int i = 0; i < buffersize; i++ ) {
		command = (Command)this.__commandsCutBuffer.get(i);
		commandList_InsertCommandAt ( command, (last_selected + 1 + i) );
	}

	// Leave in the buffer so it can be pasted again.

	commandList_SetDirty ( true );
	ui_UpdateStatus ( true );
}

/**
Method to read a TSProduct file and process the product.
@param tspFile if non-null, use it.  If null, prompt for the file.
@param view_gui If true, the graph will be displayed on the screen.
If false, an output file will be prompted for.
*/
private void uiAction_ProcessTSProductFile ( File tspFile, boolean view_gui )
throws Exception {
	String path = null;
	if ( tspFile == null ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser ( JGUIUtil.getLastFileDialogDirectory() );
		fc.setDialogTitle ( "Select TS Product File" );
		SimpleFileFilter sff = new SimpleFileFilter ( "tsp", "Time Series Product File" );
		fc.addChoosableFileFilter ( sff );
		fc.setFileFilter ( sff );
		if ( fc.showOpenDialog(this) != JFileChooser.APPROVE_OPTION) {
			// Return if no file name is selected.
			return;
		}

		path = fc.getSelectedFile().getPath();
		String directory = fc.getSelectedFile().getParent();
		JGUIUtil.setLastFileDialogDirectory ( directory );
	}
	else {
		path = tspFile.getAbsolutePath();
	}

	PropList override_props = new PropList ("TSTool");
	DateTime now = new DateTime ( DateTime.DATE_CURRENT );
	override_props.set ( "CurrentDateTime=", now.toString() );
	if ( view_gui ) {
		override_props.set ( "InitialView", "Graph" );
		override_props.set ( "PreviewOutput", "True" );
	}
	TSProcessor p = new TSProcessor ();
	// Set up the time series supplier.
	if ( this.__tsProcessor != null ) {
		// Time series should be in memory so add the TSCommandProcessor as a supplier.
		// This should result in quick supplying of in-memory time series.
		p.addTSSupplier ( this.__tsProcessor );
	}

	// Now process the product.

	p.processProduct ( path, override_props );
}

/**
Show properties for the selected ensemble(s).
*/
private void uiAction_ResultsEnsembleProperties () {
    String routine = getClass().getSimpleName() + ".uiAction_ResultsEnsembleProperties";
    String message;
    // Get the selected ensembles.
    int selected [] = this.__resultsTSEnsembles_JList.getSelectedIndices();
    if ( (selected == null) || (selected.length == 0) ) {
        // Nothing is selected to process all.
        int size = this.__resultsTSEnsembles_JListModel.size();
        selected = new int[size];
        for ( int i = 0; i < size; i++ ) {
            selected[i] = i;
        }
    }
    // Get the list of time series from the processor, to check whether time series are shared.
    List<TS> tslist = null;
    int tsResultsSize = -1;
    try {
        @SuppressWarnings("unchecked")
		List<TS> dataList = (List<TS>)__tsProcessor.getPropContents("TSResultsList");
        tslist = dataList;
        tsResultsSize = tslist.size();
    }
    catch ( Exception e ) {
        // Should not happen.
        message = "Error getting time series list from processor:";
        Message.printWarning ( 3, routine, message );
        Message.printWarning ( 3, routine, e );
    }
    // Get the properties from the ensembles, including included time series properties.
    String ensembleDisplay;
    String ensembleID;
    TSEnsemble ensemble;
    List<String> v = new ArrayList<>();
    v.add ( "Ensemble Properties" );
    TS ts;
    for ( int i = 0; i < selected.length; i++ ) {
        // Get the ensemble ID from the list.
        ensembleDisplay = this.__resultsTSEnsembles_JListModel.get(selected[i]);
        ensemble = results_Ensembles_GetEnsembleID ( ensembleDisplay );
        if ( ensemble == null ) {
            continue;
        }
        ensembleID = ensemble.getEnsembleID();
        // TODO smalers 2016-02-25 Need a tabbed panel UI like for time series properties.
        // Format the output and append to what is displayed.
        v.add ( "" );
        v.add ( "EnsembleID = " + ensembleID );
        v.add ( "EnsembleName = " + ensemble.getEnsembleName() );
        HashMap<String,Object> properties = ensemble.getProperties();
        if ( properties.size() > 0 ) {
        	ArrayList<String> keyList = new ArrayList<>(properties.keySet());
            Collections.sort(keyList);
            for ( String key : keyList ) {
            	if ( key.equals("EnsembleID") || key.equals("EnsembleName") ) {
            		// Printed above so don't print - case-specific.
            		continue;
            	}
                Object value = properties.get(key);
                if ( value == null ) {
                    value = "";
                }
            	v.add ( key + " = " + value );
            }
        }
        int ensembleSize = ensemble.size();
        v.add ( "" );
        v.add ( "Number of time series:  " + ensembleSize );
        for ( int its = 0; its < ensembleSize; its++ ) {
            ts = ensemble.get(its);
            v.add ( "  " + StringUtil.formatString( (its + 1), "%4d") + " Time series identifier:  " + ts.getIdentifierString() + ", Alias: " + ts.getAlias() );
            v.add ( "        Period:  " + ts.getDate1() + " - " + ts.getDate2() );
            // Determine if the time series exists in the main time series list.
            boolean found = false;
            int foundPos = -1;
            if ( tslist == null ) {
                // Did not have the main time series list for some reason.
                v.add ( "        Shared with main time series list:  UNKNOWN (no main list available)" );
            }
            else {
                // Loop through the main time series list and try to match the time series reference,
                // which will differ if the time series was copied.
                TS tsr;
                for ( int irts = 0; irts < tsResultsSize; irts++ ) {
                    tsr = tslist.get(irts);
                    // Compare by reference.
                    if ( tsr == ts ) {
                        found = true;
                        foundPos = irts;
                        break;
                    }
                }
                if ( found ) {
                    v.add ( "        Shared with main time series list:  YES, time series " + (foundPos + 1) +
                    " (was not copied to ensemble)" );
                }
                else {
                    v.add ( "        Shared with main time series list:  NO (was copied to ensemble)" );
                }
            }
        }
    }
    PropList reportProp = new PropList ("ReportJFrame.props");
    // Too big (make this big when we have more stuff).
    //reportProp.set ( "TotalWidth", "750" );
    //reportProp.set ( "TotalHeight", "550" );
    reportProp.set ( "TotalWidth", "800" );
    reportProp.set ( "TotalHeight", "500" );
    reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
    reportProp.set ( "DisplaySize", "11" );
    reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
    reportProp.set ( "PrintSize", "7" );
    reportProp.set ( "Title", "Ensemble Properties" );
    reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
    new ReportJFrame ( v, reportProp );
}

/**
Run the commands in the command list.  These time series are saved in
__ts_processor and are then available for export, analysis, or viewing.
This method should only be called if there are commands in the command list.
@param runAllCommands If false, then only the selected commands are run.
If true, then all commands are run.
@param createOutput If true, then all write* methods are processed by the TSEngine.
If false, only the time series in memory remain at the end and can be viewed.
The former is suitable for batch files, both for the GUI.
*/
private void uiAction_RunCommands ( boolean runAllCommands, boolean createOutput ) {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommands";
	ui_UpdateStatusTextFields ( 1, routine, null, "Running commands...", TSToolConstants.STATUS_BUSY);
	results_Clear ();
	System.gc();
	// Get commands to run (all or selected).
	List<Command> commands = commandList_GetCommands ( runAllCommands );
	// The limits of the command progress bar are handled in commandStarted().
	// Run the commands in a thread.
	commandProcessor_RunCommandsThreaded ( commands, createOutput );
	// List of time series is displayed when CommandProcessorListener detects that the last command is complete.
}

/**
Display the results of the run, time series and output files.
This is handled as a "pinch point" in hand-off from the processor and the UI,
to try to gracefully handle displaying output.
*/
private void uiAction_RunCommands_ShowResults() {
	// This method may be called from a thread different than the Swing thread.
	// To avoid bad behavior in GUI components (like the results list having big gaps),
	// use the following to queue up GUI actions on the Swing thread.

	Runnable r = new Runnable() {
		public void run() {
            // Close the regression results report if it is open (have to do here because
            // layers of recursion can occur when running a command file).
            TSCommandProcessorUtil.closeRegressionTestReportFile();
			results_Clear();
            uiAction_RunCommands_ShowResultsEnsembles();
            uiAction_RunCommands_ShowResultsNetworks();
            uiAction_RunCommands_ShowResultsOutputFiles();
            uiAction_RunCommands_ShowResultsObjects();
            uiAction_RunCommands_ShowResultsProblems();
            uiAction_RunCommands_ShowResultsProperties();
            uiAction_RunCommands_ShowResultsTables();
			uiAction_RunCommands_ShowResultsTimeSeries();
			uiAction_RunCommands_ShowResultsViews();

            // Repaint the list to reflect the status of the commands.
            ui_ShowCurrentCommandListStatus (CommandPhaseType.RUN);
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
Display the ensembles from the command processor in the results list.
*/
private void uiAction_RunCommands_ShowResultsEnsembles () {
    String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsEnsembles";
    //Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsEnsembles", "Entering method.");

    // Fill the ensemble list with the descriptions of the in-memory time series.
    int size = commandProcessor_GetEnsembleResultsListSize();
    Message.printStatus ( 2, routine, "Adding " + size + " ensembles to results." );
    TSEnsemble tsensemble = null;
    for ( int i = 0; i < size; i++ ) {
        try {
            tsensemble = commandProcessor_GetEnsembleAt(i);
        }
        catch ( Exception e ) {
            results_Ensembles_AddEnsembleToResults ( "" + (i + 1) + " - Error getting ensemble from processor." );
            Message.printWarning ( 3, routine, e );
            continue;
        }
        if ( tsensemble == null ) {
            results_Ensembles_AddEnsembleToResults ( "" + (i + 1)+ " - Null ensemble from processor." );
            continue;
        }
        else {
            // Have actual data to display.
            String id = tsensemble.getEnsembleID();
            String name = tsensemble.getEnsembleName();
            results_Ensembles_AddEnsembleToResults ( "" + (i + 1) + ") " + id + " - " + name );
            //+ " - " + ts.getIdentifier() + " (" + ts.getDate1() + " to " + ts.getDate2() + ")" );
        }
    }
    ui_UpdateStatus ( false );

    ui_UpdateStatusTextFields ( 1, routine, null, "Completed running commands.  Use Results and Tools menus.",
           TSToolConstants.STATUS_READY );
    // Make sure that the user is not waiting on the wait cursor.
    //JGUIUtil.setWaitCursor ( this, false );

    //Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsTimeSeries", "Leaving method.");
}

/**
Display the network results.
*/
private void uiAction_RunCommands_ShowResultsNetworks() {
    // Get the list of networks from the processor.
    List<NodeNetwork> networkList = commandProcessor_GetNetworkResultsList();
    int size = 0;
    if ( networkList != null ) {
        size = networkList.size();
    }
    ui_SetIgnoreActionEvent(true);
    NodeNetwork network;
    // Use HTML only when needed to show a zero or 1-node (end node) size network.
    String htmlStart = "<html><span style=\"color:red;font-weight:bold\">", htmlStart2;
    String htmlEnd = "</span></html>", htmlEnd2;
    String endNote;
    int numNodes = 0;
    for ( int i = 0; i < size; i++ ) {
        network = networkList.get(i);
        if ( network instanceof HydrologyNodeNetwork ) {
        	HydrologyNodeNetwork hn = (HydrologyNodeNetwork)network;
        	numNodes = hn.size();
        }
        htmlStart2 = "";
        htmlEnd2 = "";
        endNote = "";
        if ( numNodes <= 1 ) {
            htmlStart2 = htmlStart;
            htmlEnd2 = htmlEnd;
            endNote = " (includes end node)";
        }
        results_Networks_AddNetwork ( htmlStart2 + (i + 1) + ") " + network.getNetworkId() +
            " - " + network.getNetworkName() + ", " + numNodes + " nodes" + htmlEnd2 + endNote );
    }
    ui_SetIgnoreActionEvent(false);
}

/**
Display the object results.
*/
private void uiAction_RunCommands_ShowResultsObjects() {
    // Get the list of objects from the processor.
    List<JSONObject> objectList = commandProcessor_GetObjectResultsList();
    int size = 0;
    if ( objectList != null ) {
        size = objectList.size();
    }
    ui_SetIgnoreActionEvent(true);
    JSONObject object;
    // Use HTML only when needed to show a zero-size object.
    //String htmlStart = "<html><span style=\"color:red;font-weight:bold\">";
    String htmlStart2;
    //String htmlEnd = "</span></html>";
    String htmlEnd2;
    String endNote;
    //int numNodes = 0;
    for ( int i = 0; i < size; i++ ) {
        object = objectList.get(i);
        htmlStart2 = "";
        htmlEnd2 = "";
        endNote = "";
        //if ( numNodes <= 1 ) {
        //    htmlStart2 = htmlStart;
        //    htmlEnd2 = htmlEnd;
        //    endNote = " (includes end node)";
        //}
        results_Objects_AddObject ( htmlStart2 + (i + 1) + ") " + object.getObjectID()
            //" - " + object.getObjectName() + ", " + numNodes + " nodes"
        	+ htmlEnd2 + endNote );
    }
    ui_SetIgnoreActionEvent(false);
}

/**
Display the list of output files from the commands.
*/
private void uiAction_RunCommands_ShowResultsOutputFiles() {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsOutputFiles";
	// Loop through the commands.  For any that implement the FileGenerator interface,
	// get the output file names and add to the list.
	// Only add a file if not already in the list.
	//Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsOutputFiles", "Entering method.");
	ui_SetIgnoreActionEvent(true);
	try {
		Object o = commandProcessor_GetCommandProcessor().getPropContents("OutputFileList");
		if ( o != null ) {
			@SuppressWarnings("unchecked")
			List<File> outputFileList = (List<File>)o;
			for ( File f: outputFileList ) {
				results_OutputFiles_AddOutputFile ( f );
			}
		}
	}
	catch ( Exception e ) {
		Message.printWarning(3, routine, e);
		Message.printWarning(1, routine, "Error showing output files in results (" + e + ").");
	}
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
        // Get all of the command log messages from all commands for run phase:
    	// - logging code below wants a list of CommandStatusProvider, which commands are
        @SuppressWarnings("rawtypes")
		List commands = this.__tsProcessor.getCommands();
        // For normal commands, the log records will be for the specific command.
        // For RunCommand() commands, the log records will include commands in the command file that was run.
        // If show discovery it can be confusing with ${Property}, etc.
        // TODO smalers 2024-04-18 this may cause some notifications that are created in initialization to not show up.
        CommandPhaseType [] commandPhases = {
        	CommandPhaseType.RUN
       	};
        // List failures first
        CommandStatusType [] statusTypes = {
        	CommandStatusType.FAILURE,
        	CommandStatusType.WARNING,
        	CommandStatusType.NOTIFICATION
        };
        @SuppressWarnings("unchecked")
		List<CommandLogRecord> logRecordList = CommandStatusUtil.getLogRecordList ( commands, commandPhases, statusTypes );
        Message.printStatus( 2, routine, "There were " + logRecordList.size() +
            " problems processing " + commands.size() + " commands.");
        // Create a new table model for the problem list.
        // TODO smalers 2009-03-01 Evaluate whether should just update data in existing table model (performance?).
        CommandLog_TableModel tableModel = new CommandLog_TableModel ( logRecordList );
        CommandLog_CellRenderer cellRenderer = new CommandLog_CellRenderer( tableModel );
        this.__resultsProblems_JWorksheet.setCellRenderer ( cellRenderer );
        this.__resultsProblems_JWorksheet.setModel ( tableModel );
        this.__resultsProblems_JWorksheet.setColumnWidths ( cellRenderer.getColumnWidths() );
        ui_SetIgnoreActionEvent(false);
    }
    catch ( Exception e ) {
        Message.printWarning( 3 , routine, e);
        Message.printWarning ( 1, routine, "Unexpected error displaying problems from run (" + e + ") - contact support.");
    }
    //Message.printStatus ( 2, "uiAction_RunCommands_ShowProblems", "Leaving method.");
}

/**
Display the list of properties from the command processor.
*/
private void uiAction_RunCommands_ShowResultsProperties() {
    String routine = getClass().getSimpleName() + ".uiAction_RunCommands_ShowResultsProperties";
    try {
        // Create a new table model for the command processor properties:
    	// - make a copy of the properties so as to not impact the processor
        // - TODO smalers 2009-03-01 Evaluate whether should just update data in existing table model (performance?)
        TSCommandProcessor processor = commandProcessor_GetCommandProcessor();
        Collection<String> propertyNames = processor.getPropertyNameList(true, true);
        PropList props = new PropList("processor");
        Object propContents = null;
        for ( String propertyName : propertyNames ) {
        	try {
        		propContents = processor.getPropContents(propertyName);
        		// See the TSTool UI properties for values.
        		// Want to minimize noise and possibly sensitive data in log file.
        		//if ( propContents != null ) {
		     	//	Message.printStatus(2, "", "Property " + propertyName + " = " + propContents);
		     	//	Message.printStatus(2, "", "Property " + propertyName + " (class) = " + propContents.getClass());
	     		//}
        	}
        	catch ( Exception e ) {
        		Message.printWarning(2,routine,e);
        	}
            if ( propContents == null) {
            	// Set as null object with blank string value.
                props.set(new Prop(propertyName, propContents, ""));
            }
            else {
            	// Set the object pointer and string equivalent.
                props.set(new Prop(propertyName, propContents, "" + propContents) );
            }
        }
        PropList_TableModel tableModel = new PropList_TableModel ( props, false, false );
        tableModel.setKeyColumnName("Property Name");
        tableModel.setTypeColumnName("Property Type");
        tableModel.setValueColumnName("Property Value");
        PropList_CellRenderer cellRenderer = new PropList_CellRenderer( tableModel );
        this.__resultsProperties_JWorksheet.setCellRenderer ( cellRenderer );
        this.__resultsProperties_JWorksheet.setModel ( tableModel );
        this.__resultsProperties_JWorksheet.setColumnWidths ( cellRenderer.getColumnWidths() );
        ui_SetIgnoreActionEvent(false);
    }
    catch ( Exception e ) {
        Message.printWarning( 3 , routine, e);
        Message.printWarning ( 1, routine, "Unexpected error displaying processor properties (" + e + ") - contact support.");
    }
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
Display the time series from the command processor in the results list.
*/
private void uiAction_RunCommands_ShowResultsTimeSeries () {
	String routine = getClass().getSimpleName() + "uiAction_RunCommands_ShowResultsTimeSeries";
	//Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsTimeSeries", "Entering method.");

	// Fill the time series list with the descriptions of the in-memory time series.
	int size = commandProcessor_GetTimeSeriesResultsListSize();
	Message.printStatus ( 2, routine, "Adding " + size + " time series to results." );
	TS ts = null;
	String desc = null;
	String alias = null;
	DateTime date1, date2;
	boolean [] selected_boolean = new boolean[size];   // Size to results list.
	// HTML brackets to deal with data issues - is red OK or is that a problem for people that are color-blind?
	String htmlStart = "<html><span style=\"color:red;font-weight:bold\">", htmlStart2;
	String htmlEnd = "</span></html>", htmlEnd2;
	for ( int i = 0; i < size; i++ ) {
		selected_boolean[i] = false;
		try {
            ts = commandProcessor_GetTimeSeries(i);
		}
		catch ( Exception e ) {
			results_TimeSeries_AddTimeSeriesToResults ( htmlStart + (i + 1) + ") - Error getting time series from processor." + htmlEnd );
			Message.printWarning ( 3, routine, e );
			continue;
		}
		if ( ts == null ) {
			results_TimeSeries_AddTimeSeriesToResults ( htmlStart + (i + 1) + ") - Null time series from processor." + htmlEnd );
			continue;
		}
		else {
			// Have actual data to display.
			desc = ts.getDescription();
			alias = ts.getAlias();
			if ( !alias.equals("") ) {
				alias = alias + " - ";
			}
			if ( (desc == null) || (desc.length() == 0) ) {
				desc = ts.getIdentifier().getLocation();
			}
			date1 = ts.getDate1();
			date2 = ts.getDate2();
			String dateString = null;
			htmlStart2 = "";
			htmlEnd2 = "";
			if ( (date1 == null) || (date2 == null) ) {
			    dateString = " (NO DATA)";
			    htmlStart2 = htmlStart;
			    htmlEnd2 = htmlEnd;
			}
			else if ( !ts.hasData() ) {
			    dateString = " (" + ts.getDate1() + " to " + ts.getDate2() + " NO DATA)";
	            htmlStart2 = htmlStart;
	            htmlEnd2 = htmlEnd;
			}
			else {
			    dateString = " (" + ts.getDate1() + " to " + ts.getDate2() + ")";
			}
			results_TimeSeries_AddTimeSeriesToResults ( htmlStart2 + (i + 1) + ") " + alias +
			    desc + " - " + ts.getIdentifier() +	dateString + htmlEnd2 );
			// Determine whether the time series was programmatically selected in the commands.
			selected_boolean[i] = ts.isSelected();
		}
	}
	// If no time series are selected programmatically, then visually select all.
	// If any are selected, then visually select only the ones that are selected.
	// First determine the number that have been selected programmatically.
	int num_selected = 0;
	for ( int i = 0; i < size; i++ ) {
		if ( selected_boolean[i] ) {
			++num_selected;
		}
	}
	// Now create the list of indices to use for visually selecting.
	int [] selected = null;
	if ( num_selected == 0 ) {
		// All need to be selected in output.
		selected = new int[size];	// Whether visually selected.
		for ( int i = 0; i < size; i++ ) {
			selected[i] = i;
		}
	}
	else {
        // Select the time series of interest.
		selected = new int[num_selected];	// Whether visually selected.
		int selectedCount = 0;
		for ( int i = 0; i < size; i++ ) {
			if ( selected_boolean[i] ) {
				selected[selectedCount++] = i;
			}
		}
	}
	// Now actually select the time series in the visual output.
	this.__resultsTS_JList.setSelectedIndices ( selected );
	ui_UpdateStatus ( false );
	ui_UpdateStatusTextFields ( 1, routine, null, "Completed running commands.  Use Results and Tools menus.",
		TSToolConstants.STATUS_READY );
	// Make sure that the user is not waiting on the wait cursor.
	//JGUIUtil.setWaitCursor ( this, false );

	// TODO smalers 2010-08-09 Evaluate whether this fixes the problem and evaluate the approach.
	// Redraw the list because sometimes it gets out of sync with the UI.
	this.__resultsTS_JList.invalidate();

	// Disable or enable the template graph depending on whether the time series list is empty.
	if ( this.__resultsTSEnsembles_JListModel.getSize() > 0) {
		this.__resultsTSEnsemblesGraphTemplates_JButton.setEnabled(true);
		this.__resultsTSEnsemblesGraphTemplates_JComboBox.setEnabled(true);
	}
	else {
		this.__resultsTSEnsemblesGraphTemplates_JButton.setEnabled(false);
		this.__resultsTSEnsemblesGraphTemplates_JComboBox.setEnabled(false);
	}

	if ( this.__resultsTS_JListModel.getSize() > 0) {
		this.__resultsTSGraphTemplates_JButton.setEnabled(true);
		this.__resultsTSGraphTemplates_JComboBox.setEnabled(true);
	}
	else {
		this.__resultsTSGraphTemplates_JButton.setEnabled(false);
		this.__resultsTSGraphTemplates_JComboBox.setEnabled(false);
	}

	//Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsTimeSeries", "Leaving method.");
}

/**
Display the table results.
*/
private void uiAction_RunCommands_ShowResultsViews() {
    // Get the list of views from the processor.
    //Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsTables", "Entering method.");
    // Get the list of table identifiers from the processor.
    List<TimeSeriesView> view_List = commandProcessor_GetTimeSeriesViewResultsList();
    int size = 0;
    if ( view_List != null ) {
        size = view_List.size();
    }
    TimeSeriesView view;
    for ( int i = 0; i < size; i++ ) {
        view = view_List.get(i);
        results_Views_AddView ( view );
    }
    //Message.printStatus ( 2, "uiAction_RunCommands_ShowResultsTables", "Leaving method.");
}

/**
Run a command file, independent of what is shown in the UI.
This is essentially a way to do a batch run with a separate processor
*/
private void uiAction_RunCommandFile () {
	String routine = getClass().getSimpleName() + ".uiAction_RunCommandFile";
	// Select from the directory where the previous selection occurred.
	JFileChooser fc = JFileChooserFactory.createJFileChooser ( ui_GetDir_LastExternalCommandFileRun() );
	fc.setDialogTitle("Select " + IOUtil.getProgramName() + " Command File to Run");
	SimpleFileFilter sff = new SimpleFileFilter("TSTool", "TSTool Command File");
	fc.addChoosableFileFilter(sff);
	fc.setFileFilter(sff);
	if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
		// If the user approves a selection do the following.
		String directory = fc.getSelectedFile().getParent();
		String path = fc.getSelectedFile().getPath();
		ui_SetDir_LastExternalCommandFileRun(directory);
		// TODO smalers 2007-11-02 Put in thread - but need to figure out how to show completion.
		try {
			TSCommandFileRunner runner = new TSCommandFileRunner(
				this.__tsProcessor.getInitialPropList(),
				this.__tsProcessor.getPluginCommandClasses());
			JGUIUtil.setWaitCursor ( this, true );
			// Read the file.
			boolean runDiscoveryOnLoad = false; // No need for discovery since run independently.
			runner.readCommandFile ( path, runDiscoveryOnLoad );
			// Set the DMI information.
			HydroBaseDMI hbdmi = null;
			if ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() != null ) {
			    hbdmi = (HydroBaseDMI)TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy().getDMI();
			}
			commandProcessor_SetHydroBaseDMI ( runner.getProcessor(), hbdmi );
			commandProcessor_SetNWSRFSFS5FilesDMI ( runner.getProcessor(), TSTool_FS5Files.getInstance(this).getNwsrfsFS5FilesDMI() );
			// Now run the command file.
			Message.printStatus ( 1, routine, "Running external command file \"" + path + "\"" );
			runner.runCommands(null);
			Message.printStatus ( 1, routine, "Successfully processed command file \"" + path + "\"" );
			JGUIUtil.setWaitCursor ( this, false );
		}
		catch ( Exception e ) {
			JGUIUtil.setWaitCursor ( this, false );
			Message.printWarning ( 1, routine, "Error running command file \"" + path + "\"" );
			Message.printWarning ( 2, routine, e );
			JGUIUtil.setWaitCursor ( this, false );
		}
	}
}

//TODO smalers 2007-08-31 - need to enable/disable filters based on the list of time series that are selected.
/**
Save the current time series to the selected format.
The user picks the file and the format, via the chooser filter.
*/
private void uiAction_SaveTimeSeries () {
	JFileChooser fc = JFileChooserFactory.createJFileChooser( JGUIUtil.getLastFileDialogDirectory() );
	fc.setDialogTitle("Save Time Series (full period)");
	// Default, and always enabled.
	SimpleFileFilter datevalue_sff = null;
	datevalue_sff = new SimpleFileFilter( "dv", "DateValue Time Series File");
	fc.addChoosableFileFilter( datevalue_sff );
	fc.setFileFilter(datevalue_sff);
	// Add ESP Trace Ensemble only if enabled in the configuration.
	SimpleFileFilter esp_cs_sff = null;
	if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
		esp_cs_sff = new SimpleFileFilter( "CS","ESP Conditional Trace Ensemble File");
		fc.addChoosableFileFilter ( esp_cs_sff );
	}
	// Add NWS Card only if enabled in the configuration.
	FileFilter[] nwscardFilters = null;
	if ( this.__source_NWSCard_enabled ) {
		nwscardFilters = NWSCardTS.getFileFilters();
		for (int i = 0; i < nwscardFilters.length - 1; i++) {
			fc.addChoosableFileFilter(nwscardFilters[i]);
		}
	}
	// Add RiverWare only if enabled in the configuration.
	SimpleFileFilter riverware_sff = null;
	if ( this.__source_RiverWare_enabled ) {
		riverware_sff = new SimpleFileFilter("txt", "RiverWare Time Series Format File" );
		fc.addChoosableFileFilter( riverware_sff );
	}
	// Add SHEF only if enabled in the configuration.
	SimpleFileFilter shef_sff = null;
	if ( this.__source_SHEF_enabled ) {
		shef_sff = new SimpleFileFilter("shef", "SHEF .A Format File" );
		fc.addChoosableFileFilter( shef_sff );
	}
	// Add StateMod only if enabled in the configuration.
	SimpleFileFilter statemod_sff = null;
	if ( this.__source_StateMod_enabled ) {
		statemod_sff = new SimpleFileFilter("stm", "StateMod Time Series File" );
		fc.addChoosableFileFilter( statemod_sff );
	}
	// Add Summary always.
	SimpleFileFilter summary_sff=new SimpleFileFilter("txt","Summary File");
	fc.addChoosableFileFilter( summary_sff );
	if ( fc.showSaveDialog(this) != JFileChooser.APPROVE_OPTION ) {
		// Did not approve.
		return;
	}
	// If here, the file was selected for writing.
	String directory = fc.getSelectedFile().getParent();
	JGUIUtil.setLastFileDialogDirectory( directory );
	String path = fc.getSelectedFile().getPath();

	FileFilter ff = fc.getFileFilter();
	// TODO smalers - need to do this cleaner and perhaps let users pick some output options.  Do enforce the file extensions.
	if ( ff == datevalue_sff ) {
		uiAction_ExportTimeSeriesResults("-odatevalue", IOUtil.enforceFileExtension(path,"dv") );
	}
	else if ( ff == esp_cs_sff ) {
		uiAction_ExportTimeSeriesResults("-onwsrfsesptraceensemble",
		IOUtil.enforceFileExtension(path,"CS") );
	}
	else if ( ff == riverware_sff ) {
		// Don't know for sure what extension.
		uiAction_ExportTimeSeriesResults("-oriverware", path );
	}
	else if ( ff == shef_sff ) {
		// Don't know for sure what extension.
		uiAction_ExportTimeSeriesResults("-oshefa", path );
	}
	else if ( ff == statemod_sff ) {
		// Don't know for sure what extension.
		uiAction_ExportTimeSeriesResults("-ostatemod", path );
	}
	else if ( ff == summary_sff ) {
		uiAction_ExportTimeSeriesResults("-osummary", IOUtil.enforceFileExtension(path,"txt") );
	}
	else {
		for (int i = 0; i < nwscardFilters.length; i++) {
			if (ff == nwscardFilters[i]) {
				uiAction_ExportTimeSeriesResults("-onwscard", path);
				break;
			}
		}
	}
}

/**
Select all commands in the commands list.  This occurs in response to a user selecting a menu choice.
*/
private void uiAction_SelectAllCommands() {
	JGUIUtil.selectAll(ui_GetCommandJList());
	ui_UpdateStatus ( true );
}

/**
Select on the map the features that are shown in the time series list in the
upper right of the main TSTool interface and zoom to the selected features.
@exception Exception if there is an error showing the related time series features on the map.
*/
private void uiAction_SelectOnMap ()
throws Exception {
	String routine = getClass().getSimpleName() + ".selectOnMap";
	int size = this.__query_JWorksheet.getRowCount();	// To size the list.
	List<String> idlist = new ArrayList<>(size);
	Message.printStatus ( 1, routine, "Selecting and zooming to stations on map.  Please wait...");
	JGUIUtil.setWaitCursor(this, true);

	String selectedInputType = ui_GetSelectedInputType();
	String selectedDataType = ui_GetSelectedDataType();
	String selectedTimeStep = ui_GetSelectedTimeStep();

	// Get the list of layers to select from, and the attributes to use.
	// First read the file with the lookup of time series to layer information.

	// TODO smalers 2006-03-01
	// Currently read this each time because it is a small file and it helps in development to not restart.
	// However, in the future, change so that the file is read once.

	String filename = TSToolMain.getPropValue ( "TSTool.MapLayerLookupFile" );
	if ( filename == null ) {
		Message.printWarning ( 1, routine, "The TSTool.MapLayerLookupFile is not defined - cannot link map and time series." );
		return;
	}

	String full_filename = IOUtil.getPathUsingWorkingDir ( filename );
	if ( !IOUtil.fileExists(full_filename) ) {
		Message.printWarning ( 1, routine,
		"The map layer lookup file \"" + full_filename + "\" does not exist.  Cannot link map and time series." );
		return;
	}

	PropList props = new PropList ("");
	props.set ( "Delimiter=," );		// See existing prototype.
	props.set ( "CommentLineIndicator=#" );	// New - skip lines that start with this.
	props.set ( "TrimStrings=True" );	// If true, trim strings after reading.
	DataTable table = DataTable.parseFile ( full_filename, props );

	int tsize = 0;
	int TS_InputTypeCol_int = -1;
	int TS_DataTypeCol_int = -1;
	int TS_IntervalCol_int = -1;
	int Layer_NameCol_int = -1;
	int Layer_LocationCol_int = -1;
	int Layer_DataSourceCol_int = -1;
	int Layer_IntervalCol_int = -1;
	StringBuffer attributes = new StringBuffer();	// List of attribute names and values for queries.
	if ( table != null ) {
		tsize = table.getNumberOfRecords();

		TS_InputTypeCol_int = table.getFieldIndex ( "TS_InputType" );
		TS_DataTypeCol_int = table.getFieldIndex ( "TS_DataType" );
		TS_IntervalCol_int = table.getFieldIndex ( "TS_Interval" );
		Layer_NameCol_int = table.getFieldIndex ( "Layer_Name" );
		Layer_LocationCol_int = table.getFieldIndex ( "Layer_Location");
		Layer_DataSourceCol_int = table.getFieldIndex ( "Layer_DataSource");
		Message.printStatus ( 2, routine, "TimeSeriesLookup table for "+
		"map has columns...TS_InputType=" + TS_InputTypeCol_int +
		",TS_DataType=" + TS_DataTypeCol_int +
		",TS_Interval=" + TS_IntervalCol_int +
		",Layer_Name=" + Layer_NameCol_int +
		",Layer_Location=" + Layer_LocationCol_int +
		",Layer_DataSource=" + Layer_DataSourceCol_int );
	}

	List<String> layerlist = new ArrayList<>();	// List of layers to match features.
	List<String> mapidlist = new ArrayList<>();	// List of identifier attributes in map data to match features.
	String ts_inputtype, ts_datatype, ts_interval,
		layer_name, layer_location, layer_datasource = "",
		layer_interval = ""; // TSTool input to match against layers.
	TableRecord rec;
	if ( (TS_InputTypeCol_int >= 0) && (TS_DataTypeCol_int >= 0) &&
		(TS_IntervalCol_int >= 0) && (Layer_NameCol_int >= 0) &&
		(Layer_LocationCol_int >= 0) ) {
		// Have the necessary columns in the file to search for a matching layer.
		for ( int i = 0; i < tsize; i++ ) {
			rec = table.getRecord(i);
			ts_inputtype = (String)rec.getFieldValue(TS_InputTypeCol_int);
			ts_datatype = (String)rec.getFieldValue(TS_DataTypeCol_int);
			ts_interval = (String)rec.getFieldValue(TS_IntervalCol_int);
			layer_name = (String)rec.getFieldValue(Layer_NameCol_int);
			layer_location = (String)rec.getFieldValue(Layer_LocationCol_int);
			if ( Layer_DataSourceCol_int >= 0 ) {
				// Also include the data source in the query.
				layer_datasource = (String)rec.getFieldValue(Layer_DataSourceCol_int);
			}
			if ( Layer_IntervalCol_int >= 0 ) {
				// Also include the data interval in the query.
				layer_interval = (String)rec.getFieldValue( Layer_IntervalCol_int);
			}
			// Required fields.
			if (!ts_inputtype.equalsIgnoreCase(selectedInputType)){
				continue;
			}
			if ( !ts_datatype.equalsIgnoreCase(selectedDataType)){
				continue;
			}
			if ( !ts_interval.equalsIgnoreCase(selectedTimeStep)){
				continue;
			}
			// The layer matches the main input selections.
			// Save optional information that will be used for record by record comparisons.
			if ( Layer_DataSourceCol_int >= 0 ) {
				layer_datasource = (String)rec.getFieldValue(Layer_DataSourceCol_int);
			}
			if ( Layer_IntervalCol_int >= 0 ) {
				layer_interval = (String)rec.getFieldValue(Layer_IntervalCol_int);
			}
			// Save the layer to search and attribute(s) to match.
			layerlist.add ( layer_name );
			attributes.setLength(0);
			attributes.append ( layer_location );
			if ( (Layer_DataSourceCol_int >= 0) && (layer_datasource != null) && !layer_datasource.equals("") ) {
				attributes.append ( "," + layer_datasource );
			}
			if ( (Layer_IntervalCol_int >= 0) && (layer_interval != null) && !layer_interval.equals("") ) {
				attributes.append ( "," + layer_interval );
			}
			mapidlist.add ( attributes.toString() );
		}
	}

	// Determine the list of features (by ID, and optionally data source and interval) to select.
	// TODO smalers 2006-01-16 Need to make this more generic by using an interface to retrieve important time series data?

	// Get the worksheet of interest.

	int row = -1, location_col = -1, datasource_col = -1, interval_col = -1;
	if ( selectedInputType.equals ( TSToolConstants.INPUT_TYPE_HydroBase )) {
		if ( this.__query_TableModel instanceof TSTool_TS_TableModel){
			TSTool_TS_TableModel model = (TSTool_TS_TableModel)__query_TableModel;
			location_col = model.COL_ID;
			datasource_col = model.COL_DATA_SOURCE;
			interval_col = model.COL_TIME_STEP;
		}
		else if ( this.__query_TableModel instanceof TSTool_HydroBase_StationGeolocMeasType_TableModel){
		    TSTool_HydroBase_StationGeolocMeasType_TableModel model =
		        (TSTool_HydroBase_StationGeolocMeasType_TableModel)__query_TableModel;
			location_col = model.COL_ID;
			datasource_col = model.COL_DATA_SOURCE;
			interval_col = model.COL_TIME_STEP;
		}
        else if ( this.__query_TableModel instanceof TSTool_HydroBase_StructureGeolocStructMeasType_TableModel){
            TSTool_HydroBase_StructureGeolocStructMeasType_TableModel model =
                (TSTool_HydroBase_StructureGeolocStructMeasType_TableModel)__query_TableModel;
            location_col = model.COL_ID;
            datasource_col = model.COL_DATA_SOURCE;
            interval_col = model.COL_TIME_STEP;
        }
        else if ( this.__query_TableModel instanceof TSTool_HydroBase_GroundWaterWellsView_TableModel){
            TSTool_HydroBase_GroundWaterWellsView_TableModel model =
                (TSTool_HydroBase_GroundWaterWellsView_TableModel)__query_TableModel;
            location_col = model.COL_ID;
            datasource_col = model.COL_DATA_SOURCE;
            interval_col = model.COL_TIME_STEP;
        }
	}

	// Get the selected rows or all if none are selected.

	int rows[] = this.__query_JWorksheet.getSelectedRows();

	boolean all = false;	// Only process selected rows.
	if ( rows == null || rows.length == 0) {
		all = true;
		size = this.__query_JWorksheet.getRowCount();
	}
	else {
        size = rows.length;
	}

	// Loop through either all rows or selected rows to get the identifiers of interest.

	String id = null;
	for ( int i = 0; i < size; i++ ) {
		if (all) {
			// Process all rows.
			row = i;
		}
		else {
            // Process only selected rows.
			row = rows[i];
		}

		// Get the station identifier from the table model row.

		if ( (row >= 0) && (location_col >= 0) ) {
			// The identifier is always matched.
			id = (String)this.__query_TableModel.getValueAt( row, location_col );
			if ( (id == null) || (id.length() <= 0) ) {
				continue;
			}
			attributes.setLength(0);
			attributes.append ( id );
			// Optional fields that if non-null should be used.
			if ( (Layer_DataSourceCol_int >= 0) && (layer_datasource != null) && !layer_datasource.equals("") ) {
				attributes.append ( "," + (String)this.__query_TableModel.getValueAt( row, datasource_col ) );
			}
			if ( (Layer_IntervalCol_int >= 0) && (layer_interval != null) && !layer_interval.equals("") ) {
				attributes.append ( "," + (String)this.__query_TableModel.getValueAt( row,interval_col ) );
			}
			// Add to the list to match.
			idlist.add ( attributes.toString() );
		}
	}

	// Select the features, specifying the layers and features of interest
	// corresponding to the currently selected input type, data type, and interval.
	// Zoom to the selected shapes.
	PropList select_props = new PropList ( "search" );
	select_props.set ( "ZoomToSelected=True" );
	Message.printStatus ( 2, routine, "Selecting features..." );
	Message.printStatus ( 2, routine, "LayerList=" + layerlist );
	Message.printStatus ( 2, routine, "AttributeList=" + mapidlist );
	Message.printStatus ( 2, routine, "IDList=" + idlist );
	List<GeoRecord> matching_features = __geoview_JFrame.getGeoViewJPanel().selectLayerFeatures(
			layerlist,	// Layers to search.
			mapidlist,	// Attributes to use to compare to the identifiers.
			idlist,		// Identifiers to find.
			select_props );	// Properties to control search/select.
	int matches = 0;
	if ( matching_features != null ) {
		matches = matching_features.size();
	}
	if (matches == 0) {
		Message.printWarning ( 1, routine,
		"No matching features were found in map data.\n" +
		"This may be because the location data are incomplete or\n" +
		"because no suitable data layers are being used.");
	}
	else if ( matches != idlist.size() ) {
		Message.printWarning ( 1, routine,
		"" + matches + " matching features out of " + idlist.size()+
		" records were found in map data.\n" +
		"This may be because of incomplete location data.");
	}
    //__statusJTextField.setText("Map is zoomed to selected stations.  Ready.");
	JGUIUtil.setWaitCursor(this, false);
	idlist = null;
}

/**
Display the status of the selected command(s).
*/
private void uiAction_ShowCommandStatus() {
  SwingUtilities.invokeLater(new Runnable() {
    public void run() {
      try {
        String status = uiAction_ShowCommandStatus_GetCommandsStatus();

        // Display and center on the TSTool UI.
        HTMLViewer hTMLViewer = new HTMLViewer(Message.getTopLevel());
        hTMLViewer.setTitle ( "TSTool" + ui_GetTitleMod() + " - Command Status" );
        hTMLViewer.setHTML(status);
        hTMLViewer.setSize(750,600);
        hTMLViewer.setVisible(true);
      }
      catch(Throwable t){
        Message.printWarning(1, "uiAction_ShowCommandStatus", "Problem showing Command status (" + t + ").");
        String routine = "TSTool_JFrame.showCommandStatus";
        Message.printWarning(3, routine, t);
      }
    }
  });
}

/**
Gets Commands status in html - this is currently only a helper for the above method.
Rename if it will be used generically.
@return command status in HTML format
*/
private String uiAction_ShowCommandStatus_GetCommandsStatus() {
    List<Command> commands = commandList_GetCommandsBasedOnUI();
    return CommandStatusUtil.getHTMLStatusReport(commands);
}

/**
Show the datastores.
*/
private void uiAction_ShowDataStores () {
    try {
        new DataStores_JFrame ( "Datastores", this, this.__tsProcessor.getDataStores(), this.datastoreSubstituteList );
    }
    catch ( Exception e ) {
		String routine = getClass().getSimpleName() + "uiAction_ShowDataStores";
        Message.printWarning ( 1, routine, "Error displaying datastores (" + e + ")." );
    }
}

/**
Show the data units.
*/
private void uiAction_ShowDataUnits () {
    String routine = getClass().getSimpleName() + "uiAction_ShowDataUnits";
    try {
        new DataUnits_JFrame ( "Data Units", this, DataUnits.getUnitsData() );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine, "Error displaying data units (" + e + ")." );
    }
}

/**
Show the Help About dialog in response to a user selecting a menu.
*/
private void uiAction_ShowHelpAbout () {
    new HelpAboutJDialog ( this, "About TSTool",
    "TSTool - Time Series Tool " + IOUtil.getProgramVersion() + "\n" +
    " \n" +
    "TSTool is a part of Colorado's Decision Support Systems (CDSS)\n" +
    "Copyright (C) 1997-2024 Colorado Department of Natural Resources\n" +
    " \n" +
    "TSTool is free software:  you can redistribute it and/or modify\n" +
    "    it under the terms of the GNU General Public License as published by\n" +
    "    the Free Software Foundation, either version 3 of the License, or\n" +
    "    (at your option) any later version.\n" +
    " \n" +
    "TSTool is distributed in the hope that it will be useful,\n" +
    "    but WITHOUT ANY WARRANTY; without even the implied warranty of\n" +
    "    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n" +
    "    GNU General Public License for more details.\n" +
    " \n" +
    "You should have received a copy of the GNU General Public License\n" +
    "    along with TSTool.  If not, see <https://www.gnu.org/licenses/>.\n" +
    " \n" +
    "Developed by the Open Water Foundation\n" +
    "Funded by:\n" +
    "Colorado Division of Water Resources\n" +
    "Colorado Water Conservation Board\n" +
    "and others\n" +
    "Send questions and comments to:\n" +
    "steve.malers@openwaterfoundation.org or\n" +
    "DNR_OpenCDSS@state.co.us\n", true );
}

/**
Show the properties for a table.
*/
private void uiAction_ShowNetworkProperties () {
    String routine = getClass().getSimpleName() + "uiAction_ShowNetworkProperties";
    try {
        // Simple text display of network properties.
        PropList reportProp = new PropList ("Network Properties");
        reportProp.set ( "TotalWidth", "600" );
        reportProp.set ( "TotalHeight", "600" );
        reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "DisplaySize", "11" );
        reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "PrintSize", "7" );
        reportProp.set ( "Title", "Network Properties" );
        List<String> v = new ArrayList<>();
        // Get the network of interest.
        if ( this.__resultsNetworks_JList.getModel().getSize() > 0 ) {
            // If something is selected, show properties for the selected.
        	// Otherwise, show properties for all.
        	// TODO smalers 2017-05-31 Add intelligence to select based on mouse click?
            int [] sel = this.__resultsNetworks_JList.getSelectedIndices();
            if ( sel.length == 0 ) {
                // Process all.
                sel = new int[this.__resultsNetworks_JList.getModel().getSize()];
                for ( int i = 0; i < sel.length; i++ ) {
                    sel[i] = i;
                }
            }
            for ( int i = 0; i < sel.length; i++ ) {
                // TODO smalers 2012-10-15 Evaluate putting this in DataTable class for general use.
                String displayString = this.__resultsNetworks_JList.getModel().getElementAt(sel[i]);
                String networkId = uiAction_ShowResultsTable_GetTableID ( displayString );
                NodeNetwork network = commandProcessor_GetNetwork ( networkId );
                v.add ( "" );
                v.add ( "Network \"" + network.getNetworkId() + "\" properties:" );
                v.add ( "Network ID = " + networkId );
                v.add ( "Network name = " + network.getNetworkName() );
                v.add ( "Network nodes are listed below (most downstream to most upstream):" );
                if ( network instanceof HydrologyNodeNetwork ) {
                	HydrologyNodeNetwork hnetwork = (HydrologyNodeNetwork)network;
                	// TODO smalers 2017-05-31 need to evaluate how to get indentation working.
                	boolean doIndent = false;
                	if ( doIndent ) {
                		v.addAll(hnetwork.createIndentedRiverNetworkStrings());
                	}
                	else {
	                	// Start at the bottom and navigate the network to output basic information about the network.
	                	int count = 0;
	                	for ( HydrologyNode node = hnetwork.getMostUpstreamNode(); ; node = HydrologyNodeNetwork.getDownstreamNode(node, HydrologyNodeNetwork.POSITION_COMPUTATIONAL) ) {
	                		if ( node == null ) {
	                			break;
	                		}
	                   		++count;
	                   		HydrologyNode downstreamNode = node.getDownstreamNode();
	                   		String downstreamNodeId = "";
	                   		if ( downstreamNode != null ) {
	                   			downstreamNodeId = downstreamNode.getCommonID();
	                   		}
	                		v.add ( "" + count + " Node ID = \"" + node.getCommonID() + "\", Node Name = \"" + node.getDescription() + "\", Downstream node = \"" + downstreamNodeId + "\"");
	                		if ( node.getType() == HydrologyNode.NODE_TYPE_END ) {
	                			break;
	                		}
	                	}
                	}
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
Show the properties for an object.
*/
private void uiAction_ShowObjectProperties () {
    String routine = getClass().getSimpleName() + "uiAction_ShowObjectProperties";
    try {
        // Simple text display of object properties.
        PropList reportProp = new PropList ("Object Properties");
        reportProp.set ( "TotalWidth", "600" );
        reportProp.set ( "TotalHeight", "600" );
        reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "DisplaySize", "11" );
        reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "PrintSize", "7" );
        reportProp.set ( "Title", "Object Properties" );
        List<String> v = new ArrayList<>();
        // Get the object of interest.
        if ( this.__resultsObjects_JList.getModel().getSize() > 0 ) {
            // If something is selected, show properties for the selected.  Otherwise, show properties for all.
            // TODO smalers 2012-10-12 Add intelligence to select based on mouse click?
            int [] sel = this.__resultsObjects_JList.getSelectedIndices();
            if ( sel.length == 0 ) {
                // Process all.
                sel = new int[this.__resultsObjects_JList.getModel().getSize()];
                for ( int i = 0; i < sel.length; i++ ) {
                    sel[i] = i;
                }
            }
            for ( int i = 0; i < sel.length; i++ ) {
                // TODO smalers 2012-10-15 Evaluate putting this in JSON class for general use.
                String displayString = this.__resultsObjects_JList.getModel().getElementAt(sel[i]);
                String objectId = uiAction_ShowResultsObject_GetObjectID ( displayString );
                JSONObject object = commandProcessor_GetObject ( objectId );
                v.add ( "" );
                v.add ( "Object \"" + object.getObjectID() + "\" properties:" );
               	v.add ( "  Currently nothing to show - view the object contents by left-clicking on the object ID." );
            }
        }
        // Use so that the dialog is displayed on same screen as TSTool main GUI.
        reportProp.setUsingObject ( "ParentUIComponent", this );
        new ReportJFrame ( v, reportProp );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine, "Error displaying object properties (" + e + ")." );
        Message.printWarning ( 3, routine, e );
    }
}

/**
Show the properties for the current commands run (processor).
*/
private void uiAction_ShowProperties_CommandsRun () {
	PropList reportProp = new PropList ("ReportJFrame.props");
	// Too big (make this big when we have more stuff).
	//reportProp.set ( "TotalWidth", "750" );
	//reportProp.set ( "TotalHeight", "550" );
	reportProp.set ( "TotalWidth", "800" );
	reportProp.set ( "TotalHeight", "500" );
	reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
	reportProp.set ( "DisplaySize", "11" );
	reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
	reportProp.set ( "PrintSize", "7" );
	reportProp.set ( "Title", "TSTool Commands Run Properties" );
	List<String> v = new ArrayList<> ( 4 );
	v.add ( "Properties from the last commands run." );
	v.add ( "Note that property values are as of the time the window is opened." );
	v.add ( "Properties are set as defaults initially and change value when a command is processed." );
	v.add ( "" );

	String s1 = "", s2 = "";
	// Initial and current working directory.
	v.add ( "Working directory (from user.dir system property):  " + System.getProperty ( "user.dir" ) );
	v.add ( "Initial working directory (internal to TSTool):  " + this.__tsProcessor.getInitialWorkingDir() );
	try {
	    v.add ( "Current working directory ${WorkingDir}:  " + this.__tsProcessor.getPropContents("WorkingDir") );
	}
	catch ( Exception e ) {
	    v.add ( "Current working directory ${WorkingDir}:  Unknown" );
	}
    try {
        v.add ( "Software install directory ${InstallDir}:  " + this.__tsProcessor.getPropContents("InstallDir") );
    }
    catch ( Exception e ) {
        v.add ( "Software install directory ${InstallDir}:  Unknown" );
    }
    try {
        v.add ( "Software install directory URL ${InstallDirURL}:  " + this.__tsProcessor.getPropContents("InstallDirURL") );
    }
    catch ( Exception e ) {
        v.add ( "Software install directory URL ${InstallDirURL}:  Unknown" );
    }
	// Whether running and cancel requested.
	v.add ( "Are commands running:  " + __tsProcessor.getIsRunning() );
	v.add ( "Has cancel been requested (and is pending):  " + this.__tsProcessor.getCancelProcessingRequested() );
	v.add ( "Total number of failure/warning messages from run:  " +
	    CommandStatusUtil.getLogRecordListFromCommands(__tsProcessor.getCommands(), CommandPhaseType.RUN ).size());

	// Input period.
	DateTime date1 = commandProcessor_GetInputStart();
	if ( date1 == null ) {
		s1 = "NOT SPECIFIED (use all available data)";
	}
	else {
        s1 = date1.toString();
	}
	DateTime date2 = commandProcessor_GetInputEnd();
	if ( date2 == null ) {
		s2 = "NOT SPECIFIED (use all available data)";
	}
	else {
	    s2 = date2.toString();
	}
	v.add ( "Input (query/read) start: " + s1 );
	v.add ( "Input (query/read) end:   " + s2 );
	// Output period.
	date1 = commandProcessor_GetOutputStart();
	if ( date1 == null ) {
		s1 = "NOT SPECIFIED (output all available data)";
	}
	else {
        s1 = date1.toString();
	}
	date2 = commandProcessor_GetOutputEnd();
	if ( date2 == null ) {
		s2 = "NOT SPECIFIED (output all available data)";
	}
	else {
        s2 = date2.toString();
	}
	v.add ( "Output period start: " + s1 );
	v.add ( "Output period end:   " + s2 );
	// Auto-extend period.
	v.add ( "Automatically extend period to output period during read: " +
		commandProcessor_GetAutoExtendPeriod () );
	// Include missing TS automatically.
	v.add ( "Include missing TS automatically: " + commandProcessor_GetIncludeMissingTS() );
	if ( this.__source_HydroBase_enabled ) {
		v.add ( "" );
		List<HydroBaseDMI> dmis = commandProcessor_GetHydroBaseDMIList();
		if ( (dmis == null) || (dmis.size() == 0) ) {
			v.add ( "No HydroBase connections are open for the command processor." );
		}
		else {
			int size = dmis.size();
			for ( int i = 0; i < size; i++ ) {
				v.add ( "Command processor HydroBase connection information:" );
				try {
					StringUtil.addListToStringList ( v, StringUtil.toList( dmis.get(i).getVersionComments() ) );
				}
				catch ( Exception e ) {
					// Ignore for now.
				}
			}
		}
	}
	reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
	new ReportJFrame ( v, reportProp );
}

/**
Show properties from the TSTool session.
*/
private void uiAction_ShowProperties_TSToolSession ( HydroBaseDataStore dataStore ) {
   HydroBaseDMI hbdmi = null;
    if ( dataStore != null ) {
        hbdmi = (HydroBaseDMI)dataStore.getDMI();
    }
    // Simple text display of session data, including last command file that was read.
    // Put here where in the past information was shown in labels.
    // Now need the label space for other information.
    PropList reportProp = new PropList ("ReportJFrame.props");
    // Too big (make this big when we have more stuff).
    //reportProp.set ( "TotalWidth", "750" );
    //reportProp.set ( "TotalHeight", "550" );
    reportProp.set ( "TotalWidth", "600" );
    reportProp.set ( "TotalHeight", "300" );
    reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
    reportProp.set ( "DisplaySize", "11" );
    reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
    reportProp.set ( "PrintSize", "7" );
    reportProp.set ( "Title", "TSTool Session Properties" );
    List<String> v = new ArrayList<>( 4 );
    v.add ( "TSTool Session Properties" );
    v.add ( "" );
    if ( this.__commandFileName == null ) {
        v.add ( "No command file has been read or saved." );
    }
    else {
        v.add ( "Last command file read/saved: \"" + __commandFileName + "\"" );
    }
    v.add ( "Working directory (from user.dir system property):  " + System.getProperty ( "user.dir" ) );
    v.add ( "Current working directory (internal to TSTool):  " + IOUtil.getProgramWorkingDir() );
    v.add ( "Run commands in thread (internal to TSTool):  " + ui_Property_RunCommandProcessorInThread() );
    // List open database information.
    if ( this.__source_HydroBase_enabled ) {
        v.add ( "" );
        if ( TSTool_HydroBase.getInstance(this).getHydroBaseDataStoreLegacy() == null ) {
            v.add ( "GUI HydroBase connection not defined.");
        }
        else {
            v.add ( "GUI HydroBase connection information:" );
            try {
                StringUtil.addListToStringList ( v, StringUtil.toList( hbdmi.getVersionComments() ) );
            }
            catch ( Exception e ) {
                v.add ( "Error getting HydroBase connection information (" + e + ")." );
            }
        }
    }
    // List enabled data types.
    v.add ( "" );
    v.add ( "Input types and whether enabled:" );
    v.add ( "" );
    if ( this.__source_DateValue_enabled ) {
        v.add ( "DateValue input type is enabled" );
    }
    else {
        v.add ( "DateValue input type is not enabled" );
    }
    if ( this.__source_DelftFews_enabled ) {
        v.add ( "DELFT FEWS input type is enabled" );
    }
    else {
        v.add ( "DELFT FEWS input type is not enabled" );
    }
    if ( __source_HECDSS_enabled ) {
        v.add ( "HEC-DSS input type is enabled" );
    }
    else {
        v.add ( "HEC-DSS input type is not enabled");
    }
    if ( this.__source_HydroBase_enabled ) {
        v.add ( "HydroBase input type is enabled" );
    }
    else {
        v.add ( "HydroBase input type is not enabled" );
    }
    if ( this.__source_MODSIM_enabled ) {
        v.add ( "MODSIM input type is enabled" );
    }
    else {
        v.add ( "MODSIM input type is not enabled" );
    }
    if ( this.__source_NWSCard_enabled  ) {
        v.add ( "NWSCARD input type is enabled" );
    }
    else {
        v.add ( "NWSCARD input type is not enabled" );
    }
    if ( this.__source_NWSRFS_FS5Files_enabled ) {
        v.add ( "NWSRFS FS5Files input type is enabled");
    }
    else {
        v.add ( "NWSRFS FS5Files input type is not enabled" );
    }
    if ( this.__source_NWSRFS_ESPTraceEnsemble_enabled ) {
        v.add ( "NWSRFS_ESPTraceEnsemble input type is enabled" );
    }
    else {
        v.add ( "NWSRFS_ESPTraceEnsemble input type is not enabled" );
    }
    if ( this.__source_RCCACIS_enabled ) {
        v.add ( "RCC ACIS datastore is enabled" );
    }
    else {
        v.add ( "RCC ACIS datastore is not enabled");
    }
    if ( this.__source_ReclamationHDB_enabled ) {
        v.add ( "ReclamationHDB datastore is enabled" );
    }
    else {
        v.add ( "ReclamationHDB datastore is not enabled");
    }
    if ( this.__source_ReclamationPisces_enabled ) {
        v.add ( "ReclamationPisces datastore is enabled" );
    }
    else {
        v.add ( "ReclamationPisces datastore is not enabled");
    }
    if ( this.__source_RiverWare_enabled ) {
        v.add ( "RiverWare input type is enabled" );
    }
    else {
        v.add ( "RiverWare input type is not enabled");
    }
    if ( this.__source_SHEF_enabled ) {
        v.add ( "SHEF input type is enabled" );
    }
    else {
        v.add ( "SHEF input type is not enabled");
    }
    if ( this.__source_StateCU_enabled ) {
        v.add ( "StateCU input type is enabled" );
    }
    else {
        v.add ( "StateCU input type is not enabled");
    }
    if ( this.__source_StateCUB_enabled ) {
        v.add ( "StateCUB input type is enabled" );
    }
    else {
        v.add ( "StateCUB input type is not enabled");
    }
    if ( this.__source_StateMod_enabled ) {
        v.add ( "StateMod input type is enabled" );
    }
    else {
        v.add ( "StateMod input type is not enabled");
    }
    if ( this.__source_StateModB_enabled ) {
        v.add ( "StateModB input type is enabled" );
    }
    else {
        v.add ( "StateModB input type is not enabled");
    }
    if ( this.__source_UsgsNwisRdb_enabled ) {
        v.add ( "UsgsNwisRdb input type is enabled" );
    }
    else {
        v.add ( "UsgsNwisRdb input type is not enabled");
    }

    v.add ( "" );
    v.add ( "Environment properties:" );
    v.add ( "" );
    v.add ( "Software installation directory = \"" + IOUtil.getApplicationHomeDir() + "\"" );
    v.add ( "Global working directory = \"" + IOUtil.getProgramWorkingDir() + "\"" );
    reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
    new ReportJFrame ( v, reportProp );
}

/**
Show an object as formatted JSON text.
@param selected table display string for the table to display "#) TableID - other information".
*/
private void uiAction_ShowResultsObject ( String selected ) {
    String routine = getClass().getSimpleName() + ".uiAction_ShowResultsObject";
    if ( selected == null ) {
        // May be the result of some UI event.
        return;
    }
    // Display the object.
    String objectId = "";
    try {
        objectId = uiAction_ShowResultsObject_GetObjectID ( selected );
        // If column widths are set, they are used.
        JSONObject object = commandProcessor_GetObject ( objectId );
        if ( object == null ) {
            Message.printWarning (1, routine, "Unable to get object \"" + objectId + "\" from processor to view." );
        }
        else {
        	// TODO smalers 2022-10-15 need to format as pretty JSON.
        	// Simple text display of object properties.
        	PropList reportProp = new PropList ("Object");
        	reportProp.set ( "TotalWidth", "600" );
        	reportProp.set ( "TotalHeight", "600" );
        	reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
        	reportProp.set ( "DisplaySize", "11" );
        	reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
        	reportProp.set ( "PrintSize", "7" );
        	reportProp.set ( "Title", "Object - " + objectId );
        	List<String> lines = new ArrayList<>();
        	// Format using Jackson.
        	ObjectMapper mapper = new ObjectMapper();
        	// Get the default pretty printer and set the indent:
        	// - use two spaces to indent because
        	DefaultPrettyPrinter.Indenter indenter = new DefaultIndenter("  ", DefaultIndenter.SYS_LF);
        	DefaultPrettyPrinter printer = new DefaultPrettyPrinter();
        	printer.indentObjectsWith(indenter);
        	printer.indentArraysWith(indenter);
        	if ( object.getObjectMap() != null ) {
        		String json = mapper.writer(printer).writeValueAsString(object.getObjectMap());
            	lines.add ( json );
        	}
        	else if ( object.getObjectArray() != null ) {
        		String json = mapper.writer(printer).writeValueAsString(object.getObjectArray());
            	lines.add ( json );
        	}
        	// Use so that the dialog is displayed on same screen as TSTool main GUI.
        	reportProp.setUsingObject ( "ParentUIComponent", this );
        	new ReportJFrame ( lines, reportProp );
        }
    }
    catch (Exception e2) {
        Message.printWarning (1, routine, "Unable to view object \"" + objectId + "\"" );
    }
}

/**
Helper method to get the object identifier from the displayed object results list string.
Currently only the object ID is displayed as follows:
  1) ObjectID
@param objectDisplayString the full object display string shown in the UI list
@return the object ID
*/
private String uiAction_ShowResultsObject_GetObjectID ( String objectDisplayString ) {
    // Determine the object identifier from the displayed string,
	// which will may have at least one dash, but table identifiers may also have a dash.
    if ( objectDisplayString == null ) {
        return null;
    }
    int pos1 = objectDisplayString.indexOf( ")"); // Count at start of string.
    int pos2 = objectDisplayString.indexOf( " -"); // Break between ID.
    String objectId = null;
    if ( pos2 >= 0 ) {
    	objectId = objectDisplayString.substring(pos1+1,pos2).trim();
    }
    else {
    	objectId = objectDisplayString.substring(pos1+1).trim();
    }
    return objectId;
}

/**
Show an output file using the appropriate display software/editor.
@param selected Path to selected output file.
*/
private void uiAction_ShowResultsOutputFile ( String selected ) {
    String routine = getClass().getSimpleName() + ".uiAction_ShowResultsOutputFile";
    if ( selected == null ) {
        // May be the result of some UI event.
        return;
    }
    // Display the selected file.
    if ( !( new File( selected ).isAbsolute() ) ) {
        selected = IOUtil.getPathUsingWorkingDir( selected );
    }
    // If the extension is "tstool", prompt to see if should load the command file:
    // - this may be the case if a command file is expanded or created for regression testing
    if ( IOUtil.getFileExtension(selected).equalsIgnoreCase("tstool") ) {
		int x = new ResponseJDialog ( this, "Open TSTool command file?",
			"Open the TSTool command file in this TSTool session?",
			ResponseJDialog.YES|ResponseJDialog.NO).response();
		if ( x == ResponseJDialog.YES ) {
			uiAction_OpenCommandFile(selected, true);
			return;
		}
		// Else, will try to open below using operating system command, default, text editor, etc.
    }
    // Try the application that is configured by the operating system based on file extension.
    try {
        Desktop desktop = Desktop.getDesktop();
        desktop.open ( new File(selected) );
    }
    catch ( Exception e ) {
        // Else display as text (will show up in courier fixed width font, which looks better than the html browser).
        Message.printWarning ( 3, routine, "Unable to view file \"" + selected + "\" using desktop default (" + e + ")." );
        Message.printWarning ( 3, routine, e );
        try {
            if ( IOUtil.isUNIXMachine() ) {
                // Use a built in viewer (may be slow).
                PropList reportProp = new PropList ("Output File");
                reportProp.set ( "TotalWidth", "800" );
                reportProp.set ( "TotalHeight", "600" );
                reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
                reportProp.set ( "DisplaySize", "11" );
                reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
                reportProp.set ( "PrintSize", "7" );
                reportProp.set ( "Title", selected );
                reportProp.set ( "URL", selected );
                reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
                new ReportJFrame ( null, reportProp );
            }
            else {
                // Rely on Notepad on Windows.
            	// TODO smalers 2021-07-29 would be nice to determine the default application for "txt" file and use that.
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
        // If column widths are set, they are used.
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
    // Determine the table identifier from the displayed string,
	// which will always have at least one dash, but table identifiers may also have a dash
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
        reportProp.set ( "DisplayFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "DisplaySize", "11" );
        reportProp.set ( "PrintFont", TSToolConstants.FIXED_WIDTH_FONT );
        reportProp.set ( "PrintSize", "7" );
        reportProp.set ( "Title", "Table Properties" );
        List<String> v = new ArrayList<>();
        // Get the table of interest.
        if ( __resultsTables_JList.getModel().getSize() > 0 ) {
            // If something is selected, show properties for the selected.  Otherwise, show properties for all.
            // TODO smalers 2012-10-12 Add intelligence to select based on mouse click?
            int [] sel = this.__resultsTables_JList.getSelectedIndices();
            if ( sel.length == 0 ) {
                // Process all.
                sel = new int[this.__resultsTables_JList.getModel().getSize()];
                for ( int i = 0; i < sel.length; i++ ) {
                    sel[i] = i;
                }
            }
            for ( int i = 0; i < sel.length; i++ ) {
                // TODO smalers 2012-10-15 Evaluate putting this in DataTable class for general use.
                String displayString = this.__resultsTables_JList.getModel().getElementAt(sel[i]);
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
                	if ( t.getFieldDataType(ifld) == TableField.DATA_TYPE_DATETIME ) {
                		// TODO smalers 2022-05-06 need to show DateTime column precision.
                		b.append(" width=" + t.getFieldWidth(ifld) + " precision=" + t.getFieldPrecision(ifld) );
                	}
                	else {
                		b.append(" width=" + t.getFieldWidth(ifld) + " precision=" + t.getFieldPrecision(ifld) );
                	}
                	v.add(b.toString());
                }
            }
        }
        reportProp.setUsingObject ( "ParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI
        new ReportJFrame ( v, reportProp );
    }
    catch ( Exception e ) {
        Message.printWarning ( 1, routine, "Error displaying table properties (" + e + ")." );
    }
}

/**
Method to run test code.  This is usually accessible only when running with the -test command line option.
@exception Exception if there is an error.
*/
private void uiAction_Test ()
throws Exception {
	String routine = getClass().getSimpleName() + ".test";
	int test_num = 9;
	Message.printStatus ( 2, routine, "Executing test " + test_num );
}

/**
Fill in appropriate selections for the data type modifier choices based on
the currently selected input data source, data type and time step.
*/
private void uiAction_TimeStepChoiceClicked() {
	String rtn = getClass().getSimpleName() + ".uiAction_TimeStepChoiceClicked";
	if ( (this.__inputType_JComboBox == null) || (this.__dataType_JComboBox == null) || (this.__timeStep_JComboBox == null) ) {
		// GUI still initializing.
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, rtn, "Time step has been selected but the GUI is not initialized." );
		}
		return;
	}
	String selectedTimeStep = ui_GetSelectedTimeStep();
	if ( selectedTimeStep == null ) {
		// Apparently this happens when setData() or similar is called on the JComboBox, and before select() is called.
		if ( Message.isDebugOn ) {
			Message.printDebug ( 1, rtn, "Time step has been selected:  null (select is ignored)" );
		}
		return;
	}
	if ( Message.isDebugOn ) {
		Message.printStatus ( 2, rtn, "Time step has been selected:  \"" + selectedTimeStep + "\"" );
	}
	// Show the input filters that are appropriate for data time and timestep choices.
	ui_SetInputFilterForSelections();
}

/**
Transfer all the time series from the query results to the command List.
*/
private void uiAction_TransferAllQueryResultsToCommandList() {
	String routine = getClass().getSimpleName() + ".uiAction_TransferAllQueryResultsToCommandList";

	int nrows = this.__query_TableModel.getRowCount();
	Message.printStatus ( 1, routine, "Transferring all time series to commands (" + nrows + " in list)..." );
	JGUIUtil.setWaitCursor ( this, true );
	int iend = nrows - 1;
	ui_SetIgnoreListSelectionEvent ( true ); // To increase performance during transfer.
	ui_SetIgnoreItemEvent ( true );	// To increase performance.
	int numInserted = 0;
	for ( int i = 0; i < nrows; i++ ) {
		// Only force the GUI state to be updated if the last item.
		if ( i == iend ) {
			ui_SetIgnoreListSelectionEvent ( false );
			this.__ignoreItemEvent = false;
			numInserted += queryResultsList_TransferOneTSFromQueryResultsListToCommandList ( i, true, numInserted );
		}
		else {
		    numInserted += queryResultsList_TransferOneTSFromQueryResultsListToCommandList ( i, false, numInserted );
		}
	}
	ui_SetIgnoreListSelectionEvent ( false );
	ui_SetIgnoreItemEvent ( false );
	JGUIUtil.setWaitCursor ( this, false );

	Message.printStatus ( 1, routine, "Selected all time series." );
}

/**
Transfer selected time series from the query results to the command List.
*/
private void uiAction_TransferSelectedQueryResultsToCommandList () {
	String routine = getClass().getSimpleName() + ".uiAction_TransferSelectedQueryResultsToCommandList";

	int nrows = this.__query_JWorksheet.getSelectedRowCount();
	Message.printStatus ( 1, routine, "Transferring selected time series to commands (" + nrows + " in list)..." );
	int [] selected = this.__query_JWorksheet.getSelectedRows();
	int iend = nrows - 1;
	int numInserted = 0;
	for ( int i = 0; i < nrows; i++ ) {
		// Only update the GUI state if transferring the last command.
		if ( i == iend ) {
			numInserted += queryResultsList_TransferOneTSFromQueryResultsListToCommandList ( selected[i], true, numInserted );
		}
		else {
		    numInserted += queryResultsList_TransferOneTSFromQueryResultsListToCommandList ( selected[i], false, numInserted );
		}
	}
	Message.printStatus ( 1, routine, "Transferred selected time series." );
}

/**
 * Show the difference between the current commands and the command file that is saved on disk.
 */
private void uiAction_ViewCommandFileDiff () {
	String diffProgram = uiAction_ViewCommandFileDiff_GetDiffProgram();
	if ( diffProgram != null ) {
		// Diff program exists so save a temporary file with UI commands and then compare with file version.
		// Run the diff program on the two files.
		String file1Path = this.__commandFileName;
		if ( file1Path == null ) {
	         new ResponseJDialog ( this, IOUtil.getProgramName(),
                  "No command file was previously read or saved.  The commands being edited are new.",
                  ResponseJDialog.OK).response();
	         return;
		}
		String tempFolder = System.getProperty("java.io.tmpdir");
		String file2Path = null;
		if ( this.__commandsDirty ) {
			// Write the UI commands to a temporary file.
			file2Path = tempFolder + File.separator + "TSTool-commands-from-UI.tstool";
			try {
				uiAction_WriteCommandFile_Helper(file2Path, false);
			}
			catch ( Exception e ) {
				Message.printWarning(1, "", "Error saving commands to temporary file for diff (" + e + ")" );
				return;
			}
		}
		else {
			// Can compare the existing commands file.
			file2Path = this.__commandFileName;
		}
		// Run the diff program.
		String [] programAndArgsList = { diffProgram, file1Path, file2Path };
		try {
			ProcessManager pm = new ProcessManager (
				programAndArgsList,
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
 * Get the path to the diff program to used for file comparisons
 * @return path for the diff program
 */
private String uiAction_ViewCommandFileDiff_GetDiffProgram () {
	// If the diff tool is not configured, provide information:
	// - handle generic property name and versions for the operating system
	// - the DiffProgram property can be a comma-separated list of paths to program to run,
	//   or program name without path to find in the PATH
	Prop prop = IOUtil.getProp("DiffProgram");
	String diffProgram = null;
	if ( prop != null ) {
		diffProgram = prop.getValue();
	}
	if ( IOUtil.isUNIXMachine() ) {
		prop = IOUtil.getProp("DiffProgram.Linux");
		if ( prop != null ) {
			diffProgram = prop.getValue();
		}
	}
	else {
		prop = IOUtil.getProp("DiffProgram.Windows");
		if ( prop != null ) {
			diffProgram = prop.getValue();
		}
	}
	if ( diffProgram == null ) {
         new ResponseJDialog ( this, IOUtil.getProgramName(),
             "The visual diff program has not been configured in the TSTool.cfg file.\n" +
             "Define the \"DiffProgram\" (or \"DiffProgram.Windows\" and \"DiffProgram.Linux\") property\n" +
             "as the path to a visual diff program, for example:\n" +
             "    DiffProgram.Windows = C:\\Program Files\\KDiff3\\kdiff3.exe\n" +
             "    DiffProgram.Linux = /usr/bin/kdiff3\n" +
             "Cannot show the command file difference.",
             ResponseJDialog.OK).response();
         return null;
	}
	// Figure out the difference program to run as the first existing found program (from a path),
	// or a program name found in the PATH.
	// Make sure that the difference program exists specified as a path or in the PATH.
	List<String> diffPrograms = new ArrayList<String>();
	if ( diffProgram.indexOf(",") < 0) {
		// Have a single program.
		diffPrograms.add(diffProgram);
	}
	else {
		// Have more than one program.
		diffPrograms = StringUtil.breakStringList(diffProgram, ",", StringUtil.DELIM_TRIM_STRINGS);
	}
	diffProgram = null;
	for ( String prog : diffPrograms ) {
		if ( prog == null ) {
			continue;
		}
		File f = new File(prog);
		// TODO smalers 2022-10-20 the following does not handle just a program found in the path.
		if ( f.exists() || (IOUtil.findProgramInPath(prog) != null) ) {
			diffProgram = prog;
			break;
		}
	}
	return diffProgram;
}

/**
 * Show the difference between the current commands and the source version:
 * - the source version is typically stored in a version control system such as GitHub
 */
private void uiAction_ViewCommandFileSourceDiff () {
	String routine = getClass().getSimpleName() + ".uiAction_CompareCommandsWithSource";
	// If the diff tool is not configured, provide information:
	// - handle generic property name and versions for the operating system
	// - the DiffProgram property can be a comma-separated list of paths to program to run,
	//   or program name without path to find in the PATH
	String diffProgram = uiAction_ViewCommandFileDiff_GetDiffProgram();
	if ( diffProgram != null ) {
		// Diff program exists so save a temporary file with UI commands,
		// retrieve the source to another temporary file, and then compare.
		// Then run the diff program on the files.

		// Get the remote source file:
		// - time out is 5 seconds
		String tempFolder = System.getProperty("java.io.tmpdir");
		String file1Path = tempFolder + File.separator + "TSTool-commands-from-sourceUrl.tstool";
		// Get the source URL from the #@sourceUrl annotation.
		List<Command> commands = TSCommandProcessorUtil.getAnnotationCommands(commandProcessor_GetCommandProcessor(),"sourceUrl");
		if ( commands.size() == 0 ) {
			Message.printWarning(1, "", "The commands have no #@sourceUrl annotation - can't get the source command file." );
			return;
		}
		if ( commands.size() > 1 ) {
			Message.printWarning(1, "", "The commands have multiple #@sourceUrl annotations - can't get the source command file." );
			return;
		}

		// Else, able to continue and get the source copy:
		// - get the URL from the command as parameter 1
		// - timeout after 5 seconds
		String sourceUrl = TSCommandProcessorUtil.getAnnotationCommandParameter(commands.get(0), 1);

		if ( IOUtil.getUriContent(sourceUrl, file1Path, null, 5000, 5000) != 200 ) {
			Message.printWarning(1, "", "Error retrieving source command file from: " + sourceUrl );
			return;
		}
		else {
			Message.printStatus(2, routine, "Retrieved source command file and saved to \"" + file1Path + "\"." );
		}

		// Write the UI commands to a second temporary file.
		String file2Path = null;
		if ( this.__commandsDirty ) {
			file2Path = tempFolder + File.separator + "TSTool-commands-from-UI.tstool";
			try {
				uiAction_WriteCommandFile_Helper(file2Path, false);
				Message.printStatus(2, routine, "Saved TSTool current command to \"" + file2Path + "\"." );
			}
			catch ( Exception e ) {
				Message.printWarning(1, "", "Error saving current TSTool commands to temporary file for diff (" + e + ")" );
				return;
			}
		}
		else {
			// Can compare the existing commands file.
			file2Path = this.__commandFileName;
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
    //String routine = getClass().getSimpleName() + ".uiAction_ViewDocumentation";
	String docUri = formatHelpViewerUrl("", command);
    if ( docUri != null ) {
        try {
            Desktop desktop = Desktop.getDesktop();
            desktop.browse ( new URI(docUri) );
        }
        catch ( Exception e ) {
            Message.printWarning(2, "", "Unable to display documentation at \"" + docUri + "\" (" + e + ")." );
        }
    }
    else {
		// Could not determine the URL to display.
		Message.printWarning(1, "", "Unable to determine URL for documentation for \"" + command + "\"." );
    }
}

/**
View the training materials by displaying in file browser in the training materials folder.
*/
@SuppressWarnings("unused")
private void uiAction_ViewTrainingMaterials () {
    String routine = getClass().getSimpleName() + ".uiAction_ViewTrainingMaterials";
    // The location of the documentation is relative to the application home:
    // - prior to 14.0.4 uppercase
    // - as of 14.0.4 lowercase to be more portable
    //String trainingFolderName = IOUtil.getApplicationHomeDir() + "/doc/Training";
    String trainingFolderName = IOUtil.getApplicationHomeDir() + "/doc/training";
    // Convert for the operating system
    trainingFolderName = IOUtil.verifyPathForOS(trainingFolderName, true);
    // Now display using the default application for the file extension
    Message.printStatus(2, routine, "Opening training material folder \"" + trainingFolderName + "\"" );
    File f = new File(trainingFolderName);
    if ( f.exists() ) {
    	try {
        	Desktop desktop = Desktop.getDesktop();
        	desktop.open ( new File(trainingFolderName) );
    	}
    	catch ( Exception e ) {
        	Message.printWarning(1, routine, "Unable to display training materials at \"" +
            	trainingFolderName + "\" (" + e + ")." );
    	}
    }
    else {
       	Message.printWarning(1, routine, "Training materials folder does not exist: " + trainingFolderName );
    }
}

/**
Write the current command file list (all lines, whether selected or not) to the specified file.
Do not prompt for header comments (and do not add).
@param promptForFile If true, prompt for the file name rather than using the value that is passed.
An extension of .TSTool is enforced.
@param file Command file to write.
@param saveVersion9 whether to save the file considering the software version (this is generally
only needed when pre-10 TSTool version is saved, which will retain "TS Alias = " command notation
*/
private void uiAction_WriteCommandFile ( String file, boolean promptForFile, boolean saveVersion9 ) {
	String routine = getClass().getSimpleName() + ".uiAction_WriteCommandFile";
    String directory = null;
	if ( promptForFile ) {
		JFileChooser fc = JFileChooserFactory.createJFileChooser(ui_GetDir_LastCommandFileOpened() );
		fc.setDialogTitle("Save Command File");
		// Default name.
		File default_file = new File("commands.tstool");
		fc.setSelectedFile ( default_file );
		List<String> extensions = new ArrayList<>();
		extensions.add("tstool");
		extensions.add("TSTool");
		SimpleFileFilter sff = new SimpleFileFilter(extensions,"TSTool Command File");
		fc.setFileFilter(sff);
		if (fc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
			directory = fc.getSelectedFile().getParent();
			file = fc.getSelectedFile().getPath();
			// Enforce extension.
			file = IOUtil.enforceFileExtension ( file, extensions );
			ui_SetDir_LastCommandFileOpened( directory );
		}
		else {
		    // Did not approve.
			return;
		}
	}
	// Now write the file.
	try {
		uiAction_WriteCommandFile_Helper(file, saveVersion9);
		commandList_SetDirty(false);
		commandList_SetCommandFileName ( file );
		// Save the file in the history.
		this.session.pushHistory(file);
		// Do this here because the write may be in a sequence of steps.
		ui_InitGUIMenus_File_OpenRecentFiles();

		if ( directory != null ) {
			// Set the "WorkingDir" property, which will NOT contain a trailing separator.
			IOUtil.setProgramWorkingDir(directory);
			ui_SetDir_LastCommandFileOpened(directory);
			this.__props.set ("WorkingDir=" + IOUtil.getProgramWorkingDir());
			ui_SetInitialWorkingDir (this.__props.getValue("WorkingDir"));
		}
	}
	catch ( Exception e ) {
		Message.printWarning (1, routine, "Error writing command file \"" + file + "\" (" + e + ").");
		// Leave the dirty flag the previous value.
	}
	// Update the status information.
	ui_UpdateStatus ( false );
}

/**
 * Helper method to write the commands to a file.
 * @param saveVersion9 if true, save version 9 syntax, false to save current syntax.
 * @param file Path to file to write.
 */
private void uiAction_WriteCommandFile_Helper(String file, boolean saveVersion9) throws FileNotFoundException {
	PrintWriter out = new PrintWriter(new FileOutputStream(file));
	int size = this.__commands_JListModel.size();
	Command command;
	for (int i = 0; i < size; i++) {
		command = (Command)this.__commands_JListModel.get(i);
		if ( saveVersion9 && command instanceof CommandSavesMultipleVersions ) {
		    // TODO smalers This is a work-around to transition from the "TS Alias = " notation to
		    // Command(Alias=...), which was introduced in version 10.
		    CommandSavesMultipleVersions versionCommand = (CommandSavesMultipleVersions)command;
		    out.println(versionCommand.toString(command.getCommandParameters(),9));
		}
		else {
		    out.println(command.toString());
		}
	}
	out.close();
}

/**
Handle ListSelectionListener events.
@param e list event to handle
*/
public void valueChanged ( ListSelectionEvent e ) {
	// e.getSource() apparently does not return __commands_JList - it must
	// return a different component so don't check the object address.
	if ( ui_GetIgnoreListSelectionEvent() ) {
		return;
	}
    Object component = e.getSource();
    if ( component == this.__resultsTSEnsembles_JList ) {
        //Message.printStatus(2, "", "Ensemble selected in list");
    }
    else if ( component == this.__resultsObjects_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = this.__resultsObjects_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    uiAction_ShowResultsObject( this.__resultsObjects_JListModel.elementAt(i) );
                }
            }
        }
    }
    else if ( component == this.__resultsOutputFiles_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = this.__resultsOutputFiles_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    uiAction_ShowResultsOutputFile( this.__resultsOutputFiles_JListModel.elementAt(i) );
                }
            }
        }
    }
    else if ( component == this.__resultsTables_JList ) {
        if ( !e.getValueIsAdjusting() ) {
            // User is done adjusting selection so do the display.
            ListSelectionModel lsm = this.__resultsTables_JList.getSelectionModel();
            int minIndex = lsm.getMinSelectionIndex();
            int maxIndex = lsm.getMaxSelectionIndex();
            for (int i = minIndex; i <= maxIndex; i++) {
                if (lsm.isSelectedIndex(i)) {
                    uiAction_ShowResultsTable( this.__resultsTables_JListModel.elementAt(i) );
                }
            }
        }
    }
	ui_UpdateStatus ( false );
}

/**
Needed for WindowListener interface.  Currently does nothing.
*/
public void windowActivated ( WindowEvent e ) {
}

/**
This class is listening for GeoViewFrame closing so it can gracefully handle.
*/
public void windowClosed ( WindowEvent e ) {
	// Get the window that is being closed.
	// If it is the __geoview_JFrame, then set the __geoview_JFrame instance to null.
	Component c = e.getComponent();
	if ( (this.__geoview_JFrame != null) && (c == this.__geoview_JFrame) ) {
		// GeoView window is closing.
		this.__geoview_JFrame = null;
		TSToolMenus.View_MapInterface_JCheckBoxMenuItem.setSelected ( false );
	}
	/* FIXME smalers 2008-01-11 Need to test how -nomaingui mode is working with recent changes and then delete this code.
	else if ( !__show_main ) {
		// Running in hidden mode and the TSViewJFrame has closed so close the application.
		uiAction_FileExitClicked ();
	}
	*/
}

/**
Need to monitor TSTool GUI is closing to shut it down gracefully.
*/
public void windowClosing ( WindowEvent e ) {
	Component c = e.getComponent();
	if ( c.equals(this) ) {
		// This may cancel the close if the user decides not to exit.
        uiAction_FileExitClicked();
	}
}

/**
Needed for WindowListener interface.  Currently does nothing.
*/
public void windowDeactivated ( WindowEvent e ) {
}

/**
Needed for WindowListener interface.  Currently does nothing.
*/
public void windowDeiconified ( WindowEvent e ) {
}

/**
Needed for WindowListener interface.  Currently does nothing.
*/
public void windowIconified ( WindowEvent e ) {
}

/**
Needed for WindowListener interface.  Currently does nothing.
*/
public void windowOpened ( WindowEvent e ) {
}

// TODO smalers 2006-03-02 - Evaluate need.
// The JWorksheet_Listener may be deprecated or reworked in the future.
// It is used in a limited capacity here to detect row select/deselect from the popup menu,
// so that the status labels can be updated properly.

/**
Required by JWorksheet_Listener.
*/
public void worksheetDeselectAllRows(int timeframe) {
	if (timeframe == JWorksheet.POST_SELECTION_CHANGE) {
		ui_UpdateStatus ( true );
	}
}

/**
Required by JWorksheet_Listener.
*/
public void worksheetRowAdded ( int row ) {
}

/**
Required by JWorksheet_Listener.
*/
public void worksheetRowDeleted ( int row ) {
}

/**
Required by JWorksheet_Listener.
*/
public void worksheetSelectAllRows(int timeframe) {
	if (timeframe == JWorksheet.POST_SELECTION_CHANGE) {
		ui_UpdateStatus ( true );
	}
}

/**
Required by JWorksheet_Listener.
*/
public void worksheetSetRowCount ( int count ) {
}

/**
Internal class to handle action events from ensemble results list.
*/
private class ActionListener_ResultsEnsembles implements ActionListener {
	private TSTool_JFrame parent = null;

	public ActionListener_ResultsEnsembles ( TSTool_JFrame parent ) {
		this.parent = parent;
	}

    /**
    Handle a group of actions for the ensemble popup menu.
    @param event Event to handle.
    */
    public void actionPerformed (ActionEvent event) {
        String command = event.getActionCommand();

        if ( command.equals(TSToolConstants.Results_Ensemble_Graph_Line_String) ) {
        	try {
	        	// This event corresponds to:
	        	// 1) an ensemble is selected in results
	        	// 2) Graph - Line (Ensemble Graph)
	        	// Display the dialog to confirm how to further process the ensemble and graph.
	        	boolean isDialogForTS = false; // Graph is for ensemble, not time series
	        	EnsembleGraph_JDialog dialog = new EnsembleGraph_JDialog(this.parent, TSToolSession.getInstance(), isDialogForTS, new PropList(""));
	        	String userStatistics = dialog.getStatistics().trim();
	        	String userGraphTemplate = dialog.getGraphTemplate().trim();
	        	String[] statisticsArray = new String[0];
	        	if ( !userStatistics.isEmpty() ) {
	        		statisticsArray = userStatistics.split(",");
	        		for ( int istat = 0; istat < statisticsArray.length; istat++ ) {
	        			statisticsArray[istat] = statisticsArray[istat].trim();
	        		}
	        	}
	        	boolean ok = dialog.ok();
	        	if ( ok ) {
	        		// The ensemble is already created so don't need to recreate.
	    	    	//DateTime inputStart = null;
	    	    	//DateTime inputEnd = null;
	    	    	// Time series is the first selected time series in the results
	    	    	int pos = -1;
	    	    	if ( JGUIUtil.selectedSize(__resultsTSEnsembles_JList) == 0 ) {
	    				pos = 0;
	    			}
	    			else {
	    	            pos = JGUIUtil.selectedIndex(__resultsTSEnsembles_JList,0);
	    			}
	    	    	List<TS> tslist = new ArrayList<>();
	    	    	TSEnsemble tsensemble = null;
	    			if ( pos >= 0 ) {
	    				tsensemble = commandProcessor_GetEnsembleAt(pos);
	    				// Create a new list for the time series so that if statistics are added below
	    				// they don't get added to the original list.
	    				tslist = tsensemble.getTimeSeriesList(true);
	    			}
	    			// Get the time series for the ensemble.
	    			String propVal = null;
	    			File userGraphTemplateFile = null;
	    			if ( (userGraphTemplate != null) && !userGraphTemplate.isEmpty() ) {
	    				userGraphTemplateFile = TSToolSession.getInstance().getGraphTemplateFile(userGraphTemplate);
	    				TSProduct tsp0 = new TSProduct(userGraphTemplateFile.getAbsolutePath(),new PropList(""));
	    				propVal = tsp0.getLayeredPropValue("TemplatePreprocessCommandFile", -1, -1);
	    				Message.printStatus(2,"","Value of TemplatePreprocessCommandFile = \"" + propVal + "\"");
	    			}
	    			// Ensemble is necessary when processing statistics.
	    			TSCommandFileRunner runner = null;
	    			if ( (propVal != null) && !propVal.isEmpty() ) {
	    				// Get the time series by processing the specified command file.
	    				// Command file in template is relative to the template folder.
	    				String preprocessCommandFile = IOUtil.verifyPathForOS(
	    				    IOUtil.toAbsolutePath(userGraphTemplateFile.getParent(),propVal) );
	    				runner = new TSCommandFileRunner(
	    					parent.getProcessor().getInitialPropList(),
	    					parent.getProcessor().getPluginCommandClasses());
	    				Message.printStatus(2,"","Preprocess command file for graph template is \"" + preprocessCommandFile + "\"");
	    				runner.readCommandFile(preprocessCommandFile, false);
	    				// Seed the processor with all the time series from the original processor
	    				// so it can be found for subsequent processing.
	    				Message.printStatus(2,"","Running internal processor with ensemble time series");
	    				@SuppressWarnings("unchecked")
						List<TS> tslist0 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
	    				for ( TS ts2 : tslist ) {
	    					tslist0.add(ts2);
	    				}
	    				// TODO smalers 2020-02-22 the following throws an exception:
	    				// - instead do how it works elsewhere
	    				//runner.getProcessor().setPropContents("AppendResults","true");
	    				PropList runProps = new PropList ( "run");
				 		runProps.set("AppendResults","true");
	    				//runner.runCommands(runProps);
	    				runner.runCommands(runProps);
	    				// Now get the time series out and use for the graphing:
	    				// - the main difference is that the new time series list might include statistics
	    				@SuppressWarnings("unchecked")
						List<TS> tslist1 = (List<TS>)runner.getProcessor().getPropContents("TSResultsList");
	    				tslist = tslist1;
	    				Message.printStatus(2,"","After running internal processor have " + tslist.size() + " time series.");
	    			}
	    			// If any statistics were requested, process and add to the list, but not in the ensemble itself.
	    	        // This is similar to the NewStatisticTimeSeriesFromEnsemble() command functionality.
	    			for ( int istat = 0; istat < statisticsArray.length; istat++ ) {
	    				TSStatisticType statType = TSStatisticType.valueOfIgnoreCase(statisticsArray[istat]);
	    				DateTime analysisStart = null;
	    				DateTime analysisEnd = null;
	    				DateTime outputStart = null;
	    				DateTime outputEnd = null;
	    				String description = tsensemble.getEnsembleName() + ", " + statType;
	    				Integer allowMissingCount = null;
	    				Integer minimumSampleSize = null;
	    				Double value1 = null;
	    				boolean createData = true;
	    				// The newTSID is not critical, but want to make sure the alias and sequence ID is properly set.
	    				TS ts = tslist.get(0); // use the first time series in ensemble for some information.
	    				TSIdent tsident = new TSIdent(ts.getIdentifier());
	    				tsident.setSequenceID("");
	    				tsident.setInputName("");
	    				tsident.setInputType("");
	    				tsident.setType(tsident.getType() + "-" + statType);
	    				String newTSID = tsident.toString();
	    			    TSUtil_NewStatisticTimeSeriesFromEnsemble tsu = new TSUtil_NewStatisticTimeSeriesFromEnsemble (
	    				    tsensemble, analysisStart, analysisEnd, outputStart, outputEnd,
	    				    newTSID, description, statType, value1, allowMissingCount, minimumSampleSize );
	    				TS stat_ts = tsu.newStatisticTimeSeriesFromEnsemble ( createData );
	    				stat_ts.setAlias(ts.getLocation() + "_" + statType);
	    				stat_ts.getIdentifier().setSequenceID(""+ statType); // So %z legend will show statistic.
	    				tslist.add(stat_ts);
	    			}
	    			if ( (userGraphTemplate != null) && !userGraphTemplate.isEmpty() ) {
	    				// If a graph template was specified, expand it with properties that are relevant
	    				// and then graph using similar logic to ProcessTSProduct() command,
	    				// but pass the time series in directly rather than searching in the processor results.
	    				// Determine whether a command file should be run to preprocess the time series for the template.
	    				String tempTSPFile = IOUtil.tempFileName() + "-TSTool-template.tsp";
	    				GraphTemplateProcessor graphTemplateProcessor = new GraphTemplateProcessor (
	    					TSToolSession.getInstance().getGraphTemplateFile(userGraphTemplate) );
	    				// Create a model.
	    				CommandProcessor runnerProcessor = null;
	    				if ( runner != null ) {
	    					runnerProcessor = runner.getProcessor();
	    				}
	    				List<TSEnsemble> tsensembleList = new ArrayList<>();
	    				tsensembleList.add(tsensemble);
	    				graphTemplateProcessor.expandTemplate (tslist, tsensembleList, commandProcessor_GetCommandProcessor(),
	    					runnerProcessor, new File(tempTSPFile));
	    				Message.printStatus(2, "", "Expanded temporary graph template to \"" + tempTSPFile + "\"");
	    				TSProcessor p = new TSProcessor();
	    				PropList overrideProps = new PropList ( "OverrideProps" );
	    				overrideProps.set ( "InitialView", "Graph" ); // Initial view when display opened.
	    				overrideProps.set ( "PreviewOutput", "True" ); // Display a view window (not just file output).
	    				overrideProps.setUsingObject ( "TSViewParentUIComponent", this ); // Use so that interactive graphs are displayed on same screen as TSTool main GUI.
	    				TSProduct tsp = new TSProduct ( tempTSPFile, overrideProps );
	    				// Now process the product.
	    				p.addTSSupplier(graphTemplateProcessor);
	    				p.processProduct ( tsp );
	    			}
	    			else {
	    				// No graph template so use the normal graphing approach.
	    		    	// Display the graph using the created list of time series from the ensemble:
	    		        // - rather than using the time series in the processor, use the supplied list
	    				PropList graphProps = new PropList("GraphProps");
	    				// TODO smalers 2017-04-08 there is currently no way to pass these properties:
	    				// - alternative is to use the template
	    				// - need to figure out how to pass in properties that goes to the TSProduct
	    				// - currently the following does nothing and the graph legend will be at the bottom (not desirable)
	    				graphProps.set("Subproduct 1.LegendPosition","Left");
	    				graphProps.set("Subproduct 1.LegendFormat","%z"); // Would require setting the statistic as the sequence ID.
	    		    	uiAction_GraphEnsembleResults(tslist,"-olinegraph",graphProps);
	    			}
	        	}
        	}
        	catch ( Exception e ) {
        		Message.printWarning(1, "", "Error creating ensemble graph (" + e + ").");
        		Message.printWarning(3, "", e);
        	}
        }
        else if ( command.equals(TSToolConstants.Results_Ensemble_Table_String) ) {
            uiAction_GraphEnsembleResults(null,"-otable",null);
        }
        else if ( command.equals(TSToolConstants.Results_Ensemble_Properties_String) ) {
            uiAction_ResultsEnsembleProperties();
        }
    }
}

/**
Internal class to handle action events from object results list.
*/
private class ActionListener_ResultsObjects implements ActionListener {
    /**
    Handle a group of actions for the ensemble popup menu.
    @param event Event to handle.
    */
    public void actionPerformed (ActionEvent event) {
        String command = event.getActionCommand();
        if ( command.equals(TSToolConstants.Results_Object_Properties_String) ) {
            uiAction_ShowObjectProperties();
        }
    }
}

/**
Internal class to handle action events from network results list.
*/
private class ActionListener_ResultsNetworks implements ActionListener {
    /**
    Handle a group of actions for the network popup menu.
    @param event Event to handle.
    */
    public void actionPerformed (ActionEvent event) {
        String command = event.getActionCommand();
        if ( command.equals(TSToolConstants.Results_Network_Properties_String) ) {
            uiAction_ShowNetworkProperties();
        }
    }
}

/**
Internal class to handle action events from output files results list.
*/
private class ActionListener_ResultsOutputFiles implements ActionListener {
    /**
    Handle a group of actions for the network popup menu.
    @param event Event to handle.
    */
    public void actionPerformed (ActionEvent event) {
        String command = event.getActionCommand();
        if ( command.equals(TSToolConstants.Results_OutputFile_FindOutputFiles_String) ) {
            uiAction_FindOutputFiles();
        }
    }
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
        if ( command.equals(TSToolConstants.Results_Table_Properties_String) ) {
            uiAction_ShowTableProperties();
        }
        else if (command.equals(TSToolConstants.Results_Table_FindTables_String) ) {
        	// Find tables in the table results list.
        	uiAction_FindTables();
        }
    }
}

}