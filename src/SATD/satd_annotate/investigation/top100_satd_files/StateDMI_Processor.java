// StateDMI_Processor - class to process StateDMI commands

/* NoticeStart

StateDMI
StateDMI is a part of Colorado's Decision Support Systems (CDSS)
Copyright (C) 1997-2019 Colorado Department of Natural Resources

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

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import java.lang.String;
import java.lang.StringBuffer;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import RTi.DMI.DMI;
import RTi.DMI.DatabaseDataStore;
import RTi.TS.DayTS;
import RTi.TS.MonthTS;
import RTi.TS.MonthTSLimits;
import RTi.TS.StringMonthTS;
import RTi.TS.TS;
import RTi.TS.TSIdent;
import RTi.TS.TSSupplier;
import RTi.TS.TSUtil;
import RTi.TS.YearTS;

import RTi.Util.IO.Command;
import RTi.Util.IO.CommandDiscoverable;
import RTi.Util.IO.CommandException;
import RTi.Util.IO.CommandListListener;
import RTi.Util.IO.CommandLogRecord;
import RTi.Util.IO.CommandPhaseType;
import RTi.Util.IO.CommandProcessor;
import RTi.Util.IO.CommandProcessorEvent;
import RTi.Util.IO.CommandProcessorEventListener;
import RTi.Util.IO.CommandProcessorEventProvider;
import RTi.Util.IO.CommandProcessorListener;
import RTi.Util.IO.CommandProcessorRequestResultsBean;
import RTi.Util.IO.CommandProfile;
import RTi.Util.IO.CommandStatus;
import RTi.Util.IO.CommandStatusProvider;
import RTi.Util.IO.CommandStatusProviderUtil;
import RTi.Util.IO.CommandStatusType;
import RTi.Util.IO.CommandStatusUtil;
import RTi.Util.IO.CommandWarningException;
import RTi.Util.IO.DataSetComponent;
import RTi.Util.IO.GenericCommand;
import RTi.Util.IO.InvalidCommandParameterException;
import RTi.Util.IO.InvalidCommandSyntaxException;
import RTi.Util.IO.IOUtil;
import RTi.Util.IO.ProcessListener;
import RTi.Util.IO.Prop;
import RTi.Util.IO.PropList;
import RTi.Util.IO.RequestParameterNotFoundException;
import RTi.Util.IO.UnknownCommandException;
import RTi.Util.IO.UnrecognizedRequestException;
import RTi.Util.Message.Message;
import RTi.Util.Message.MessageJDialogListener;
import RTi.Util.Message.MessageUtil;
import RTi.Util.String.StringUtil;
import RTi.Util.Table.DataTable;
import RTi.Util.Time.DateTime;
import RTi.Util.Time.StopWatch;
import RTi.Util.Time.TimeInterval;
import RTi.Util.Time.TimeUtil;
import RTi.Util.Time.YearType;
import riverside.datastore.DataStore;
import rti.tscommandprocessor.commands.check.CheckFileCommandProcessorEventListener;
import rti.tscommandprocessor.commands.util.Comment_Command;
import rti.tscommandprocessor.commands.util.CommentBlockStart_Command;
import rti.tscommandprocessor.commands.util.CommentBlockEnd_Command;
import rti.tscommandprocessor.commands.util.Exit_Command;

import DWR.DMI.HydroBaseDMI.HydroBaseDMI;
import DWR.DMI.HydroBaseDMI.HydroBase_CUMethod;
import DWR.DMI.HydroBaseDMI.HydroBase_CUPenmanMonteith;
import DWR.DMI.HydroBaseDMI.HydroBase_CountyRef;
import DWR.DMI.HydroBaseDMI.HydroBase_ParcelUseTS;
import DWR.DMI.HydroBaseDMI.HydroBase_Structure;
import DWR.DMI.HydroBaseDMI.HydroBase_StructureView;
import DWR.DMI.HydroBaseDMI.HydroBase_WaterDistrict;
import DWR.DMI.HydroBaseDMI.HydroBase_Wells;

import DWR.StateMod.StateMod_DataSet;
import DWR.StateMod.StateMod_DelayTable;
import DWR.StateMod.StateMod_Diversion;
import DWR.StateMod.StateMod_DiversionRight;
import DWR.StateMod.StateMod_InstreamFlow;
import DWR.StateMod.StateMod_InstreamFlowRight;
import DWR.StateMod.StateMod_NodeNetwork;
import DWR.StateMod.StateMod_OperationalRight;
import DWR.StateMod.StateMod_Plan;
import DWR.StateMod.StateMod_Plan_WellAugmentation;
import DWR.StateMod.StateMod_PrfGageData;
import DWR.StateMod.StateMod_Reservoir;
import DWR.StateMod.StateMod_ReservoirRight;
import DWR.StateMod.StateMod_ReturnFlow;
import DWR.StateMod.StateMod_RiverNetworkNode;
import DWR.StateMod.StateMod_StreamEstimate;
import DWR.StateMod.StateMod_StreamEstimate_Coefficients;
import DWR.StateMod.StateMod_StreamGage;
import DWR.StateMod.StateMod_Util;
import DWR.StateMod.StateMod_Well;
import DWR.StateMod.StateMod_WellRight;

import DWR.StateCU.StateCU_BlaneyCriddle;
import DWR.StateCU.StateCU_ClimateStation;
import DWR.StateCU.StateCU_CropCharacteristics;
import DWR.StateCU.StateCU_CropPatternTS;
import DWR.StateCU.StateCU_DataSet;
import DWR.StateCU.StateCU_IrrigationPracticeTS;
import DWR.StateCU.StateCU_Location;
import DWR.StateCU.StateCU_Parcel;
import DWR.StateCU.StateCU_PenmanMonteith;
import DWR.StateCU.StateCU_Supply;
import DWR.StateCU.StateCU_Util;

/**
Class for processing StateDMI commands.
Lists of data are maintained for all StateCU and StateMod components.
*/
public class StateDMI_Processor
implements CommandProcessor, CommandProcessorEventListener, MessageJDialogListener, TSSupplier
{

private final int __FYI_warning_level = StateDMI_Util._FYI_warning_level;

/**
The list of commands managed by this command processor, guaranteed to be non-null.
*/
private List<Command> __commandList = new ArrayList<>();

/**
The name of the file to read for commands.
*/
private String __commandFilename = null;

/**
The array of CommandListListeners to be called when the command list changes.
*/
private CommandListListener [] __CommandListListener_array = null;

/**
The array of CommandProcessorListeners to be called when the commands are
running, to indicate progress.
*/
private CommandProcessorListener [] __CommandProcessorListener_array = null;

/**
The list of CommandProcessorEventListener managed by this command processor,
which is currently used only by the check file.  See the
OpenCheckFile command for creation of the instances.
*/
private CommandProcessorEventListener[] __CommandProcessorEventListener_array = null;

/**
If true, all commands that create output, including write*(), will be
processed.  If false, they will not.  The latter results in faster
processing and only in-memory results.
*/
private boolean __create_output = true;

/**
The initial working directory for processing, typically the location of the commands
file from read/write.  This is used to adjust the working directory with
SetWorkingDir() commands and is used as the starting location with RunCommands().
*/
private String __InitialWorkingDir_String;

/**
The current working directory for processing, which is determined from the initial
working directory and adjustments from setWorkingDir() commands.
*/
private String __WorkingDir_String;

/**
Hashtable of properties used by the processor.
*/
Hashtable<String,Object> __property_Hashtable = new Hashtable<String,Object>();

/**
HashMap of properties used by the processor.
HashMap allows null keys and values, although here keys should be non-null.
*/
private HashMap<String,Object> __propertyHashmap = new HashMap<String,Object>();

/**
Indicates whether the processCommands() is currently running.
*/
private volatile boolean __is_running = false;

/**
Indicates whether the processing loop should be canceled.  This is a request
(e.g., from a GUI) that needs to be handled as soon as possible during command
processing.  It is envisioned that cancel can always occur between commands and
as time allows it will also be enabled within a command.
*/
private volatile boolean __cancel_processing_requested = false;

/**
List of DataTable objects maintained by the processor.
*/
List<DataTable> __TableList = new ArrayList<>();

/**
Special flag to handle limitDiversionHistoricalTSMonthlyToRights() command,
which requires that a copy of the original data are saved.
*/
protected boolean __need_diversion_ts_monthly_copy = false;

/**
The first date of the output period.
*/
private DateTime __OutputStart_DateTime = null;

/**
The last date of the output period.
*/
private DateTime __OutputEnd_DateTime = null;

/**
The output year type ("Calendar", "Water", or "NovToOct").
*/
private YearType __OutputYearType = YearType.CALENDAR; // Default

/**
The internal list of StateCU_BlaneyCriddle being processed.
*/
private List<StateCU_BlaneyCriddle> __CUBlaneyCriddle_List = new ArrayList<>();

/**
The internal list of StateCU_ClimateStation being processed.
*/
private List<StateCU_ClimateStation> __CUClimateStation_List = new ArrayList<>();

/**
The internal list of StateCU_CropCharacteristics being processed.
*/
private List<StateCU_CropCharacteristics> __CUCropCharacteristics_List = new ArrayList<>();

/**
The internal list of StateCU_CropPatternTS being processed.
See also supplemental data __ParcelUseTS_FromSet_List.
*/
private List<StateCU_CropPatternTS> __CUCropPatternTS_List = new ArrayList<>();

/**
Additional HydroBase_ParcelUseTS data provided by the SetCropPatternTS() and SetCropPatternTSFromList() commands.
The additional data are stored as raw parcel data as if from HydroBase and provide data when
ReadCropPatternTSFromHydroBase is called.
 */
private List<HydroBase_ParcelUseTS_FromSet> __HydroBase_ParcelUseTS_FromSet_List = new ArrayList<>();

/**
The internal list of StateCU_Location being processed.
*/
private List<StateCU_Location> __CULocation_List = new ArrayList<>();

/**
The internal list of StateCU_Location being processed.
*/
private List<StateCU_PenmanMonteith> __CUPenmanMonteith_List = new ArrayList<>();

/**
The internal list of StateCU_IrrigationPracticeTS being processed.
The supplemental data are supplied with readIrrigationPracticeTSFromList and
are used by readIrrigationPracticeTSFromHyroBase().
*/
private List<StateCU_IrrigationPracticeTS> __CUIrrigationPracticeTS_List = new ArrayList<>();
// TODO smalers 2019-11-13 need to fix the following to not interfere with __HydroBase_Supplemental_ParcelUseTS_List
//private List<StateDMI_HydroBase_StructureView> __HydroBase_Supplemental_ParcelUseTS_List = new ArrayList<>();
private List<HydroBase_ParcelUseTS> __HydroBase_Supplemental_ParcelUseTS_List = new ArrayList<>();

/**
The internal list of TS contain Agricultural Statistics (AgStats)...
*/
private List<YearTS> __CUAgStatsTS_List = new ArrayList<>();

/**
The internal list of HydroBase_ParcelUseTS records that can be examined.  These
are either read from one or more DBF files or from HydroBase.   These data are
mainly used when processing well to parcel relationships.
*/
// TODO SAM 2007-02-18 Evaluate if needed
//private List __CUParcelUseTS_List = new ArrayList();

/**
The internal list of StateCU_Parcel being processed.
- a hashmap is kept for lookups of the parcels
- lists to parcels are kept with the StateCU_Location
*/
private HashMap<String,StateCU_Parcel> __CUParcel_Map = new HashMap<>();

/**
The internal list of HydroBase_StructureToParcel records that can be examined.
These are either read from one or more DBF files or from HydroBase.   These data
are mainly used when processing well to parcel relationships.
*/
// TODO SAM 2007-02-18 Evaluate if needed
//private List __CUStructureToParcel_List = new ArrayList();

/**
The StateMod data set that is used to track processing when commands are run.
Separate lists of data are maintained in this command processor and are set in the data
set components.
*/
private StateMod_DataSet __StateMod_DataSet = null;

/**
The StateCU data set that is used to track processing when commands are run.
*/
private StateCU_DataSet __StateCU_DataSet = null;

/**
The internal list of StateMod_StreamGage being processed.
*/
private List<StateMod_StreamGage> __SMStreamGageStationList = new ArrayList<>();

/**
The internal list of StateMod_DelayTable (monthly) being processed.
*/
private List<StateMod_DelayTable> __SMDelayTableMonthlyList = new ArrayList<>();

/**
The internal list of StateMod_DelayTable (daily) being processed.
*/
private List<StateMod_DelayTable> __SMDelayTableDailyList = new ArrayList<>();

/**
The internal list of StateMod_Diversion being processed.
*/
private List<StateMod_Diversion> __SMDiversionStationList = new ArrayList<>();

/**
The internal list of StateMod_DiversionRight being processed.
*/
private List<StateMod_DiversionRight> __SMDiversionRightList = new ArrayList<>();

/**
The internal list of StateMod diversion time series (monthly) being processed.
*/
private List<MonthTS> __SMDiversionTSMonthlyList = new ArrayList<>();

/**
The internal list of StateMod diversion time series (monthly) being processed.
This is a saved version to be used to check for observations when using the
LimitDiversionHistoricalTSMonthlyToRights() command.
*/
private List<MonthTS> __SMDiversionTSMonthly2List = new ArrayList<>();

/**
The internal list of monthly pattern time series used for data filling.
*/
private List<StringMonthTS> __SMPatternTSMonthlyList = new ArrayList<>();

/**
Data store list, to generically manage database connections.  This list is guaranteed to be
non-null, although the individual data stores may not be opened and need to be handled appropriately.
*/
private List<DataStore> __dataStoreList = new ArrayList<>();

/**
The internal list of StateMod daily historical TS being processed.
*/
private List<DayTS> __SMDiversionTSDailyList = new ArrayList<>();

/**
The internal list of StateMod demand time series (monthly) being processed.
*/
private List<MonthTS> __SMDemandTSMonthlyList = new ArrayList<>();

/**
The internal list of StateMod demand time series (daily) being processed.
*/
private List<DayTS> __SMDemandTSDailyList = new ArrayList<>();

/**
The internal list of StateMod consumptive water requirement time series (monthly) being processed.
*/
private List<MonthTS> __SMConsumptiveWaterRequirementTSMonthlyList = new ArrayList<>();

/**
The internal list of StateMod_Reservoir being processed.
*/
private List<StateMod_Reservoir> __SMReservoirStationList = new ArrayList<>();

/**
The internal list of StateMod_ReservoirRight being processed.
*/
private List<StateMod_ReservoirRight> __SMReservoirRightList = new ArrayList<>();

/**
The internal list of reservoir StateMod_ReturnFlow being processed.
*/
private List<StateMod_ReturnFlow> __SMReservoirReturnList = new ArrayList<>();

/**
The internal list of StateMod_InstreamFlow being processed.
*/
private List<StateMod_InstreamFlow> __SMInstreamFlowStationList = new ArrayList<>();

/**
The internal list of StateMod_InstreamFlowRight being processed.
*/
private List<StateMod_InstreamFlowRight> __SMInstreamFlowRightList = new ArrayList<>();

/**
The internal list of StateMod instream flow demand TS (average monthly) being processed.
*/
private List<MonthTS> __SMInstreamFlowDemandTSAverageMonthlyList = new ArrayList<>();

/**
The internal list of StateMod_Well being processed.
*/
private List<StateMod_Well> __SMWellList = new ArrayList<>();

/**
The internal list of StateMod_WellRight being processed.
*/
private List<StateMod_WellRight> __SMWellRightList = new ArrayList<>();

/**
The internal list of StateMod well historical pumping time series (monthly) being processed.
*/
private List<MonthTS> __SMWellHistoricalPumpingTSMonthlyList = new ArrayList<>();

/**
The internal list of StateMod well demand time series (monthly) being processed.
*/
private List<MonthTS> __SMWellDemandTSMonthlyList = new ArrayList<>();

/**
The internal list of StateMod_Plan being processed.
*/
private List<StateMod_Plan> __SMPlanList = new ArrayList<>();

/**
The internal list of StateMod_Plan_WellAugmentation being processed.
*/
private List<StateMod_Plan_WellAugmentation> __SMPlanWellAugmentationList = new ArrayList<>();

/**
The internal list of StateMod_ReturnFlow being processed.
*/
private List<StateMod_ReturnFlow> __SMPlanReturnList = new ArrayList<>();

/**
The internal list of StateMod_StreamEstimate being processed.
*/
private List<StateMod_StreamEstimate> __SMStreamEstimateStationList = new ArrayList<>();

/**
The internal list of StateMod_StreamEstimate_Coefficients being processed.
*/
private List<StateMod_StreamEstimate_Coefficients> __SMStreamEstimateCoefficients_List = new ArrayList<>();

/**
The internal list of StateMod_PrfGageData used when processing stream estimate coefficients.
*/
private List<StateMod_PrfGageData> __SMPrfGageData_List = new ArrayList<>();

/**
The internal list of StateMod_RiverNetworkNode being processed.
*/
private List<StateMod_RiverNetworkNode> __SMRiverNetworkNode_List = new ArrayList<>();

/**
The internal list of StateMod_OperationalRight being processed.
*/
private List<StateMod_OperationalRight> __SMOperationalRightList = new ArrayList<>();

/**
The internal StateMod_Network that defines the StateMod model network (not
to be confused with the StateMod network file).
*/
private StateMod_NodeNetwork __SM_network = null;

// Dynamic memory to keep track of data objects that are matched during
// processing, resulting in updates...

private List<String> __CUBlaneyCriddle_match_List = new ArrayList<>();
private List<String> __CUClimateStation_match_List = new ArrayList<>();
private List<String> __CUCropCharacteristics_match_List = new ArrayList<>();
private List<String> __CUCropPatternTS_match_List = new ArrayList<String>();
//private List<String> __CUDelayTableAssignment_match_List = new ArrayList<>();
private List<String> __CULocation_match_List = new ArrayList<>();
private List<String> __CUIrrigationPracticeTS_match_List = new ArrayList<>();
//private List<String> __CUDelayTableDaily_match_List = new ArrayList<String>();
//private List<String> __CUDelayTableMonthly_match_List = new ArrayList<String>();
private List<String> __CUPenmanMonteith_match_List = new ArrayList<>();

private List<String> __SMStreamGage_match_List = new ArrayList<>();
private List<String> __SMDelayTableMonthly_match_List = new ArrayList<>();
private List<String> __SMDelayTableDaily_match_List = new ArrayList<>();
private List<String> __SMDiversion_match_List = new ArrayList<>();
private List<String> __SMDiversionRight_match_List = new ArrayList<>();
private List<String> __SMDiversionTSMonthly_match_List = new ArrayList<>();
// TODO SAM 2007-02-18 Enable if needed
//private List __SMDiversionTSDaily_match_List = new ArrayList();
private List<String> __SMConsumptiveWaterRequirementTSMonthly_match_List = new ArrayList<>();
private List<String> __SMDemandTSMonthly_match_List = new ArrayList<>();
private List<String> __SMReservoir_match_List = new ArrayList<>();
private List<String> __SMReservoirRight_match_List = new ArrayList<>();
private List<String> __SMReservoirReturn_match_List = new ArrayList<>();
private List<String> __SMInstreamFlow_match_List = new ArrayList<>();
private List<String> __SMInstreamFlowRight_match_List = new ArrayList<>();
private List<String> __SMInstreamFlowDemandTSAverageMonthly_match_List = new ArrayList<>();
private List<String> __SMWell_match_List = new ArrayList<>();
private List<String> __SMWellRight_match_List = new ArrayList<>();
private List<String> __SMWellHistoricalPumpingTSMonthly_match_List = new ArrayList<>();
private List<String> __SMWellDemandTSMonthly_match_List = new ArrayList<>();
private List<String> __SMPlan_match_List = new ArrayList<>();
private List<String> __SMPlanReturn_match_List = new ArrayList<>();
private List<String> __SMPlanWellAugmentation_match_List = new ArrayList<>();
private List<String> __SMStreamEstimate_match_List = new ArrayList<>();
private List<String> __SMStreamEstimateCoefficients_match_List = new ArrayList<>();
private List<String> __SMPrfGageData_match_List = new ArrayList<>();
private List<String> __SMRiverNetworkNode_match_List = new ArrayList<>();
private List<String> __SMOperationalRight_match_List = new ArrayList<>();

/**
The HydroBase DMI instance that is used for database queries.
*/
private HydroBaseDMI __hdmi = null;

/**
Default width for WDIDs (2 for WD, 5 for ID).  For now automatically override internally based on
what is read from existing data.
*/
private int __defaultWdidLength = 7;

private ProcessListener [] __listeners = null;	// Listeners to receive process output.

/**
Internal data that is used to set/get data so new DateTime objects don't need to
be created each time.  The object has full precision - other objects with
different precision may need to be created.
*/
private DateTime __temp_DateTime = new DateTime();

/**
Gets set to true if a run has occurred and was successful.  It is to false at the beginning of a
run and is only set to true if run is successful.  Needed for running in batch mode for validation of runs.
*/
private boolean runSuccessful = false;

/**
Construct a command processor with no commands.
*/
public StateDMI_Processor ()
{	super();

	__propertyHashmap.put ( "InstallDir", IOUtil.getApplicationHomeDir() );
	// This is used to locate the HTML documentation for command editor dialogs, etc.
	__propertyHashmap.put ( "InstallDirURL", "file:///" + IOUtil.getApplicationHomeDir().replace("\\", "/") );
	String homeDir = System.getProperty("user.home") + File.separator + ".tstool";
	__propertyHashmap.put ( "UserHomeDir", homeDir );
	__propertyHashmap.put ( "UserHomeDirURL", "file:///" + homeDir.replace("\\", "/") );
}

/**
StateDMI_Processor Constructor.
@param gui the gui in which this processor is running
@param hbdmi HydroBaseDMI instance for database I/O.
@param commands the list of commands to execute.
@param num_prepended_commands The count of the commands at the start of
"commmands" that have been automatically added and which should not be indicated
in the count in messages.  It is assumed that these commands run "flawlessly" so
as to not confuse the user.
@param app_PropLIst properties from the application (e.g., containing the
initial "WorkingDir".
*/
/* FIXME SAM 2008-12-05 Does not appear to be needed - confirm that can be removed
public StateDMI_Processor (	StateDMI_JFrame gui, HydroBaseDMI hbdmi,
		List commands, int num_prepended_commands,
				PropList app_PropList )
{	setCommands ( commands );
	__gui = gui;
	__hdmi = hbdmi;
	__app_PropList = app_PropList;
	__num_prepended_commands = num_prepended_commands;
	initialize();
}
*/

/**
Add a command at the end of the list and notify command list listeners of the
add.
@param command Command to add.
*/
public void addCommand ( Command command )
{
	addCommand ( command, true );
}

/**
Add a command at the end of the list.
@param command Command to add.
@param notifyCommandListListeners Indicate whether registered CommandListListeners should be notified.
*/
public void addCommand ( Command command, boolean notifyCommandListListeners )
{	String routine = getClass().getName() + ".addCommand";
	getCommands().add( command );
	// Also add this processor as a listener for events
	if ( command instanceof CommandProcessorEventProvider ) {
	    CommandProcessorEventProvider ep = (CommandProcessorEventProvider)command;
	    ep.addCommandProcessorEventListener(this);
	}
	if ( notifyCommandListListeners ) {
		notifyCommandListListenersOfAdd ( getCommands().size() - 1, getCommands().size() - 1 );
	}
	Message.printStatus(2, routine, "Added command object \"" +	command + "\"." );
}

/**
Add a command at the end of the list using the string text.  This should currently only be
used for commands that do not have command classes, which perform
additional validation on the commands.  A GenericCommand instance will
be instantiated to maintain the string and allow command status to be set.
@param command_string Command string for command.
@param index Index (0+) at which to insert the command.
*/
public void addCommand ( String command_string )
{	String routine = "StateDMI_Processor.addCommand";
	Command command = new GenericCommand ();
	command.setCommandString ( command_string );
	addCommand ( command );
	Message.printStatus(2, routine, "Creating generic command from string \"" + command_string + "\"." );
}

/**
Add a CommandListListener, to be notified when commands are added, removed,
or change (are edited or execution status is updated).
If the listener has already been added, the listener will remain in
the list in the original order.
*/
public void addCommandListListener ( CommandListListener listener )
{
	// Use arrays to make a little simpler than lists to use later...
	if ( listener == null ) {
		return;
	}
	// See if the listener has already been added...
	// Resize the listener array...
	int size = 0;
	if ( __CommandListListener_array != null ) {
		size = __CommandListListener_array.length;
	}
	for ( int i = 0; i < size; i++ ) {
		if ( __CommandListListener_array[i] == listener ) {
			return;
		}
	}
	if ( __CommandListListener_array == null ) {
		__CommandListListener_array = new CommandListListener[1];
		__CommandListListener_array[0] = listener;
	}
	else {
		// Need to resize and transfer the list...
		size = __CommandListListener_array.length;
		CommandListListener [] newlisteners =
			new CommandListListener[size + 1];
		for ( int i = 0; i < size; i++ ) {
			newlisteners[i] = __CommandListListener_array[i];
		}
		__CommandListListener_array = newlisteners;
		__CommandListListener_array[size] = listener;
	}
}

/**
Add a CommandProcessorEventListener, to be notified when commands generate CommandProcessorEvents.
This is currently utilized by the check file capability, which queues events and generates a report file.
If the listener has already been added, the listener will remain in
the list in the original order.
TODO SAM 2008-08-21 Make this private for now but may need to rethink if other than the check file use
the events.
*/
private void addCommandProcessorEventListener ( CommandProcessorEventListener listener )
{
    // Use arrays to make a little simpler than lists to use later...
    if ( listener == null ) {
        return;
    }
    // See if the listener has already been added...
    // Resize the listener array...
    int size = 0;
    if ( __CommandProcessorEventListener_array != null ) {
        size = __CommandProcessorEventListener_array.length;
    }
    for ( int i = 0; i < size; i++ ) {
        if ( __CommandProcessorEventListener_array[i] == listener ) {
            return;
        }
    }
    if ( __CommandProcessorEventListener_array == null ) {
        __CommandProcessorEventListener_array = new CommandProcessorEventListener[1];
        __CommandProcessorEventListener_array[0] = listener;
    }
    else {
        // Need to resize and transfer the list...
        size = __CommandProcessorEventListener_array.length;
        CommandProcessorEventListener [] newlisteners = new CommandProcessorEventListener[size + 1];
        for ( int i = 0; i < size; i++ ) {
            newlisteners[i] = __CommandProcessorEventListener_array[i];
        }
        __CommandProcessorEventListener_array = newlisteners;
        __CommandProcessorEventListener_array[size] = listener;
    }
}

/**
Add a CommandProcessorListener, to be notified when commands are started,
progress made, and completed.  This is useful to allow calling software to report progress.
If the listener has already been added, the listener will remain in
the list in the original order.
*/
public void addCommandProcessorListener ( CommandProcessorListener listener )
{
	// Use arrays to make a little simpler than lists to use later...
	if ( listener == null ) {
		return;
	}
	// See if the listener has already been added...
	// Resize the listener array...
	int size = 0;
	if ( __CommandProcessorListener_array != null ) {
		size = __CommandProcessorListener_array.length;
	}
	for ( int i = 0; i < size; i++ ) {
		if ( __CommandProcessorListener_array[i] == listener ) {
			return;
		}
	}
	if ( __CommandProcessorListener_array == null ) {
		__CommandProcessorListener_array = new CommandProcessorListener[1];
		__CommandProcessorListener_array[0] = listener;
	}
	else {	// Need to resize and transfer the list...
		size = __CommandProcessorListener_array.length;
		CommandProcessorListener [] newlisteners = new CommandProcessorListener[size + 1];
		for ( int i = 0; i < size; i++ ) {
			newlisteners[i] = __CommandProcessorListener_array[i];
		}
		__CommandProcessorListener_array = newlisteners;
		__CommandProcessorListener_array[size] = listener;
	}
}

/**
Add a ProcessListener to receive Process output.  Multiple listeners can be
registered.  If an attempt is made to register the same listener more than
once, the later attempt is ignored.
@param listener ProcessListener to add.
*/
public void addProcessListener ( ProcessListener listener )
{	// Use arrays to make a little simpler than lists to use later...
	if ( listener == null ) {
		return;
	}
	// See if the listener has already been added...
	// Resize the listener array...
	int size = 0;
	if ( __listeners != null ) {
		size = __listeners.length;
	}
	for ( int i = 0; i < size; i++ ) {
		if ( __listeners[i] == listener ) {
			return;
		}
	}
	if ( __listeners == null ) {
		__listeners = new ProcessListener[1];
		__listeners[0] = listener;
	}
	else {
		// Need to resize and transfer the list...
		size = __listeners.length;
		ProcessListener [] newlisteners = new ProcessListener[size + 1];
		for ( int i = 0; i < size; i++ ) {
			newlisteners[i] = __listeners[i];
		}
		__listeners = newlisteners;
		__listeners[size] = listener;
	}
}

// TODO smalers 2019-05-29 need to evaluate whether to use or delete method
/**
Calculate a structure's capacity, for assignment from HydroBase.
The order of assignment is as follows:
<ol>
<li>	The estimated capacity is used if not missing.</li>
<li>	The decreed capacity is used if not missing.</li>
<li>	A value of 999 is used.</li>
</ol>
@param id The identifier for the main station being analyzed (used for messages).
@param capacity0 Original capacity (or StateMod_Util.MISSING_DOUBLE if missing).
@param hbdiv HydroBase_Structure used with W&D node types where wells supplement
diversion supply (null if processing an explicit well or well-only aggregate/system).
@param ditch_cov Fraction of a diversion's irrigation of a parcel (only used
when processing well structures or permits).
@param hbwell HydroBase_Structure for a well structure, used when a supplemental
well is a structure (null when processing diversions).
@param hbwell_parcel HydroBase_Wells for a well, used when a supplemental
well is a well permit (null when processing diversions).
@param collection_type the collection type for "id" or blank if not a
collection (used for messages).
@param part_id Identifier for the part being processed.
@param comp_type Data set component:  StateMod_DataSet.COMP_DIVERSION_STATIONS
or StateMod_DataSet.COMP_WELL_STATIONS.
@param add If true, then add to the capacity.  If false, reset.
*/
@SuppressWarnings("unused")
private double calculateStructureCapacity (	double capacity0,
						String id,
						HydroBase_Structure hbdiv,
						double ditch_cov,
						HydroBase_Structure hbwell,
						HydroBase_Wells hbwell_parcel,
						String collection_type,
						String part_id,
						int comp_type,
						boolean add )
{	String routine = "StateDMI_Processor.calculateStructureCapacity";
	String station_type = " diversion ";
	if ( comp_type == StateMod_DataSet.COMP_WELL_STATIONS ) {
		station_type = " well ";
	}
	String part_string = "";
	if ( collection_type.length() > 0 ) {
		part_string = collection_type + " part: " + part_id;
	}
	double capacity = 0.0;
	if ( hbdiv == null ) {
		// Well is not tied to a ditch.
		ditch_cov = 1.0;
	}
	if ( (hbdiv != null) && (hbwell == null) && (hbwell_parcel == null) ) {
		// Processing a diversion station...
		if ( hbdiv.getEst_capacity() > 0.0 ) {
			capacity = hbdiv.getEst_capacity();
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" estimated capacity -> " +
			StringUtil.formatString(capacity,"%.2f"));
		}
		else if ( hbdiv.getDcr_capacity() > 0.0 ) {
			capacity = hbdiv.getDcr_capacity();
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" decreed capacity -> " +
			StringUtil.formatString(capacity,"%.2f") );
		}
		else {	// Default 999 value as per watright
			// code
			// TODO SAM 2004-06-08 may need a
			// better way to handle but often gets
			// reset to the maximum diversion value.
			capacity = 999.0;
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" default capacity -> 999" );
		}
	}
	else if ( hbwell != null ) {
		// Processing a well structure...
		if ( hbwell.getEst_capacity() > 0.0 ) {
			capacity = hbwell.getEst_capacity()*ditch_cov*
				hbwell_parcel.getPercent_yield();
			if ( hbdiv == null ) {
			// No ditch coverage...
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" well WDID=" +
			HydroBase_WaterDistrict.formWDID(hbwell.getWD(),
			hbwell.getID()) +
			" estimated capacity*percent_yield: " +
			StringUtil.formatString(hbwell.getEst_capacity(),"%.4f")
			+ "*" +
			StringUtil.formatString(
			hbwell_parcel.getPercent_yield(),"%.4f") + " -> " +
			StringUtil.formatString(capacity,"%.2f"));
			}
			else {
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" well WDID=" +
			HydroBase_WaterDistrict.formWDID(hbwell.getWD(),
			hbwell.getID()) +
			" estimated capacity*ditch_cov*percent_yield: " +
			StringUtil.formatString(hbwell.getEst_capacity(),"%.4f")
			+ "*" +
			StringUtil.formatString(ditch_cov,"%.4f")
			+ "*" +
			StringUtil.formatString(
			hbwell_parcel.getPercent_yield(),"%.4f") + " -> " +
			" -> " + StringUtil.formatString(capacity,"%.2f"));
			}
		}
		else if ( hbwell.getDcr_capacity() > 0.0 ) {
			capacity = hbwell.getDcr_capacity()*ditch_cov*
				hbwell_parcel.getPercent_yield();
			if ( hbdiv == null ) {
			// No ditch coverage...
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" decreed capacity*percent_yield: " +
			StringUtil.formatString(hbwell.getDcr_capacity(),"%.4f")
			+ "*" +
			StringUtil.formatString(ditch_cov,"%.4f")
			+ "*" +
			StringUtil.formatString(
			hbwell_parcel.getPercent_yield(),"%.4f") + " -> " +
			" -> " + StringUtil.formatString(capacity,"%.2f") );
			}
			else {
			// Include ditch coverage...
			Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" decreed capacity*ditch_cov*percent_yield: " +
			StringUtil.formatString(hbwell.getDcr_capacity(),"%.4f")
			+ "*" +
			StringUtil.formatString(ditch_cov,"%.4f")
			+ "*" +
			StringUtil.formatString(
			hbwell_parcel.getPercent_yield(),"%.4f") + " -> " +
			StringUtil.formatString(capacity,"%.2f") );
			}
		}
		else {	Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" yield -> NO DATA." );
			return capacity0;
		}
	}
	else if ( hbwell_parcel != null ) {
		// Processing a "well permit"...
		if ( hbwell_parcel.getYield() > 0.0 ) {
			capacity = hbwell_parcel.getYield()
				*.002228	// GPM to CFS
				*ditch_cov
				*hbwell_parcel.getPercent_yield();
			if ( hbdiv == null ) {
			// No diversion...
			Message.printStatus ( 2, routine,
			"Using " + id +
			" receipt=" + hbwell_parcel.getReceipt()+
			" class=" + hbwell_parcel.getClass() +
			" yield*.002228CFS/GPM*percent_yield: " +
			StringUtil.formatString(
				hbwell_parcel.getPercent_yield(),"%.4f") +
				"*.002228*" +
				StringUtil.formatString(
				hbwell_parcel.getPercent_yield(),"%.4f") +
				" -> " +
				StringUtil.formatString(capacity,"%.2f") );
			}
			else {
			// With diversion...
			Message.printStatus ( 2, routine,
			"Using " + id +
			" receipt=" + hbwell_parcel.getReceipt()+
			" class=" + hbwell_parcel.getClass() +
			" yield*.002228CFS/GPM*ditch_cov*percent_yield: " +
			StringUtil.formatString(
				hbwell_parcel.getPercent_yield(),"%.4f") +
				"*.002228*" + ditch_cov + "*" +
				StringUtil.formatString(
				hbwell_parcel.getPercent_yield(),"%.4f") +
				" -> " +
				StringUtil.formatString(capacity,"%.2f") );
			}
		}
		else {	Message.printStatus ( 2, routine,
			"Using " + id + station_type + part_string +
			" yield -> NO DATA." );
			return capacity0;
		}
	}
	if ( !add || StateMod_Util.isMissing(capacity0) ) {
		return capacity;
	}
	else {	return capacity0 + capacity;
	}
}

// TODO SAM 2005-08-15
// Should this method search the commands for write*() commands, in order to
// better decide which warnings are important?  Currently some checks are only
// done when debug is turned on.
/**
Check the integrity of the data set.  The following checks are always done:
<ol>
<li>	A location cannot be in zero or one of the following, for the entire
	data set:  aggregate, system, MultiStruct.
	</li>
</ol>
The following checks are only done but do not result in "important" warnings:
<ol>
<li>	If diversion stations and historical monthly time series are in memory,
	check whether each station has a time series, and check whether there
	are time series that do not match an ID.
	</li>
</ol>
@return the number of warnings that are displayed.
*/
// TODO SAM 2007-02-18 Evaluate how used in check code
/*
private int checkDataSet ()
{	int warning_count = 0, warning_count_fyi = 0;
	int wl = 2;
	int wl_fyi = 3;
	String command_tag = "EndChecks";	// See StateDMI_JFrame.
						// goToMessageTag
	String routine = "StateDMI_Processor.checkDataSet";

	Message.printStatus ( 2, routine, __LOG_THICK_LINE );
	Message.printStatus ( 2, routine,
	"Checking data set for consistency, correctness..." );

	// Loop through the StateCU locations, first checking for duplicate
	// IDs and then checking to make sure that identifiers used in
	// aggregates are only used in one place.

	StateCU_Location culoc_i, culoc_j;
	StateMod_Diversion dds_i;
	String id_i, id_j;
	TS ts_i;
	int pos;
	int size = __CULocation_Vector.size();
	for ( int i = 0; i < size; i++ ) {
		culoc_i = (StateCU_Location)__CULocation_Vector.get(i);
		id_i = culoc_i.getID();
		for ( int j = 0; j < size; j++ ) {
			if ( i == j ) {
				// Don't compare to itself...
				continue;
				// TODO SAM 2005-08-15
				// Could put warnings here about a location
				// calling itself a collection - alternate
				// identifiers are advised.
			}
			culoc_j = (StateCU_Location)
				__CULocation_Vector.get(j);
			id_j = culoc_j.getID();
			// Simple check to make sure the ID is not repeated...
			if ( id_i.equalsIgnoreCase(id_j) ) {
				Message.printWarning ( wl,
				formatMessageTag(command_tag,++warning_count),
				routine,
				"CU Location \"" + id_i + "\" (position "+
				(i + 1) + " is repeated in position " +(j + 1));
			}
		}
	}

	// If debug is on, do some additional checks...

	// TODO SAM 2005-08-16
	// For now always do this but at a lower warning level.
	//if ( Message.isDebugOn ) {

	if (	(__SMDiversion_Vector.size() > 0) &&
		(__SMDiversionTSMonthly_Vector.size() > 0) ) {
		// Diversion stations and historical monthly time series are
		// in the data set.

		// Make sure that there is a diversion time series for every
		// location...

		size = __SMDiversion_Vector.size();
		for ( int i = 0; i < size; i++ ) {
			dds_i = (StateMod_Diversion)
				__SMDiversion_Vector.get(i);
			id_i = dds_i.getID();
			pos = TSUtil.indexOf(
				__SMDiversionTSMonthly_Vector,
				id_i, "Location", 0 );
			if ( pos < 0 ) {
				Message.printWarning ( wl_fyi,
				formatMessageTag(command_tag,
				++warning_count_fyi), routine,
				"Diversion station \"" + id_i + "\" does not " +
				"have a historical monthly time series." );
			}
		}

		// Check to see whether there are extra time series that do
		// not correspond to stations...

		size = __SMDiversionTSMonthly_Vector.size();
		for ( int i = 0; i < size; i++ ) {
			ts_i = (TS)__SMDiversionTSMonthly_Vector.get(i);
			id_i = ts_i.getLocation();
			pos = StateMod_Util.indexOf(
				__SMDiversion_Vector, id_i );
			if ( pos < 0 ) {
				Message.printWarning ( wl_fyi,
				formatMessageTag(command_tag,
				++warning_count_fyi), routine,
				"Diversion historical time series (monthly) " +
				"for \"" + id_i + "\" does not " +
				"have a diversion station." );
			}
		}
	}

	// Make sure well stations have rights...

	/ * TODO SAM 2006-04-10
	May not need this if checks occurring at write are OK.
	if (	__StateMod_DataSet.getComponentForComponentType(
		StateMod_DataSet.COMP_WELL_RIGHTS).isOutput() ) {
		// Make sure that there is at least one well right for each well
		// station...

		size = __SMWell_Vector.size();
		message_list = new ArrayList();
		for ( int i = 0; i < size; i++ ) {
			wes_i = (StateMod_Well)
				__SMWell_Vector.get(i);
			id_i = wes_i.getID();
			rights = StateMod_Util.getRights (
				id_i, __SMWellRight_Vector );
			if ( (rights == null) || (rights.size() == 0) ) {
				// Format suitable for output in a list that
				// can be copied to a spreadsheet or table.
				message_list.add (
				StringUtil.formatString(id_i,"%-12.12s") +
				", \"" + wes_i.getName() + "\"" );
			}
		}
		size = message_list.size();
		if ( size > 0 ) {
			// Need to notify the user...
			message_list.insertget ( "The following well " +
			"stations have no water rights.", 0 );
			message_list.insertget ( "", 1 );
			message_list.insertget ( "     ID     , NAME", 2);
			for ( int i = 0; i < size; i++ ) {
				Message.printWarning ( wl_fyi,
				formatMessageTag(command_tag,
				++warning_count_fyi), routine,
				(String)message_list.get(i) );
			}
		}
		__StateMod_DataSet.getComponentForComponentType(
			StateMod_DataSet.COMP_WELL_RIGHTS).setDataCheckResults(
			message_list);
	}
	* /

	//} // End if debug is on.

	Message.printStatus ( 2, routine,
	"Done checking data set for consistency." );
	Message.printStatus ( 2, routine, __LOG_THICK_LINE );

	return warning_count;
}
*/

/**
Clear the results of processing.  This resets the lists of data objects to empty.
*/
public void clearResults()
{
	__CUBlaneyCriddle_List.clear();
	__CUClimateStation_List.clear();
	__CUCropCharacteristics_List.clear();
	__CUCropPatternTS_List.clear();
	__CULocation_List.clear();
	__CUParcel_Map.clear();
	__CUIrrigationPracticeTS_List.clear();
	__CUPenmanMonteith_List.clear();

	// TODO SAM 2007-06-15 Remove after using parcels only is verified
	//__HydroBase_Supplemental_StructureIrrigSummaryTS_List.clear();
	__HydroBase_Supplemental_ParcelUseTS_List.clear();

	__SMDelayTableMonthlyList.clear();
	__SMDelayTableDailyList.clear();
	__SMDiversionStationList.clear();
	__SMDiversionRightList.clear();
	__SMDiversionTSMonthlyList.clear();
	__SMDiversionTSMonthly2List.clear();
	__SMPatternTSMonthlyList.clear();
	__SMConsumptiveWaterRequirementTSMonthlyList.clear();
	__SMDemandTSMonthlyList.clear();
	__SMDemandTSDailyList.clear();
	__SM_network = null;	// Will be retrieved from GUI if necessary.
	__SMOperationalRightList.clear();
	__SMPlanList.clear();
	__SMPlanWellAugmentationList.clear();
	__SMPlanReturnList.clear();
	__SMReservoirReturnList.clear();
	__SMReservoirStationList.clear();
	__SMReservoirRightList.clear();
	__SMRiverNetworkNode_List.clear();
	__SMInstreamFlowStationList.clear();
	__SMInstreamFlowRightList.clear();
	__SMInstreamFlowDemandTSAverageMonthlyList.clear();
	__SMStreamGageStationList.clear();
	__SMStreamEstimateStationList.clear();
	__SMStreamEstimateCoefficients_List.clear();
	__SMPrfGageData_List.clear();
	__SMWellList.clear();
	__SMWellRightList.clear();
	__SMWellHistoricalPumpingTSMonthlyList.clear();
	__SMWellDemandTSMonthlyList.clear();
	
	if ( __TableList != null ) {
        __TableList.clear();
    }
}

/**
Convert the supplemental HydroBase_ParcelUseTS_FromSet data (raw data specified by set commands)
to StateDMI_HydroBase_StructureView records (used for ditch processing).
Data records are set with SetCropPatternTS() and SetCropPatternTSFromList() commands and
are then used to create crop patterns when ReadCropPatternTSFromHydroBase() is called.
*/
protected List<HydroBase_StructureView_FromSet> convertHydroBaseParcelUseTSFromSetToHydroBaseStructureViewFromSet (
	List<HydroBase_ParcelUseTS_FromSet> hydroBaseParcelUseTSFromSetList )
{	String routine = "StateDMI_Processor.convertParcelUseTSFromSetToStructureViewFromSet";
	List<HydroBase_StructureView_FromSet> hydroBaseStructureViewFromSet_List = new ArrayList<>();
	int size_parcels = hydroBaseParcelUseTSFromSetList.size();
	HydroBase_ParcelUseTS_FromSet parcel = null;
	HydroBase_StructureView_FromSet sits = null;
	boolean found = false; // Whether a matching summary is found
	// Loop through the raw parcel data...
	for ( int iparcel = 0; iparcel < size_parcels; iparcel++ ){
		parcel = hydroBaseParcelUseTSFromSetList.get(iparcel);
		// Find a matching location in irrig summary data and add to it...
		found = false;
		/* TODO SAM 2007-06-17 Evaluate whether needed - old code does
		not have true irrig summary ts but simple records.
		for ( int isummary = 0; isummary < size_summary; isummary++ ) {
			summary = (StateDMI_HydroBase_StructureView)HydroBase_Supplemental_StructureIrrigSummaryTS_List.get(isummary);
			if ( parcel.getLocationID().equalsIgnoreCase(summary.getLocationID()) {
				found = true;
				break;
			}
		}
		*/
		if ( !found ) {
			// Create a new summary to add to
			sits = new HydroBase_StructureView_FromSet();
		}
		sits.setLocationID ( parcel.getLocationID() );
		if ( HydroBase_WaterDistrict.isWDID(parcel.getLocationID())) {
			try {
				int [] wdid_parts = new int[2];
				HydroBase_WaterDistrict.parseWDID(parcel.getLocationID());
				sits.setWD ( wdid_parts[0] );
				sits.setID ( wdid_parts[1] );
			}
			catch ( Exception e ) {
				//Absorb - just use the LocationID
			}
		}
		// Set the IrrigSummaryTS information using only the total area...
		sits.setCal_year ( parcel.getCal_year() );
		sits.setLand_use ( parcel.getLand_use() );
		sits.setAcres_total ( parcel.getArea() );
		hydroBaseStructureViewFromSet_List.add(sits);
	}
	if ( hydroBaseStructureViewFromSet_List.size() == 0 ) {
		Message.printStatus ( 2, routine, "No additional crop pattern time series records have been provided." );
	}
	else {
		Message.printStatus ( 2, routine,
			"Created " + hydroBaseStructureViewFromSet_List.size() +
			" structure view/irrig_summary_ts records from " + hydroBaseParcelUseTSFromSetList.size() +
			" parcel use records:" );
		for ( int i = 0; i < hydroBaseStructureViewFromSet_List.size(); i++ ) {
			sits = hydroBaseStructureViewFromSet_List.get(i);
			Message.printStatus ( 2, routine, "Location=" + sits.getLocationID() +
				" Year=" + sits.getCal_year() +
				" Crop=" + sits.getLand_use() +
				" Area=" + StringUtil.formatString(sits.getAcres_total(),"%.3f") );
		}
	}
	return hydroBaseStructureViewFromSet_List;
}

// TODO smalers 2020-02-15 This is used with StateDMI version < 5.00.00
/**
Convert the supplemental StateDMI_HydroBase_ParcelUseTS data (raw data specified by set commands)
to StateDMI_HydroBase_StructureView records (used for ditch processing).
This method is called from a couple of commands.  Data records are set with SetCropPatternTS() and
SetCropPatternTSFromList() commands and are later used to create crop patterns when
ReadCropPatternTSFromHydroBase() is called.
*/
protected List<StateDMI_HydroBase_StructureView> convertSupplementalParcelUseTSToStructureView (
	List<StateDMI_HydroBase_ParcelUseTS> supplementalParcelUseTSList )
{	String routine = "StateDMI_Processor.convertSupplementalParcelUseTSToStructureIrrigSummaryTS";
	List<StateDMI_HydroBase_StructureView> HydroBase_Supplemental_StructureIrrigSummaryTS_List = new ArrayList<>();
	int size_parcels = supplementalParcelUseTSList.size();
	StateDMI_HydroBase_ParcelUseTS parcel = null;
	StateDMI_HydroBase_StructureView sits = null;
	boolean found = false; // Whether a matching summary is found
	// Loop through the raw parcel data...
	for ( int iparcel = 0; iparcel < size_parcels; iparcel++ ){
		parcel = supplementalParcelUseTSList.get(iparcel);
		// Find a matching location in irrig summary data and add to it...
		found = false;
		/* TODO SAM 2007-06-17 Evaluate whether needed - old code does
		not have true irrig summary ts but simple records.
		for ( int isummary = 0; isummary < size_summary; isummary++ ) {
			summary = (StateDMI_HydroBase_StructureView)HydroBase_Supplemental_StructureIrrigSummaryTS_List.get(isummary);
			if ( parcel.getLocationID().equalsIgnoreCase(summary.getLocationID()) {
				found = true;
				break;
			}
		}
		*/
		if ( !found ) {
			// Create a new summary to add to
			sits = new StateDMI_HydroBase_StructureView();
		}
		sits.setLocationID ( parcel.getLocationID() );
		if ( HydroBase_WaterDistrict.isWDID(parcel.getLocationID())) {
			try {
				int [] wdid_parts = new int[2];
				HydroBase_WaterDistrict.parseWDID(parcel.getLocationID());
				sits.setWD ( wdid_parts[0] );
				sits.setID ( wdid_parts[1] );
			}
			catch ( Exception e ) {
				//Absorb - just use the LocationID
			}
		}
		// Set the IrrigSummaryTS information using only the total area...
		sits.setCal_year ( parcel.getCal_year() );
		sits.setLand_use ( parcel.getLand_use() );
		sits.setAcres_total ( parcel.getArea() );
		HydroBase_Supplemental_StructureIrrigSummaryTS_List.add(sits);
	}
	Message.printStatus ( 2, routine,
		"Created " + HydroBase_Supplemental_StructureIrrigSummaryTS_List.size() +
		" structure view/irrig_summary_ts records from " + supplementalParcelUseTSList.size() +
		" supplemental parcel records:" );
	for ( int i = 0; i < HydroBase_Supplemental_StructureIrrigSummaryTS_List.size(); i++ ) {
		sits = (StateDMI_HydroBase_StructureView)HydroBase_Supplemental_StructureIrrigSummaryTS_List.get(i);
		Message.printStatus ( 2, routine, "Location=" + sits.getLocationID() +
			" Year=" + sits.getCal_year() +
			" Crop=" + sits.getLand_use() +
			" Area=" + StringUtil.formatString(sits.getAcres_total(),"%.3f") );
	}
	return HydroBase_Supplemental_StructureIrrigSummaryTS_List;
}

/**
Fill a time series using a pattern.  This is a utility method to help with
several commands, to avoid duplicate code.
@param command_tag Command tag used for messaging.
@param warning_count Warning count used for messaging.
@param ts Monthly time series to fill.
@param routine The calling routine name, used for output messages.
@param id Identifier of the time series (station) to fill.
@param part_id Identifier of the time series part (station) to fill.  If
specified as null, it will not be printed to output.
@param data_type Data type to use in messages.
@param FillStart_DateTime Start date for filling.
@param FillEnd_DateTime End date for filling.
@param props properties used when filling.  Set FillFlag to a single character to flag the data when filling.
@return the updated warning count.
@exception Exception if there is an error finding the pattern time series.
*/
protected int fillTSMonthlyAverage ( String command_tag, int warning_count,
	MonthTS ts, String routine, String id, String part_id, String data_type,
	DateTime FillStart_DateTime, DateTime FillEnd_DateTime, PropList props )
throws Exception
{	MonthTSLimits average_limits = (MonthTSLimits)ts.getDataLimitsOriginal();
	// Usually want to use the location ID.  If it is not available, use what is in the time series...
	if ( (id == null) || id.equals("") ) {
		id = ts.getIdentifier().getLocation();
	}
	if ( average_limits == null ) {
		// Before warning, check whether there is actually any missing data.  Otherwise, the warning is
		// generated for no reason and confuses users
		int nMissing = TSUtil.missingCount(ts, FillStart_DateTime, FillEnd_DateTime);
		if ( nMissing > 0 ) {
			// Go ahead and warn
			String message = null;
			if ( part_id == null ) {
				message = "Unable to get average limits for \"" + id + "\".  Entire time series is missing.";
				Message.printWarning ( 2, formatMessageTag(command_tag,++warning_count), routine, message );
			}
			else {
				message = "Unable to get average limits for \"" + id +
				"\" (part " + part_id + ").  Entire time series is missing.";
				Message.printWarning ( 2, formatMessageTag(command_tag,++warning_count), routine, message );
			}
			ts.addToGenesis( "Attempted to fill with historical averages but no historical averages were available.");
			throw new Exception ( message );
		}
	}
	else {
		String nl = System.getProperty ( "line.separator" );
		if ( part_id != null ) {
			Message.printStatus ( 2, routine, "Filling missing data in " + id + " (part " + part_id +
				") diversion TS with monthly averages:" + nl + average_limits.toString() );
		}
		else {
			Message.printStatus ( 2, routine, "Filling missing data in " + id +
				" diversion TS with monthly averages:" + nl + average_limits.toString() );
		}
		String FillFlag = props.getValue("FillFlag");
		TSUtil.fillConstantByMonth ( ts, FillStart_DateTime,
			FillEnd_DateTime, average_limits.getMeanArray(), ", fill w/ hist mon ave", FillFlag, null );
	}
	return warning_count;
}

/**
Fill a time series using a pattern.  This is a utility method to help with
several commands, to avoid duplicate code.
@param ts Time series to fill.
@param routine The calling routine name, used for output messages.
@param PatternID The pattern identifier to use for filling.
@param id Identifier of the time series (station) to fill.
@param part_id Identifier of the time series part (station) to fill.  If
specified as null, it will not be printed to output.
@param data_type Data type to use in messages.
@param FillStart_DateTime Start date for filling.
@param FillEnd_DateTime End date for filling.
@param fillprops Properties for TSUtil.fillTSPattern().
@exception Exception if there is an error finding the pattern time series.
*/
protected int fillTSPattern ( TS ts, String routine, String PatternID, String id, String part_id,
	String data_type, DateTime FillStart_DateTime, DateTime FillEnd_DateTime, PropList fillprops,
	int warningLevel, int warningCount, String commandTag, CommandStatus status )
throws Exception
{	if ( part_id == null ) {
		Message.printStatus ( 2, routine, "Filling missing data in " +
		id + " " + data_type + " TS with pattern averages using \"" + PatternID + "\"" );
	}
	else {
		Message.printStatus ( 2, routine, "Filling missing data in " +
		id + " (part " + part_id + ") " + data_type +
		" TS with pattern averages using \"" + PatternID + "\"" );
	}
	// Get the pattern time series to use...
	StringMonthTS patternts = lookupFillPatternTS(PatternID);
	if ( patternts == null ) {
		if ( part_id == null ) {
			String message = "Unable to find pattern time series \"" + PatternID +
			"\" to fill \"" + ts.getIdentifierString() + "\"";
			Message.printWarning(warningLevel,
				MessageUtil.formatMessageTag( commandTag, ++warningCount), routine, message );
			status.addToLog ( CommandPhaseType.RUN,
				new CommandLogRecord(CommandStatusType.FAILURE,
					message, "Report problem to software support." ) );
			throw new Exception ( message );
		}
		else {
			String message = "Unable to find pattern time series \"" + PatternID +
			"\" to fill \"" + ts.getIdentifierString() + "\" (part " + part_id + ")";
			Message.printWarning(warningLevel,
				MessageUtil.formatMessageTag( commandTag, ++warningCount), routine, message );
			status.addToLog ( CommandPhaseType.RUN,
				new CommandLogRecord(CommandStatusType.FAILURE,
					message, "Report problem to software support." ) );
			throw new Exception ( message );
		}
	}
	TSUtil.fillPattern ( ts, patternts, FillStart_DateTime, FillEnd_DateTime, null, fillprops );
	return warningCount;
}

/**
Find an AgStats time series using the location (county) and data type (crop).
@return the found time series or null if not found.
@param county County to find.
@param crop_type Crop type to find.
*/
protected YearTS findAgStatsTS ( String county, String crop_type )
{	int size = 0;
	if ( __CUAgStatsTS_List != null ) {
		size = __CUAgStatsTS_List.size();
	}
	YearTS ts;
	for ( int i = 0; i < size; i++ ) {
		ts = (YearTS)__CUAgStatsTS_List.get(i);
		if ( ts.getLocation().equalsIgnoreCase(county) && ts.getDataType().equalsIgnoreCase(crop_type) ) {
			return ts;
		}
	}
	return null;
}

/**
Add a StateCU_BlaneyCriddle instance to the __CUBlaneyCriddle_List.  If
an existing instance is found, it is optionally replaced and added to the __CUBlaneyCriddle_match_List
so that a warning can be printed using warnAboutDataMatches().
@param kbc StateCU_BlaneyCriddle instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUBlaneyCriddle ( StateCU_BlaneyCriddle kbc, boolean replace )
{	String id = kbc.getName();

	int pos = StateCU_Util.indexOfName ( __CUBlaneyCriddle_List, kbc.getName() );
	if ( pos >= 0 ) {
		// The StateCU_BlaneyCriddle is already in the list...
		__CUBlaneyCriddle_match_List.add(id);
		if ( replace ) {
			__CUBlaneyCriddle_List.set ( pos, kbc );
		}
	}
	else {
		// Add at the end of the list...
		__CUBlaneyCriddle_List.add ( kbc );
	}
}

/**
Add a StateCU_ClimateStation instance to the __CUClimateStations_List.  If an
existing instance is found, it is optionally replaced and added to the
__CUClimateStations_match_List so that a warning can be printed using warnAboutDataMatches().
@param cli CUClimateStation instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUClimateStation ( StateCU_ClimateStation cli, boolean replace )
{	String id = cli.getID();
	int pos = StateCU_Util.indexOf(__CUClimateStation_List,id);
	if ( pos >= 0 ) {
		// The StateCU_ClimateStation is already in the list...
		__CUClimateStation_match_List.add(id);
		if ( replace ) {
			__CUClimateStation_List.set ( pos, cli );
		}
	}
	else {
		// Add at the end of the list...
		__CUClimateStation_List.add ( cli );
	}
}

/**
Add a StateCU_CropCharacteristics instance to the __CUCropCharacteristics_List.  If
an existing instance is found, it is optionally replaced and added to the __CUCropCharacteristics_match_List
so that a warning can be printed using warnAboutDataMatches().
@param cch StateCU_CropCharacteristics instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUCropCharacteristics ( StateCU_CropCharacteristics cch, boolean replace )
{	String id = cch.getName();	// Name is used because ID is the numeridal crop ID that is no longer used.

	int pos = StateCU_Util.indexOfName(__CUCropCharacteristics_List, id );
	if ( pos >= 0 ) {
		// The StateCU_CropCharacteristics is already in the list...
		__CUCropCharacteristics_match_List.add(id);
		if ( replace ) {
			__CUCropCharacteristics_List.set ( pos, cch );
		}
	}
	else {
		// Add at the end of the list...
		__CUCropCharacteristics_List.add ( cch );
	}
}

/**
Add StateCU_CropPatternTS data to the __CUCropPatternTS_List.  If
an existing instance is found, it is optionally replaced and added to the
__CUCropPatternTS_match_List so that a warning can be printed using
warnAboutDataMatches().  This version is used when reading individual ID/Crop/Year
data from HydroBase or other sources, where single values are found.
The parcel data are also stored with the time series, for later data filling.
@param id CULocation identifier.
@param part_id The source ID for the data, which may be the same location or
part of a collection.  If null or blank is passed, the main "id" is used for messages.
@param cal_year Year for crop data.
@param parcel_id Parcel identifier for the calendar year.
@param crop_name Name of the crop.
@param total_acres Total acres for the crop (all irrigation methods).
@param datetime1 Start of period for crops - used if a new time series is added.
@param datetime2 End of period for crops - used if a new time series is added.
@param replace If 0, an existing data value is replaced if found.  If -1,
the original instance is used.  If 1, the value is added to the previous value (this is used for aggregates).
@return the time series that was modified.
*/
protected StateCU_CropPatternTS findAndAddCUCropPatternTSValue ( String id, String part_id,	int cal_year,
	int parcel_id, String crop_name, double total_acres, DateTime datetime1, DateTime datetime2,
	String units, int replace ) // TODO SAM 2009-02-12 Evaluate , String irrigationMethod, String supplyType )
{	// First see if there is a matching instance for the CU location...
	int pos = StateCU_Util.indexOf ( __CUCropPatternTS_List, id);
	int dl = 1;
	StateCU_CropPatternTS cds = null;
	YearTS yts = null;
	if ( (part_id == null) || (part_id.length() == 0) ) {
		// No parts, use the main identifier...
		part_id = id;
	}
	else {
		part_id = "part:" + part_id;
	}
	if ( pos < 0 ) {
		// Add at the end of the list...
		cds = new StateCU_CropPatternTS ( id, datetime1, datetime2, units );
		__CUCropPatternTS_List.add ( cds );
	}
	else {
		cds = (StateCU_CropPatternTS)__CUCropPatternTS_List.get(pos);
	}
	// The StateCU_CropPatternTS is in the list.  Now check to see if the
	// crop is in the list of time series...
	yts = cds.getCropPatternTS ( crop_name );
	if ( yts == null ) {
		// Add the crop time series...
		yts = cds.addTS ( crop_name, true );
	}
	// Now check to see if there is an existing value...
	__temp_DateTime.setYear ( cal_year );
	double val = yts.getDataValue ( __temp_DateTime );
	boolean do_store_parcel = true;	// Whether to store raw parcel data
	if ( yts.isDataMissing(val) ) {
		// Value is missing so set...
		if ( Message.isDebugOn ) {
			Message.printDebug ( dl, "", "Initializing " + id + " from " + part_id + " " +
			cal_year + " " + crop_name + " to " + StringUtil.formatString(total_acres,"%.4f") );
		}
		yts.setDataValue ( __temp_DateTime, total_acres );
	}
	else {
		// Value is not missing.  Need to either set or add to it...
		__CUCropPatternTS_match_List.add ( id + "-" + cal_year + "-" + crop_name );
		if ( replace == 0 ) {
			if ( Message.isDebugOn ) {
				Message.printDebug ( dl, "", "Replacing " + id + " from " + part_id + " " +
				cal_year + " " + crop_name + " with " + StringUtil.formatString(total_acres,"%.4f") );
			}
			yts.setDataValue ( __temp_DateTime, total_acres );
			do_store_parcel = false;
			// FIXME SAM 2007-05-18 Evaluate whether need to save observations.
		}
		else if ( replace == 1 ) {
			if ( Message.isDebugOn ) {
				Message.printDebug ( dl, "", "Adding " + id + " from " + part_id + " " +
				cal_year + " " + crop_name + " + " + total_acres + " = " +
				StringUtil.formatString( (val + total_acres), "%.4f") );
			}
			yts.setDataValue ( __temp_DateTime, val + total_acres );
		}
	}
	if ( do_store_parcel ) {
		// Save the parcel information so that it can be used to fill later with water rights.
		StateCU_Parcel parcel = new StateCU_Parcel ();
		parcel.setID( "" + parcel_id );
		parcel.setYear( cal_year );
		parcel.setCrop( crop_name );
		parcel.setArea( total_acres );
		parcel.setAreaUnits ( units );
		/* TODO SAM 2009-02-12 Evaluate whether needed - may have mutiple supply types
		if ( irrigationMethod != null ) {
			parcel.setIrrigationMethod ( irrigationMethod );
		}
		if ( supplyType != null ) {
			parcel.setSupplyType ( supplyType );
		}
		*/
		cds.addParcel ( parcel );
	}
	return cds;
}

/**
Add a StateCU_CropPatternTS instance to the __CUCropPatternTS_List.  If
an existing instance is found, it is optionally replaced and added to the __CUCropPatternTS_match_List
so that a warning can be printed using warnAboutDataMatches().
This version is used when reading data from StateCU files, where entire periods of crop data are found.
@param cch StateCU_CropPatternTS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUCropPatternTS ( StateCU_CropPatternTS cds, boolean replace )
{	String id = cds.getID();

	int pos = StateCU_Util.indexOf ( __CUCropPatternTS_List, id);
	if ( pos >= 0 ) {
		// The StateCU_CropPatternTS is already in the list...
		__CUCropPatternTS_match_List.add(id);
		if ( replace ) {
			__CUCropPatternTS_List.set ( pos, cds );
		}
	}
	else {
		// Add at the end of the list...
		__CUCropPatternTS_List.add ( cds );
	}
}

/**
Add a StateCU_IrrigationPracticeTS instance to the __CUIrrigationPracticeTS_List.  If
an existing instance is found, it is optionally replaced and added to the
__CUIrrigationPracticeTS_match_List
so that a warning can be printed using warnAboutDataMatches().
This version is used when reading data from StateCU files, where entire periods of parameter data are found.
@param ipy StateCU_IrrigationPracticeTS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUIrrigationPracticeTS ( StateCU_IrrigationPracticeTS ipy, boolean replace )
{	String id = ipy.getID();

	int pos = StateCU_Util.indexOf ( __CUIrrigationPracticeTS_List, id );
	if ( pos >= 0 ) {
		// The StateCU_IrrigationPracticeTS is already in the list...
		__CUIrrigationPracticeTS_match_List.add(id);
		if ( replace ) {
			__CUIrrigationPracticeTS_List.set ( pos, ipy );
		}
	}
	else {
		// Add at the end of the list...
		__CUIrrigationPracticeTS_List.add ( ipy );
	}
}

/**
Add a StateCU_Location instance to the __CULocation_List.  If an existing
instance is found, it is optionally replaced and added to the
__CULocation_match_List so that a warning can be printed using warnAboutDataMatches().
@param cu_loc CULocation instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCULocation ( StateCU_Location cu_loc, boolean replace )
{	String id = cu_loc.getID();

	int pos = StateCU_Util.indexOf(__CULocation_List, cu_loc.getID());
	if ( pos >= 0 ) {
		// The StateCU_Location is already in the list...
		__CULocation_match_List.add(id);
		if ( replace ) {
			__CULocation_List.set ( pos, cu_loc );
		}
	}
	else {
		// Add at the end of the list...
		__CULocation_List.add ( cu_loc );
	}
}

/**
Add a StateCU_Parcel instance to the __CUParcel_Map.
Because parcels may be referenced by more than one supply (ditch or well),
adding a second time is ignored.
If supply data exist for the parcel, they are added if not already added
by calling the parcel.addSupply() method,
which only adds a supply if not matched.
@param parcel parcel instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
This should only be used with commands that correct data, such as a set command.
@param routine Routine to use for logging.
@param messagePrefix Prefix for message line, for example spaces that align the message.
@return true if the parcel was added, false if not (because already added).
*/
protected boolean findAndAddCUParcel ( StateCU_Parcel parcel, boolean replace, String routine, String messagePrefix, List<String> problems )
{ 
	// Unique key is year and parcel ID.  Parcel ID contains the district.
	String key = parcel.getYear() + "-" + parcel.getID();
	StateCU_Parcel parcelFound = __CUParcel_Map.get(key);
	String message;
	// Use debug to increase logging messages
	boolean debug = Message.isDebugOn;
	boolean didAdd = false;
	if ( parcelFound != null ) {
		// The StateCU_Parcel is already in the hashmap...
		//__CUParcel_match_List.add(id);
		if ( replace ) {
			// TODO smalers 2020-11-08 change from a warning when set commands are added for parcel data
			message = messagePrefix + "Found existing parcel for year " + parcel.getYear() +
				", parcelId=" + parcel.getID() + " - replacing previous global parcel using key: " + key;
			problems.add(message);
			__CUParcel_Map.put ( key, parcel );
			didAdd = true;
		}
		else {
			Message.printStatus(2,routine,messagePrefix + "Parcel previously added to global list using key: " + key );
			// Don't want to replace because will lose previous supply relationships.
			// - leave the parcel as is but make sure the main parts are the same
			// - parcel year and ID must match since they are in the hash map key
			// - this should never happen and is an error
			if ( !parcel.getCrop().equals(parcelFound.getCrop()) ) {
				message = messagePrefix +
    	    	    "Existing parcel for year " + parcel.getYear() + ", parcelId=" + parcel.getID() +
    	    	    " has different crop (" + parcelFound.getCrop() + "/" + parcel.getCrop() + ")";
				Message.printWarning ( 3, routine, message );
				problems.add(message);
			}
			if ( !parcel.getIrrigationMethod().equals(parcelFound.getIrrigationMethod()) ) {
				message = messagePrefix +
    	    	    "Existing parcel for year " + parcel.getYear() + ", parcelId=" + parcel.getID() +
    	    	    " has different irrigation method (" + parcelFound.getIrrigationMethod() + "/" + parcel.getIrrigationMethod() + ")";
				Message.printWarning ( 3, routine, message );
				problems.add(message);
			}
			if ( parcel.getArea() != parcelFound.getArea() ) {
				// Try an exact comparison but may need to allow for tolerance.
				message = messagePrefix +
    	    	    "Existing parcel for year " + parcel.getYear() + ", parcelId=" + parcel.getID() +
    	    	    " has different area (" + parcelFound.getArea() + "/" + parcel.getArea() + ")";
				Message.printWarning ( 3, routine, message );
				problems.add(message);
			}

			// Add supply if does not exist.
			// - won't be added if it already exists for the parcel
			for ( StateCU_Supply supply : parcel.getSupplyList() ) {
				parcel.addSupply(supply);
			}
			didAdd = false;
		}
	}
	else {
		// Parcel was not found in the list.  Add to the hashmap.
		__CUParcel_Map.put ( key, parcel );
		if ( debug ) {
			Message.printStatus(2,routine,messagePrefix + "Adding parcel to global list using key: " + key );
		}
		didAdd = true;
	}
	return didAdd;
}

/**
Add a time series instance to the __SMConsumptiveWaterRequirementTSMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the
__SMConsumptiveWaterRequirementTSMonthly_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMConsumptiveWaterRequirementTSMonthly ( MonthTS ts, boolean replace )
{	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMConsumptiveWaterRequirementTSMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMConsumptiveWaterRequirementTSMonthly_match_List.add(id);
		if ( replace ) {
			__SMConsumptiveWaterRequirementTSMonthlyList.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMConsumptiveWaterRequirementTSMonthlyList.add ( ts );
	}
}

/**
Add a StateCU_PenmanMonteith instance to the __CUPenmanMonteith_List.  If
an existing instance is found, it is optionally replaced and added to the __CUPenmanMonteith_match_List
so that a warning can be printed using warnAboutDataMatches().
@param kpm StateCU_PenmanMonteith instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddCUPenmanMonteith ( StateCU_PenmanMonteith kpm, boolean replace )
{	String id = kpm.getName();

	int pos = StateCU_Util.indexOfName ( __CUPenmanMonteith_List, kpm.getName() );
	if ( pos >= 0 ) {
		// The StateCU_PenmanMonteith is already in the list...
		__CUPenmanMonteith_match_List.add(id);
		if ( replace ) {
			__CUPenmanMonteith_List.set ( pos, kpm );
		}
	}
	else {
		// Add at the end of the list...
		__CUPenmanMonteith_List.add ( kpm );
	}
}

/**
Add a StateMod_DelayTable instance to the __SMDelayTable_List.  If
an existing instance is found, it is optionally replaced and added to the __SMDelayTable_match_List
so that a warning can be printed using warnAboutDataMatches().
@param dly StateMod_DelayTable instance to be added.
@param interval TimeInterval.MONTH or TimeInterval.DAY.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDelayTable ( StateMod_DelayTable dly, int interval, boolean replace )
{	String id = dly.getID();

	List<StateMod_DelayTable> delay_List = __SMDelayTableMonthlyList;
	List<String> match_List = __SMDelayTableMonthly_match_List;
	if ( interval == TimeInterval.DAY ) {
		delay_List = __SMDelayTableDailyList;
	}
	int pos = StateMod_Util.indexOf( delay_List, id );
	if ( pos >= 0 ) {
		// The StateMod_DelayTable is already in the list...
		match_List.add(id);
		if ( replace ) {
			delay_List.set ( pos, dly );
		}
	}
	else {
		// Add at the end of the list...
		delay_List.add ( dly );
	}
}

/**
Add a StateMod demand time series (monthly) instance to the __SMDemandTSMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the __SMDemandTSMonthly_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDemandTSMonthly ( MonthTS ts, boolean replace )
{	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMDemandTSMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMDemandTSMonthly_match_List.add(id);
		if ( replace ) {
			__SMDemandTSMonthlyList.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMDemandTSMonthlyList.add ( ts );
	}
}

/**
Add a StateMod_Diversion instance to the __SMDiversion_List.  If
an existing instance is found, it is optionally replaced and added to the __SMDiversion_match_List
so that a warning can be printed using warnAboutDataMatches().
@param div StateMod_Diversion instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDiversion ( StateMod_Diversion div, boolean replace )
{	String id = div.getID();

	int pos = StateMod_Util.indexOf( __SMDiversionStationList, id );
	if ( pos >= 0 ) {
		// The StateMod_Diversion is already in the list...
		__SMDiversion_match_List.add(id);
		if ( replace ) {
			__SMDiversionStationList.set ( pos, div );
		}
	}
	else {
		// Add at the end of the list...
		__SMDiversionStationList.add ( div );
	}
}

/**
Add a StateMod_DiversionRight instance to the __SMDiversionRight_List.  If
an existing instance is found, it is optionally replaced and added to the __SMDiversionRight_match_List
so that a warning can be printed using warnAboutDataMatches().
@param divr StateMod_DiversionRight instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDiversionRight ( StateMod_DiversionRight divr, boolean replace )
{	String id = divr.getID(), routine = "StateDMI_Processor.findAndAddSMDiversionRight";

	int pos = StateMod_Util.indexOf( __SMDiversionRightList, id );
	if ( pos >= 0 ) {
		// The StateMod_DiversionRight is already in the list...
		__SMDiversionRight_match_List.add(id);
		if ( replace ) {
			__SMDiversionRightList.set ( pos, divr );
		}
	}
	else {
		// Add in sorted order...
		pos = StateMod_Util.findWaterRightInsertPosition(__SMDiversionRightList, divr );
		if ( pos < 0 ) {
			// Insert at the end...
			Message.printStatus ( 2, routine, "Cannot determine insert position for right \""
			+ divr.getID() + "\" adding at end." );
			__SMDiversionRightList.add ( divr );
		}
		else {
			// Do the insert at the given location...
			__SMDiversionRightList.add ( pos, divr );
		}
	}
}

/**
Add a StateMod diversion time series (monthly) instance to the __SMDiversionTSMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the
__SMDiversionTSMonthly_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDiversionTSMonthly ( MonthTS ts, boolean replace )
{
	if( ts == null ) {
		return;
	}
	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMDiversionTSMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMDiversionTSMonthly_match_List.add(id);
		if ( replace ) {
			__SMDiversionTSMonthlyList.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMDiversionTSMonthlyList.add ( ts );
	}
}

/**
Add a StateMod diversion time series (monthly) instance to the
__SMDiversionTSMonthly2_List.  The copy (clone) of the time series should be made before calling this method.
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMDiversionTSMonthly2 ( MonthTS ts, boolean replace )
{
	if ( ts == null ) {
		return;
	}
	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMDiversionTSMonthly2List, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		if ( replace ) {
			__SMDiversionTSMonthly2List.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMDiversionTSMonthly2List.add ( ts );
	}
}

/**
Add a StateMod_InstreamFlow instance to the __SMInstreamFlow_List.  If
an existing instance is found, it is optionally replaced and added to the __SMInstreamFlow_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ifs StateMod_InstreamFlow instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMInstreamFlow ( StateMod_InstreamFlow ifs, boolean replace )
{	String id = ifs.getID();

	int pos = StateMod_Util.indexOf( __SMInstreamFlowStationList, id );
	if ( pos >= 0 ) {
		// The StateMod_InstreamFlow is already in the list...
		__SMInstreamFlow_match_List.add(id);
		if ( replace ) {
			__SMInstreamFlowStationList.set ( pos, ifs );
		}
	}
	else {
		// Add at the end of the list...
		__SMInstreamFlowStationList.add ( ifs );
	}
}

/**
Add a StateMod instream flow demand time series (average monthly) instance to the
__SMInstreamFlowDemandTSAverageMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the list
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMInstreamFlowDemandTSAverageMonthly ( MonthTS ts, boolean replace )
{	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMInstreamFlowDemandTSAverageMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMInstreamFlowDemandTSAverageMonthly_match_List.add(id);
		if ( replace ) {
			__SMInstreamFlowDemandTSAverageMonthlyList.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMInstreamFlowDemandTSAverageMonthlyList.add ( ts );
	}
}

/**
Add a StateMod_InstreamFlowRight instance to the __SMInstreamFlowRight_List.
If an existing instance is found, it is optionally replaced and added to the __SMInstreamFlowRight_match_List
so that a warning can be printed using warnAboutDataMatches().
If the right is not found, it is added in alphabetical order.
@param ifr StateMod_InstreamFlowRight instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMInstreamFlowRight ( StateMod_InstreamFlowRight ifr, boolean replace )
{	String id = ifr.getID();
	String routine = "StateDMI_Processor.findAndAddSMInstreamFlowRight";

	int pos = StateMod_Util.indexOf( __SMInstreamFlowRightList, id );
	if ( pos >= 0 ) {
		// The StateMod_InstreamFlowRight is already in the list...
		__SMInstreamFlowRight_match_List.add(id);
		if ( replace ) {
			__SMInstreamFlowRightList.set ( pos, ifr );
		}
	}
	else {
		// Add in sorted order...
		pos = StateMod_Util.findWaterRightInsertPosition( __SMInstreamFlowRightList, ifr );
		if ( pos < 0 ) {
			// Insert at the end...
			Message.printStatus ( 2, routine, "Cannot determine insert position for right \""
			+ ifr.getID() + "\" adding at end." );
			__SMInstreamFlowRightList.add ( ifr );
		}
		else {
			// Do the insert at the given location...
			__SMInstreamFlowRightList.add (pos, ifr);
		}
	}
}

/**
Add a StateMod_OperationalRight instance to the __SMOperationalRight_List.  If
an existing instance is found, it is optionally replaced and added to the __SMOperationalRight_match_List
so that a warning can be printed using warnAboutDataMatches().
@param opr StateMod_OperationalRight instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMOperationalRight ( StateMod_OperationalRight opr, boolean replace )
{	String id = opr.getID();
	//String routine = "StateDMI_Processor.findAndAddSMOperationalRight";

	int pos = StateMod_Util.indexOf( __SMOperationalRightList, id );
	if ( pos >= 0 ) {
		// The StateMod_OperationalRight is already in the list...
		__SMOperationalRight_match_List.add(id);
		if ( replace ) {
			__SMOperationalRightList.set ( pos, opr );
		}
	}
	else {
		// TODO SAM 2010-12-11 Add at end since user probably wants in a certain order
		// Add in sorted order...
		//pos = StateMod_Util.findWaterRightInsertPosition(__SMOperationalRightList, opr );
		//if ( pos < 0 ) {
			// Insert at the end...
			//Message.printStatus ( 2, routine, "Cannot determine insert position for right \""
			//+ opr.getID() + "\" adding at end." );
			__SMOperationalRightList.add ( opr );
		//}
		//else {
			// Do the insert at the given location...
			//__SMOperationalRightList.add ( pos, opr );
		//}
	}
}

/**
Add a StateMod_Plan instance to the __SMPlan_List.  If
an existing instance is found, it is optionally replaced and added to the __SMPlan_match_List
so that a warning can be printed using warnAboutDataMatches().
@param plan StateMod_Well instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMPlan ( StateMod_Plan plan, boolean replace )
{	String id = plan.getID();

	int pos = StateMod_Util.indexOf( __SMPlanList, id );
	if ( pos >= 0 ) {
		// The StateMod_Plan is already in the list...
		__SMPlan_match_List.add(id);
		if ( replace ) {
			__SMPlanList.set ( pos, plan );
		}
	}
	else {
		// Add at the end of the list...
		__SMPlanList.add ( plan );
	}
}

// TODO SAM 2011-01-02 Add based on multiple identifiers
/**
Add a StateMod_Plan_WellAugmentation instance to the __SMPlanWellAugmentation_List.  Currently this always
adds at the end.
@param wellAug StateMod_Plan_WellAugmentation instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMPlanWellAugmentation ( StateMod_Plan_WellAugmentation wellAug, boolean replace )
{	//String id = wellAug.getID();

/*
	int pos = StateMod_Util.indexOf( __SMPlanList, id );
	if ( pos >= 0 ) {
		// The StateMod_Plan is already in the list...
		__SMPlan_match_List.add(id);
		if ( replace ) {
			__SMPlanList.set ( pos, wellAug );
		}
	}
	else {*/
		// Add at the end of the list...
		__SMPlanWellAugmentationList.add ( wellAug );
	//}
}

//TODO SAM 2011-01-02 Add based on multiple identifiers
/**
Add a StateMod_ReturnFlow instance to the __SMPlanReturn_List.  Currently this always
adds at the end.
@param planReturn StateMod_ReturnFlow instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMPlanReturn ( StateMod_ReturnFlow planReturn, boolean replace )
{	//String id = wellAug.getID();

/*
	int pos = StateMod_Util.indexOf( __SMPlanList, id );
	if ( pos >= 0 ) {
		// The StateMod_Plan is already in the list...
		__SMPlan_match_List.add(id);
		if ( replace ) {
			__SMPlanList.set ( pos, wellAug );
		}
	}
	else {*/
		// Add at the end of the list...
		__SMPlanReturnList.add ( planReturn );
	//}
}

/**
Add a StateMod_PrfGageData instance to the __SMPrfGageData_List.  If an
existing instance is found, it is optionally replaced and added to the
__SMPrfGageData_match_List so that a warning can be printed using warnAboutDataMatches().
@param prf StateMod_PrfGageData instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
@return true if the location was matched, false if not.
*/
protected boolean findAndAddSMPrfGageData ( StateMod_PrfGageData prf, boolean replace )
{	String id = prf.getID();

	int pos=StateMod_Util.indexOf(__SMPrfGageData_List,id);
	if ( pos >= 0 ) {
		// The StateMod_PrfGageData is already in the list...
		__SMPrfGageData_match_List.add(id);
		if ( replace ) {
			__SMPrfGageData_List.set ( pos, prf );
		}
		return true;
	}
	else {
		// Add at the end of the list...
		__SMPrfGageData_List.add ( prf );
		return false;
	}
}

/**
Add a StateMod_Reservoir instance to the __SMReservoir_List.  If
an existing instance is found, it is optionally replaced and added to the __SMReservoir_match_List
so that a warning can be printed using warnAboutDataMatches().
@param div StateMod_Reservoir instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMReservoir ( StateMod_Reservoir res, boolean replace )
{	String id = res.getID();

	int pos = StateMod_Util.indexOf( __SMReservoirStationList, id );
	if ( pos >= 0 ) {
		// The StateMod_Reservoir is already in the list...
		__SMReservoir_match_List.add(id);
		if ( replace ) {
			__SMReservoirStationList.set ( pos, res );
		}
	}
	else {
		// Add at the end of the list...
		__SMReservoirStationList.add ( res );
	}
}

//TODO SAM 2011-01-02 Add based on multiple identifiers
/**
Add a StateMod_ReturnFlow instance to the __SMReservoirReturn_List.  Currently this always
adds at the end.
@param resReturn StateMod_ReturnFlow instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMReservoirReturn ( StateMod_ReturnFlow resReturn, boolean replace )
{	//String id = wellAug.getID();

/*
	int pos = StateMod_Util.indexOf( __SMPlanList, id );
	if ( pos >= 0 ) {
		// The StateMod_Plan is already in the list...
		__SMPlan_match_List.add(id);
		if ( replace ) {
			__SMPlanList.set ( pos, wellAug );
		}
	}
	else {*/
		// Add at the end of the list...
		__SMReservoirReturnList.add ( resReturn );
	//}
}

/**
Add a StateMod_ReservoirRight instance to the __SMReservoirRight_List.  If
an existing instance is found, it is optionally replaced and added to the __SMReservoirRight_match_List
so that a warning can be printed using warnAboutDataMatches().
@param resr StateMod_ReservoirRight instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMReservoirRight ( StateMod_ReservoirRight resr, boolean replace )
{	String id = resr.getID(), routine = "StateDMI_Processor.findAndAddSMReservoirRight";

	int pos = StateMod_Util.indexOf( __SMReservoirRightList, id );
	if ( pos >= 0 ) {
		// The StateMod_ReservoirRight is already in the list...
		__SMReservoirRight_match_List.add(id);
		if ( replace ) {
			__SMReservoirRightList.set ( pos, resr );
		}
	}
	else {
		// Add in sorted order...
		pos = StateMod_Util.findWaterRightInsertPosition(__SMReservoirRightList, resr );
		if ( pos < 0 ) {
			// Insert at the end...
			Message.printStatus ( 2, routine, "Cannot determine insert position for right \""
			+ resr.getID() + "\" adding at end." );
			__SMReservoirRightList.add ( resr );
		}
		else {
			// Do the insert at the given location...
			__SMReservoirRightList.add ( pos, resr );
		}
	}
}

/**
Add a StateMod_RiverNetworkNode instance to the __SMRiverNetworkNode_List.  If
an existing instance is found, it is optionally replaced and added to the __SMRiverNetworkNode_match_List
so that a warning can be printed using warnAboutDataMatches().
@param rin StateMod_RiverNetworkNode instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMRiverNetworkNode (	StateMod_RiverNetworkNode rin, boolean replace )
{	String id = rin.getID();

	int pos = StateMod_Util.indexOf( __SMRiverNetworkNode_List, id );
	if ( pos >= 0 ) {
		// The StateMod_RiverNetworkNode is already in the list...
		__SMRiverNetworkNode_match_List.add(id);
		if ( replace ) {
			__SMRiverNetworkNode_List.set ( pos, rin );
		}
	}
	else {
		// Add at the end of the list...
		__SMRiverNetworkNode_List.add ( rin );
	}
}

/**
Add a StateMod_StreamEstimate instance to the __SMStreamEstimate_List.  If
an existing instance is found, it is optionally replaced and added to the __SMStreamEstimate_match_List
so that a warning can be printed using warnAboutDataMatches().
@param estimate StateMod_StreamEstimate instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMStreamEstimate (	StateMod_StreamEstimate estimate, boolean replace )
{	String id = estimate.getID();

	int pos = StateMod_Util.indexOf( __SMStreamEstimateStationList, id );
	if ( pos >= 0 ) {
		// The StateMod_StreamEstimate is already in the list...
		__SMStreamEstimate_match_List.add(id);
		if ( replace ) {
			__SMStreamEstimateStationList.set ( pos, estimate );
		}
	}
	else {
		// Add at the end of the list...
		__SMStreamEstimateStationList.add ( estimate );
	}
}

/**
Add a StateMod_StreamEstimate_Coefficients instance to the
__SMStreamEstimateCoefficients_List.  If an existing instance is found, it is
optionally replaced and added to the __SMStreamEstimateCoefficients_match_List
so that a warning can be printed using warnAboutDataMatches().
@param rib StateMod_StreamEstimate_Coefficients instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMStreamEstimateCoefficients ( StateMod_StreamEstimate_Coefficients rib, boolean replace )
{	String id = rib.getID();

	int pos=StateMod_Util.indexOf(__SMStreamEstimateCoefficients_List,id);
	if ( pos >= 0 ) {
		// The StateMod_StreamEstimate_Coefficients is already in the list...
		__SMStreamEstimateCoefficients_match_List.add(id);
		if ( replace ) {
			__SMStreamEstimateCoefficients_List.set ( pos, rib );
		}
	}
	else {
		// Add at the end of the list...
		__SMStreamEstimateCoefficients_List.add ( rib );
	}
}

/**
Add a StateMod_StreamGage instance to the __SMStreamGage_List.  If
an existing instance is found, it is optionally replaced and added to the __SMStreamGage_match_List
so that a warning can be printed using warnAboutDataMatches().
@param gage StateMod_StreamGage instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMStreamGage (StateMod_StreamGage gage, boolean replace )
{	String id = gage.getID();

	int pos = StateMod_Util.indexOf( __SMStreamGageStationList, id );
	if ( pos >= 0 ) {
		// The StateMod_StreamGage is already in the list...
		__SMStreamGage_match_List.add(id);
		if ( replace ) {
			__SMStreamGageStationList.set ( pos, gage );
		}
	}
	else {
		// Add at the end of the list...
		__SMStreamGageStationList.add ( gage );
	}
}

/**
Add a StateMod_Well instance to the __SMWell_List.  If
an existing instance is found, it is optionally replaced and added to the __SMWell_match_List
so that a warning can be printed using warnAboutDataMatches().
@param well StateMod_Well instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMWell ( StateMod_Well well, boolean replace )
{	String id = well.getID();

	int pos = StateMod_Util.indexOf( __SMWellList, id );
	if ( pos >= 0 ) {
		// The StateMod_Well is already in the list...
		__SMWell_match_List.add(id);
		if ( replace ) {
			__SMWellList.set ( pos, well );
		}
	}
	else {
		// Add at the end of the list...
		__SMWellList.add ( well );
	}
}

/**
Add a StateMod well demand time series (monthly) instance to the __SMWellDemandTSMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the
__SMWellDemandTSMonthly_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMWellDemandTSMonthly ( MonthTS ts, boolean replace )
{	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMWellDemandTSMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMWellDemandTSMonthly_match_List.add(id);
		if ( replace ) {
			__SMWellDemandTSMonthlyList.set ( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMWellDemandTSMonthlyList.add ( ts );
	}
}

/**
Add a StateMod well historical pumping time series (monthly) instance to the
__SMWellHistoricalPumpingTSMonthly_List.  If
an existing instance is found, it is optionally replaced and added to the
__SMWellHistoricalPumpingTSMonthly_match_List
so that a warning can be printed using warnAboutDataMatches().
@param ts TS instance to be added.
@param replace If true, an existing instance is replaced if found.  If false, the original instance is used.
*/
protected void findAndAddSMWellHistoricalPumpingTSMonthly(MonthTS ts, boolean replace )
{	String id = ts.getLocation();

	int pos = TSUtil.indexOf( __SMWellHistoricalPumpingTSMonthlyList, id, "Location", null, 1 );
	if ( pos >= 0 ) {
		// The ts is already in the list...
		__SMWellHistoricalPumpingTSMonthly_match_List.add(id);
		if ( replace ) {
			__SMWellHistoricalPumpingTSMonthlyList.set( pos, ts );
		}
	}
	else {
		// Add at the end of the list...
		__SMWellHistoricalPumpingTSMonthlyList.add ( ts );
	}
}

/**
Find a CU Location given a ditch ID and collection information - therefore find
a well-only CU Location.  Do not combine this with findCULocationForParcel()
because the parcel_id could conceivably conflict with the ditch ID!
@return the StateCU_Location that is a collection that includes the parcel.
@param ditch_id the Ditch id to match, fully expanded WDID.
@param CULocations_List the list of StateCU_Location to search.
*/
// TODO SAM 2007-02-18 Evaluate whether needed
/*
protected StateCU_Location findCULocationForDitch ( String ditch_id, Vector CULocations_Vector )
{	// Loop through the CU Locations...

	StateCU_Location culoc = null;
	int size = 0;
	if ( CULocations_Vector != null ) {
		size = CULocations_Vector.size();
	}
	Vector partids;
	int ic;
	int collection_size;
	for ( int i = 0; i < size; i++ ) {
		culoc = (StateCU_Location)CULocations_Vector.get(i);
		if ( !culoc.isCollection() ) {
			continue;
		}
		// Currently ditches have same collection for full period...
		if ( (partids=culoc.getCollectionPartIDs(0))==null){
			continue;
		}
		// Else have a list of IDs that need to be searched...
		collection_size = partids.size();
		for ( ic = 0; ic < collection_size; ic++ ) {
			if ( ditch_id.equalsIgnoreCase(
				(String)partids.get(ic)) ) {
				// Found the matching CU Location....
				return culoc;
			}
		}
	}
	return null;
}
*/

/**
Find a CU Location given a parcel and collection information - therefore find
a well-only CU Location.  Do not combine this with findCULocationForDitch()
because the parcel_id could conceivably conflict with the ditch ID!
@return the StateCU_Location that is a collection that includes the parcel.
@param parcel_id the Parcel id to match.
@param CULocations_Vector the Vector of StateCU_Location to search.
@param div The division - used to uniquely identify the parcel.
@param parcelid_year The year to use for parcel IDs in the collection.
*/
// TODO SAM 2007-02-18 Evaluate if needed
/*
private StateCU_Location findCULocationForParcel (	int parcel_id,
						Vector CULocations_Vector,
						int div, int parcelid_year )
{	// Loop through the CU Locations...

	StateCU_Location culoc = null;
	int size = 0;
	if ( CULocations_Vector != null ) {
		size = CULocations_Vector.size();
	}
	Vector partids;
	int ic;
	int collection_size;
	String parcelid_string = "" + parcel_id;	// ID as string.
	for ( int i = 0; i < size; i++ ) {
		culoc = (StateCU_Location)CULocations_Vector.get(i);
		if ( !culoc.isCollection() ) {
			continue;
		}
		if ( culoc.getCollectionDiv() != div ) {
			continue;
		}
		if ( (partids=culoc.getCollectionPartIDs(parcelid_year))==null){
			continue;
		}
		// Else have a list of IDs that need to be searched...
		collection_size = partids.size();
		for ( ic = 0; ic < collection_size; ic++ ) {
			if ( parcelid_string.equalsIgnoreCase(
				(String)partids.get(ic)) ) {
				// Found the matching CU Location....
				return culoc;
			}
		}
	}
	return null;
}
*/

/**
Find parcel from a Vector of HydroBase_ParcelUseTS.
@return parcel from a Vector of HydroBase_ParcelUseTS, or null if not found.
@param parcelusets_Vector Vector of HydroBase_ParcelUseTS to search.
@param parcel_id Parcel id to search for.
@param div Division for data.
@param year Year to search for.
*/
// TODO SAM 2007-02-18 Review after StateCU review
/*private HydroBase_ParcelUseTS findParcelUseTS (	Vector parcelusets_Vector,
						int parcel_id,
						int div, int year )
{	if ( parcelusets_Vector == null ) {
		return null;
	}
	int size = parcelusets_Vector.size();
	HydroBase_ParcelUseTS pts = null;
	for ( int i = 0; i < size; i++ ) {
		pts = (HydroBase_ParcelUseTS)parcelusets_Vector.get(i);
		if (	(pts.getParcel_id() == parcel_id) &&
			(pts.getDiv() == div) &&
			(pts.getCal_year() == year) ) {
			return pts;
		}
	}
	return null;
}
*/

// TODO smalers 2019-05-29 decide whether to keep or delete method
/**
Find parcels from a list of HydroBase_ParcelUseTS.
@return parcels from a list of HydroBase_ParcelUseTS.
@param parcelusets_List list of HydroBase_ParcelUseTS to search.
@param div Division for data.
@param ids_array Array of parcel identifiers to search for.
@param datetime1 Start for query.
@param datetime2 End for query.
*/
@SuppressWarnings("unused")
private List<HydroBase_ParcelUseTS> findParcelUseTSListForParcelList(
		List<HydroBase_ParcelUseTS> parcelusets_List, int div,
		int [] ids_array, DateTime datetime1, DateTime datetime2 )
{	List<HydroBase_ParcelUseTS> crop_patterns = new ArrayList<HydroBase_ParcelUseTS>();
	// For debugging...
	/*
	List ids_Vector = new ArrayList();
	if ( ids_array != null ) {
		for ( int i = 0; i < ids_array.length; i++ ) {
			ids_Vector.add ( "" + ids_array[i] );
		}
	}
	Message.printStatus ( 1, "", "Looking for parcel_use_ts for ids:" +
			ids_Vector );
	*/
	int size = 0;
	if ( parcelusets_List != null ) {
		size = parcelusets_List.size();
	}
	HydroBase_ParcelUseTS pts;
	int iid;
	int pts_id;
	int year1 = -5000;	// To simplify comparison
	if ( datetime1 != null) {
		year1 = datetime1.getYear();
	}
	int year2 = 5000;
	if ( datetime2 != null) {
		year2 = datetime2.getYear();
	}
	int pts_year;
	for ( int i = 0; i < size; i++ ) {
		pts = parcelusets_List.get(i);
		if ( div != pts.getDiv() ) {
			continue;
		}
		// Check to see if the year is in the requested range...
		pts_year = pts.getCal_year();
		if ( (pts_year < year1) || (pts_year > year2) ) {
			continue;
		}
		// Check to see if the parcel ID is one of the requested
		// identifiers...
		pts_id = pts.getParcel_id();
		for ( iid = 0; iid < ids_array.length; iid++ ) {
			if ( ids_array[iid] == pts_id ) {
				crop_patterns.add ( pts );
			}
		}
	}
	return crop_patterns;
}

// TODO smalers 2019-05-29 need to evaluate whether to use function
/**
Find crop patterns from a list of HydroBase_StructureIrrigSummaryTS (new
is HydroBase_StructureView).
@return crop patterns from a list of HydroBase_StructureIrrigSummaryTS (new
is HydroBase_StructureView).
@param irrigsummaryts_List A list of HydroBase_StructureIrrigSummaryTS (new
is HydroBase_StructureView) to search.
@param culoc_wdids A list of identifiers for locations to match.
@param datetime1 First year to query.
@param datetime2 Last year to query.
*/
@SuppressWarnings("unused")
private List<HydroBase_StructureView> findStructureIrrigSummaryTSListForWDIDListLand_usePeriod (
	List<HydroBase_StructureView> irrigsummaryts_List, List<String> culoc_wdids,
	DateTime datetime1, DateTime datetime2 )
{	List<HydroBase_StructureView> crop_patterns = new ArrayList<>();
	int size = 0;
	if ( irrigsummaryts_List != null ) {
		size = irrigsummaryts_List.size();
	}
	HydroBase_StructureView sits;
	int iid;
	int wdids_size = 0;
	if ( culoc_wdids != null ) {
		wdids_size = culoc_wdids.size();
	}
	int year1 = -5000;	// To simplify comparison
	if ( datetime1 != null) {
		year1 = datetime1.getYear();
	}
	int year2 = 5000;
	if ( datetime2 != null) {
		year2 = datetime2.getYear();
	}
	int sits_year;
	String sits_id;
	String culoc_wdid;
	for ( int i = 0; i < size; i++ ) {
		sits = irrigsummaryts_List.get(i);
		sits_year = sits.getCal_year();
		if ( (sits_year < year1) || (sits_year > year2) ) {
			continue;
		}
		sits_id = sits.getStructure_id();
		for ( iid = 0; iid < wdids_size; iid++ ) {
			culoc_wdid = culoc_wdids.get(iid);
			if ( culoc_wdid.equalsIgnoreCase(sits_id) ) {
				crop_patterns.add ( sits );
			}
		}
	}
	return crop_patterns;
}

/**
Find parcel from a list of HydroBase_ParcelUseTS.
@return parcel from a list of HydroBase_ParcelUseTS, or null if not found.
@param struct2parcel_List List of HydroBase_StructureToParcel to search.
@param parcel_id Parcel id to search for.
@param div Division for data.
@param year Year to search for.
*/
// TODO SAM 2007-02-18 Evaluate if needed
/*
private List findStructureToParcelListForParcel (
				List struct2parcel_List,
				int parcel_id,
				int div, int year )
{	if ( struct2parcel_List == null ) {
		return null;
	}
	int size = struct2parcel_List.size();
	HydroBase_StructureToParcel stp = null;
	List stp_Vector = new ArrayList();
	for ( int i = 0; i < size; i++ ) {
		stp = struct2parcel_Vector.get(i);
		if ( (stp.getParcel_id() == parcel_id) &&
			(stp.getDiv() == div) &&
			(stp.getCal_year() == year) ) {
			stp_List.add(stp);
		}
	}
	if ( stp_List.size() == 0 ) {
		return null;
	}
	else {	return stp_List;
	}
}
*/

/**
Format a message tag for use with the Message class print methods.
The format of the string will be:
<pre>
root,count
</pre>
@param tag_root A root string to include in the tag.
@param count A count to modify the root (1+), for example, indicating the
count of warnings within a command.
*/
private String formatMessageTag ( String tag_root, int count )
{	return MessageUtil.formatMessageTag ( tag_root, count );
}

/**
Return the Command instance at the requested position.
@return The number of commands being managed by the processor
*/
public Command get( int pos )
{
	return (Command)getCommands().get(pos);
}

/**
Indicate whether cancelling processing has been requested.
@return true if cancelling has been requested.
*/
public boolean getCancelProcessingRequested ()
{
	return __cancel_processing_requested;
}

/**
Return the list of commands.
@return the list of commands.
*/
public List<Command> getCommands ()
{
	return __commandList;
}

// TODO smalers 2019-05-29 evaluate whether to keep or remove method, maybe make public
/**
Helper method to return the current list of commands as a String.
@return Text of commands that are currently in memory.
*/
@SuppressWarnings("unused")
private String getCommandsAsString()
{
	String commandStr = "";
	List<Command> commandList = getCommands();
	for ( int i = 0; i < commandList.size(); i++ ) {
		commandStr += commandList.get(i).toString() + "\n";
	}
	return commandStr;
}

/**
Return the name of the command file that is being processed.
@return the name of the command file that is being processed.
*/
public String getCommandFileName ()
{	return __commandFilename;
}

/**
Return whether output files should be created.
@return whether output files should be created.
*/
private boolean getCreateOutput ()
{
	return __create_output;
}

/**
Return the data store for the requested name, or null if not found.
@param name the data store name to match (case is ignored in the comparison)
@param dataStoreClass the class of the data store to match, useful when ensuring that the data store
is compatible with intended use - specify as null to not match class
@return the data store for the requested name, or null if not found.
*/
public DataStore getDataStoreForName ( String name, Class<? extends DataStore> dataStoreClass )
{   for ( DataStore dataStore : getDataStores() ) {
        if ( dataStore.getName().equalsIgnoreCase(name) ) {
            if ( dataStoreClass != null ) {
                //if (dataStore.getClass() == dataStoreClass ) {
                if (dataStore.getClass().equals(dataStoreClass) ) {
                    ; // Match is OK
                }
                // Also check for common base classes
                // TODO SAM 2012-01-31 Why not just use instanceof all the time?
                //else if ( (dataStoreClass == DatabaseDataStore.class) && dataStore instanceof DatabaseDataStore ) {
                else if ( dataStoreClass.isInstance(dataStore) ) {
                    ; // Match is OK
                }
                else {
                    // Does not match class
                    dataStore = null;
                }
            }
            return dataStore;
        }
    }
    return null;
}

/**
Return the list of all DataStore instances known to the processor.  These are named database
connections that correspond to input type/name for time series.  Active and inactive datastores are returned.
*/
public List<DataStore> getDataStores()
{
    return __dataStoreList;
}

/**
Return the list of all DataStore instances known to the processor.  These are named database
connections that correspond to input type/name for time series.
*/
public List<DataStore> getDataStores ( boolean activeOnly )
{
	// Get the list of all datastores...
	List<DataStore> datastoreList = __dataStoreList;
	if ( activeOnly ) {
		// Loop through and remove datastores where status != 0
		for ( int i = datastoreList.size() - 1; i >= 0; i-- ) {
			DataStore ds = datastoreList.get(i);
			if ( ds.getStatus() != 0 ) {
				datastoreList.remove(i);
			}
		}
	}
	return datastoreList;
}

/**
Return the list of data stores for the requested type (e.g., HydroBaseRestDataStore).  A non-null list
is guaranteed, but the list may be empty.  Only active datastores are returned, those that are enabled
and status is 0 (Ok).
@param dataStoreClass the data store class to match (required).
@return the list of data stores matching the requested type
*/
public List<DataStore> getDataStoresByType ( Class<? extends DataStore> dataStoreClass )
{
	return getDataStoresByType ( dataStoreClass, true );
}

/**
Return the list of data stores for the requested type (e.g., HydroBaseRestDataStore).  A non-null list
is guaranteed, but the list may be empty.
@param dataStoreClass the data store class to match (required).
@return the list of data stores matching the requested type
*/
public List<DataStore> getDataStoresByType ( Class<? extends DataStore> dataStoreClass, boolean activeOnly )
{   List<DataStore> dataStoreList = new ArrayList<DataStore>();
    for ( DataStore dataStore : getDataStores() ) {
    	// If only active are requested, then status must be 0
    	if ( activeOnly && (dataStore.getStatus() != 0) ) {
    		continue;
    	}
        // Check for exact match on class
        if ( dataStore.getClass() == dataStoreClass ) {
            dataStoreList.add(dataStore);
        }
        // Also check for common base classes
        // TODO SAM 2012-01-31 Why not just use instanceof all the time?
        else if ( (dataStoreClass == DatabaseDataStore.class) && dataStore instanceof DatabaseDataStore ) {
            dataStoreList.add(dataStore);
        }
    }
    return dataStoreList;
}

/**
 * @param cmdStr - runCommand command string
 * @return runCmdFile - Input file specified by the command
 */
protected String getFileFromRunCommand(String cmdStr)
{
	String runCmdFile = "";
	String routine = "StateDMI_Processor.getFileFromRunCommand";

	//parse the command string for the InputFile
	// Split by quotes since filename should be in quotes
	runCmdFile = cmdStr.split("\"")[1];

	// Make sure we have something and if not supply message
	if(runCmdFile.equals("") || runCmdFile == null)
		Message.printWarning(1, routine, "runCommand syntax is incorrect." +
			"The correct syntax is: runCommands(InputFile=\"commands.StateDMI\")" +
			".  The corresponding command could not be run");

	return runCmdFile;
}

// TODO smalers 2019-05-29 evaluate whether to keep or delete method
/**
Returns the getProgramHeader() text and HydroBase comments if HydroBase is being used.
@return The entire program header including StateDMI and
HydroBase information. 
*/
@SuppressWarnings("unused")
private String getFullProgramHeader()
{
	String full_header = getProgramHeader() + "\n";
	full_header += ( "Command:   " + StateDMI.PROGRAM_NAME + " " + StateDMI.getArgs() );
	if ( __hdmi != null ) {
		try {
			String [] comments = __hdmi.getVersionComments();
			for ( int i = 0; i < comments.length; i++ ) {
				if ( !comments[i].startsWith("---") ) {
					 full_header = full_header + "\n" + comments[i];
				}
			}
		}
		catch ( Exception e ) {
			Message.printWarning(2, "StateDMI_Processor.runComponentChecks",
				"Couldn't get version comments from HydroBase because:\n +" +
				e.toString());
		}
	}
	return full_header;
}

/**
Returns the current HydroBaseDMI connection.
@return HydroBaseDMI HydroBaseDMI database connection.
*/
public HydroBaseDMI getHydroBaseDMIConnection()
{
	return __hdmi;
}

/**
Returns additional parcel use data from SetParcelUseTS and SetParcelUseTSFromList commands to add to HydroBase data.
@return additional parcel use data to add to HydroBase data.
*/
private List<HydroBase_ParcelUseTS_FromSet> getHydroBaseParcelUseTSFromSetList ()
{
	return __HydroBase_ParcelUseTS_FromSet_List;
}

/**
Returns additional ParcelUseTS from 
*/
//private List<StateDMI_HydroBase_StructureView> getHydroBaseSupplementalParcelUseTSList() {
private List<HydroBase_ParcelUseTS> getHydroBaseSupplementalParcelUseTSList() {
	return __HydroBase_Supplemental_ParcelUseTS_List;
}

/**
Return the initial working directory for the processor.
@return the initial working directory for the processor.
*/
protected String getInitialWorkingDir()
{
	return __InitialWorkingDir_String;
}

/**
 * Return a parcel for year and parcel ID.
 * @return a parcel for year and parcel ID, or null if not found.
 */
public StateCU_Parcel getParcel ( int year, String parcelId ) {
	String key = "" + year + "-" + parcelId;
	return this.__CUParcel_Map.get(key);
}

/**
Returns the header for the check file.
@return String - Header to show in the check file.
*/
private String getProgramHeader()
{
	String header = "";
	String host = "host name could not be resolved";
	header = "Program:   " + StateDMI.PROGRAM_NAME + " " +
	StateDMI.PROGRAM_VERSION + "\n" +
	"User:      " + System.getProperty("user.name").trim() + "\n" +
	"Date:      " + TimeUtil.getSystemTimeString("") + "\n";
	try {
		host = InetAddress.getLocalHost().getHostName();
	} catch (UnknownHostException e) {
		Message.printWarning(3, "StateDMI_Process.getProgramHeader",
			"Host name could not be resolved");
	}
	header = header + "Host:      " + host + "\n";
	header = header + "Directory: " + IOUtil.getProgramWorkingDir();

	return header;
}

/**
Return data for a named property, required by the CommandProcessor
interface.  See the overloaded version for a list of properties that are handled.
@param prop Property to set.
@return the named property, or null if a value is not found.
*/
public Prop getProp ( String prop ) throws Exception
{	Object o = getPropContents ( prop );
	if ( o == null ) {
		return null;
	}
	else {
		// Contents will be a list, etc., so convert to a full property.
		// TODO SAM 2005-05-13 This will work seamlessly for strings
		// but may have a side-effects (conversions) for non-strings...
		Prop p = new Prop ( prop, o, o.toString() );
		return p;
	}
}

/**
Return the contents for a named property, required by the CommandProcessor
interface. Currently the following properties are handled:
<table width=100% cellpadding=10 cellspacing=0 border=2>
<tr>
<td><b>Property</b></td>	<td><b>Description</b></td>
</tr>

<tr>
<td><b>CreateOutput</b></td>
<td>Indicate if output should be created.  If True, commands that create output
should do so.  If False, the commands should be skipped.  This is used to
speed performance during initial testing.
</td>
</tr>

<tr>
<td><b>HydroBaseDMIList</b></td>
<td>A list of open HydroBaseDMI, available for reading.
Currently only one object at most will be returned.
</td>
</tr>

<tr>
<td><b>OutputYearType</b></td>
<td>The output year type.
</td>
</tr>

<tr>
<td><b>OutputEnd</b></td>
<td>The output end from the setOutputPeriod() command, as a DateTime object.
</td>
</tr>

<tr>
<td><b>OutputStart</b></td>
<td>The output start from the setOutputPeriod() command, as a DateTime object.
</td>
</tr>

<tr>
<td><b>WorkingDir</b></td>
<td>The working directory for the processor (initially the same as the
application but may be changed by commands during execution).</td>
</tr>

</table>
@return the contents for a named property, or null if a value is not found.
*/
public Object getPropContents ( String prop ) throws Exception
{
	if ( prop.equalsIgnoreCase("CreateOutput") ) {
		if ( getCreateOutput() ) {
			return new Boolean("True");
		}
		else {
			return new Boolean("False");
		}
	}
	else if ( prop.equalsIgnoreCase("CommandFileName") ) {
		return getCommandFileName();
	}
	else if ( prop.equalsIgnoreCase("CountyList") ) {
		// Get the list of counties, for use in dialogs
		List<String> countyList = new ArrayList<>();
		if ( __hdmi != null ) {
			List<HydroBase_CountyRef> countyRefList = __hdmi.getCountyRef();
			for( int i = 0; i < countyRefList.size(); i++ ) {
				countyList.add ( countyRefList.get(i).getCounty() );
			}
		}
		return countyList;
	}
	else if ( prop.equalsIgnoreCase("CUMethod_List") ) {
		// Get the list of CU methods, for use in crop characteristics
		List<String> cuMethodList = new ArrayList<>();
		if ( __hdmi != null ) {
			List<HydroBase_CUMethod> hbList = __hdmi.readCUMethodList(true);
			HydroBase_CUMethod m;
			for ( int i = 0; i < hbList.size(); i++ ) {
				m = hbList.get(i);
				cuMethodList.add ( m.getMethod_desc());
			}
		}
		return cuMethodList;
	}
	else if ( prop.equalsIgnoreCase("CUPenmanMonteithMethod_List") ) {
		// Get the list of distinct CU methods used with Penman-Montieth
		List<String> cuPenmanMonteithMethodList = new ArrayList<>();
		if ( __hdmi != null ) {
			List<HydroBase_CUPenmanMonteith> hbList = __hdmi.getPenmanMonteithCUMethod();
			for ( HydroBase_CUPenmanMonteith pm: hbList ) {
				cuPenmanMonteithMethodList.add ( pm.getMethod_desc());
			}
		}
		return cuPenmanMonteithMethodList;
	}
	else if ( prop.equalsIgnoreCase("DefaultWDIDLength") ) {
		return new Integer(__defaultWdidLength);
	}
    else if ( prop.equalsIgnoreCase("DebugLevelLogFile") ) {
        return new Integer(Message.getDebugLevel(Message.LOG_OUTPUT));
    }
    else if ( prop.equalsIgnoreCase("DebugLevelScreen") ) {
        return new Integer(Message.getDebugLevel(Message.TERM_OUTPUT));
    }
	else if ( prop.equalsIgnoreCase("HUCList") ) {
		// Get the list of HUC basin identifiers, for use in dialogs
		List<Integer> hucList = __hdmi.getHUC();
		return hucList;
	}
	else if ( prop.equalsIgnoreCase("HydroBaseDMI") ) {
		return __hdmi;
	}
	else if ( prop.equalsIgnoreCase("HydroBaseDMIList") ) {
		List<HydroBaseDMI> v = new ArrayList<>();
		v.add ( __hdmi );
		return v;
	}
	else if ( prop.equalsIgnoreCase("HydroBase_ParcelUseTS_FromSet_List") ) {
		return getHydroBaseParcelUseTSFromSetList();
	}
	else if ( prop.equalsIgnoreCase("HydroBase_SupplementalParcelUseTS_List") ||
		prop.equalsIgnoreCase("HydroBase_Supplemental_ParcelUseTS_List") ) {
		return getHydroBaseSupplementalParcelUseTSList();
		// TODO smalers 2021-01-18 go back to the original functionality since can work separately from StateDMI 5.05 parcels approach.
		//throw new RuntimeException("Need to update code to use \"HydroBase_ParcelUseTS_FromSet_List\" instead of " +
		//"\"HydroBase_SupplementalParcelUseTS_List\" or \"HydroBase_Supplemental_ParcelUseTS_List\"" );
	}
	else if ( prop.equalsIgnoreCase("InitialWorkingDir") ) {
		return getInitialWorkingDir();
	}
	else if ( prop.equalsIgnoreCase("OutputComments") ) {
		return getPropContents_OutputComments();
	}
	else if ( prop.equalsIgnoreCase("OutputEnd") ) {
		return __OutputEnd_DateTime;
	}
	else if ( prop.equalsIgnoreCase("OutputStart") ) {
		return __OutputStart_DateTime;
	}
	else if ( prop.equalsIgnoreCase("OutputYearType") ) {
		return __OutputYearType;
	}
	else if ( prop.equalsIgnoreCase("NeedToCopyDiversionHistoricalTSMonthly") ) {
		return new Boolean(__need_diversion_ts_monthly_copy);
	}
	else if ( prop.equalsIgnoreCase("StateCU_BlaneyCriddle_List") ) {
		return getStateCUBlaneyCriddleList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_CropCharacteristics_List") ) {
		return getStateCUCropCharacteristicsList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_CropPatternTS_List") ) {
		return getStateCUCropPatternTSList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_ClimateStation_List") ) {
		return getStateCUClimateStationList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_DataSet") ) {
		return __StateCU_DataSet;
	}
	else if ( prop.equalsIgnoreCase("StateCU_IrrigationPracticeTS_List") ) {
		return getStateCUIrrigationPracticeTSList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_Location_List") ) {
		return getStateCULocationList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_Parcel_List") ) {
		// This actually returns a map
		return getStateCUParcelList();
	}
	else if ( prop.equalsIgnoreCase("StateCU_PenmanMonteith_List") ) {
		return getStateCUPenmanMonteithList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DataSet") ) {
		return __StateMod_DataSet;
	}
	else if ( prop.equalsIgnoreCase("StateMod_ConsumptiveWaterRequirementTSMonthly_List") ){
		return getStateModConsumptiveWaterRequirementTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DelayTableDaily_List") ){
		return getStateModDelayTableList(TimeInterval.DAY);
	}
	else if ( prop.equalsIgnoreCase("StateMod_DelayTableMonthly_List") ){
		return getStateModDelayTableList(TimeInterval.MONTH);
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionDemandTSMonthly_List") ){
		return getStateModDiversionDemandTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionHistoricalTSMonthly_List") ){
		return getStateModDiversionHistoricalTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionHistoricalTSMonthlyCopy_List") ){
		return getStateModDiversionHistoricalTSMonthlyCopyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionRight_List") ){
		return getStateModDiversionRightList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionStation_List")){
		return getStateModDiversionStationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_InstreamFlowDemandTSAverageMonthly_List") ){
		return getStateModInstreamFlowDemandTSAverageMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_InstreamFlowRight_List") ){
		return getStateModInstreamFlowRightList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_InstreamFlowStation_List")){
		return getStateModInstreamFlowStationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_Network")){
		return getStateModNetwork();
	}
	else if ( prop.equalsIgnoreCase("StateMod_OperationalRight_List") ){
		return getStateModOperationalRightList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_PatternTSMonthly_List") ) {
		return getStateModPatternTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateModPlanList") || prop.equalsIgnoreCase("StateMod_PlanStation_List") ) {
		return getStateModPlanStationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_PlanReturn_List") ) {
		return getStateModPlanReturnList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_PlanWellAugmentation_List") ) {
		return getStateModPlanWellAugmentationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_PrfGageData_List")){
		return getStateModPrfGageDataList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_ReservoirReturn_List") ) {
		return getStateModReservoirReturnList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_ReservoirRight_List") ){
		return getStateModReservoirRightList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_ReservoirStation_List")){
		return getStateModReservoirStationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_RiverNetworkNode_List")){
		return getStateModRiverNetworkNodeList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_StreamEstimateCoefficients_List") ){
		return getStateModStreamEstimateCoefficientsList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_StreamEstimateStation_List") ){
		return getStateModStreamEstimateStationList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_StreamGageStation_List") ){
		return getStateModStreamGageStationList();
	}
	else if ( prop.equalsIgnoreCase("StateModWellList") || prop.equalsIgnoreCase("StateMod_Well_List") ||
		prop.equalsIgnoreCase("StateMod_WellStation_List") ) {
		return getStateModWellStationList();
	}
	else if ( prop.equalsIgnoreCase("StateModWellRightList") || prop.equalsIgnoreCase("StateMod_WellRight_List")) {
		return getStateModWellRightList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_WellHistoricalPumpingTSMonthly_List") ){
		return getStateModWellHistoricalPumpingTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("StateMod_WellDemandTSMonthly_List") ){
		return getStateModWellDemandTSMonthlyList();
	}
	else if ( prop.equalsIgnoreCase("TableResultsList") ) {
        return getPropContents_TableResultsList();
    }
    else if ( prop.equalsIgnoreCase("WarningLevelLogFile") ) {
        return new Integer(Message.getWarningLevel(Message.LOG_OUTPUT));
    }
    else if ( prop.equalsIgnoreCase("WarningLevelScreen") ) {
        return new Integer(Message.getWarningLevel(Message.TERM_OUTPUT));
    }
	else if ( prop.equalsIgnoreCase("WorkingDir") ) {
		return getWorkingDir();
	}
	else {
	    // Property is not one of the individual objects that have been historically
	    // maintained, but it may be a user-supplied property in the hashtable.
	    Object o = __propertyHashmap.get ( prop );
	    if ( o == null ) {
	    	// Changed on 2016-09-18 to allow null to be returned,
	    	// generally indicating that user-supplied property is being processed
    	    //String warning = "Unknown GetPropContents request \"" + propName + "\"";
    		// TODO SAM 2007-02-07 Need to figure out a way to indicate
    		// an error and pass back useful information.
    		//throw new UnrecognizedRequestException ( warning );
	    	return null;
	    }
	    else {
	        // Return the object from the hashtable
	        return o;
	    }
	}
}

/**
Handle the OutputComments property request.  This includes, for example,
the commands that are active and HydroBase version information that documents
data available for a command.
@return list of String containing comments for output.
*/
private List<String> getPropContents_OutputComments()
{
	List<String> comments = new ArrayList<>();
	// Commands.  Show the file name but all commands may be in memory.
	comments.add ( "-----------------------------------------------------------------------" );
	String commands_filename = getCommandFileName();
	if ( commands_filename == null ) {
		comments.add ( "Command file name:  COMMANDS NOT SAVED TO FILE" );
	}
	else {
	    comments.add ( "Command file name: \"" + commands_filename + "\"" );
	}
	comments.add ( "Commands: " );
	List<Command> commandList = getCommands();
	int size_commands = commandList.size();
	for ( int i = 0; i < size_commands; i++ ) {
		comments.add ( commandList.get(i).toString() );
	}
	// Save information about data sources.
	HydroBaseDMI hbdmi = getHydroBaseDMIConnection();
	List<HydroBaseDMI> hbdmiList = new ArrayList<>();
	if ( hbdmi != null ) {
		hbdmiList.add ( hbdmi );
	}
	int hsize = hbdmiList.size();
	String db_comments[] = null;
	for ( int ih = 0; ih < hsize; ih++ ) {
		hbdmi = hbdmiList.get(ih);
		if ( hbdmi != null ) {
			try {
			    db_comments = hbdmi.getVersionComments ();
			}
			catch ( Exception e ) {
				db_comments = null;
			}
		}
		if ( db_comments != null ) {
			for ( int i = 0; i < db_comments.length; i++ ) {
				comments.add(db_comments[i]);
			}
		}
	}
	return new ArrayList<>(comments);
}

/**
Handle the TableResultsList property request.
@return The table results list, as a List of DataTable.
*/
private List<DataTable> getPropContents_TableResultsList()
{
    return __TableList;
}

/**
Return the list of property names available from the processor.
These properties can be requested using getPropContents().
@return the list of property names available from the processor.
*/
public Collection<String> getPropertyNameList( boolean includeBuiltInProperties, boolean includeDynamicProperties )
{
	// Create a set that includes the above.
    TreeSet<String> set = new TreeSet<String>();
	// FIXME SAM 2008-02-15 Evaluate whether these should be in the
	// property hashtable - should properties be available before ever
	// being defined (in case they are used later) or should only defined
	// properties be available (and rely on discovery to pass to other commands)?
	// Add properties that are hard-coded.
	if ( includeBuiltInProperties ) {
	    List<String> v = new ArrayList<String>();
        v.add ( "AutoExtendPeriod" );
        v.add ( "AverageStart" );
        v.add ( "AverageEnd" );
        v.add ( "CreateOutput" ); // Useful?
        v.add ( "DebugLevelLogFile" );
        v.add ( "DebugLevelScreen" );
        v.add ( "HaveOutputPeriod" ); // Useful?
        v.add ( "HydroBaseDMIListSize" );
        v.add ( "IgnoreLEZero" );
        v.add ( "IncludeMissingTS" );
        v.add ( "InitialWorkingDir" );
    	//v.add ( "InputStart" );
    	//v.add ( "InputEnd" );
    	//v.add ( "OutputComments" ); // Not sure this needs to be visible
    	v.add ( "OutputStart" );
    	v.add ( "OutputEnd" );
        v.add ( "OutputYearType" );
        v.add ( "StartLogEnabled" );
        v.add ( "TSEnsembleResultsListSize" );   // Useful for testing when zero time series are expected
        v.add ( "TSResultsListSize" );   // Useful for testing when zero time series are expected
        v.add ( "WarningLevelLogFile" );
        v.add ( "WarningLevelScreen" );
        v.add ( "WorkingDir" );
        set.addAll ( v );
	}
    if ( includeDynamicProperties ) {
        // Add the hashtable keys and make a unique list
        set.addAll ( __propertyHashmap.keySet() );
    }
	return set;
}

/**
Determine if the commands are read-only.  In this case, applications may disable
save features.  The special comment "#@readOnly" indicates that the commands are read-only.
@return true if read-only, false if can be written.
*/
public boolean getReadOnly ()
{   // String that indicates readOnly
    String readOnlyString = "@readOnly";
    // Loop through the commands and check comments for the special string
    int size = size();
    Command c;
    List<Command> commandList = getCommands();
    for ( int i = 0; i < size; i++ ) {
        c = commandList.get(i);
        String commandString = c.toString();
        if ( commandString.trim().startsWith("#") &&
                (StringUtil.indexOfIgnoreCase(commandString,readOnlyString,0) > 0) ) {
            return true;
        }
    }
    return false;
}

/**
 * Returns the status of the last run.
 * false = errors encountered on run
 * true = successful run
 * @return whether the run was successful.
 */
public boolean getRunStatus()
{
	return runSuccessful;
}

/**
Return the list of StateCU_BlaneyCriddle being maintained by this StateDMI_Processor.
@return the list of StateCU_BlaneyCriddle being maintained by this StateDMI_Processor.
*/
public List<StateCU_BlaneyCriddle> getStateCUBlaneyCriddleList()
{	return __CUBlaneyCriddle_List;
}

/**
Return the list of StateCU_BlaneyCriddle matches being maintained by this StateDMI_Processor.
@return the list of StateCU_BlaneyCriddle matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateCUBlaneyCriddleMatchList()
{	return __CUBlaneyCriddle_match_List;
}

/**
Return the list of StateCU_ClimateStation being maintained by this StateDMI_Processor.
@return the list of StateCU_ClimateStation being maintained by this StateDMI_Processor.
*/
public List<StateCU_ClimateStation> getStateCUClimateStationList()
{	return __CUClimateStation_List;
}

/**
Return the list of StateCU_ClimateStation matches being maintained by this StateDMI_Processor.
@return the list of StateCU_ClimateStation matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateCUClimateStationMatchList()
{	return __CUClimateStation_match_List;
}

/**
Return the list of StateCU_CropCharacteristics being maintained by this StateDMI_Processor.
@return the list of StateCU_CropCharacteristics being maintained by this StateDMI_Processor.
*/
public List<StateCU_CropCharacteristics> getStateCUCropCharacteristicsList()
{	return __CUCropCharacteristics_List;
}

/**
Return the list of StateCU_CropCharacteristics matches being maintained by this StateDMI_Processor.
@return the list of StateCU_CropCharacteristics matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateCUCropCharacteristicsMatchList()
{	return __CUCropCharacteristics_match_List;
}

/**
Return the list of StateCU_CropPatternTS being maintained by this StateDMI_Processor.
@return the list of StateCU_CropPatternTS being maintained by this StateDMI_Processor.
*/
public List<StateCU_CropPatternTS> getStateCUCropPatternTSList()
{	return __CUCropPatternTS_List;
}

/**
Return the list of StateCU_CropPatternTS matches being maintained by this StateDMI_Processor.
@return the list of StateCU_CropPatternTS matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateCUCropPatternTSMatchList()
{	return __CUCropPatternTS_match_List;
}

/**
Return the list of StateCU_IrrigationPracticeTS being maintained by this StateDMI_Processor.
@return the list of StateCU_IrrigationPracticeTS being maintained by this StateDMI_Processor.
*/
public List<StateCU_IrrigationPracticeTS> getStateCUIrrigationPracticeTSList()
{	return __CUIrrigationPracticeTS_List;
}

/**
Return the list of StateCU_IrrigationPracticeTS matches being maintained by this StateDMI_Processor.
@return the list of StateCU_IrrigationPracticeTS matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateCUIrrigationPracticeTSMatchList()
{	return __CUIrrigationPracticeTS_match_List;
}

/**
Return the list of StateCU_Location being maintained by this StateDMI_Processor.
@return the list of StateCU_Location being maintained by this StateDMI_Processor.
*/
public List<StateCU_Location> getStateCULocationList()
{	return __CULocation_List;
}

/**
Return the list of StateCU_Location matches being maintained by this StateDMI_Processor.
@return the list of StateCU_Location matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateCULocationMatchList()
{	return __CULocation_match_List;
}

/**
Return the list of StateCU_Parcel being maintained by this StateDMI_Processor.
@return the list of StateCU_Parcel being maintained by this StateDMI_Processor.
*/
public HashMap<String,StateCU_Parcel> getStateCUParcelList()
{	return __CUParcel_Map;
}

/**
Return the list of StateCU_PenmanMonteith being maintained by this StateDMI_Processor.
@return the list of StateCU_PenmanMonteith being maintained by this StateDMI_Processor.
*/
public List<StateCU_PenmanMonteith> getStateCUPenmanMonteithList()
{	return __CUPenmanMonteith_List;
}

/**
Return the list of StateCU_BlaneyCriddle matches being maintained by this StateDMI_Processor.
@return the list of StateCU_BlaneyCriddle matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateCUPenmanMonteithMatchList()
{	return __CUPenmanMonteith_match_List;
}

/**
 * Return the StateDMI version.
 * @return the StateDMI version string (e.g., "5.00.00" for full version string "5.00.00 (YYYY-MM-dd"),
 * useful for checking test version requirements.
 */
public String getStateDmiVersionString() {
	return StateDMI.PROGRAM_VERSION.split(" ")[0].trim();
}

/**
Return the output end date/time.
@return the output end date/time.
*/
public DateTime getOutputPeriodEnd()
{	return __OutputEnd_DateTime;
}

/**
Return the output start date/time.
@return the output start date/time.
*/
public DateTime getOutputPeriodStart()
{	return __OutputStart_DateTime;
}

/**
Return the list of consumptive water requirement monthly TS being maintained by this StateDMI_Processor.
@return the list of consumptive water requirement monthly TS being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModConsumptiveWaterRequirementTSMonthlyList ()
{	return __SMConsumptiveWaterRequirementTSMonthlyList;
}

/**
Return the list of consumptive water requirement monthly TS matches being maintained by this StateDMI_Processor.
@return the list of consumptive water requirement monthly TS matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModConsumptiveWaterRequirementTSMonthlyMatchList ()
{	return __SMConsumptiveWaterRequirementTSMonthly_match_List;
}

/**
Return the list of StateMod_DelayTable being maintained by this StateDMI_Processor.
These are used by both StateCU and StateMod data sets.
@param interval TimeInterval.MONTH or TimeInterval.DAY, indicating the interval for delay tables.
@return the list of StateMod_DelayTable being maintained by this StateDMI_Processor.
*/
public List<StateMod_DelayTable> getStateModDelayTableList ( int interval )
{	if ( interval == TimeInterval.MONTH ) {
		return __SMDelayTableMonthlyList;
	}
	else if ( interval == TimeInterval.DAY ) {
		return __SMDelayTableDailyList;
	}
	else {
		return null;
	}
}

/**
Return the list of StateMod_DelayTable matches being maintained by this StateDMI_Processor.
These are used by both StateCU and StateMod data sets.
@param interval TimeInterval.MONTH or TimeInterval.DAY, indicating the interval for delay tables.
@return the list of StateMod_DelayTable matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModDelayTableMatchList ( int interval )
{	if ( interval == TimeInterval.MONTH ) {
		return __SMDelayTableMonthly_match_List;
	}
	else if ( interval == TimeInterval.DAY ) {
		return __SMDelayTableDaily_match_List;
	}
	else {
		return null;
	}
}

/**
Return the list of diversion demand daily TS being maintained by this StateDMI_Processor.
@return the list of diversion demand daily TS being maintained by this StateDMI_Processor.
*/
public List<DayTS> getStateModDiversionDemandTSDailyList ()
{	return __SMDemandTSDailyList;
}

/**
Return the list of diversion demand monthly TS being maintained by this StateDMI_Processor.
@return the list of diversion demand monthly TS being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModDiversionDemandTSMonthlyList ()
{	return __SMDemandTSMonthlyList;
}

/**
Return the list of diversion demand monthly TS matches being maintained by this StateDMI_Processor.
@return the list of diversion demand monthly TS matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateModDiversionDemandTSMonthlyMatchList ()
{	return __SMDemandTSMonthly_match_List;
}

/**
Return the list of diversion historical daily TS being maintained by this StateDMI_Processor.
@return the list of diversion historical daily TS being maintained by this StateDMI_Processor.
*/
public List<DayTS> getStateModDiversionHistoricalTSDailyList ()
{	return __SMDiversionTSDailyList;
}

/**
Return the list of diversion historical monthly TS copy being maintained by this StateDMI_Processor.
@return the list of diversion historical monthly TS copy being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModDiversionHistoricalTSMonthlyCopyList ()
{	return __SMDiversionTSMonthly2List;
}

/**
Return the list of diversion historical monthly TS being maintained by this StateDMI_Processor.
@return the list of diversion historical monthly TS being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModDiversionHistoricalTSMonthlyList ()
{	return __SMDiversionTSMonthlyList;
}

/**
Return the list of diversion historical monthly TS matches being maintained by this StateDMI_Processor.
@return the list of diversion historical monthly TS matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateModDiversionHistoricalTSMonthlyMatchList ()
{	return __SMDiversionTSMonthly_match_List;
}

/**
Return the list of StateMod_DiversionRight being maintained by this StateDMI_Processor.
@return the list of StateMod_DiversionRight being maintained by this StateDMI_Processor.
*/
public List<StateMod_DiversionRight> getStateModDiversionRightList ()
{	return __SMDiversionRightList;
}

/**
Return the list of StateMod_DiversionRight matches being maintained by this StateDMI_Processor.
@return the list of StateMod_DiversionRight matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModDiversionRightMatchList ()
{	return __SMDiversionRight_match_List;
}

/**
Return the list of StateMod_Diversion being maintained by this StateDMI_Processor.
@return the list of StateMod_Diversion being maintained by this StateDMI_Processor.
*/
public List<StateMod_Diversion> getStateModDiversionStationList ()
{	return __SMDiversionStationList;
}

/**
Return the list of StateMod_Diversion matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Diversion matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModDiversionStationMatchList ()
{	return __SMDiversion_match_List;
}

/**
Returns the list of instream flow demand (average monthly) time series
being maintained by the StateDMI processor.
@return the list of instream flow demand (average monthly) time series
being maintained by the StateDMI processor.
*/
public List<MonthTS> getStateModInstreamFlowDemandTSAverageMonthlyList()
{	return __SMInstreamFlowDemandTSAverageMonthlyList;
}

/**
Returns the list of instream flow demand (average monthly) time series matches
being maintained by the StateDMI processor.
@return the list of instream flow demand (average monthly) time series matches
being maintained by the StateDMI processor.
*/
public List<String> getStateModInstreamFlowDemandTSAverageMonthlyMatchList()
{	return __SMInstreamFlowDemandTSAverageMonthly_match_List;
}

/**
Returns the list of StateMod_InstreamFlowRight being maintained by the StateDMI processor.
@return the list of StateMod_InstreamFlowRight being maintained by the StateDMI processor.
*/
public List<StateMod_InstreamFlowRight> getStateModInstreamFlowRightList()
{	return __SMInstreamFlowRightList;
}

/**
Returns the list of StateMod_InstreamFlowRight matches being maintained by the StateDMI processor.
@return the list of StateMod_InstreamFlowRight matches being maintained by the StateDMI processor.
*/
public List<String> getStateModInstreamFlowRightMatchList()
{	return __SMInstreamFlowRight_match_List;
}

/**
Returns the list of StateMod_InstreamFlow being maintained by the StateDMI processor.
@return the list of StateMod_InstreamFlow being maintained by the StateDMI processor.
*/
public List<StateMod_InstreamFlow> getStateModInstreamFlowStationList()
{	return __SMInstreamFlowStationList;
}

/**
Returns the list of StateMod_InstreamFlow matches being maintained by the StateDMI processor.
@return the list of StateMod_InstreamFlow matches being maintained by the StateDMI processor.
*/
public List<String> getStateModInstreamFlowStationMatchList()
{	return __SMInstreamFlow_match_List;
}

/**
Returns the StateMod_Network being maintained by the StateDMI processor.
@return the StateMod_Network being maintained by the StateDMI processor.
*/
public StateMod_NodeNetwork getStateModNetwork()
{	return __SM_network;
}

/**
Return the list of StateMod_OperationalRight being maintained by this StateDMI_Processor.
@return the list of StateMod_OperationalRight being maintained by this StateDMI_Processor.
*/
public List<StateMod_OperationalRight> getStateModOperationalRightList ()
{	return __SMOperationalRightList;
}

/**
Return the list of StateMod_OperationalRight matches being maintained by this StateDMI_Processor.
@return the list of StateMod_OperationalRight matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModOperationalRightMatchList ()
{	return __SMOperationalRight_match_List;
}

/**
Return the list of pattern time series used with Fill*Pattern().
@return the list of pattern time series used with Fill*Pattern().
*/
protected List<StringMonthTS> getStateModPatternTSMonthlyList()
{
	return __SMPatternTSMonthlyList;
}

/**
Return the list of StateMod_ReturnFlow for plan stations being maintained by this StateDMI_Processor.
@return the list of StateMod_ReturnFlow for plan stations being maintained by this StateDMI_Processor.
*/
public List<StateMod_ReturnFlow> getStateModPlanReturnList ()
{	return __SMPlanReturnList;
}

/**
Return the list of StateMod_Plan being maintained by this StateDMI_Processor.
@return the list of StateMod_Plan being maintained by this StateDMI_Processor.
*/
public List<StateMod_Plan> getStateModPlanStationList ()
{	return __SMPlanList;
}

/**
Return the list of StateMod_Plan_WellAugmentation being maintained by this StateDMI_Processor.
@return the list of StateMod_Plan_WellAugmentation being maintained by this StateDMI_Processor.
*/
public List<StateMod_Plan_WellAugmentation> getStateModPlanWellAugmentationList ()
{	return __SMPlanWellAugmentationList;
}

/**
Return the list of StateMod_Plan_Return matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Plan_Return matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModPlanReturnMatchList ()
{	return __SMPlanReturn_match_List;
}

/**
Return the list of StateMod_Plan matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Plan matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModPlanStationMatchList ()
{	return __SMPlan_match_List;
}

/**
Return the list of StateMod_Plan_WellAugmentation matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Plan_WellAugmentation matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModPlanWellAugmentationMatchList ()
{	return __SMPlanWellAugmentation_match_List;
}

/**
Return the list of StateMod_PrfGageData being maintained by this StateDMI_Processor.
@return the list of StateMod_PrfGageData being maintained by this StateDMI_Processor.
*/
public List<StateMod_PrfGageData> getStateModPrfGageDataList()
{	return __SMPrfGageData_List;
}

/**
Return the list of StateMod_ReturnFlow for reservoir stations being maintained by this StateDMI_Processor.
@return the list of StateMod_ReturnFlow for reservoir stations being maintained by this StateDMI_Processor.
*/
public List<StateMod_ReturnFlow> getStateModReservoirReturnList ()
{	return __SMReservoirReturnList;
}

/**
Return the list of StateMod_Reservoir_Return matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Reservoir_Return matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModReservoirReturnMatchList ()
{	return __SMReservoirReturn_match_List;
}

/**
Return the list of StateMod_ReservoirRight being maintained by this StateDMI_Processor.
@return the list of StateMod_ReservoirRight being maintained by this StateDMI_Processor.
*/
public List<StateMod_ReservoirRight> getStateModReservoirRightList()
{	return __SMReservoirRightList;
}

/**
Return the list of StateMod_ReservoirRight matches being maintained by this StateDMI_Processor.
@return the list of StateMod_ReservoirRight matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModReservoirRightMatchList()
{	return __SMReservoirRight_match_List;
}

/**
Return the list of StateMod_Reservoir being maintained by this StateDMI_Processor.
@return the list of StateMod_Reservoir being maintained by this StateDMI_Processor.
*/
public List<StateMod_Reservoir> getStateModReservoirStationList ()
{	return __SMReservoirStationList;
}

/**
Return the list of StateMod_Reservoir matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Reservoir matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModReservoirStationMatchList ()
{	return __SMReservoir_match_List;
}

/**
Return the list of StateMod_RiverNetworkNode being maintained by this StateDMI_Processor.
@return the list of StateMod_RiverNetworkNode being maintained by this StateDMI_Processor.
*/
public List<StateMod_RiverNetworkNode> getStateModRiverNetworkNodeList ()
{	return __SMRiverNetworkNode_List;
}

/**
Return the list of StateMod_RiverNetworkNode matches being maintained by this StateDMI_Processor.
@return the list of StateMod_RiverNetworkNode matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateModRiverNetworkNodeMatchList ()
{	return __SMRiverNetworkNode_match_List;
}

/**
Return the list of StateMod_StreamEstimate being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamEstimate being maintained by this StateDMI_Processor.
*/
public List<StateMod_StreamEstimate> getStateModStreamEstimateStationList()
{	return __SMStreamEstimateStationList;
}

/**
Return the list of StateMod_StreamEstimate matches being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamEstimate matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModStreamEstimateStationMatchList ()
{	return __SMStreamEstimate_match_List;
}

/**
Return the list of StateMod_StreamEstimateCoefficients being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamEstimateCoefficients being maintained by this StateDMI_Processor.
*/
public List<StateMod_StreamEstimate_Coefficients> getStateModStreamEstimateCoefficientsList()
{	return __SMStreamEstimateCoefficients_List;
}

/**
Return the list of StateMod_StreamEstimate_Coefficients matches being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamEstimate_Coefficients matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModStreamEstimateCoefficientsMatchList ()
{	return __SMStreamEstimateCoefficients_match_List;
}

/**
Return the list of StateMod_StreamGage being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamGage being maintained by this StateDMI_Processor.
*/
public List<StateMod_StreamGage> getStateModStreamGageStationList ()
{	return __SMStreamGageStationList;
}

/**
Return the list of StateMod_StreamGage matches being maintained by this StateDMI_Processor.
@return the list of StateMod_StreamGage matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModStreamGageStationMatchList ()
{	return __SMStreamGage_match_List;
}

/**
Return the list of well demand monthly TS being maintained by this StateDMI_Processor.
@return the list of well demand monthly TS being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModWellDemandTSMonthlyList ()
{	return __SMWellDemandTSMonthlyList;
}

/**
Return the list of well demand monthly TS matches being maintained by this StateDMI_Processor.
@return the list of well demand monthly TS matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateModWellDemandTSMonthlyMatchList ()
{	return __SMWellDemandTSMonthly_match_List;
}

/**
Return the list of well historical pumping monthly TS being maintained by this StateDMI_Processor.
@return the list of well historical pumping monthly TS being maintained by this StateDMI_Processor.
*/
public List<MonthTS> getStateModWellHistoricalPumpingTSMonthlyList ()
{	return __SMWellHistoricalPumpingTSMonthlyList;
}

/**
Return the list of well historical pumping monthly TS matches being maintained by this StateDMI_Processor.
@return the list of well historical pumping monthly TS matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModWellHistoricalPumpingTSMonthlyMatchList ()
{	return __SMWellHistoricalPumpingTSMonthly_match_List;
}

/**
Return the list of StateMod_Well being maintained by this StateDMI_Processor.
@return the list of StateMod_Well being maintained by this StateDMI_Processor.
*/
public List<StateMod_Well> getStateModWellStationList ()
{	return __SMWellList;
}

/**
Return the list of StateMod_WellRight being maintained by this StateDMI_Processor.
@return the list of StateMod_WellRight being maintained by this StateDMI_Processor.
*/
public List<StateMod_WellRight> getStateModWellRightList()
{	return __SMWellRightList;
}

/**
Return the list of StateMod_WellRight matches being maintained by this StateDMI_Processor.
@return the list of StateMod_WellRight matches being maintained by this StateDMI_Processor.
*/
protected List<String> getStateModWellRightMatchList()
{	return __SMWellRight_match_List;
}

/**
Return the list of StateMod_Well matches being maintained by this StateDMI_Processor.
@return the list of StateMod_Well matches being maintained by this StateDMI_Processor.
*/
public List<String> getStateModWellStationMatchList ()
{	return __SMWell_match_List;
}

/**
Return the TSSupplier name.
@return the TSSupplier name ("StateDMI_Processor").
*/
public String getTSSupplierName()
{	return "StateDMI_Processor";
}

/**
Return the current working directory for the processor.
@return the current working directory for the processor.
*/
protected String getWorkingDir ()
{	return __WorkingDir_String;
}

/**
Handle the CommandProcessorEvent events generated during processing and format for output.
Currently this method passes on the events to listeners registered on this processor.
@param event CommandProcessorEvent to handle.
*/
public void handleCommandProcessorEvent ( CommandProcessorEvent event )
{
    if ( __CommandProcessorEventListener_array != null ) {
        for ( int i = 0; i < __CommandProcessorEventListener_array.length; i++ ) {
            __CommandProcessorEventListener_array[i].handleCommandProcessorEvent(event);
        }
    }
}

/**
Determine the index of a command in the processor.  A reference comparison occurs.
@param command A command to search for in the processor.
@return the index (0+) of the matching command, or -1 if not found.
*/
public int indexOf ( Command command )
{	// Uncomment to troubleshoot
	//String routine = getClass().getName() + ".indexOf";
	int size = size();
	Command c;
	//Message.printStatus ( 2, routine, "Checking " + size + " commands for command " + command );
	for ( int i = 0; i < size; i++ ) {
		c = (Command)__commandList.get(i);
		//Message.printStatus ( 2, routine, "Comparing to command " + c );
		if ( c == command ) {
			//Message.printStatus ( 2, routine, "Found command." );
			return i;
		}
	}
	//Message.printStatus ( 2, routine, "Did not find command." );
	return -1;
}

/**
Add a command using the Command instance.
@param command Command to insert.
@param index Index (0+) at which to insert the command.
*/
public void insertCommandAt ( Command command, int index )
{	String routine = getClass().getName() + ".insertCommandAt";
	getCommands().add( index, command );
	// Also add this processor as a listener for events
    if ( command instanceof CommandProcessorEventProvider ) {
        CommandProcessorEventProvider ep = (CommandProcessorEventProvider)command;
        ep.addCommandProcessorEventListener(this);
    }
	notifyCommandListListenersOfAdd ( index, index );
	Message.printStatus(2, routine, "Inserted command object \"" + command + "\" at [" + index + "]" );
}

/**
Add a command using the string text.  This should currently only be
used for commands that do not have command classes, which perform
additional validation on the commands.  A GenericCommand instance will
be instantiated to maintain the string and allow command status to be set.
@param command_string Command string for command.
@param index Index (0+) at which to insert the command.
*/
public void insertCommandAt ( String command_string, int index )
{	String routine = getClass().getName() + ".insertCommandAt";
	Command command = new GenericCommand ();
	command.setCommandString ( command_string );
	insertCommandAt ( command, index );
	// Also add this processor as a listener for events
    if ( command instanceof CommandProcessorEventProvider ) {
        CommandProcessorEventProvider ep = (CommandProcessorEventProvider)command;
        ep.addCommandProcessorEventListener(this);
    }
	Message.printStatus(2, routine, "Creating generic command from string \"" + command_string + "\"." );
}

/**
Indicate whether the processing is running.
@return true if the command processor is running, false if not.
*/
public boolean getIsRunning ()
{	return __is_running;
}

/**
Get a date/time from a string.  The string is first expanded to fill ${Property} strings and then the
matching property name is used to determine the date/time using the following rules:
<ol>
<li> If the string is null, "*" or "", return null.</li>
<li> If the string uses a standard name InputStart (QueryStart), InputEnd (QueryEnd), OutputStart, OutputEnd, return the corresponding DateTime.</li>
<li> Check the processor date/time hash table for user-defined date/time properties.</li>
<li> Parse the string using DateTime.parse().
</ol>
@param dtString Date/time string to parse.
@exception if the date/time cannot be determined using the defined procedure.
*/
protected DateTime getDateTime ( String dtString )
throws Exception
{
	if ( dtString != null ) {
		dtString = dtString.trim();
	}
	if ( (dtString == null) || dtString.isEmpty() || dtString.equals("*") ) {
		// Want to use all available...
		return null;
	}

	// TODO SAM 2015-05-17 Need to decide whether to continue supporting or move to ${OutputEnd} notation exclusively
	// Handle built-in property ${InputStart} etc. below so that nulls don't cause an issue (nulls are OK for full period)
	// Check for named DateTime instances...

	if ( dtString.equalsIgnoreCase("OutputEnd") || dtString.equalsIgnoreCase("${OutputEnd}") || dtString.equalsIgnoreCase("OutputPeriodEnd") ) {
		return __OutputEnd_DateTime;
	}
	else if(dtString.equalsIgnoreCase("OutputStart") || dtString.equalsIgnoreCase("${OutputStart}") || dtString.equalsIgnoreCase("OutputPeriodStart") ) {
		return __OutputStart_DateTime;
	}
	
	// Check for requested user-defined property
	if ( dtString.startsWith("${") && dtString.endsWith("}") ) {
		String propName = dtString.substring(2,dtString.length() - 1);
		Object o = this.getPropContents(propName);
		if ( o != null ) {
			if ( o instanceof DateTime ) {
				return (DateTime)o;
			}
			else if ( o instanceof String ) {
				// Reset the string and try parsing below
				dtString = (String)o;
			}
		}
	}

	// Else did not find a date time so try parse the string (OK to throw an exception)...

	return DateTime.parse ( dtString );
}

/**
Search for a fill pattern TS.
@return reference to found StringMonthTS instance.
@param PatternID Fill pattern identifier to search for.
*/
public StringMonthTS lookupFillPatternTS ( String PatternID )
{	if ( PatternID == null ) {
		return null;
	}
	if ( __SMPatternTSMonthlyList == null ) {
		return null;
	}

	int nfill_pattern_ts = __SMPatternTSMonthlyList.size();

	StringMonthTS fill_pattern_ts_i = null;
	for ( int i = 0; i < nfill_pattern_ts; i++ ) {
		fill_pattern_ts_i =
			(StringMonthTS)__SMPatternTSMonthlyList.get(i);
		if ( fill_pattern_ts_i == null ) {
			continue;
		}
		if (	PatternID.equalsIgnoreCase(
			fill_pattern_ts_i.getLocation()) ) {
			return fill_pattern_ts_i;
		}
	}
	fill_pattern_ts_i = null;
	return null;
}

/**
Process the events from the MessageJDialog class.  If the "Cancel" button has
been pressed, then request that the time series processing should stop.
@param command If "Cancel", then a request will be made to cancel processing.
*/
public void messageJDialogAction ( String command )
{	if ( command.equalsIgnoreCase("Cancel") ) {
		setCancelProcessingRequested ( true );
	}
}

/**
Notify registered CommandListListeners about one or more commands being added.
@param index0 The index (0+) of the first command that is added.
@param index1 The index (0+) of the last command that is added.
*/
private void notifyCommandListListenersOfAdd ( int index0, int index1 )
{	if ( __CommandListListener_array != null ) {
		for ( int i = 0; i < __CommandListListener_array.length; i++ ) {
			__CommandListListener_array[i].commandAdded(index0, index1);
		}
	}
}

/**
Notify registered CommandListListeners about one or more commands being changed.
@param index0 The index (0+) of the first command that is added.
@param index1 The index (0+) of the last command that is added.
*/
//private void notifyCommandListListenersOfChange ( int index0, int index1 )
//{	if ( __CommandListListener_array != null ) {
//		for ( int i = 0; i < __CommandListListener_array.length; i++ ) {
//			__CommandListListener_array[i].commandChanged(index0, index1);
//		}
//	}
//}

/**
Notify registered CommandListListeners about one or more commands being removed.
@param index0 The index (0+) of the first command that is added.
@param index1 The index (0+) of the last command that is added.
*/
private void notifyCommandListListenersOfRemove ( int index0, int index1 )
{	if ( __CommandListListener_array != null ) {
		for ( int i = 0; i < __CommandListListener_array.length; i++ ) {
			__CommandListListener_array[i].commandRemoved(index0, index1);
		}
	}
}

/**
Notify registered CommandProcessorListeners about a command being cancelled.
@param icommand The index (0+) of the command that is cancelled.
@param ncommand The number of commands being processed.  This will often be the
total number of commands but calling code may process a subset.
@param command The instance of the neareset command that is being cancelled.
*/
protected void notifyCommandProcessorListenersOfCommandCancelled (
		int icommand, int ncommand, Command command )
{	if ( __CommandProcessorListener_array != null ) {
		for ( int i = 0; i < __CommandProcessorListener_array.length; i++ ) {
			__CommandProcessorListener_array[i].commandCanceled(icommand,ncommand,command,-1.0F,
				"Command cancelled.");
		}
	}
}

/**
Notify registered CommandProcessorListeners about a command completing.
@param icommand The index (0+) of the command that is completing.
@param ncommand The number of commands being processed.  This will often be the
total number of commands but calling code may process a subset.
@param command The instance of the command that is completing.
*/
protected void notifyCommandProcessorListenersOfCommandCompleted (
		int icommand, int ncommand, Command command )
{	if ( __CommandProcessorListener_array != null ) {
		for ( int i = 0; i < __CommandProcessorListener_array.length; i++ ) {
			__CommandProcessorListener_array[i].commandCompleted(icommand,ncommand,command,-1.0F,"Command completed.");
		}
	}
}

/**
Notify registered CommandProcessorListeners about a command starting.
@param icommand The index (0+) of the command that is starting.
@param ncommand The number of commands being processed.  This will often be the
total number of commands but calling code may process a subset.
@param command The instance of the command that is starting.
*/
protected void notifyCommandProcessorListenersOfCommandStarted (
		int icommand, int ncommand, Command command )
{	if ( __CommandProcessorListener_array != null ) {
		for ( int i = 0; i < __CommandProcessorListener_array.length; i++ ) {
			__CommandProcessorListener_array[i].commandStarted(icommand,ncommand,command,-1.0F,"Command started.");
		}
	}
}

/**
Process a list of commands, resulting in lists of data set objects and properties.  The resulting
objects can be displayed in the GUI.
<b>Filling with historical averages is handled for monthly time series
so that original data averages are used.</b>
@param commandList The list of Command from the this instance of StateDMI_Processor,
to be processed.  If null, process all.  Non-null is typically only used, for example,
if a user has selected commands in a GUI.
@param app_PropList if not null, then properties are set as the commands are
run.  This is typically used when running commands prior to using an edit
dialog in the StateDMI GUI.  Properties can have the following values:
<table width=100% cellpadding=10 cellspacing=0 border=2>
<tr>
<td><b>Property</b></td>	<td><b>Description</b></td>
</tr>

<tr>
<td><b>CreateOutput</b></td>
<td>Indicate whether output files should be created.  False is faster but
results in incomplete products.
</td>
<td>True - create output files.</td>
</tr>

<tr>
<td><b>InitialWorkingDir</b></td>
<td>The initial working directory for the run.  Normally this is only set when using a
command like RunCommands() to avoid confusion between the second command file and the
controlling command file.
</td>
<td>True - create output files.</td>
</tr>

</table>
*/
private void processCommands ( List<Command> commandList, PropList app_PropList )
throws Exception
{	String	message, routine = "StateDMI.processCommands";
	//String message_tag = "ProcessCommands"; // Tag used with messages generated in this method.
	int error_count = 0;	// For errors during time series retrieval
	int update_count = 0;	// For warnings about command updates
	if ( commandList == null ) {
		// Process all commands if a subset has not been provided.
		commandList = getCommands();
	}
	
	// Save the passed in properties processRequest
	// call, so that they can be retrieved with other requests.
	
	if ( app_PropList == null ) {
		app_PropList = new PropList ( "StateDMI" );
	}

	/* FIXME SAM 2008-10-14 Evaluate if needed
	 * 	// Save class version...
	__processor_PropList = app_PropList;
	*/

	// Initialize the working directory to the initial directory that is
	// passed in.  Do this because software may request the working directory that
	// is the result of processing and the initial directory may never have
	// been changed dynamically.
	
	/* TODO SAM 2007-10-13 Remove when test out.  The initial working dir is no
	 * longer dynamic but is a data member on the processor.
	String InitialWorkingDir = __processor_PropList.getValue ( "InitialWorkingDir" );
	*/
	String InitialWorkingDir = getInitialWorkingDir(); //app_PropList.getValue("InitialWorkingDir");
	//if (InitialWorkingDir == null) {
	//	// None passed in so use what was previously defined for the processor (command file location).
	//	InitialWorkingDir = getInitialWorkingDir();
	//}
	// Set the working directory to the initial working directory
	if ( InitialWorkingDir != null ) {
		setPropContents ( "WorkingDir", InitialWorkingDir );
	}
	Message.printStatus(2, routine,"InitialWorkingDir=" + InitialWorkingDir );
	
	// Indicate whether output products/files should be created, or
	// just time series (to allow interactive graphing).
	String CreateOutput = app_PropList.getValue ( "CreateOutput" );
	if ( (CreateOutput != null) && CreateOutput.equalsIgnoreCase("False")){
		setCreateOutput ( false );
	}
	else {
		setCreateOutput ( true );
	}
	Message.printStatus(2, routine,"CreateOutput=" + getCreateOutput() );
	
	// Indicate whether time series should be cleared between runs.
	// If true, do not clear the time series between recursive
	// calls.  This is somewhat experimental to evaluate a master
	// commands file that runs other commands files.
	boolean AppendResults_boolean = false;

	int size = commandList.size();
	Message.printStatus ( 1, routine, "Processing " + size + " commands..." );
	StopWatch stopwatch = new StopWatch();
	stopwatch.start();
	String command_String = null;

	boolean inComment = false;
	Command command = null;	// The command to process
	CommandStatus command_status = null; // Put outside of main try to be able to use in catch.

	// Change setting to allow warning messages to be turned off during the main loop.
    // This capability should not be needed if a command uses the new command status processing.

	int popup_warning_level = 2;		// Do not popup warnings (only to log)
    // Turn off interactive warnings to pretent overload on user in loops.
    Message.setPropValue ( "ShowWarningDialog=false" );
    
    // Clear any settings that may have been left over from the previous run and which
    // can impact the current run.
    
    processCommands_ResetDataForRunStart ( AppendResults_boolean );

	// Now loop through the commands to process.

	inComment = false;
	int i_for_message;	// This will be adjusted by
				// __num_prepended_commands - the user will
				// see command numbers in messages like (12),
				// indicating the twelfth command.

	String command_tag = null;	// String used in messages to allow
					// link back to the application
					// commands, for use with each command.
	int i;	// Put here so can check count outside of end of loop
	boolean prev_command_complete_notified = false;// If previous command completion listeners were notified
										// May not occur if "continue" in loop.
	Command command_prev = null;	// previous command in loop
	CommandProfile commandProfile = null; // Profile to track execution time, memory use
	// Indicate the state of the processor...
	setIsRunning ( true );
	// Stopwatch to time each command...
	StopWatch stopWatch = new StopWatch();
	for ( i = 0; i < size; i++ ) {
		// 1-offset command count for messages
		i_for_message = i + 1;
		command_tag = "" + i_for_message;	// Command number as integer 1+, for message/log handler.
		// If for some reason the previous command did not notify listeners of its completion (e.g., due to
		// continue in loop, do it now)...
		if ( !prev_command_complete_notified && (command_prev != null) ) {
			notifyCommandProcessorListenersOfCommandCompleted ( (i - 1), size, command_prev );
		}
		prev_command_complete_notified = false;
		// Save the previous command before resetting to new command below.
		if ( i > 0 ) {
			command_prev = command;
		}
		// Check for a cancel, which would have been set by pressing
		// the cancel button on the warning dialog or by using the other StateDMI UI menus...
		if ( getCancelProcessingRequested() ) {
            // Turn on interactive warnings again.
            Message.setPropValue ( "ShowWarningDialog=true" );
			// Set flag so code interested in processor knows it is not running...
			setIsRunning ( false );
			// Reset the cancel processing request and let interested code know that
			// processing has been cancelled.
			setCancelProcessingRequested ( false );
			notifyCommandProcessorListenersOfCommandCancelled (	i, size, command );
			return;
		}
		try {
		    // Catch errors in all the commands.
    		command = commandList.get(i);
    		command_String = command.toString();
    		if ( command_String == null ) {
    			continue;
    		}
    		command_String = command_String.trim();
    		// All commands will implement CommandStatusProvider so get it...
    		command_status = ((CommandStatusProvider)command).getCommandStatus();
    		// Clear the run status (internally will set to UNKNOWN).
    		command_status.clearLog(CommandPhaseType.RUN);
    		commandProfile = command.getCommandProfile(CommandPhaseType.RUN);
    		Message.printStatus ( 1, routine, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
    		Message.printStatus ( 1, routine,
    			"Start processing command " + (i + 1) + " of " + size + ": \"" + command_String + "\" " );
    		stopWatch.clear();
    		stopWatch.start();
    		commandProfile.setStartTime(System.currentTimeMillis());
            commandProfile.setStartHeap(Runtime.getRuntime().totalMemory());
    		// Notify any listeners that the command is running...
    		notifyCommandProcessorListenersOfCommandStarted ( i, size, command );
    
    		if ( command instanceof Comment_Command ) {
    			// Comment.  Mark as processing successful unless requirements were not met.
                String commandStringUpper = command_String.toUpperCase();
                if ( commandStringUpper.indexOf("@REQUIRE") > 0 ) {
                	// Check @require comments for syntax errors
                	// - need to be correct to ensure that tests run properly
                	// - when running automated tests with RunCommands, these conditions are checked for the entire command file
                	//   before even attempting to run so FAILURE will not occur in test (it won't even be run)
                	// - TODO smalers 2021-01-03 evaluate whether this can be put in Comment_Command.runCommand(),
                	//   but currently the logic depends on the processor so not generic for StateDMI and TSTool.
                	try {
                		List<Command> commentList = new ArrayList<>();
                		commentList.add(command);
        	        	if ( StateDMICommandFileRunner.areRequirementsMet(this, commentList) ) {
        	        		command_status.addToLog(CommandPhaseType.RUN,
			    			    new CommandLogRecord(CommandStatusType.SUCCESS,
				   			    "@require condition was met", "Command file will be run unless other requirement is not met.") );
        	        	}
        	        	else {
        	        		command_status.addToLog(CommandPhaseType.RUN,
			    			    new CommandLogRecord(CommandStatusType.FAILURE,
				   			    "@require condition was NOT met", "Command file should not be run unless requirements are met.") );
        	        	}
                	}
                	catch ( Exception e ) {
        	        	// Syntax error - mark the command with an error
                		// Set the command status information.
        	    		if ( command instanceof CommandStatusProvider ) {
				    		// Add to the command log as a failure...
				    		command_status.addToLog(CommandPhaseType.RUN,
				    			new CommandLogRecord(CommandStatusType.FAILURE,
					   			"Error checking @require comment (" + e + ").", "See log file for details.") );
			    		}
                	}
                }
        	    // Refresh severity since not handled in the command
       	    	command_status.refreshPhaseSeverity(CommandPhaseType.INITIALIZATION,CommandStatusType.SUCCESS);
   			 	command_status.refreshPhaseSeverity(CommandPhaseType.RUN,CommandStatusType.SUCCESS);
   			 	commandProfile.setEndTime(System.currentTimeMillis());
               	commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			continue;
    		}
    		else if ( command instanceof CommentBlockStart_Command ) {
    			inComment = true;
    			command_status.refreshPhaseSeverity(CommandPhaseType.INITIALIZATION,CommandStatusType.SUCCESS);
    			command_status.refreshPhaseSeverity(CommandPhaseType.RUN,CommandStatusType.SUCCESS);
    			commandProfile.setEndTime(System.currentTimeMillis());
                commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			continue;
    		}
    		else if ( command instanceof CommentBlockEnd_Command ) {
    			inComment = false;
    			command_status.refreshPhaseSeverity(CommandPhaseType.INITIALIZATION,CommandStatusType.SUCCESS);
    			command_status.refreshPhaseSeverity(CommandPhaseType.RUN,CommandStatusType.SUCCESS);
    			commandProfile.setEndTime(System.currentTimeMillis());
                commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			continue;
    		}
    		if ( inComment ) {
    		    // Commands won't know themselves that they are in a comment so set the status for them
    		    // and continue.
    		    // TODO SAM 2008-09-30 Do the logs need to be cleared?
    			command_status.refreshPhaseSeverity(CommandPhaseType.INITIALIZATION,CommandStatusType.SUCCESS);
    			command_status.refreshPhaseSeverity(CommandPhaseType.RUN,CommandStatusType.SUCCESS);
    			commandProfile.setEndTime(System.currentTimeMillis());
                commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			Message.printStatus ( 1, routine, "In comment...skipping command." );
    			continue;
    		}
    		else if ( command instanceof Exit_Command ) {
    			// Exit the processing...
    			Message.printStatus ( 1, routine, "Exit - stop processing commands." );
    			commandProfile.setEndTime(System.currentTimeMillis());
                commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			break;
    		}
    	
    		// Check for obsolete commands (do this last to minimize the amount of processing through this code)...
    		// Do this at the end because this logic may seldom be hit if valid commands are processed above.  
    		/* FIXME SAM 2008-10-14 Evaluate whether needed
    		else if ( processCommands_CheckForObsoleteCommands(command_String, (CommandStatusProvider)command, message_tag, i_for_message) ) {
    			// Had a match so increment the counters.
    			++update_count;
    			++error_count;
    		}
    		*/
    		// Command factory for remaining commands...
    		else {
                // Try the Command class code...
    			try {
                    // Make sure the command is valid...
    				// Initialize the command (parse)...
    				// TODO SAM 2007-09-05 Need to evaluate where the initialization occurs (probably the initial edit or load)?
    				if ( Message.isDebugOn ) {
    					Message.printDebug ( 1, routine, "Initializing the Command for \"" +	command_String + "\"" );
    				}
    				if ( command instanceof CommandStatusProvider ) {
    					((CommandStatusProvider)command).getCommandStatus().clearLog(CommandPhaseType.INITIALIZATION);
    				}
    				if ( command instanceof CommandStatusProvider ) {
    					((CommandStatusProvider)command).getCommandStatus().clearLog(CommandPhaseType.DISCOVERY);
    				}
    				command.initializeCommand ( command_String, this, true );
    				// TODO SAM 2005-05-11 Is this the best place for this or should it be in RunCommand()?
    				// Check the command parameters...
    				if ( Message.isDebugOn ) {
    					Message.printDebug ( 1, routine, "Checking the parameters for command \"" + command_String + "\"" );
    				}
    				command.checkCommandParameters ( command.getCommandParameters(), command_tag, 2 );
    				// Clear the run status for the command...
    				if ( command instanceof CommandStatusProvider ) {
    					((CommandStatusProvider)command).getCommandStatus().clearLog(CommandPhaseType.RUN);
    				}
    				// Run the command...
    				if ( Message.isDebugOn ) {
    					Message.printDebug ( 1, routine, "Running command through new code..." );
    				}
    				command.runCommand ( i_for_message );
    				if ( Message.isDebugOn ) {
    					Message.printDebug ( 1, routine, "...back from running command." );
    				}
    			}
    			catch ( InvalidCommandSyntaxException e ) {
    				message = "Unable to process command - invalid syntax (" + e + ").";
    				if ( command instanceof CommandStatusProvider ) {
    				       if (	CommandStatusUtil.getHighestSeverity((CommandStatusProvider)command).
                                   greaterThan(CommandStatusType.UNKNOWN) ) {
    				           // No need to print a message to the screen because a visual marker will be shown, but log...
    				           Message.printWarning ( 2,
    				                   MessageUtil.formatMessageTag(command_tag,
    				                           ++error_count), routine, message );
                           }
    				}
    				else {
    				    // Command has not been updated to set warning/failure in status so show here
    					Message.printWarning ( popup_warning_level,
    						MessageUtil.formatMessageTag(command_tag,
    						++error_count), routine, message );
    				}
    				// Log the exception.
    				if (Message.isDebugOn) {
    					Message.printDebug(3, routine, e);
    				}
    				continue;
    			}
    			catch ( InvalidCommandParameterException e ) {
    				message = "Unable to process command - invalid parameter (" + e + ").";
    				if ( command instanceof CommandStatusProvider ) {
    				    if ( CommandStatusUtil.getHighestSeverity((CommandStatusProvider)command).
                                greaterThan(CommandStatusType.UNKNOWN) ) {
    				        // No need to print a message to the screen because a visual marker will be shown, but log...
    				        Message.printWarning ( 2,
    				                MessageUtil.formatMessageTag(command_tag,
    				                        ++error_count), routine, message );
                        }
    				}
    				else {
    				    // Command has not been updated to set warning/failure in status so show here
    					Message.printWarning ( popup_warning_level,
    							MessageUtil.formatMessageTag(command_tag,
    									++error_count), routine, message );
    				}
    				if (Message.isDebugOn) {
    					Message.printWarning(3, routine, e);
    				}
    				continue;
    			}
    			catch ( CommandWarningException e ) {
    				message = "Warnings were generated processing command - output may be incomplete (" + e + ").";
    				if ( command instanceof CommandStatusProvider ) {
    				    if ( CommandStatusUtil.getHighestSeverity((CommandStatusProvider)command).
                                greaterThan(CommandStatusType.UNKNOWN) ) {
    				        // No need to print a message to the screen because a visual marker will be shown, but log...
    				        Message.printWarning ( 2,
    				                MessageUtil.formatMessageTag(command_tag,
    				                        ++error_count), routine, message );
                        }
    				}
    				else {	// Command has not been updated to set warning/failure in status so show here
    					Message.printWarning ( popup_warning_level,
    							MessageUtil.formatMessageTag(command_tag,
    									++error_count), routine, message );
    				}
    				if (Message.isDebugOn) {
    					Message.printDebug(3, routine, e);
    				}
    				continue;
    			}
    			catch ( CommandException e ) {
    				message = "Error processing command - unable to complete command (" + e + ").";
    				if ( command instanceof CommandStatusProvider ) {
    				    if ( CommandStatusUtil.getHighestSeverity((CommandStatusProvider)command).
                                greaterThan(CommandStatusType.UNKNOWN) ) {
    				        // No need to print a message to the screen because a visual marker will be shown, but log...
    				        Message.printWarning ( 2,
    				                MessageUtil.formatMessageTag(command_tag,++error_count), routine, message );
                        }
    				}
    				else {
    				    // Command has not been updated to set warning/failure in status so show here
    					Message.printWarning ( popup_warning_level,
    						MessageUtil.formatMessageTag(command_tag,
    						++error_count), routine, message );
    				}
    				if (Message.isDebugOn) {
    					Message.printDebug(3, routine, e);
    				}
    				continue;
    			}
    			catch ( Exception e ) {
    				message = "Unexpected error processing command - unable to complete command (" + e + ").";
    				if ( command instanceof CommandStatusProvider ) {
    					// Add to the log as a failure...
    					Message.printWarning ( 2,
    						MessageUtil.formatMessageTag(command_tag,++error_count), routine, message );
                        // Always add to the log because this type of exception is unexpected from a Command object.
    					command_status.addToLog(CommandPhaseType.RUN,
    							new CommandLogRecord(CommandStatusType.FAILURE,
    									"Unexpected exception \"" + e.getMessage() + "\"",
    									"See log file for details.") );
    				}
    				else {
    					Message.printWarning ( popup_warning_level,
    							MessageUtil.formatMessageTag(command_tag,
    									++error_count), routine, message );
    				}
    				Message.printWarning ( 3, routine, e );
    				continue;
    			}
    			finally {
    				// Save the time spent running the command
    	    		stopWatch.stop();
    	    		commandProfile.setEndTime(System.currentTimeMillis());
                    commandProfile.setEndHeap(Runtime.getRuntime().totalMemory());
    			}
    		}
		} // Main catch
		catch ( Exception e ) {
			Message.printWarning ( popup_warning_level, MessageUtil.formatMessageTag(command_tag,
			++error_count), routine, "There was an error processing command: \"" + command_String +
			"\".  Cannot continue processing." );
			Message.printWarning ( 3, routine, e );
			if ( command instanceof CommandStatusProvider ) {
				// Add to the command log as a failure...
				command_status.addToLog(CommandPhaseType.RUN,
						new CommandLogRecord(CommandStatusType.FAILURE,
								"Unexpected error \"" + e.getMessage() + "\"", "See log file for details.") );
			}
		}
		catch ( OutOfMemoryError e ) {
		    message = "The command processor ran out of memory. (" + e + ").";
			Message.printWarning ( popup_warning_level,
			MessageUtil.formatMessageTag(command_tag,
			++error_count), routine, message );
			if ( command instanceof CommandStatusProvider ) {
				// Add to the command log as a failure...
				command_status.addToLog(CommandPhaseType.RUN,
					new CommandLogRecord(CommandStatusType.FAILURE, message,
						"Try increasing JRE memory with -Xmx and restarting the software.  " +
						"See the log file for details.  See troubleshooting documentation.") );
			}
			Message.printWarning ( 2, routine, e );
			System.gc();
			// May be able to save commands.
		}
		finally {
			// Always want to get to here for each command.
		}
		// Notify any listeners that the command is done running...
		prev_command_complete_notified = true;
		notifyCommandProcessorListenersOfCommandCompleted ( i, size, command );
		Message.printStatus ( 1, routine,
            "Done processing command \"" + command_String + "\" (" +  (i + 1) + " of " + size + " commands, " +
            StringUtil.formatString(commandProfile.getRunTime(),"%d") + " ms runtime)" );
        Message.printStatus ( 1, routine, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" );
	}
	// If necessary, do a final notify for the last command...
	if ( !prev_command_complete_notified ) {
		if ( i == size ) {
			--i;
		}
		notifyCommandProcessorListenersOfCommandCompleted ( i, size, command );
	}
	
	// Indicate that processing is done and now there is no need to worry about cancelling.
	setIsRunning ( false );
	if ( getCancelProcessingRequested() ) {
		// Have gotten to here probably because the last command was processed
		// and need to notify the listeners.
		notifyCommandProcessorListenersOfCommandCancelled (	i, size, command );
	}
	setCancelProcessingRequested ( false );
	
    // Make sure that important warnings are shown to the user...
    Message.setPropValue ( "ShowWarningDialog=true" );

	// Get the final time - note this includes intervening warnings if any occurred...

	stopwatch.stop();
	Message.printStatus ( 1, routine, "Processing took " +
		StringUtil.formatString(stopwatch.getSeconds(),"%.2f") + " seconds" );

	// Check for fatal errors (for Command classes, only warn if failures since
	// others are likely not a problem)...

	int ml = 2;	// Message level for cleanup warnings
	List<CommandStatusProvider> cspList = new ArrayList<CommandStatusProvider>();
	for ( Command c : commandList ) {
	    if ( c instanceof CommandStatusProvider ) {
	        cspList.add((CommandStatusProvider)c);
	    }
	}
	CommandStatusType max_severity = CommandStatusProviderUtil.getHighestSeverity ( cspList );
	if ( (error_count > 0) || max_severity.greaterThan(CommandStatusType.WARNING)) {

		if ( IOUtil.isBatch() ) {
			// The following should will be passed through StateDMI_Processor.RunCommands() and should
			// be caught when using StateDMI_Processor_ThreadRunner.runCommands().
			message = "There were warnings or failures processing commands.  The output may be incomplete.";
			Message.printWarning ( ml, routine, message );
			throw new RuntimeException ( message );
		}
		else {
		    Message.printWarning ( ml, routine,
			"There were warnings processing commands.  The output may be incomplete.\n" +
			"See the log file for information." );
		}
	}
	if ( update_count > 0 ) {
		Message.printWarning ( ml, routine,
		"There were warnings printed for obsolete commands.\n" +
		"See the log file for information.  The output may be incomplete." );
	}
}

/**
Reset all the data/results lists to be empty.
@param appendResults if false, remove all the previous results before processing.
*/
private void processCommands_ResetDataForRunStart ( boolean appendResults )
throws Exception
{
	setPropContents ( "OutputStart", null );
	setPropContents ( "OutputEnd", null );
	setPropContents ( "OutputYearType", YearType.CALENDAR );
	// Clear all old results
	if ( !appendResults ) {
		clearResults();
	}
	// Clear the HydroBase DMI caches
	HydroBaseDMI dmi = getHydroBaseDMIConnection();
	if ( dmi != null ) {
		dmi.clearCaches();
	}

	// Create data sets, to track which components are created and store
	// data check information by component.
	// TODO SAM 2006-04-10
	// This may allow the list of output files to be removed at some point.
	// However, there are output files (e.g., efficiency reports) that are
	// not currently data components.  Some things that could use further study:
	// 1)	Should the data set components be used instead of the separate lists?
	// 2)	Should the data sets be integrated with the StateDMI_JFrame so
	//	that results can be taken from the data set?

	// Need the following to register data with
	// StateMod and StateCU to allow validation cross-checks between components.
	__StateCU_DataSet = new StateCU_DataSet();
	__StateMod_DataSet = new StateMod_DataSet();
	////// StateMod data //////
	// Well Components
	DataSetComponent comp = __StateMod_DataSet.getComponentForComponentType( StateMod_DataSet.COMP_WELL_STATIONS );
	comp.setData ( __SMWellList );
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_WELL_RIGHTS );
	comp.setData ( __SMWellRightList );
	// Diversion Components
	comp = __StateMod_DataSet.getComponentForComponentType( StateMod_DataSet.COMP_DIVERSION_STATIONS );
	comp.setData ( __SMDiversionStationList );
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_DIVERSION_RIGHTS );
	comp.setData ( __SMDiversionRightList );
	// Operational Components
	comp = __StateMod_DataSet.getComponentForComponentType( StateMod_DataSet.COMP_OPERATION_RIGHTS);
	comp.setData ( __SMOperationalRightList );
	// Plan Components
	comp = __StateMod_DataSet.getComponentForComponentType( StateMod_DataSet.COMP_PLANS );
	comp.setData ( __SMPlanList );
	// Stream Gage Components
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_STREAMGAGE_STATIONS);
	comp.setData ( __SMStreamGageStationList );
//		// Delay Table Monthly
//		comp = __StateMod_DataSet.getComponentForComponentType (
//			StateMod_DataSet.COMP_DELAY_TABLES_MONTHLY);
//		comp.setData ( __SMDelayTableMonthly_List );
//		// Delay Table Daily
//		comp = __StateMod_DataSet.getComponentForComponentType (
//			StateMod_DataSet.COMP_DELAY_TABLES_DAILY);
//		comp.setData ( __SMDelayTableDaily_List );
	// Reservoir Components
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_RESERVOIR_STATIONS);
	comp.setData ( __SMReservoirStationList );
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_RESERVOIR_RIGHTS);
	comp.setData ( __SMReservoirRightList );
	// Instream Flow Components
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_INSTREAM_STATIONS);
	comp.setData ( __SMInstreamFlowStationList );
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_INSTREAM_RIGHTS);
	comp.setData ( __SMInstreamFlowRightList );
	// Stream Estimate Components
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_STREAMESTIMATE_STATIONS);
	comp.setData ( __SMStreamEstimateStationList );
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_STREAMESTIMATE_COEFFICIENTS);
	comp.setData ( __SMStreamEstimateCoefficients_List );
	// River Network Components
	comp = __StateMod_DataSet.getComponentForComponentType ( StateMod_DataSet.COMP_RIVER_NETWORK);
	comp.setData ( __SMRiverNetworkNode_List );
	
	////// StateCU data //////
	// TODO KAT 2007-04-16
	// Need to add checks for Time Series data components
	// Crop Pattern TS Data
//		comp = __StateCU_DataSet.getComponentForComponentType(
//			StateCU_DataSet.COMP_CROP_PATTERN_TS_YEARLY );
//		comp.setData ( __CUCropPatternTS_List );
//		// Irrigation Practice TS Yearly Data
//		comp = __StateCU_DataSet.getComponentForComponentType(
//			StateCU_DataSet.COMP_IRRIGATION_PRACTICE_TS_YEARLY );
//		comp.setData ( __CUIrrigationPracticeTS_List );
	// Blaney-Criddle Data
	comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_BLANEY_CRIDDLE );
	comp.setData ( __CUBlaneyCriddle_List );
	// Penman-Monteith Data
	comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_PENMAN_MONTEITH );
	comp.setData ( __CUPenmanMonteith_List );
	// Climate Station Data
	comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_CLIMATE_STATIONS );
	comp.setData ( __CUClimateStation_List );
	// Crop Characteristics Data
	comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_CROP_CHARACTERISTICS );
	comp.setData ( __CUCropCharacteristics_List );
	// Location Data
	comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_CU_LOCATIONS );
	comp.setData ( __CULocation_List );
	// Parcel Data
	// - TODO smalers 2020-11-05 decide whether parcels are officially part of the dataset
	//comp = __StateCU_DataSet.getComponentForComponentType( StateCU_DataSet.COMP_CU_PARCELS );
	//comp.setData ( __CUParcel_List );
}

/**
Process a request, required by the CommandProcessor interface.
This is a generalized way to allow commands to call specialized functionality
through the interface without directly naming a processor.  For example, the
request may involve data that only the StateDMI_Processor has access to and that a command does not.
Currently the following requests are handled:
<table width=100% cellpadding=10 cellspacing=0 border=2>
<tr>
<td><b>Request</b></td>	<td><b>Description</b></td>
</tr>

<tr>
<td><b>AddCommandProcessorEventListener</b></td>
<td>Add a CommandProcessorEventListener to the processor, which will pass on events from
commands to these listeners.  It is expected that the listener will be added before each
run (via commands) and will be removed at the end of the run.  This design may need to
change as testing occurs.  Parameters to this request are:
<ol>
<li>    <b>TS</b> Monthly time series to process, as TS (MonthTS) object.</li>
<li>    <b>Index</b> The index (0+) of the time series identifier being processed,
        as an Integer.</li>
</ol>
Returned values from this request are:
<ol>
<li>    <b>CommandProcessorEventListener</b>the listener to add.</li>
</ol>
</td>
</tr>

<tr>
<td><b>RunCommands</b></td>
<td>Run commands to create the results:
<ol>
<li>	<b>CommandList</b> A list of Command instances to run.</li>
<li>	<b>InitialWorkingDir</b> The initial working directory as a String, to initialize paths.</li>
</ol>
Returned values from this request are:
<ol>
<li>	None - time series results will contain the results.</li>
</ol>
</td>
</tr>

</table>
@param request_params An optional list of parameters to be used in the request.
@exception Exception if the request cannot be processed.
@return the results of a request, or null if a value is not found.
*/
public CommandProcessorRequestResultsBean processRequest ( String request, PropList request_params )
throws Exception
{	// Call helper methods based on the request that is being made...
    if ( request.equalsIgnoreCase("AddCommandProcessorEventListener") ) {
        return processRequest_AddCommandProcessorEventListener ( request, request_params );
    }
	else if ( request.equalsIgnoreCase("DateTime") ) {
		return processRequest_DateTime ( request, request_params );
	}
    else if ( request.equalsIgnoreCase("GetTable") ) {
        return processRequest_GetTable ( request, request_params );
    }
    else if ( request.equalsIgnoreCase("GetPropertyHashtable") ) {
        return processRequest_GetPropertyHashtable ( request, request_params );
    }
    else if ( request.equalsIgnoreCase("GetProperty") ) {
        return processRequest_GetProperty ( request, request_params );
    }
    else if ( request.equalsIgnoreCase("GetWorkingDirForCommand") ) {
		return processRequest_GetWorkingDirForCommand ( request, request_params );
	}
    else if ( request.equalsIgnoreCase("RemoveProperty") ) {
        return processRequest_RemoveProperty ( request, request_params );
    }
	else if ( request.equalsIgnoreCase("RunCommands") ) {
		return processRequest_RunCommands ( request, request_params );
	}
	else if ( request.equalsIgnoreCase("SetHydroBaseDMI") ) {
		return processRequest_SetHydroBaseDMI ( request, request_params );
	}
	else if ( request.equalsIgnoreCase("SetProperty") ) {
        return processRequest_SetProperty ( request, request_params );
    }
	else if ( request.equalsIgnoreCase("SetTable") ) {
        return processRequest_SetTable ( request, request_params );
    }
	else if ( request.equalsIgnoreCase("RemoveTableFromResultsList") ) {
        return processRequest_RemoveTableFromResultsList ( request, request_params );
    }
	else {
		StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
		String warning = "Unknown StateDMIProcessor request \"" + request + "\"";
		bean.setWarningText( warning );
		// TODO SAM 2007-02-07 Need to figure out a way to indicate
		// an error and pass back useful information.
		throw new UnrecognizedRequestException ( warning );
	}
}

/**
Process the AddCommandProcessorEventListener request.
*/
private CommandProcessorRequestResultsBean processRequest_AddCommandProcessorEventListener (
        String request, PropList request_params )
throws Exception
{   StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "CommandProcessorEventListener" );
    if ( o == null ) {
            String warning = "Request AddCommandProcessorEventListener() does not " +
            		"provide a CommandProcessorEventListener parameter.";
            bean.setWarningText ( warning );
            bean.setWarningRecommendationText ( "This is likely a software code error.");
            throw new RequestParameterNotFoundException ( warning );
    }
    CommandProcessorEventListener listener = (CommandProcessorEventListener)o;
    addCommandProcessorEventListener ( listener );
    // No data are returned in the bean.
    return bean;
}

/**
Get a date/time property (DateTime instances) from a string.  The string is first expanded to fill ${Property} strings and then the
matching property name is used to determine the date/time using the following rules:
<ol>
<li> If the string is null, "*" or "", return null.</li>
<li> If the string uses a standard name InputStart (QueryStart), InputEnd (QueryEnd), OutputStart, OutputEnd, return the corresponding DateTime.</li>
<li> Check the processor date/time hash table for user-defined date/time properties.</li>
<li> Parse the string using DateTime.parse().
</ol>
@param request the processor request "DateTime" for logging
@param request_params request parameters:
<ol>
<li> DateTime - date/time string to process into a DateTime object
</ol>
*/
private CommandProcessorRequestResultsBean processRequest_DateTime ( String request, PropList request_params )
throws Exception
{	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
	// Get the necessary parameters...
	Object o = request_params.getContents ( "DateTime" );
	if ( o == null ) {
		String warning = "Request DateTime() does not provide a DateTime parameter.";
		bean.setWarningText ( warning );
		bean.setWarningRecommendationText ( "This is likely a software code error.");
		throw new RequestParameterNotFoundException ( warning );
	}
	String DateTime = (String)o;
	DateTime dt = getDateTime ( DateTime );
	PropList results = bean.getResultsPropList();
	// This will be set in the bean because the PropList is a reference...
	results.setUsingObject("DateTime", dt );
	return bean;
}

/**
Process the GetTable request.
*/
private CommandProcessorRequestResultsBean processRequest_GetTable (
        String request, PropList request_params )
throws Exception
{   StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "TableID" );
    if ( o == null ) {
            String warning = "Request GetTable() does not provide a TableID parameter.";
            bean.setWarningText ( warning );
            bean.setWarningRecommendationText ( "This is likely a software code error.");
            throw new RequestParameterNotFoundException ( warning );
    }
    String TableID = (String)o;
    int size = 0;
    if ( __TableList != null ) {
        size = __TableList.size();
    }
    DataTable table = null;
    boolean found = false;
    for ( int i = 0; i < size; i++ ) {
        table = (DataTable)__TableList.get(i);
        if ( table.getTableID().equalsIgnoreCase(TableID) ) {
            found = true;
            break;
        }
    }
    if ( !found ) {
        table = null;
    }
    PropList results = bean.getResultsPropList();
    // This will be set in the bean because the PropList is a reference...
    results.setUsingObject("Table", table );
    return bean;
}

/**
Process the GetProperty request.  User-specified properties are checked first and
if not found the built-in properties are requested.
*/
private CommandProcessorRequestResultsBean processRequest_GetProperty (
        String request, PropList request_params )
throws Exception
{   StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "PropertyName" );
    if ( o == null ) {
        String warning = "Request GetProperty() does not provide a PropertyName parameter.";
        bean.setWarningText ( warning );
        bean.setWarningRecommendationText ( "This is likely a software code error.");
        throw new RequestParameterNotFoundException ( warning );
    }
    String PropertyName = (String)o;
    Object PropertyValue = __propertyHashmap.get ( PropertyName );
    if ( PropertyValue == null ) {
        // Try the built-in properties
        PropertyValue = getPropContents(PropertyName);
    }
    // Return the property value in the bean.
    PropList results = bean.getResultsPropList();
    // This will be set in the bean because the PropList is a reference...
    results.setUsingObject("PropertyValue", PropertyValue );
    return bean;
}

/**
Process the GetPropertyHashtable request.  Currently only user-specified properties are returned and only if the request parameter "UserProperties=True".
@return Hashtable of properties, not in sorted order.  This is a new Hashtable instance whose contents generally should not be modified.
*/
private CommandProcessorRequestResultsBean processRequest_GetPropertyHashtable (
        String request, PropList request_params )
throws Exception
{  	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
	// New Hashtable to return
	Hashtable<String,Object> ph = new Hashtable<String,Object>();
	// Get the necessary parameters...
	Object o = request_params.getContents ( "GetUserProperties" );
	if ( o != null ) {
		String propval = (String)o;
		if ( (propval != null) && propval.equalsIgnoreCase("true") ) {
			// Transfer the user-specified properties
			Set<String> keys = __propertyHashmap.keySet();
			for ( String key : keys ) {
				o = __propertyHashmap.get ( key );
				ph.put(key,o);
			}			
		}
	}
	// TODO SAM 2015-04-26 Transfer the internal properties
    // Return the property value in the bean.
    PropList results = bean.getResultsPropList();
    // This will be set in the bean because the PropList is a reference...
    results.setUsingObject("PropertyHashtable", ph );
    return bean;
}

/**
Process the GetWorkingDirForCommand request.  This runs a processor on only the SetWorkingDir() commands
in a command list.  The initial working directory is set to that of the processor.
If no SetWorkingDir() commands are found, then the current initial working directory will be returned.
*/
private CommandProcessorRequestResultsBean processRequest_GetWorkingDirForCommand (
		String request, PropList request_params )
throws Exception
{	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
	// Get the necessary parameters...
	Object o = request_params.getContents ( "Command" );
	if ( o == null ) {
			String warning = "Request GetWorkingDirForCommand() does not provide a Command parameter.";
			bean.setWarningText ( warning );
			bean.setWarningRecommendationText (
					"This is likely a software code error.");
			throw new RequestParameterNotFoundException ( warning );
	}
	Command command = (Command)o;
	// Get the index of the requested command...
	int index = indexOf ( command );
	// Get the setWorkingDir() commands...
	List<String> neededCommandsList = new ArrayList<>();
	neededCommandsList.add ( "SetWorkingDir" );
	List<Command> setWorkingDir_CommandList = StateDMI_Processor_Util.getCommandsBeforeIndex (
			index,
			this,
			neededCommandsList,
			false );	// Get all, not just last
	String WorkingDir = getInitialWorkingDir();
	if ( neededCommandsList.size() > 0 ) {
		// Have some SetWorkingDir() commands so need to do some more work
		// Create a local command processor
		StateDMI_Processor statedmi_processor = new StateDMI_Processor();
		statedmi_processor.setInitialWorkingDir ( getInitialWorkingDir() );
		int size = setWorkingDir_CommandList.size();
		// Add all the commands (currently no method to add all because this is normally not done).
		for ( int i = 0; i < size; i++ ) {
			statedmi_processor.addCommand ( setWorkingDir_CommandList.get(i));
		}
		// Run the commands to set the working directory in the temporary processor...
		try {
			statedmi_processor.runCommands(
				null,	// Process all commands in this processor
				null );	// No need for controlling properties since controlled by commands
			WorkingDir = (String)statedmi_processor.getPropContents ( "WorkingDir");
		}
		catch ( Exception e ) {
			// This is a software problem.
			String routine = getClass().getName() + ".processRequest_GetWorkingDirForCommand";
			Message.printWarning(2, routine, "Error getting working directory for command." );
			Message.printWarning(2, routine, e);
			// Rethrow
			throw e;
		}
	}
	// Return the working directory as a String.  This can then be used in editors, for
	// example.  The WorkingDir property will have been set in the temporary processor.
	PropList results = bean.getResultsPropList();
	results.set( "WorkingDir", WorkingDir );
	return bean;
}

/**
Process the SetProperty request.  Null property values are NOT allowed.
*/
private CommandProcessorRequestResultsBean processRequest_RemoveProperty (
        String request, PropList request_params )
throws Exception
{   StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "PropertyName" );
    if ( o == null ) {
            String warning = "Request SetProperty() does not provide a PropertyName parameter.";
            bean.setWarningText ( warning );
            bean.setWarningRecommendationText ( "This is likely a software code error.");
            throw new RequestParameterNotFoundException ( warning );
    }
    String PropertyName = (String)o;
    // Do not allow removing official property like InputStart as this would likely cause problems.
    // First see if it is a known user-defined property
    Object o2 = __propertyHashmap.get ( PropertyName );
    if ( o2 != null ) {
    	// Found it so remove (for some reason can't pass in o2 and have it work)
    	__propertyHashmap.remove(PropertyName);
    }
    // No data are returned in the bean.
    return bean;
}

/**
Process the RemoveTableFromResultsList request.
*/
private CommandProcessorRequestResultsBean processRequest_RemoveTableFromResultsList (
    String request, PropList request_params )
throws Exception
{   //String routine = "TSCommandProcessor.processRequest_RemoveTableFromResultsList";
    StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "TableID" );
    if ( o == null ) {
        String warning = "Request RemoveTableFromResultsList() does not provide a TableID parameter.";
        bean.setWarningText ( warning );
        bean.setWarningRecommendationText ( "This is likely a software code error.");
        throw new RequestParameterNotFoundException ( warning );
    }
    String TableID = (String)o;
    // Remove all tables having the same identifier.
    DataTable table;
    for ( int i = 0; i < __TableList.size(); i++ ) {
        table = __TableList.get(i);
        // Remove and decrement the counter so that the next table is checked
        if ( table.getTableID().equalsIgnoreCase(TableID) ) {
            __TableList.remove(i--);
        }
    }
    return bean;
}

/**
Process the RunCommands request.
*/
private CommandProcessorRequestResultsBean processRequest_RunCommands (
		String request, PropList request_params )
throws Exception
{	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
	// Get the necessary parameters...
	// Command list.
	Object o = request_params.getContents ( "CommandList" );
	if ( o == null ) {
			String warning = "Request RunCommands() does not provide a CommandList parameter.";
			bean.setWarningText ( warning );
			bean.setWarningRecommendationText (	"This is likely a software code error.");
			throw new RequestParameterNotFoundException ( warning );
	}
	@SuppressWarnings("unchecked")
	List<Command> commands = (List<Command>)o;
	// Whether commands should create output...
	Object o3 = request_params.getContents ( "CreateOutput" );
	if ( o3 == null ) {
			String warning = "Request RunCommands() does not provide a CreateOutput parameter.";
			bean.setWarningText ( warning );
			bean.setWarningRecommendationText ( "This is likely a software code error.");
			throw new RequestParameterNotFoundException ( warning );
	}
	Boolean CreateOutput_Boolean = (Boolean)o3;
	// Set properties as per the legacy application.
	PropList props = new PropList ( "RunCommands");
	props.set ( "CreateOutput", "" + CreateOutput_Boolean );

	runCommands ( commands, props );
	// No results need to be returned.
	return bean;
}

/**
Process the SetHydroBaseDMI request.
*/
private CommandProcessorRequestResultsBean processRequest_SetHydroBaseDMI (
		String request, PropList request_params )
throws Exception
{	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
	// Get the necessary parameters...
	Object o = request_params.getContents ( "HydroBaseDMI" );
	if ( o == null ) {
			String warning = "Request SetHydroBaseDMI() does not provide a HydroBaseDMI parameter.";
			bean.setWarningText ( warning );
			bean.setWarningRecommendationText ( "This is likely a software code error.");
			throw new RequestParameterNotFoundException ( warning );
	}
	HydroBaseDMI dmi = (HydroBaseDMI)o;
	// Add an open HydroBaseDMI instance, closing a previous connection
	// of the same name if it exists.
	__hdmi = dmi;
	// No results need to be returned.
	return bean;
}

/**
Process the SetProperty request.
Nulls are allowed, but typically only with a special request.
Otherwise, it is difficult to check input for errors.
*/
private CommandProcessorRequestResultsBean processRequest_SetProperty (
        String request, PropList request_params )
throws Exception
{   
	StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "PropertyName" );
    if ( o == null ) {
            String warning = "Request SetProperty() does not provide a PropertyName parameter.";
            bean.setWarningText ( warning );
            bean.setWarningRecommendationText ( "This is likely a software code error.");
            throw new RequestParameterNotFoundException ( warning );
    }
    String PropertyName = (String)o;
    Object o2 = request_params.getContents ( "PropertyValue" );
    if ( o2 == null ) {
    	Object o3 = request_params.getValue ( "SetNull" );
    	if ( (o3 != null) && o3.toString().equalsIgnoreCase("true") ) { 
	        String warning = "Request SetProperty() does not provide a PropertyValue parameter.";
	        bean.setWarningText ( warning );
	        bean.setWarningRecommendationText ( "This is likely a software code error.");
	        throw new RequestParameterNotFoundException ( warning );
    	}
    	// Else OK to set a null property
    }
    // Try to set official property...
    Collection<String> internalProperties = getPropertyNameList(true,false);
    if ( internalProperties.contains(PropertyName) ) {
	    try {
	    	// Null is OK here for o2
	        setPropContents(PropertyName, o2);
	    }
	    catch ( UnrecognizedRequestException e ) {
	        // Not recognized as a core internal so will set below as a user property
	    }
    }
    else {
	    // Otherwise it is a user-defined property...
	    __propertyHashmap.put ( PropertyName, o2 );
    }
    // No data are returned in the bean.
    return bean;
}

/**
Process the SetTable request.
*/
private CommandProcessorRequestResultsBean processRequest_SetTable (
        String request, PropList request_params )
throws Exception
{   StateDMIProcessorRequestResultsBean bean = new StateDMIProcessorRequestResultsBean();
    // Get the necessary parameters...
    Object o = request_params.getContents ( "Table" );
    if ( o == null ) {
            String warning = "Request SetTable() does not provide a Table parameter.";
            bean.setWarningText ( warning );
            bean.setWarningRecommendationText ("This is likely a software code error.");
            throw new RequestParameterNotFoundException ( warning );
    }
    DataTable o_DataTable = (DataTable)o;
    // Loop through the tables.  If a matching table ID is found, reset.  Otherwise, add at the end.
    int size = __TableList.size();
    DataTable table;
    boolean found = false;
    for ( int i = 0; i < size; i++ ) {
        table = __TableList.get(i);
        if ( table.getTableID().equalsIgnoreCase(o_DataTable.getTableID())) {
            __TableList.set(i,o_DataTable);
            found = true;
        }
    }
    if ( !found ) {
        __TableList.add ( o_DataTable );
    }
    // No data are returned in the bean.
    return bean;
}

/**
Read the command file and initialize new commands.
@param path Path to the command file - this should be an absolute path.
@param createUnknownCommandIfNotRecognized If true, create a GenericCommand
if the command is not recognized.  This is being used during transition of old
string commands to full Command classes.
@param append If true, the commands will be appended to the existing commands.
@exception IOException if there is a problem reading the file.
@exception FileNotFoundException if the specified commands file does not exist.
*/
public void readCommandFile ( String path, boolean createUnknownCommandIfNotRecognized, boolean append )
throws IOException, FileNotFoundException
{	String routine = getClass().getName() + ".readCommandFile";
	BufferedReader br = null;
	br = new BufferedReader( new FileReader(path) );
	setCommandFileName ( path );   // This is used in headers, etc.
	// Set the working directory because this may be used by other commands.
	File path_File = new File(path);
	setInitialWorkingDir ( path_File.getParent() );
	String line;
	Command command = null;
	StateDMICommandFactory cf = new StateDMICommandFactory();
	// Use this to control whether listeners should be notified for each
	// insert.  Why would this be done?  If, for example, a GUI should display
	// the progress in reading/initializing the commands.
	//
	// Why would this not be done?  Becuse of performance issues.
	boolean notifyListenersForEachAdd = true;
	// If not appending, remove all...
	if ( !append ) {
		removeAllCommands();
	}
	// Now process each line in the file and turn into a command...
	int numAdded = 0;
	while ( true ) {
		line = br.readLine();
		if ( line == null ) {
			break;
		}
		// Trim spaces from the end of the line to clean up file.
		line = line.trim();
		// Create a command from the line.
		// Normally will create the command even if not recognized.
		if ( createUnknownCommandIfNotRecognized ) {
			try {
				command = cf.newCommand ( line, createUnknownCommandIfNotRecognized );
			}
			catch ( UnknownCommandException e ) {
				// Should not happen because of parameter passed above
			}
		}
		else {
			try {
				command = cf.newCommand ( line, createUnknownCommandIfNotRecognized );
			}
			catch ( UnknownCommandException e ) {
				// TODO SAM 2007-09-08 Evaluate how to handle unknown commands at load without stopping the load
				// In this case skip the command, although the above case may always be needed?
			}
		}
		// Have a command instance.  Initialize the command (parse the command string) and check its arguments.
		String fixme = "FIXME! ";  // String for inserted messages
		try {
			command.initializeCommand(
				line,	// Command string, needed to do full parse on parameters
				this,	// Processor, needed to make requests
				true);	// Do full initialization (parse)
		}
		catch ( InvalidCommandSyntaxException e ) {
		    // Can't use cf.newCommand() because it will recognized the command
		    // and generate yet another exception!  So, treat as a generic command with a problem.
		    Message.printWarning (2, routine, "Invalid command syntax.  Adding command with problems:  " + line );
            Message.printWarning(3, routine, e);
            // CommandStatus will be set while initializing so no need to set here
            // Do it anyway to make sure something does not fall through the cracks
            if ( (command != null) && (command instanceof CommandStatusProvider) ) {
                CommandStatus status = ((CommandStatusProvider)command).getCommandStatus();
                status.addToLog ( CommandPhaseType.INITIALIZATION,
                        new CommandLogRecord(CommandStatusType.FAILURE,
                                "Invalid command syntax (" + e + ").",
                                "Correct the command.  See log file for details." ) );
            }
            // Add generic commands as comments prior to this command to show the original,
            Command command2 = new GenericCommand ();
            command2.setCommandString ( "#" + fixme +
                    "The following command had errors and needs to be corrected below and this comment removed.");
            CommandStatus status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading the following command.",
                            "Correct the command below (typically a parameter error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            command2 = new GenericCommand ();
            command2.setCommandString ( "#" + fixme + line );
            status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading this command.",
                            "Correct the command below (typically a parameter error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            // Allow the bad command to be loaded below.  It may have no arguments or partial
            // parameters that need corrected.
		}
		catch ( InvalidCommandParameterException e) {
            // Can't use cf.newCommand() because it will recognized the command
            // and generate yet another exception!  So, treat as a generic command with a problem.
		    Message.printWarning (2, routine, "Invalid command parameter.  Adding command with problems:  " + line );
            Message.printWarning(3, routine, e);
            // CommandStatus will be set while initializing so no need to set here
            // Do it anyway to make sure something does not fall through the cracks
            if ( (command != null) && (command instanceof CommandStatusProvider) ) {
                CommandStatus status = ((CommandStatusProvider)command).getCommandStatus();
                status.addToLog ( CommandPhaseType.INITIALIZATION,
                        new CommandLogRecord(CommandStatusType.FAILURE,
                                "Invalid command parameter." + e + ").",
                                "Correct the command.  See log file for details." ) );
            }
            // Add generic commands as comments prior to this command to show the original,
            Command command2 = new GenericCommand ();
            command2.setCommandString ( "# " + fixme +
                    "The following command had errors and needs to be corrected below and this comment removed.");
            CommandStatus status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading the following command.",
                            "Correct the command below (typically an error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            command2 = new GenericCommand ();
            command2.setCommandString ( "#" + line );
            status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading this command.",
                            "Correct the command below (typically an error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            // Allow the bad command to be loaded below.  It may have no arguments or partial
            // parameters that need corrected.
		}
        catch ( Exception e ) {
            // TODO SAM 2007-11-29 Need to decide whether to handle here or in command with CommandStatus
            // It is important that the command get added, even if it is invalid, so the user can edit the
            // command file.  They will likely need to replace the command, not edit it.
            Message.printWarning( 1, routine, "Unexpected error creating command \"" + line + "\" - report to software support." );
            Message.printWarning ( 3, routine, e );
            // CommandStatus likely not set while initializing so need to set here to alert user
            if ( (command != null) && (command instanceof CommandStatusProvider) ) {
                CommandStatus status = ((CommandStatusProvider)command).getCommandStatus();
                status.addToLog ( CommandPhaseType.INITIALIZATION,
                        new CommandLogRecord(CommandStatusType.FAILURE,
                                "Unexpected error creating the command.",
                                "Check the command syntax.  See log file for details." ) );
            }
            // Add generic commands as comments prior to this command to show the original,
            Command command2 = new GenericCommand ();
            command2.setCommandString ( "#" + fixme +
                    " The following command had errors and needs to be corrected below and this comment removed.");
            CommandStatus status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading the following command.",
                            "Correct the command below (typically an error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            command2 = new GenericCommand ();
            command2.setCommandString ( "#" + fixme + line );
            status = ((CommandStatusProvider)command2).getCommandStatus();
            status.addToLog ( CommandPhaseType.INITIALIZATION,
                    new CommandLogRecord(CommandStatusType.FAILURE,
                            "There was an error loading this command.",
                            "Correct the command below (typically an error due to manual edit)." ) );
            addCommand ( command2, notifyListenersForEachAdd );
            ++numAdded;
            // Allow the bad command to be loaded below.  It may have no arguments or partial
            // parameters that need corrected.
        }
        // TODO SAM 2007-10-09 Evaluate whether to call listeners each time a command is added.
        // Could be good to indicate progress of load in the GUI.
        // For now, add the command, without notifying listeners of changes...
        if ( command != null ) {
            // Check the command parameters
            String command_tag = "" + numAdded + 1;  // Command number, for messaging
            int error_count = 0;
            try {  
                command.checkCommandParameters(command.getCommandParameters(), command_tag, 2 );
            }
            catch ( InvalidCommandParameterException e ) {
                /* TODO SAM 2008-05-14 Evaluate whether this can work - don't want a bunch
                of extra comments for commands that are already being flagged with status.
                // Add generic commands as comments prior to this command to show the original,
                Command command2 = new GenericCommand ();
                command2.setCommandString ( "#" + fixme +
                "The following command had errors and needs to be corrected below and this comment removed.");
                CommandStatus status = ((CommandStatusProvider)command2).getCommandStatus();
                status.addToLog ( CommandPhaseType.INITIALIZATION,
                        new CommandLogRecord(CommandStatusType.FAILURE,
                                "There was an error loading the following command.",
                                "Correct the command below (typically an error due to manual edit)." ) );
                addCommand ( command2, notify_listeners_for_each_add );
                ++num_added;
                command2 = new GenericCommand ();
                command2.setCommandString ( "#" + fixme + line );
                status = ((CommandStatusProvider)command2).getCommandStatus();
                status.addToLog ( CommandPhaseType.INITIALIZATION,
                        new CommandLogRecord(CommandStatusType.FAILURE,
                                "There was an error loading this command.",
                                "Correct the command below (typically an error due to manual edit)." ) );
                addCommand ( command2, notify_listeners_for_each_add );
                ++num_added;
                */
                // Add command status to the command itself, handling whether a recognized
                // command or a generic command (string command)...
                String message = "Error loading command - invalid syntax (" + e + ").";
                if ( command instanceof CommandStatusProvider ) {
                       if ( CommandStatusUtil.getHighestSeverity((CommandStatusProvider)command).
                               greaterThan(CommandStatusType.UNKNOWN) ) {
                           // No need to print a message to the screen because a visual marker will be shown, but log...
                           Message.printWarning ( 2,
                                   MessageUtil.formatMessageTag(command_tag,
                                           ++error_count), routine, message );
                       }
                       if ( command instanceof GenericCommand ) {
                            // The command class will not have added a log record so do it here...
                            ((CommandStatusProvider)command).getCommandStatus().addToLog ( CommandPhaseType.RUN,
                                    new CommandLogRecord(CommandStatusType.FAILURE,
                                            message, "Check the log for more details." ) );
                       }
                }
                else {
                    // Command has not been updated to set warning/failure in status so show here
                    Message.printWarning ( 2,
                        MessageUtil.formatMessageTag(command_tag,
                        ++error_count), routine, message );
                }
                // Log the exception.
                if (Message.isDebugOn) {
                    Message.printDebug(3, routine, e);
                }
            }
            // Now finally add the command to the list
            addCommand ( command, notifyListenersForEachAdd );
            ++numAdded;
            // Run discovery on the command so that the identifiers are available to other commands.
            // Do up front and then only when commands are edited.
            if ( command instanceof CommandDiscoverable ) {
                readCommandFile_RunDiscoveryOnCommand ( command );
            }
        }
	} // Looping over commands in file
	// Close the file...
	br.close();
	// Now notify listeners about the add one time (only need to do if it
	// was not getting done for each add...
	if ( !notifyListenersForEachAdd ) {
		notifyCommandListListenersOfAdd ( 0, (numAdded - 1) );
	}
}

/**
Run discovery on the command. This will, for example, make available a list of time series
to be requested with the ObjectListProvider.getObjectList() method.
*/
private void readCommandFile_RunDiscoveryOnCommand ( Command command_read )
{   String routine = getClass().getName() + ".commandList_EditCommand_RunDiscovery";
    // Run the discovery...
    Message.printStatus(2, routine, "Running discovery mode on command:  \"" + command_read + "\"" );
    try {
        ((CommandDiscoverable)command_read).runCommandDiscovery(indexOf(command_read));
    }
    catch ( Exception e )
    {
        // For now ignore because edit-time input may not be complete...
        String message = "Unable to make discover run - may be OK if partial data.";
        Message.printStatus(2, routine, message);
    }
}

/**
Read supplemental HydroBase_StructureView records (old was HydroBase_StructureIrrigSummaryTS)
records.  This does not actually read the records but retrieves them from memory in
HydroBase_StructureView_FromSet objects, created from HydroBase_ParcelUseTS_FromSet records
defined in the SetCropPatternTS() and SetCropPatternTSFromList() commands.
If a supplemental record is available that conflicts with existing data,
the supplemental data will be used and a warning is printed.
@param cropPatterns list of HydroBase_StructureView (old was HydroBase_StructureIrrigSummaryTS) as if read
from HydroBase.  This list will be added to and returned.
@param wdidList List of WDIDs to be checked.  Each string is parsed into WD
and ID parts.  It is assumed that only valid WDIDs are passed - any errors
parsing are ignored (should not happen).
@param InputStart_DateTime The starting date to process data.
@param InputEnd_DateTime The ending date to process data.
@param hydroBaseStructureViewFromSetList HydroBase_StructurView_FromSet instances
created from HydroBase_ParcelUseTS_FromSet records.
@param status used to add to command log
@param command_tag used to add to command log
@param warningLevel used to add to command log
@param warning_count used to add to command log
@return the list of HydroBase_StructureView (see cropPatterns).
*/
protected List<HydroBase_StructureView> readCropPatternTSFromSetForWDIDList (
	List<HydroBase_StructureView> cropPatterns, List<String> wdidList,
	DateTime InputStart_DateTime, DateTime InputEnd_DateTime,
	List<HydroBase_StructureView_FromSet> hydroBaseStructureViewFromSetList,
	CommandStatus status, String command_tag, int warningLevel, int warning_count )
{	String routine = "StateDMI_Processor.readCropPatternTSFromSetForWDIDList";
	if ( cropPatterns == null ) {
		cropPatterns = new ArrayList<>();
	}
	int cpsize = cropPatterns.size();
	HydroBase_StructureView_FromSet sits = null; // Supplemental
	HydroBase_StructureView sits2 = null; // From HydroBase
	//StateCU_CropPatternTS cp = null; // Previously read crop pattern data
	HydroBase_StructureView cp = null; // Previously read crop pattern data
	// Get a list of integer WDIDs to process...
	Message.printStatus ( 2, routine, "Getting supplemental acreage data "+
		"from SetCropPatternTS() commands for:  " + wdidList );
	int nwdid_list = 0;
	if ( wdidList != null ) {
		nwdid_list = wdidList.size();
	}
	int sits_wd, sits_id; // The WDID parts for the "sits" object
	int iwdid; // For looping through WDIDs.
	boolean found = false; // Used when searching for matching HydroBase and supplemental records.
	// Size of all supplemental data...
	int size = hydroBaseStructureViewFromSetList.size();
	for ( int i = 0; i < size; i++ ) {
		sits = hydroBaseStructureViewFromSetList.get(i);
		// Check to see if the record is in the desired year...
		if ( (InputStart_DateTime != null) && (InputEnd_DateTime != null)
			&& ((sits.getCal_year() < InputStart_DateTime.getYear()) ||
			((sits.getCal_year() > InputEnd_DateTime.getYear())) ) ){
			// The data record year is outside the requested year.
			continue;
		}
		// Figure out if the record matches a requested location identifier...
		sits_wd = sits.getWD();
		sits_id = sits.getID();
		for ( iwdid = 0; iwdid < nwdid_list; iwdid++ ) {
			// Now do the lookup on the more generic string ID...
			if ( !wdidList.get(iwdid).equalsIgnoreCase(sits.getLocationID())) {
				// Not a match...
				continue;
			}
			// If here, a match was found.  First see if there is
			// an existing matching record in the full data set.
			found = false;
			// TODO SAM 2004-05-18 - this is a major dog.  Need to rework the loops so that the large
			// vector is only traversed once.
			// FIXME SAM 2007-05-14 Need to decide with the State whether this should be flagged as an error.
			for ( int i2 = 0; i2 < cpsize; i2++ ) {
				sits2 = cropPatterns.get(i2);
				//boolean todo = true;
				//if ( todo ) {
				//throw new RuntimeException ("Need to fix.");
				cp = cropPatterns.get(i2);
				if ( (sits2.getWD() == sits_wd) && (sits2.getID() == sits_id) &&
					(sits2.getCal_year() ==	sits.getCal_year()) &&
					sits2.getLand_use().equalsIgnoreCase(sits.getLand_use()) ) {
					// Matching record, replace the old and print a warning...
					String message = "WD " + sits_wd + " ID " + sits_id +
					" supplemental data from SetCropPatternTS() matches raw (HydroBase) crop " +
					"pattern data for " + sits.getCal_year() + " " + sits.getLand_use();
					Message.printWarning ( warningLevel, 
				        MessageUtil.formatMessageTag(command_tag, ++warning_count), routine, message );
			        status.addToLog ( CommandPhaseType.RUN,
			            new CommandLogRecord(CommandStatusType.WARNING,
			                message, "Using data from set command and overriding HydroBase - " +
			                	"verify the set command." ) );
					found = true;
					// This is OK whether previously processed or not, since it is not additive.
					cropPatterns.set ( i2, sits );
				}
				//}
			}
			if ( !found ) {
				// No matching record was found so just add.  Only add if not previously processed.
				if ( sits.hasBeenProcessed() ) {
					// This is a warning that is handled internally but should
					// probably be handled by the modeler.
					String message = "Location " + sits.getLocationID() +
						" supplemental acreage data from SetCropPatternTS(): year=" +
						sits.getCal_year() + " crop=" + sits.getLand_use() + " acres=" +
						StringUtil.formatString(sits.getAcres_total(),"%.3f") +
						" has already been processed once and is " +
						"not being added again.";
					Message.printWarning ( warningLevel, 
				        MessageUtil.formatMessageTag(command_tag, ++warning_count), routine, message );
			        status.addToLog ( CommandPhaseType.RUN,
			            new CommandLogRecord(CommandStatusType.FAILURE,
			                message, "Verify that set commands only specify the data once." ) );
				}
				else {
					// Has not been previously processed so add the data...
					Message.printStatus ( 2, routine, "Location " + sits.getLocationID() +
						" supplemental acreage data from SetCropPatternTS(): year=" +
						sits.getCal_year() + " crop=" + sits.getLand_use() + " acres=" +
						StringUtil.formatString(sits.getAcres_total(),"%.3f") );
					//boolean todo = true;
					//if ( todo ) {
					//	throw new RuntimeException ("Need to fix.");
					cropPatterns.add ( sits );
					//}
				}
			}
		}
	}
	return cropPatterns;
}

/**
THIS IS THE OLD VERSION THAT WAS NOT CLEARLY DEALING WITH GENERICS.
CASTS WERE USED TO CONVERT THE OBJECTS TO PROPER DATA CLASSES.
Read supplemental HydroBase_StructureIrrigSummaryTS (new is
HydroBase_StructureView) records.  This does not
actually read the records but retrieves them from memory in
StateDMI_HydroBase_ParcelUseTS objects - the records are
defined in the setCropPatternTS() and setCropPatternTSFromList() commands.
If a supplemental record is available that conflicts with existing data,
the supplemental data will be used and a warning is printed.
@param cropPatterns list of HydroBase_StructureIrrigSummaryTS (e.g., as read
from HydroBase) (new is HydroBase_StructureView).  This list will be added to and returned.
@param wdidList List of WDIDs to be checked.  Each string is parsed into WD
and ID parts.  It is assumed that only valid WDIDs are passed - any errors
parsing are ignored (should not happen).
@param InputStart_DateTime The starting date to process data.
@param InputEnd_DateTime The ending date to process data.
*/
protected List<StateDMI_HydroBase_StructureView> readSupplementalStructureIrrigSummaryTSListForWDIDListOLD (
	List<StateDMI_HydroBase_StructureView> cropPatterns, List<String> wdidList,
	DateTime InputStart_DateTime, DateTime InputEnd_DateTime,
	List<StateDMI_HydroBase_StructureView> HydroBase_Supplemental_StructureIrrigSummaryTSList,
	CommandStatus status, String command_tag, int warningLevel, int warning_count )
{	String routine = "StateDMI_Processor.readSupplementalStructureIrrigSummaryTSListForWDIDList";
	if ( cropPatterns == null ) {
		cropPatterns = new ArrayList<>();
	}
	int cpsize = cropPatterns.size();
	StateDMI_HydroBase_StructureView sits = null; // Supplemental
	HydroBase_StructureView sits2 = null; // From HydroBase
	// Get a list of integer WDIDs to process...
	Message.printStatus ( 2, routine, "Getting supplemental acreage data "+
		"from setCropPatternTS() commands for:  " + wdidList );
	int nwdid_list = 0;
	if ( wdidList != null ) {
		nwdid_list = wdidList.size();
	}
	int sits_wd, sits_id; // The WDID parts for the "sits" object
	int iwdid; // For looping through WDIDs.
	boolean found = false; // Used when searching for matching HydroBase and supplemental records.
	// Size of all supplemental data...
	int size=HydroBase_Supplemental_StructureIrrigSummaryTSList.size();
	for ( int i = 0; i < size; i++ ) {
		sits = HydroBase_Supplemental_StructureIrrigSummaryTSList.get(i);
		// Check to see if the record is in the desired year...
		if ( (InputStart_DateTime != null) && (InputEnd_DateTime != null)
			&& ((sits.getCal_year() < InputStart_DateTime.getYear()) ||
			((sits.getCal_year() > InputEnd_DateTime.getYear())) ) ){
			// The data record year is outside the requested year.
			continue;
		}
		// Figure out if the record matches a requested location identifier...
		sits_wd = sits.getWD();
		sits_id = sits.getID();
		for ( iwdid = 0; iwdid < nwdid_list; iwdid++ ) {
			// Now do the lookup on the more generic string ID...
			if ( !wdidList.get(iwdid).equalsIgnoreCase(sits.getLocationID())) {
				// Not a match...
				continue;
			}
			// If here, a match was found.  First see if there is
			// an existing matching record in the full data set.
			found = false;
			// TODO SAM 2004-05-18 - this is a major dog.  Need to rework the loops so that the large
			// vector is only traversed once.
			// FIXME SAM 2007-05-14 Need to decide with the State whether this should be flagged as an error.
			for ( int i2 = 0; i2 < cpsize; i2++ ) {
				sits2 = cropPatterns.get(i2);
				if ( (sits2.getWD() == sits_wd) && (sits2.getID() == sits_id) &&
					(sits2.getCal_year() ==	sits.getCal_year()) &&
					sits2.getLand_use().equalsIgnoreCase(sits.getLand_use()) ) {
					// Matching record, replace the old and print a warning...
					String message = "WD " + sits_wd + " ID " + sits_id +
					" supplemental data from SetCropPatternTS() matches raw (HydroBase) crop " +
					"pattern data for " + sits.getCal_year() + " " + sits.getLand_use();
					Message.printWarning ( warningLevel, 
				        MessageUtil.formatMessageTag(command_tag, ++warning_count), routine, message );
			        status.addToLog ( CommandPhaseType.RUN,
			            new CommandLogRecord(CommandStatusType.WARNING,
			                message, "Using data from set command and overriding HydroBase - " +
			                	"verify the set command." ) );
					found = true;
					// This is OK whether previously processed or not, since it is not additive.
					cropPatterns.set ( i2, sits );
				}
			}
			if ( !found ) {
				// No matching record was found so just add.  Only add if not previously processed.
				if ( sits.hasBeenProcessed() ) {
					// This is a warning that is handled internally but should
					// probably be handled by the modeler.
					String message = "Location " + sits.getLocationID() +
						" supplemental acreage data from SetCropPatternTS(): year=" +
						sits.getCal_year() + " crop=" + sits.getLand_use() + " acres=" +
						StringUtil.formatString(sits.getAcres_total(),"%.3f") +
						" has already been processed once and is " +
						"not being added again.";
					Message.printWarning ( warningLevel, 
				        MessageUtil.formatMessageTag(command_tag, ++warning_count), routine, message );
			        status.addToLog ( CommandPhaseType.RUN,
			            new CommandLogRecord(CommandStatusType.FAILURE,
			                message, "Verify that set commands only specify the data once." ) );
				}
				else {
					// Has not been previously processed so add the data...
					Message.printStatus ( 2, routine, "Location " + sits.getLocationID() +
						" supplemental acreage data from SetCropPatternTS(): year=" +
						sits.getCal_year() + " crop=" + sits.getLand_use() + " acres=" +
						StringUtil.formatString(sits.getAcres_total(),"%.3f") );
					cropPatterns.add ( sits );
				}
			}
		}
	}
	return cropPatterns;
}

/**
Method for TSSupplier interface.
Read a time series given a time series identifier string.  The string may be
a file name if the time series are stored in files, or may be a true identifier
string if the time series is stored in a database.  The specified period is
read.  The data are converted to the requested units.
@param tsident_string Time series identifier or file name to read.
@param req_date1 First date to query.  If specified as null the entire period will be read.
@param req_date2 Last date to query.  If specified as null the entire period will be read.
@param req_units Requested units to return data.  If specified as null or an
empty string the units will not be converted.
@param read_data if true, the data will be read.  If false, only the time series
header will be read.
@return Time series of appropriate type (e.g., MonthTS, HourTS).
@exception Exception if an error occurs during the read.
*/
public TS readTimeSeries (	String tsident_string,
	DateTime req_date1, DateTime req_date2, String req_units, boolean read_data )
throws Exception
{	Message.printStatus ( 1, "", "Reading \"" + tsident_string + "\"" );

	// For now just create a dummy time series...

	MonthTS ts = new MonthTS();
	DateTime date1 = DateTime.parse ( "1950-01" );
	DateTime date2 = DateTime.parse ( "2000-12" );
	ts.setDate1 ( date1 );
	ts.setDate1Original ( date1 );
	TSIdent id = new TSIdent ( "xxxx..Streamflow.1Day" );
	ts.setDataType ( "Streamflow" );
	ts.setDate2 ( date2 );
	ts.setDate2Original ( date2 );
	ts.allocateDataSpace ();
	ts.setIdentifier ( id );
	for (	DateTime date = new DateTime(date1);
		date.lessThanOrEqualTo(date2);
		date.addDay ( 1 ) ) {
		ts.setDataValue ( date, date.toDouble() );
	}
	Message.printStatus ( 1, "", "Returning default monthly time series" );
	ts.formatOutput( new PropList ("x") );
	return ts;
}

/**
Method for TSSupplier interface.
Read a time series given an existing time series and a file name.
The specified period is read.
The data are converted to the requested units.
@param req_ts Requested time series to fill.  If null, return a new time series.
If not null, all data are reset, except for the identifier, which is assumed
to have been set in the calling code.  This can be used to query a single
time series from a file that contains multiple time series.
@param fname File name to read.
@param date1 First date to query.  If specified as null the entire period will be read.
@param date2 Last date to query.  If specified as null the entire period will be read.
@param req_units Requested units to return data.  If specified as null or an
empty string the units will not be converted.
@param read_data if true, the data will be read.  If false, only the time series
header will be read.
@return Time series of appropriate type (e.g., MonthTS, HourTS).
@exception Exception if an error occurs during the read.
*/
public TS readTimeSeries (	TS req_ts, String fname,
	DateTime date1, DateTime date2, String req_units, boolean read_data )
throws Exception
{	return null;
}

/**
Method for TSSupplier interface.
Read a time series list from a file (this is typically used used where a time
series file can contain one or more time series).
The specified period is read.  The data are converted to the requested units.
@param fname File to read.
@param date1 First date to query.  If specified as null the entire period will be read.
@param date2 Last date to query.  If specified as null the entire period will be read.
@param req_units Requested units to return data.  If specified as null or an
empty string the units will not be converted.
@param read_data if true, the data will be read.  If false, only the time series
header will be read.
@return list of time series of appropriate type (e.g., MonthTS, HourTS).
@exception Exception if an error occurs during the read.
*/
public List<TS> readTimeSeriesList ( String fname,
	DateTime date1, DateTime date2, String req_units, boolean read_data )
throws Exception
{	return null;
}

/**
Method for TSSupplier interface.
Read a time series list from a file or database using the time series identifier
information as a query pattern.
The specified period is read.  The data are converted to the requested units.
@param tsident A TSIdent instance that indicates which time series to query.
If the identifier parts are empty, they will be ignored in the selection.  If
set to "*", then any time series identifier matching the field will be selected.
If set to a literal string, the identifier field must match exactly to be selected.
@param fname File to read.
@param date1 First date to query.  If specified as null the entire period will be read.
@param date2 Last date to query.  If specified as null the entire period will be read.
@param req_units Requested units to return data.  If specified as null or an
empty string the units will not be converted.
@param read_data if true, the data will be read.  If false, only the time series
header will be read.
@return list of time series of appropriate type (e.g., MonthTS, HourTS).
@exception Exception if an error occurs during the read.
*/
public List<TS> readTimeSeriesList ( TSIdent tsident, String fname,
	DateTime date1, DateTime date2, String req_units, boolean read_data )
throws Exception {
	return null;
}

/**
Remove all CommandProcessorEventListener.
*/
public void removeAllCommandProcessorEventListeners ( )
{   // Just reset the array to null
    __CommandProcessorEventListener_array = null;
}

/**
Remove all commands.
*/
public void removeAllCommands ()
{	List<Command> commandList = getCommands();
	int size = commandList.size();
	if ( size > 0 ) {
		commandList.clear ();
		notifyCommandListListenersOfRemove ( 0, size - 1 );
	}
}

/**
Remove a command at a position.
@param index Position (0+) at which to remove command.
*/
public void removeCommandAt ( int index )
{	String routine = "StateDMI_Processor.removeCommandAt";
	List<Command> commandList = getCommands();
	commandList.remove ( index );
	notifyCommandListListenersOfRemove ( index, index );
	Message.printStatus(2, routine, "Remove command object at [" + index + "]" );
}

/**
Remove a CommandListListener.
@param listener CommandListListener to remove.
*/
public void removeCommandListListener ( CommandListListener listener )
{	if ( listener == null ) {
		return;
	}
	if ( __CommandListListener_array != null ) {
		// Loop through and set to null any listeners that match the
		// requested listener...
		int size = __CommandListListener_array.length;
		int count = 0;
		for ( int i = 0; i < size; i++ ) {
			if (	(__CommandListListener_array[i] != null) &&
				(__CommandListListener_array[i] == listener) ) {
				__CommandListListener_array[i] = null;
			}
			else {	++count;
			}
		}
		// Now resize the listener array...
		CommandListListener [] newlisteners =
			new CommandListListener[count];
		count = 0;
		for ( int i = 0; i < size; i++ ) {
			if ( __CommandListListener_array[i] != null ) {
				newlisteners[count++] = __CommandListListener_array[i];
			}
		}
		__CommandListListener_array = newlisteners;
		newlisteners = null;
	}
}

// FIXME SAM 2007-10-18 Remove following code when transitioned to other listeners
/**
Remove a ProcessListener.  The matching object address is removed, even if
it was regestered multiple times.
@param listener ProcessListener to remove.
*/
public void removeProcessListener ( ProcessListener listener )
{	if ( listener == null ) {
		return;
	}
	if ( __listeners != null ) {
		// Loop through and set to null any listeners that match the
		// requested listener...
		int size = __listeners.length;
		int count = 0;
		for ( int i = 0; i < size; i++ ) {
			if (	(__listeners[i] != null) &&
				(__listeners[i] == listener) ) {
				__listeners[i] = null;
			}
			else {	++count;
			}
		}
		// Now resize the listener array...
		ProcessListener [] newlisteners = new ProcessListener[count];
		count = 0;
		for ( int i = 0; i < size; i++ ) {
			if ( __listeners[i] != null ) {
				newlisteners[count++] = __listeners[i];
			}
		}
		__listeners = newlisteners;
		newlisteners = null;
	}
}

/**
Reset a __CU*_match_List to empty.
@param matchList List of matching identifiers/names to reset to empty.
*/
protected void resetDataMatches ( List<String> matchList )
{	matchList.clear();
}

/**
Reset the workflow global properties to defaults, necessary when a command processor is rerun.
*/
private void resetWorkflowProperties ()
throws Exception
{   String routine = getClass().getName() + ".resetWorkflowProperties";
    Message.printStatus(2, routine, "Resetting workflow properties." );
    
    // First clear user-defined properties.
    __propertyHashmap.clear();
    // Define some standard properties
    __propertyHashmap.put ( "ComputerName", InetAddress.getLocalHost().getHostName() ); // Useful for messages
    // Use new time zone class.
    ZonedDateTime now = ZonedDateTime.now();
    __propertyHashmap.put ( "ComputerTimezone", now.getZone().getId() ); // America/Denver, etc.
    __propertyHashmap.put ( "InstallDir", IOUtil.getApplicationHomeDir() );
    __propertyHashmap.put ( "InstallDirURL", "file:///" + IOUtil.getApplicationHomeDir().replace("\\", "/") );
    // Temporary directory useful in some cases
    __propertyHashmap.put ( "TempDir", System.getProperty("java.io.tmpdir") );
    // FIXME SAM 2016-04-03 This is hard-coded for TSTool - need to make more generic to work outside of TSTool?
    String homeDir = System.getProperty("user.home") + File.separator + ".tstool";
    __propertyHashmap.put ( "UserHomeDir", homeDir );
    __propertyHashmap.put ( "UserHomeDirURL", "file:///" + homeDir.replace("\\", "/") );
    __propertyHashmap.put ( "UserName", System.getProperty("user.name") );
    // Set the program version as a property, useful for version-dependent command logic
    // Assume the version is xxx.xxx.xxx beta (date), with at least one period
    // Save the program version as a string
    String programVersion = IOUtil.getProgramVersion();
    int pos = programVersion.indexOf(" ");
    if ( pos > 0 ) {
    	programVersion = programVersion.substring(0,pos);
    }
    __propertyHashmap.put ( "ProgramVersionString", programVersion );
    // Also save the numerical version.
    double programVersionNumber = -1.0;
    pos = programVersion.indexOf(".");
    StringBuilder b = new StringBuilder();
    if ( pos < 0 ) {
    	// Just a number
    	b.append(programVersion);
    }
    else {
    	// Transfer the characters including the first period but no other periods
    	b.append(programVersion.substring(0,pos) + ".");
    	for ( int i = pos + 1; i < programVersion.length(); i++ ) {
    		if ( programVersion.charAt(i) == '.' ) {
    			continue;
    		}
    		else {
    			b.append ( programVersion.charAt(i) );
    		}
    	}
    }
    // Also remove any non-digits like would occur in "beta", etc.
    for ( int i = pos + 1; i < b.length(); i++ ) {
    	if ( !Character.isDigit(b.charAt(i)) ) {
    		b.deleteCharAt(i--);
    	}
    }
    try {
    	programVersionNumber = Double.parseDouble(b.toString());
    }
    catch ( NumberFormatException e ) {
    	programVersionNumber = -1.0;
    }
    __propertyHashmap.put ( "ProgramVersionNumber", new Double(programVersionNumber) );
    
    // First clear user-defined properties.
    // FIXME SAM 2008-10-14 Evaluate whether needed like TSTool
    //__property_Hashtable.clear();
    // Now make sure that specific controlling properties are cleared out.
    setPropContents("OutputEnd", null );
    setPropContents("OutputStart", null );
    setPropContents("OutputYearType", YearType.CALENDAR );
}

/**
Run the specified commands.  If no commands are specified, run all that are being managed.
@param commands list of Command to process.
@param props Properties to control run. This method only acts on the properties shown below.
<td><b>Property</b></td>    <td><b>Description</b></td>
</tr>

<tr>
<td><b>ResetWorkflowProperties</b></td>
<td>If set to true (default), indicates that global properties like output period should be
reset before running.
</td>
<td>False</td>
</tr>

</table>
*/
public void runCommands ( List<Command> commands, PropList props )
throws Exception
{
    // Reset the global workflow properties if requested
    String ResetWorkflowProperties = "True";   // default
    if ( props != null ) {
        String prop = props.getValue ( "ResetWorkflowProperties" );
        if ( (prop != null) && prop.equalsIgnoreCase("False") ) {
            ResetWorkflowProperties = "False";
        }
    }
    if ( ResetWorkflowProperties.equalsIgnoreCase("True")) {
        resetWorkflowProperties();
    }
    // Remove all registered CommandProcessorEventListener, so that listeners don't get added
    // more than once if the processor is rerun.  Currently this will require that an OpenCheckFile()
    // command is always run since it is the only thing that handles events at this time.
    removeAllCommandProcessorEventListeners();
    
    // Now call the method to do the processing.

	processCommands ( commands, props );
	
	// Now finalize the results by processing the check files, if any

	if ( __CommandProcessorEventListener_array != null ) {
    	for ( int i = 0; i < __CommandProcessorEventListener_array.length; i++ ) {
    	    CommandProcessorEventListener listener = __CommandProcessorEventListener_array[i];
    	    if ( listener instanceof CheckFileCommandProcessorEventListener ) {
    	        CheckFileCommandProcessorEventListener cflistener = (CheckFileCommandProcessorEventListener)listener;
    	        cflistener.finalizeOutput();
    	    }
    	}
	}
	
    // Remove all registered CommandProcessorEventListener again so that if by chance editing, etc. generates
	// events don't want to deal with...
    removeAllCommandProcessorEventListeners();
}

//FIXME SAM 2008-12-23 Make sure data checks are implemented using better design.
/**
Helper method to run data checks for StateCU for a given component type.
@param Type of StateMod component.
*/
/* TODO SAM 2009-04-27 Evaluate removing code if other check commands work
protected void runStateCUDataCheck( int type )
{
	String fname = getCommandFileName();
	// If there is no commands file then use the component and program name for the file name
	if ( fname == null || fname.length() == 0 ) {
		DataSetComponent comp = __StateCU_DataSet.getComponentForComponentType( type );
		String name = comp.getComponentName();
		if ( name == null ){
			name = "CheckFile";
		}
		fname = name + ".StateDMI";
	}
	//addToResultsFileList( __StateCU_DataSet.runComponentChecks(
	//	type, fname, getCommandsAsString(), getFullProgramHeader() ) );
	__data_check_count++;
}
*/

// FIXME SAM 2008-12-23 Make sure data checks are implemented using better design.
/**
Helper method to run data checks for StateMod for a given component type.
@param Type of StateMod component.
*/
/*
protected void runStateModDataCheck( int type )
{
	String fname = getCommandFileName();
	// If type is RiverNetwork then add the data.
	// For some reason the data wasn't being added correctly like other
	// products so override and add the data here
	if ( type == StateMod_DataSet.COMP_RIVER_NETWORK ) {
		DataSetComponent comp = __StateMod_DataSet.getComponentForComponentType( type );
		comp.setData( __SMRiverNetworkNode_List );
	}
	// If there is no commands file then use the component and program name for the file name
	if ( fname == null || fname.length() == 0 ) {
		DataSetComponent comp = __StateMod_DataSet.getComponentForComponentType( type );
		String name = comp.getComponentName();
		if ( name == null ){
			name = "CheckFile";
		}
		fname = name + ".StateDMI";
	}
	// FIXME SAM 2008-12-23 Need to fix data check file.
	//addToResultsFileList( new File(__StateMod_DataSet.runComponentChecks(
	//	type, fname, getCommandsAsString(), getFullProgramHeader() )) );
	__data_check_count++;
}
*/

/**
Request that processing be cancelled.  This sets a flag that is detected in the
processCommands() method.  Processing will be cancelled as soon as the current command
completes its processing.
@param cancel_processing_requested Set to true to cancel processing.
*/
public void setCancelProcessingRequested ( boolean cancel_processing_requested )
{	__cancel_processing_requested = cancel_processing_requested;
}

/**
Set the command list, typically only called from constructor.
@param commandList list of commands for processor.
*/
public void setCommands ( List<Command> commandList )
{
	__commandList = commandList;
}

/**
Set the name of the commands file where the commands are saved.
@param filename Name of commands file (should be absolute since
it will be used in output headers).
*/
public void setCommandFileName ( String filename )
{
	__commandFilename = filename;
}

/**
Set whether the processor should create output
@param create_output If true, processing commands will execute commands that
create output (e.g., write*() commands).  If false, these commands will not
be executed, increasing execution speed and keeping results in memory only.
*/
public void setCreateOutput ( boolean create_output )
{	__create_output = create_output;
}

/**
Set a DataStore instance in the list that is being maintained for use.
The DataStore identifier is used to lookup the instance.  If a match is found,
the old instance is optionally closed and discarded before adding the new instance.
The new instance is added at the end.
@param dataStore DataStore to add to the list.  Null will be ignored.
@param closeOld If an old data store is matched and true, close the datastore database connection.
The main issue is that if something else is using a DMI instance (e.g.,
the StateDMI UI) it may be necessary to leave the old connection instance open.
*/
protected void setDataStore ( DataStore dataStore, boolean closeOld )
{   String routine = getClass().getSimpleName() + ".setDataStore";
    if ( dataStore == null ) {
        return;
    }
    //if ( Message.isDebugOn ) {
    	//Message.printDebug(1, routine, "Setting datastore \"" + dataStore.getName() + "\"" );
    	Message.printStatus(2, routine, "Setting datastore \"" + dataStore.getName() + "\"" );
    //}
    DataStore matchedDataStore = null;
    for ( DataStore ds : __dataStoreList ) {
        if ( ds.getName().equalsIgnoreCase(dataStore.getName())) {
            // The input name of the current instance matches that of the instance in the list.
            // Replace the instance in the list by the new instance...
        	matchedDataStore = ds;
            if ( closeOld ) {
                try {
                    if ( ds instanceof DatabaseDataStore ) {
                        DMI dmi = ((DatabaseDataStore)ds).getDMI();
                        dmi.close();
                    }
                }
                catch ( Exception e ) {
                    // Probably can ignore.
                    Message.printWarning (3,routine,"Error closing data store \"" + dataStore.getName() +
                        "\" before reopening:");
                    Message.printWarning (3,routine, e);
                }
            }
        }
    }
    if ( matchedDataStore != null ) {
    	// Remove from the list.
    	__dataStoreList.remove(matchedDataStore);
    }

    // Add a new instance to the list, alphabetized (ignore case)...
    if ( __dataStoreList.size() == 0 ) {
    	__dataStoreList.add ( dataStore );
    }
    else {
        int insertPos = -1;
        boolean added = false;
	    for ( DataStore ds : __dataStoreList ) {
	    	++insertPos;
	    	if ( dataStore.getName().toUpperCase().compareTo(ds.getName().toUpperCase()) < 0 ) {
	    		__dataStoreList.add(insertPos,dataStore);
	    		added = true;
	    		break;
	    	}
	    }
	    if ( !added ) {
	    	// Add at the end
	    	__dataStoreList.add ( dataStore );
	    }
	}
}

/**
Set the list of all DataStore instances known to the processor.  These are named database
connections that correspond to input type/name for time series.
This method is normally only called in special cases.  For example, the RunCommands() command
sets the data stores from the main processor into the called commands.
Note that each data store in the list is set using setDataStore() - the instance of the list that
manages the data stores is not reset.
@param dataStoreList list of DataStore to use in the processor
@param closeOld if true, then any matching data stores are first closed before being set to the
new value (normally this should be false if, for example, a list of data stores from one processor
is passed to another)
*/
public void setDataStores ( List<DataStore> dataStoreList, boolean closeOld )
{
    for ( DataStore dataStore : dataStoreList ) {
        setDataStore(dataStore, closeOld );
    }
}

/**
Set the initial working directory for the processor.  This is typically the location
of the commands file, or a temporary directory if the commands have not been saved.
Also set the current working directory by calling setWorkingDir() with the same information.
@param InitialWorkingDir The current working directory.
*/
protected void setInitialWorkingDir ( String InitialWorkingDir )
{	String routine = getClass().getSimpleName() + ".setInitialWorkingDir";
	Message.printStatus(2, routine, "Setting the initial working directory to \"" + InitialWorkingDir + "\"" );
	__InitialWorkingDir_String = InitialWorkingDir;
	// Also set the working directory...
	setWorkingDir ( __InitialWorkingDir_String );
}

/**
Indicate whether the processor is running.  This should be set in processCommands()
and can be monitored by code (e.g., GUI) that has behavior that depends on whether
the processor is running.
@param is_running indicates whether the processor is running (processing commands).
*/
private void setIsRunning ( boolean is_running )
{
	__is_running = is_running;
}

/**
Set the data for a named property, required by the CommandProcessor
interface.  See the getPropContents method for a list of properties that are handled.
@param prop Property to set.
@return the named property, or null if a value is not found.
*/
public void setProp ( Prop prop ) throws Exception
{	//String key = prop.getKey();
	/* TODO SAM 2005-05-20 Need to start enabling..
	if ( key.equalsIgnoreCase("TSResultsList") ) {
		__tslist = (Vector)prop.getContents();
		// TODO SAM 2005-05-05 Does anything need to be revisited?
	}
	*/
}

/**
Set the contents for a named property, required by the CommandProcessor
interface.  See the getPropContents method for a list of properties that are handled.
<table width=100% cellpadding=10 cellspacing=0 border=2>
<tr>
<td><b>Property</b></td>	<td><b>Description</b></td>
</tr>

<tr>
<td><b>InitialWorkingDir</b></td>
<td>A String containing the path to the initial working directory, from which all
paths are determined.  This is usually the directory to the commands file, or the
startup directory.
</td>
</tr>

<tr>
<td><b>OutputEnd</b></td>
<td>A DateTime containing the end of the processing period.
</td>
</tr>

<tr>
<td><b>OutputStart</b></td>
<td>A DateTime containing the start of the processing period.
</td>
</tr>

<tr>
<td><b>WDIDLength</b></td>
<td>An Integer containing the WDID length to be used as a default when formatting new identifiers.
</td>
</tr>

</table>
*/
public void setPropContents ( String prop, Object contents ) throws Exception
{	if ( prop.equalsIgnoreCase("HydroBaseDMIList") ) {
		// TODO SAM 2005-06-08 Currently only allow one connection...
		@SuppressWarnings("unchecked")
		List<HydroBaseDMI> objectList = (List<HydroBaseDMI>)contents;
		List<HydroBaseDMI> v = objectList;
		__hdmi = v.get(0);
	}
	else if ( prop.equalsIgnoreCase("DataStore" ) ) {
		setDataStore ( (DataStore)contents, true );
	}
	else if ( prop.equalsIgnoreCase("InitialWorkingDir" ) ) {
		setInitialWorkingDir ( (String)contents );
	}
	else if ( prop.equalsIgnoreCase("OutputEnd" ) ) {
		__OutputEnd_DateTime = (DateTime)contents;
	}
	else if ( prop.equalsIgnoreCase("OutputStart" ) ) {
		__OutputStart_DateTime = (DateTime)contents;
	}
	else if ( prop.equalsIgnoreCase("OutputYearType" ) ) {
		__OutputYearType = (YearType)contents;
	}
	else if ( prop.equalsIgnoreCase("StateCU_IrrigationPracticeTS_List") ) {
		@SuppressWarnings("unchecked")
		List<StateCU_IrrigationPracticeTS> objectList = (List<StateCU_IrrigationPracticeTS>)contents;
		__CUIrrigationPracticeTS_List = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateCU_Location_List") ) {
		@SuppressWarnings("unchecked")
		List<StateCU_Location> objectList = (List<StateCU_Location>)contents;
		__CULocation_List = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateCU_Parcel_List") || prop.equalsIgnoreCase("StateCU_Parcel_Map") ) {
		// Handle treating as a list or a map
		@SuppressWarnings("unchecked")
		HashMap<String,StateCU_Parcel> objectList = (HashMap<String,StateCU_Parcel>)contents;
		__CUParcel_Map = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionDemandTSMonthly_List") ) {
		@SuppressWarnings("unchecked")
		List<MonthTS> objectList = (List<MonthTS>)contents;
		__SMDemandTSMonthlyList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_DiversionHistoricalTSMonthly_List") ) {
		@SuppressWarnings("unchecked")
		List<MonthTS> objectList = (List<MonthTS>)contents;
		__SMDiversionTSMonthlyList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_Network") ) {
		__SM_network = (StateMod_NodeNetwork)contents;
	}
	else if ( prop.equalsIgnoreCase("StateMod_PlanReturn_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_ReturnFlow> objectList = (List<StateMod_ReturnFlow>)contents;
		__SMPlanReturnList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_PlanStation_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_Plan> objectList = (List<StateMod_Plan>)contents;
		__SMPlanList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_PlanWellAugmentation_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_Plan_WellAugmentation> objectList = (List<StateMod_Plan_WellAugmentation>)contents;
		__SMPlanWellAugmentationList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_RiverNetworkNode_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_RiverNetworkNode> objectList = (List<StateMod_RiverNetworkNode>)contents;
		__SMRiverNetworkNode_List = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_WellDemandTSMonthly_List") ) {
		@SuppressWarnings("unchecked")
		List<MonthTS> objectList = (List<MonthTS>)contents;
		__SMWellDemandTSMonthlyList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_WellHistoricalPumpingTSMonthly_List") ) {
		@SuppressWarnings("unchecked")
		List<MonthTS> objectList = (List<MonthTS>)contents;
		__SMWellHistoricalPumpingTSMonthlyList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateModWellRightList") || prop.equalsIgnoreCase("StateMod_WellRight_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_WellRight> objectList = (List<StateMod_WellRight>)contents;
		__SMWellRightList = objectList;
	}
	else if ( prop.equalsIgnoreCase("StateMod_WellStation_List") ) {
		@SuppressWarnings("unchecked")
		List<StateMod_Well> objectList = (List<StateMod_Well>)contents;
		__SMWellList = objectList;
	}
	else if ( prop.equalsIgnoreCase("DefaultWDIDLength") || // Newer
		prop.equalsIgnoreCase("WDIDLength" ) ) { // Older
		__defaultWdidLength = ((Integer)contents).intValue();
	}
    else if ( prop.equalsIgnoreCase("WorkingDir") ) {
        setWorkingDir ( (String)contents );
    }
	else {
		String routine = getClass().getName() + ".setPropContents";
		Message.printWarning ( 3, routine, "Unrecognized property \"" + prop + "\" - not setting.");
		// TODO SAM 2008-12-08 Evaluate use
		// Seems to hang the app, perhaps due to threading?  Also, User can set any property with SetProperty
		//throw new RuntimeException ( "Attempting to set unrecognized property \"" + prop + "\"" );
	}
}

/**
Set the working directory for the processor.  This is typically set by
SetInitialWorkingDir() method when initializing the processor and SetWorkingDir() commands.
@param WorkingDir The current working directory.
*/
public void setWorkingDir ( String WorkingDir )
{
	__WorkingDir_String = WorkingDir;
}

/**
Return the number of commands being managed by this processor.  This
matches the Collection interface, although that is not yet fully implemented.
@return The number of commands being managed by the processor
*/
public int size()
{
	return getCommands().size();
}

/**
Print a warning about key identifier/name matches that have occurred when adding CU locations.
@param command Command that was adding the StateCU_Location (String or Command class).
@param replace If true, an existing instance is replaced if found.  If false,
the original instance is used.  This flag should be consistent with how the StateCU_Location were processed.
@param matchList List of strings containing the key id/name values that have matches.
@param data_type String to use in messages to identify the data object type (e.g., "CU Locations").
*/
protected void warnAboutDataMatches ( Object command, boolean replace, List<String> matchList, String data_type )
{	int size = matchList.size();

	if (size == 0) {
		return;
	}

	StringBuffer matches = new StringBuffer ( matchList.get(0) );
	String id;
	int maxwidth = 100;
	String nl = System.getProperty ( "line.separator" );
	for (int i = 1; i < size; i++) {
		matches.append ( ", " );
		// Limit to "maxwidth" characters per line...
		id = matchList.get(i);
		// 2 is for the ", "
		if ( (matches.length()%maxwidth + (id.length() + 2)) >= maxwidth) {
			matches.append ( nl );
		}
		matches.append ( id );
	}

	// Warn at level 2 since this is a non-fatal error.  Later may add an
	// option to the read methods to give the choice of some behavior when matches are found...

	if ( replace ) {
		Message.printWarning ( __FYI_warning_level,	"StateDMI_Processor.warnAboutDataMatches",
		"The following " + data_type + " were already in memory and were " +
		"overwritten\nwith new data from the \"" + command + "\" " + "command :\n" + matches.toString() );
	}
	else {
		Message.printWarning ( __FYI_warning_level, "StateDMI_Processor.warnAboutDataMatches",
		"The following " + data_type + " were already in memory and were " +
		"retained\ndespite new data from the \"" + command + "\" " + "command :\n" + matches.toString() );
	}
}

}