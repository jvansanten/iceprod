Search.setIndex({envversion:49,filenames:["core/dataclasses","core/exe","core/exe_helper","core/exe_json","core/functions","core/gridftp","core/i3exec","core/index","core/init","core/jsonRPCclient","core/jsonUtil","core/parser","core/serialization","core/util","dev_notes","extra_details","guide/datasets","guide/index","guide/jsonrpc","guide/login","guide/submission","guide/tasks","index","modules/index","overview","server/config","server/dbmethods","server/details/async","server/details/dbtables","server/details/global_queueing","server/details/index","server/details/lifecycles","server/details/submit_to_queue","server/details/task_relationships","server/details/website","server/file_io","server/globus","server/grid","server/index","server/init","server/module","server/modules/db","server/modules/master_updater","server/modules/proxy","server/modules/queue","server/modules/schedule","server/modules/website","server/nginx","server/plugins/condor","server/pool","server/schedule","server/server","server/squid","server/ssl_cert"],objects:{"iceprod.core":{dataclasses:[0,0,0,"-"],exe_helper:[2,0,0,"-"],jsonRPCclient:[9,0,0,"-"],jsonUtil:[10,0,0,"-"],parser:[11,0,0,"-"],serialization:[12,0,0,"-"],to_file:[8,4,1,""],to_log:[8,4,1,""],util:[13,0,0,"-"]},"iceprod.core.dataclasses":{Class:[0,1,1,""],Data:[0,1,1,""],DataCenter:[0,1,1,""],Dif:[0,1,1,""],DifPlus:[0,1,1,""],Job:[0,1,1,""],Module:[0,1,1,""],Personnel:[0,1,1,""],Plus:[0,1,1,""],Resource:[0,1,1,""],Steering:[0,1,1,""],Task:[0,1,1,""],Tray:[0,1,1,""],_ResourceCommon:[0,1,1,""],_TaskCommon:[0,1,1,""]},"iceprod.core.dataclasses.Class":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Data":{convert:[0,2,1,""],movement_options:[0,3,1,""],output:[0,2,1,""],plural:[0,3,1,""],storage_location:[0,2,1,""],type_options:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.DataCenter":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""],valid_names:[0,3,1,""]},"iceprod.core.dataclasses.Dif":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""],valid_parameters:[0,3,1,""],valid_sensor_name:[0,3,1,""],valid_source_name:[0,3,1,""]},"iceprod.core.dataclasses.DifPlus":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Job":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Module":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Personnel":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Plus":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""],valid_category:[0,3,1,""]},"iceprod.core.dataclasses.Resource":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Steering":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Task":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses.Tray":{convert:[0,2,1,""],output:[0,2,1,""],plural:[0,3,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses._ResourceCommon":{compression_options:[0,3,1,""],convert:[0,2,1,""],valid:[0,2,1,""]},"iceprod.core.dataclasses._TaskCommon":{convert:[0,2,1,""],valid:[0,2,1,""]},"iceprod.core.exe_helper":{get_args:[2,4,1,""],main:[2,4,1,""],run:[2,4,1,""],unicode_to_ascii:[2,4,1,""]},"iceprod.core.jsonRPCclient":{Client:[9,1,1,""],JSONRPC:[9,1,1,""]},"iceprod.core.jsonRPCclient.Client":{close:[9,2,1,""],open:[9,2,1,""],request:[9,2,1,""]},"iceprod.core.jsonRPCclient.JSONRPC.MetaJSONRPC":{restart:[9,5,1,""],start:[9,5,1,""],stop:[9,5,1,""]},"iceprod.core.jsonUtil":{JSONToObj:[10,4,1,""],binary_converter:[10,1,1,""],bytearray_converter:[10,1,1,""],date_converter:[10,1,1,""],datetime_converter:[10,1,1,""],iface_converter:[10,1,1,""],json_compressor:[10,1,1,""],json_decode:[10,4,1,""],json_encode:[10,4,1,""],objToJSON:[10,4,1,""],recursive_unicode:[10,4,1,""],repr_converter:[10,1,1,""],set_converter:[10,1,1,""],time_converter:[10,1,1,""],var_converter:[10,1,1,""]},"iceprod.core.jsonUtil.binary_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.bytearray_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.date_converter":{loads:[10,6,1,""]},"iceprod.core.jsonUtil.datetime_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.iface_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.json_compressor":{compress:[10,6,1,""],uncompress:[10,6,1,""]},"iceprod.core.jsonUtil.repr_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.set_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.jsonUtil.time_converter":{loads:[10,6,1,""]},"iceprod.core.jsonUtil.var_converter":{dumps:[10,6,1,""],loads:[10,6,1,""]},"iceprod.core.parser":{ExpParser:[11,1,1,""]},"iceprod.core.parser.ExpParser":{parse:[11,2,1,""]},"iceprod.core.parser.safe_eval":{eval:[11,5,1,""]},"iceprod.core.serialization":{SerializationError:[12,7,1,""],dict_to_dataclasses:[12,4,1,""],serialize_json:[12,1,1,""]},"iceprod.core.serialization.serialize_json":{dump:[12,6,1,""],dumps:[12,6,1,""],load:[12,6,1,""],loads:[12,6,1,""]},"iceprod.core.util":{Node_Resources:[13,8,1,""],NoncriticalError:[13,7,1,""],Task_Resource_Overusage:[13,8,1,""],Task_Resources:[13,8,1,""],get_cpus:[13,4,1,""],get_disk:[13,4,1,""],get_gpus:[13,4,1,""],get_memory:[13,4,1,""],get_node_resources:[13,4,1,""],get_task_resources:[13,4,1,""],get_time:[13,4,1,""]},"iceprod.server":{GlobalID:[39,1,1,""],KwargConfig:[39,1,1,""],config:[25,0,0,"-"],dbmethods:[26,0,0,"-"],file_io:[35,0,0,"-"],find_module_recursive:[39,4,1,""],get_pkg_binary:[39,4,1,""],get_pkgdata_filename:[39,4,1,""],globus:[36,0,0,"-"],listmodules:[39,4,1,""],nginx:[47,0,0,"-"],pool:[49,0,0,"-"],run_module:[39,4,1,""],salt:[39,4,1,""],server:[51,0,0,"-"],squid:[52,0,0,"-"]},"iceprod.server.GlobalID":{CHARS:[39,3,1,""],CHARS_LEN:[39,3,1,""],IDLEN:[39,3,1,""],INTS_DICT:[39,3,1,""],MAXLOCALID:[39,3,1,""],MAXSITEID:[39,3,1,""],char2int:[39,5,1,""],globalID_gen:[39,5,1,""],int2char:[39,5,1,""],localID_ret:[39,5,1,""],siteID_gen:[39,5,1,""],siteID_ret:[39,5,1,""],string:[39,3,1,""]},"iceprod.server.KwargConfig":{validate:[39,2,1,""]},"iceprod.server.config":{IceProdConfig:[25,1,1,""],locateconfig:[25,4,1,""]},"iceprod.server.config.IceProdConfig":{defaults:[25,2,1,""],do_validate:[25,2,1,""],load:[25,2,1,""],load_string:[25,2,1,""],save:[25,2,1,""],save_to_string:[25,2,1,""]},"iceprod.server.dbmethods":{auth:[26,0,0,"-"],authorization:[26,4,1,""],datetime2str:[26,4,1,""],dbmethod:[26,4,1,""],filtered_input:[26,4,1,""],nowstr:[26,4,1,""],queue:[26,0,0,"-"],str2datetime:[26,4,1,""]},"iceprod.server.dbmethods.auth":{auth:[26,1,1,""]},"iceprod.server.dbmethods.auth.auth":{add_site_to_master:[26,2,1,""],auth_authorize_site:[26,2,1,""],auth_authorize_task:[26,2,1,""],auth_get_passkey:[26,2,1,""],auth_get_site_auth:[26,2,1,""],auth_new_passkey:[26,2,1,""],auth_user:[26,2,1,""],auth_user_create:[26,2,1,""]},"iceprod.server.dbmethods.queue":{queue:[26,1,1,""]},"iceprod.server.dbmethods.queue.queue":{queue_add_pilot:[26,2,1,""],queue_add_task_lookup:[26,2,1,""],queue_buffer_jobs_tasks:[26,2,1,""],queue_del_pilots:[26,2,1,""],queue_get_active_tasks:[26,2,1,""],queue_get_cfg_for_dataset:[26,2,1,""],queue_get_cfg_for_task:[26,2,1,""],queue_get_grid_tasks:[26,2,1,""],queue_get_pilots:[26,2,1,""],queue_get_queueing_datasets:[26,2,1,""],queue_get_queueing_tasks:[26,2,1,""],queue_get_task:[26,2,1,""],queue_get_task_by_grid_queue_id:[26,2,1,""],queue_get_task_lookup:[26,2,1,""],queue_new_pilot_ids:[26,2,1,""],queue_reset_tasks:[26,2,1,""],queue_set_site_queues:[26,2,1,""],queue_set_submit_dir:[26,2,1,""],queue_set_task_status:[26,2,1,""]},"iceprod.server.file_io":{AsyncFileIO:[35,1,1,""]},"iceprod.server.file_io.AsyncFileIO":{close:[35,2,1,""],open:[35,2,1,""],read:[35,2,1,""],readline:[35,2,1,""],write:[35,2,1,""]},"iceprod.server.globus":{SiteGlobusProxy:[36,1,1,""]},"iceprod.server.globus.SiteGlobusProxy":{get_proxy:[36,2,1,""],set_duration:[36,2,1,""],set_passphrase:[36,2,1,""],update_proxy:[36,2,1,""]},"iceprod.server.nginx":{Nginx:[47,1,1,""],deleteoldlogs:[47,4,1,""],find_mime:[47,4,1,""],find_nginx:[47,4,1,""],rotate:[47,4,1,""]},"iceprod.server.nginx.Nginx":{kill:[47,2,1,""],logrotate:[47,2,1,""],start:[47,2,1,""],stop:[47,2,1,""]},"iceprod.server.pool":{GroupingThreadPool:[49,1,1,""],NamedThreadPool:[49,1,1,""],PriorityThreadPool:[49,1,1,""],SingleGrouping:[49,1,1,""],ThreadPool:[49,1,1,""],ThreadPoolDeque:[49,1,1,""],deque2:[49,1,1,""]},"iceprod.server.pool.NamedThreadPool":{add_task:[49,2,1,""],disable_output_queue:[49,2,1,""],enable_output_queue:[49,2,1,""],finish:[49,2,1,""],pause:[49,2,1,""],start:[49,2,1,""]},"iceprod.server.pool.PriorityThreadPool":{maxint:[49,3,1,""],time:[49,2,1,""]},"iceprod.server.pool.ThreadPool":{add_task:[49,2,1,""],disable_output_queue:[49,2,1,""],enable_output_queue:[49,2,1,""],finish:[49,2,1,""],map:[49,2,1,""],pause:[49,2,1,""],start:[49,2,1,""]},"iceprod.server.pool.deque2":{empty:[49,2,1,""],full:[49,2,1,""],get:[49,2,1,""],get_nowait:[49,2,1,""],join:[49,2,1,""],mutex:[49,3,1,""],put:[49,2,1,""],put_nowait:[49,2,1,""],qsize:[49,3,1,""],task_done:[49,2,1,""],unfinished_tasks:[49,3,1,""]},"iceprod.server.schedule":{Scheduler:[50,1,1,""]},"iceprod.server.schedule.Scheduler":{MAXWAIT:[50,3,1,""],parsecron:[50,6,1,""],run:[50,2,1,""],schedule:[50,2,1,""],start:[50,2,1,""]},"iceprod.server.server":{Server:[51,1,1,""]},"iceprod.server.server.Server":{kill:[51,2,1,""],reload:[51,2,1,""],restart:[51,2,1,""],run:[51,2,1,""],stop:[51,2,1,""]},"iceprod.server.squid":{Squid:[52,1,1,""]},"iceprod.server.squid.Squid":{kill:[52,2,1,""],logrotate:[52,2,1,""],restart:[52,2,1,""],start:[52,2,1,""],stop:[52,2,1,""],update:[52,2,1,""]},iceprod:{core:[8,0,0,"-"],server:[39,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"],"5":["py","classmethod","Python class method"],"6":["py","staticmethod","Python static method"],"7":["py","exception","Python exception"],"8":["py","data","Python data"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:function","5":"py:classmethod","6":"py:staticmethod","7":"py:exception","8":"py:data"},terms:{"0123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz":11,"04d":11,"0x10":15,"1x10":15,"64k":35,"abstract":11,"boolean":28,"byte":[10,35],"case":[15,20,26,32],"char":[11,15],"class":[0,1,2,5,9,10,11,12,25,26,27,35,36],"default":[0,13,15,25,26,30,31,33,34,35,36],"else":32,"final":16,"float":[28,49],"function":0,"import":[27,35,39],"int":[26,28],"long":27,"new":[0,8,15,17,18,19,26,27,34,39,50],"public":18,"return":[0,5,9,10,11,12,26,27,34,35,39,49],"short":[19,28],"static":[10,12,34,47,50],"super":0,"true":[0,5,25,27,28,31,49,50],"try":[27,32,34,39],"while":[15,21,27,30,34],__init__:27,__len__:49,_resourcecommon:0,_taskcommon:0,a3ri:0,abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789:39,abil:34,abl:[15,35],about:[0,25,27,32,38],accept:27,access:[22,27,34],account:[18,19,30],across:15,action:[15,18,19,27,34],activ:[26,30],actual:[0,20,21,24,30,32,51],add:[26,49,50],add_callback:27,add_site_to_mast:26,add_task:49,addit:[15,19,27,28],address:[5,9],admin:14,admin_email:28,admin_nam:28,administ:22,administr:22,advanc:18,affect:30,after:[0,1],again:15,against:[26,34],ahead:26,air:0,ajax:34,algorithm:30,all:[0,15,16,17,20,24,26,33,34,47,49],alloc:[13,32],allow:[13,15,27],along:16,alreadi:[15,22,27,32,33],also:[15,24,27,30,34,47],altere:15,amanda:0,among:15,amount:13,ani:[0,2,15,18,19,21,27,34,49],anoth:[15,24],another:16,antarctic:0,anyon:[18,34],apach:34,api:[18,27,34],app:[19,27],applic:[19,27,35],applicat:27,approach:27,appropri:29,arch:[0,28],architectur:[30,38],archiv:22,area:34,arg1:27,arg2:27,arg:[0,2,5,8,11,26,27,39,47,49,50,52],argument:[5,9,12,26,27,49],arithmat:11,around:[47,52],arrai:0,ascii:18,ask:15,assign:[15,26,28,30],associ:32,assum:[27,34],astronomi:0,astrophys:0,async:35,asyncfileio:35,asyncron:5,atmospher:0,attack:[34,47],attribut:[0,21,27],auth:26,auth_authorize_sit:26,auth_authorize_task:26,auth_get_passkei:26,auth_get_site_auth:26,auth_kei:[26,28],auth_new_passkei:26,auth_rol:26,auth_us:26,auth_user_cr:26,authent:17,author:26,auto:52,autoincr:15,autom:18,automat:25,avail:[13,18,24,25,26,27,29,34,38],averag:16,avoid:30,back:[15,24,25,31,49],backport:27,bad:28,barcod:19,base:[0,2,19,26,35,39,49,50],basic:[8,16,18],batch:[22,31],batchsi:0,becaus:[15,21,27,34],becom:15,been:[15,27,33],befor:[0,15,27,34],behind:35,benefit:27,best:15,between:[27,28,34],bin:14,binari:[27,39],binary_convert:10,bind:[26,27],bit:38,blob:26,block:[0,5,27,30,34,49],blue:31,bodi:9,bool:[26,28],both:[0,27,30],bottleneck:47,bottom:21,bound:27,box:20,broken:[16,24],buffer:[15,16,26,30],build:0,built:[9,20,27,34],bulk:15,bundl:[15,39],burst:0,bytearray_convert:10,bytestr:5,bz2:0,bzip:0,c10k:27,cach:[30,52],calibr:0,call:0,call_soon:27,callback:5,callback_arg:27,can:[0,12,13,15,18,19,22,24,26,27,30,31,32,33,34,49],cannnot:34,cannot:35,capabl:[15,24,27,47],care:[18,20,30],carefulli:0,cascad:0,categori:0,categorydef:28,categorydef_id:28,categorydef_offset:28,categoryvalu:28,categoryvalue_id:28,categoryvalue_offset:28,caus:15,center:0,central:15,ceos:0,certain:19,certif:[15,22,30,34,38],cfgfile:36,challeng:15,chang:[15,27,34],char2int:39,charact:[15,26,28],characterist:0,chars:39,chars_len:39,check:[5,27,34],cherenkov:0,chmod:5,choic:11,classmethod:[5,9,11,39],classnam:2,clean:1,clear:0,click:21,client:[5,7],clock:[27,49],close:[9,15,27,35],cmd:[5,28],code:[15,19,27,38],coghlan:27,collabor:49,collis:15,color:31,com:22,combin:49,come:[15,27,33],comma:33,command:[5,15],command_lin:0,comment:[20,28],common:0,commonli:11,compil:27,complet:[15,16,27,28,33,49],complex:[5,20,27],compon:0,composit:0,compress:[0,10,28],compression_opt:0,comput:[24,27,34],concept:27,concurr:[27,35],condor:[22,38],config:[0,12,20,24,25,26],config_data:28,connect:[9,15,27,47],constant:8,consum:49,contain:[0,2,9,15,49],content:[25,47],continu:[15,27,30],contrast:27,control:[15,27,52],convert:[0,10,12,26],cooki:34,cooper:27,coordin:22,copi:[15,20],copyright:49,core:[0,2,5],coroutin:[27,35],corpor:0,cosmic:0,could:34,cpu:[13,47],crash:2,cream:30,creat:[0,15,26,30,32,34],creation:15,cron:[30,50],cross:34,cryospher:0,csrf:30,csv:28,curl:[18,27],current:[20,25,26,27,32,33,35,49],cursor:26,cvmf:22,cvmfs:22,cyan:31,cycl:27,daemon:30,dai:[34,47,50],data:[0,1,5,10,15,18,27,28,35],data_cet:0,data_id:28,data_offset:28,databas:[16,22,26,27],datacent:0,dataset:[0,11,12,15],dataset_id:[20,26,28,33],dataset_nodes_id:28,dataset_not:28,dataset_notes_offset:28,dataset_offset:28,dataset_prio:26,dataset_stat:28,dataset_stat_id:28,dataset_stat_offset:28,dataset_temp:0,date:28,date_convert:10,datetim:[26,28],datetime2str:26,datetime_convert:10,dbapi:26,dbmethod:[18,26],debug:[2,28,31],decent:15,declar:15,decod:10,decor:[26,35],deeper:27,def:[12,27,35],defin:[0,5,16,27],definit:11,delet:[5,47],deleteoldlog:47,depend:[0,22,24,28,32,33],dequ:49,deque2:49,descent:11,descript:[0,9,20,28],design:[1,5,15,20,25,34],dest:5,detail:[5,21,22],detect:13,detector:0,dict:[0,9,26],dict_to_dataclass:12,dictionari:[0,9,10,11,12,25,30],dif:[0,11],dif_creation_d:0,differ:[15,22,24,30,34,38],diffus:0,difplu:0,difplus_data:28,digit:0,direct:20,directli:[21,34,35],directori:[0,5,26,39],dirti:27,disable_output_queu:49,disk:13,displai:[15,16],dispos:34,distribut:22,do_valid:25,doe:[18,27,32,34],doesn:27,domain:28,don:14,done:34,dotfil:5,down:[15,16],download:[0,1,5,24,27,34],drill:0,dump:[10,12,30],durat:36,dure:12,duti:15,each:[0,5,12,15,16,19,30,32],earth:0,eas:27,easi:[0,20],easier:[20,27],easili:47,echo:18,edit:[14,25,34],edu:[5,17,18,22],effici:16,efficienc:16,ehwd:0,either:[5,19,35],elect:15,element:[0,49],els:27,email:[0,28],empti:[0,28,32,49],enabl:[29,34],enable_output_queu:49,encod:[9,10],encrypt:15,end:[0,34,47],end_dat:28,endfunc:5,energi:0,enforc:15,engineer:0,english:50,enhanc:0,enough:15,enter:20,entir:[16,21,22],entiti:34,entri:32,entry_id:0,entry_titl:0,env:[0,11,22],env_clear:0,env_shel:0,env_var:0,environ:0,epoch:49,eras:15,error:[5,9,16,17,20,21,28],etc:[17,27],eval:11,evalu:11,even:[15,27],event:[15,27,50],eventual:27,everi:[27,30,50],evict:28,exact:29,exampl:[5,9,11,15,19,27],except:[5,12,13,15,27],exception:[0,9],exclud:33,exe_help:2,executor:[27,35],exist:[5,9],exit:[24,49],expand:11,expect:27,experiment:0,experimental:0,expir:[26,28],explan:32,explicit:27,explicitli:27,expparser:11,expr:11,express:11,expression:11,extern:[15,19,30,34],extraterrestri:0,extreme:0,fact:27,factor:[17,18],fail:[15,26,28,31,32],fairli:[34,47],fals:[0,2,5,14,26,28,50],faster:16,fat:0,few:[27,30],field:34,figur:32,file:[0,2,5,8,10,21,22,24,25,30,33,34],file_io:35,filenam:[2,5,12,25,35,39,47],filesystem:27,fill:[20,27],filter:[0,26],filtered_input:26,find:[29,39,50],find_mim:47,find_module_recurs:39,find_nginx:47,finish:[27,34,49],first:[15,21,27,50],first_nam:0,flag:31,flow:[1,31],focu:[27,31],follow:[12,14,15,32,34],foo:[18,27],forgeri:34,form:[20,27,33],format:[0,15,50],fraction:49,framework:[22,27],from:[0,2,9,11,15,17,18,20,21,22,24,25,26,27,30],front:[34,47],ftp:5,full:[0,26,49],func:[26,49],functool:27,futur:15,galact:0,gamma:0,gasp:0,gen:[27,35],gener:[0,15,19,27,32,33,34,39,47],geoscientificinform:0,get:[0,5,26,27,32,34,35,36,39,49],get_arg:2,get_cpu:13,get_disk:13,get_event_loop:27,get_gpu:13,get_memori:13,get_node_resourc:13,get_nowait:49,get_pkg_binari:39,get_pkgdata_filenam:39,get_proxi:36,get_task_resourc:13,get_tim:13,github:[19,22],give:[0,15,33],given:[10,15,24,27,30,39],glacier:0,global_queu:26,global_storag:28,globalid:[15,39],globalid_gen:39,globu:[22,27],goal:27,goe:[0,1,15,31],good:[24,27,28,49],googl:[19,50],gpu:13,gpu_opt:11,grammar:11,grant:[27,34],graph:[28,30],graph_id:28,graph_last:28,grb:0,great:10,green:31,grid:[22,24,26,30,32],grid_queue_id:[26,28],gridspec:[26,28],gridspec_assign:26,group:[24,28,49],groupingthreadpool:49,groups_id:28,groups_offset:28,groups_prefix:28,gsiftp:5,guarante:[15,20],gzip:0,had:0,hand:25,handl:[15,19,26,27,30,34,47],handler:27,happen:[15,17,27,32,49],hard:[15,31],harden:47,hardwar:47,hash:28,have:[14,16,24,27,28,33],heavi:27,hello:27,hello_world:27,help:[2,36],here:[1,14,17,20,31],hidden:[34,35],hide:5,high:[0,27],highli:20,hinder:34,hint:47,histori:[22,28],history_id:28,history_offset:28,hit:20,hold:0,hole:0,host:24,hostnam:28,hot:0,hour:[26,36,50],how:0,howev:15,htcondor:[22,30],html:[20,34],http:[5,9,17,18,20,22,27,47],human:30,hundr:34,i3db_kei:0,ice:0,icecub:[0,5,17,18,19,22,49],icecube:0,iceprod2:[17,18],iceprod:[0,1,2,5],iceprod_config:[14,25],iceprod_serv:14,iceprodconfig:25,icetop:0,identifi:[15,28,34],idl:[28,31,32],idlen:39,idn:0,iface_convert:10,ignor:13,imag:19,immedi:[15,16,27,34],imperson:34,implicitli:27,includ:[2,5,15,16,27],indent:10,independ:[15,30,38],index:[20,28,33],info:[0,24,50],inform:[0,15,30],infrequ:15,init:7,initi:[27,29,34],inlin:27,innocu:27,input:[0,11,12,26,32],input_data:26,input_dict:12,insert:34,instal:[14,22],instanc:[22,27,32],instead:[15,27,31],institut:[0,28],instrument:0,int2char:39,integ:[15,28],integr:27,interact:[17,27,30],interfac:[5,12,17],intern:[1,19,34],internal:33,interrupt:27,interv:30,intervent:31,ints_dict:39,invok:9,involv:34,io_loop:[27,35,50],ioerror:35,ioloop:[27,35],iso:26,iso_topic_categori:0,iter:[0,26,49],iterarg:49,iterkwarg:49,itself:[1,27,33,34],javascript:0,job:[0,11,12,13,15,16,20,22,24,26,28,30],job_id:28,job_index:28,job_offset:28,job_stat:28,job_stat_id:28,job_stat_offset:28,job_temp:0,jobs_submit:[20,28],json:[0,2,7],json_compressor:10,json_decod:10,json_encod:10,jsonrpcclient:9,jsonrpcprotocol:29,jsontoobj:10,jsonutil:10,just:[0,25,26],keep:22,kei:26,key1:28,key2:28,keyword:[9,11,12],kill:[30,47,51,52],know:32,known:27,kwarg:[0,2,9,12,26,39,47,49,50,52],kwargconfig:39,kwd:8,languag:7,larg:[10,15,22,24,27,30],last:[21,50],last_login_tim:28,last_nam:0,last_tim:28,last_upd:28,last_update_tim:28,latenc:27,latest:22,launch:27,layer:22,ldap:[19,34],left:34,leftmost:49,legaci:24,len:49,lend:27,length:[15,39],less:21,let:30,letter:39,level2:33,level:[8,16,27],lib:[0,39],libev:27,librari:[12,27,35],libuv:27,lifecycl:[22,30],lifetim:34,lift:27,like:[5,8,9,12,19,24,25,27,30,34,35,50],limit:[13,15,34],line:[5,21,35],link:[16,34],list:[0,5,10,11,16,21,26,28,33,39],listen:27,listmodul:39,load:[0,10,12,22,25,32,34],load_str:25,local:[0,24,30,31,33,39],localhost:27,localid_ret:39,locat:[0,15,25,36,47],locateconfig:25,lock:27,log:[0,8,10,13,19,21,26,47,52],log_fil:0,logfil:28,login:17,logrot:[47,52],look:21,lookup:[26,33],loop:27,lose:27,lost:15,lower:[15,27],lzma:0,macro:17,mad:0,made:32,madison:0,mai:[5,18,27,32,49],main:[1,2,15,24,25,27,30,34],make:[5,15,16,20,26,27,30,34],manag:[22,36],mani:[15,16,22],manual:[25,31],map:49,master_update_histori:28,master_update_history_id:28,master_update_history_last:28,match:[24,26,29],match_us:26,max_work:27,maximum:16,maxint:49,maxlocalid:39,maxsiteid:39,maxwait:50,mean:33,meantim:27,measur:34,mechan:27,mediumtext:28,memori:13,met:[0,32],meta:7,metadata_nam:0,metadata_vers:0,metajsonrpc:9,meteorolog:0,method:[0,9,12,18,22],methodnam:9,microsecond:27,middlewar:22,might:15,mime:47,mimic:5,min:50,minbia:0,minimum:16,minut:[34,50],mirror:15,miss:32,mkdir:5,mode:5,modif:30,modifi:[14,25,34],modul:[0,2,15,22],monitor:0,monthspec:50,moon:0,more:[0,15,20,27,29,32,33,47],most:[11,15,22,27,30,34,47],mostli:[27,30],move:[5,27],movement:[0,27],movement_opt:0,much:[15,27],multi:[16,27],multiprocess:49,muon:0,must:[5,9,15,19,27,29,30,39],mutex:49,my_fil:35,my_hex_passkey_her:18,my_paramet:11,myhandl:[27,35],mysql:[22,30],name:[0,9,10,16,20,21,26,28,33,35,39,49],namedthreadpool:49,namedtupl:5,necessari:[27,34],need:[5,15,22,26,34],nest:1,network:[15,27],neutrino:0,next:[16,27,50],nginx:[14,22,30],nick:27,node:[13,15,24,28,52],node_id:28,node_offset:28,node_resourc:[13,26],noncriticalerror:13,none:[0,2,5,9,10,11,12,25,26,27,35,36,39,47,49,50],normal:27,note:[0,10],nova:0,now:[27,50],nowstr:26,nsf:0,num:26,num_task:26,num_thread:49,number:[13,20,26,27,28,30,32,35,49],numer:[0,20],obj:[2,10,12],objtojson:10,obtain:18,occur:12,off:[25,32],offici:27,official:27,offlin:15,offset:28,often:27,old:[15,47],onc:[22,24,26,30,32,49],once:32,one:[15,27,34],oneshot:50,onli:[0,10,17,24,27,30,49],onlin:15,only:[15,34],onto:24,open:[9,27,35],oper:[11,15,27],optical:0,option1:11,option:[0,11,12,14,15,20,25,26,35,36],optional:22,order:34,ordin:50,origin:[27,34],other:[0,5,10,11,15,18,19,20,22,24,27],out:[0,15,32],output:[0,5],over:[10,15],overrid:[28,31],overridden:31,overusag:13,overview:22,overwrit:25,own:[15,30],packag:[27,35,39],package_nam:39,page:[14,16,19,21,28,34],paradigm:15,parallel:27,param:[9,18],paramet:[0,8,11,12,18,25,26,29,35,36,50],parent:[5,26],parent_id:0,pars:11,parsecron:50,parser:7,part:[11,24,30],partial:27,partit:15,pass:[0,12,27,34,39],pass_kei:28,passkei:[9,18,26,28,34],passkey_id:28,passkey_last:28,passphras:36,past:20,path:39,pattern:33,paus:49,pbs:30,pend:32,pep:27,per:[27,47],perform:[15,47],period:15,perman:0,personnel:0,perspect:17,phone:19,photomultipli:0,phrase:11,piec:38,pilot:[24,26,28],pilot_id:[26,28],pilot_last:28,pip:[22,35],place:27,plane:0,plenti:15,plu:[0,11],plugin:[19,22,26,30],plural:0,point:[0,27,28,32,49],polar:0,pole:0,popen:5,possibilit:11,possibl:[11,15,18,28,32,47],post:27,potenti:32,pre:26,prefix:8,present:[0,15,49],prev_statu:28,previou:[8,27,33,50],prevtim:50,primari:[22,27,30],print:27,prioriti:[26,28,49],prioritythreadpool:49,privat:18,probabl:[15,21],problem:27,process:[16,24,26,27,28,31,32,38,49],program:[5,18,25],progress:[17,34],project:0,proof:15,propag:[0,33],proper:26,properli:15,protect:34,protocol:9,prototyp:0,provid:[27,49],proxi:22,pull:15,purpos:[22,34],push:15,put:[5,49],put_nowait:49,pybind:27,pyc:39,pyev:27,pyftpdlib:27,python2:39,python:[0,10,14,22,27,35,39],qsize:49,queri:[16,18,26],queu:[15,26,28,31,32],queue_add_pilot:26,queue_add_task_lookup:26,queue_buffer_jobs_task:26,queue_del_pilot:26,queue_get_active_task:26,queue_get_cfg_for_dataset:26,queue_get_cfg_for_task:26,queue_get_grid_task:26,queue_get_pilot:26,queue_get_queueing_dataset:26,queue_get_queueing_task:26,queue_get_task:26,queue_get_task_by_grid_queue_id:26,queue_get_task_lookup:26,queue_mast:29,queue_new_pilot_id:26,queue_oper:27,queue_reset_task:26,queue_set_site_queu:26,queue_set_submit_dir:26,queue_set_task_statu:26,quick:[27,33],quot:27,radio:0,rai:0,rais:[0,5,26,35],random:[11,15,39],randomli:15,rang:[15,20,27],raw:[9,20],raytheon:0,reach:16,read:[2,27,35],readlin:35,realli:10,reassign:15,receiv:15,recent:15,recommend:20,reconfigur:52,recurs:[0,11,39],recursive_unicod:10,red:31,redirect:8,refer:[11,27,34],referenc:32,refreez:0,regist:19,regular:[0,8,9,15,30],relai:0,relat:[20,27],relationship:30,relev:[21,27],reload:[30,51,52],remot:[0,26,27],remov:[5,26,34,49],replac:15,replica:28,repositori:15,repr_convert:10,repres:0,req_cpu:28,req_disk:28,req_gpu:28,req_memori:28,request:[5,9,18,27,29,32,34,47,52],request_timeout:5,requesthandl:[27,35],requir:[0,15,18,19,20,28,32,34,35],required:9,requr:18,research:0,reset:[17,26,28,31],resourc:[0,1,13,15,22,24,26,28,29,39],resource_id:28,resource_nam:0,resource_offset:28,respond:29,respons:[9,24],rest:[27,30],restart:[9,15,30,51,52],result:[5,9,16,27],resum:[15,26,28,31],resync:15,ret:27,retriev:[27,39],return_futur:27,revis:20,rfc:19,rice:0,right:49,risk:15,rmdir:5,rmtree:5,role:0,role_id:28,role_nam:28,roles_id:28,roles_offset:28,rotat:[47,52],round:26,rpc:7,rpsc:0,run:0,run_forev:27,run_modul:39,run_numb:0,run_on_executor:[27,35],runner:0,running_class:0,runtim:50,safe:[11,25,27],safe_ev:11,safeti:27,salt:[28,39],same:[0,11,24,27,30,34],save:[16,25,34],save_to_str:25,scalabl:27,scan:19,scenario:20,schedul:[22,27],scheme:34,science:0,scopel:11,scoper:11,script:[0,18,20,34],search:[28,32,39],second:[19,27,34,47,49],secret:14,section:[0,16,21],see:[16,17,18,27,29,32],select:[15,21,26],self:[27,30,35],send:[9,29],sensor:0,sensor_nam:[0,11],sent:10,sentenc:11,separ:[33,34,38,39],sequenti:33,serial:[0,7],serializationerror:12,serialize_json:12,serv:34,server:[5,9],servic:0,session:[9,28,34],session_id:28,session_kei:28,session_last:28,set:[0,2],set_convert:10,set_dur:36,set_passphras:36,set_task_statu:9,setting_id:28,sever:[20,27,30,31,34],shadow:0,shall:31,shallow:31,share:[27,38],sheet:0,shell:22,shorter:27,should:[0,5,15,21,27,35],show:[20,21],shower:0,shown:21,side:49,sign:[15,30],signatur:27,simdb_kei:0,simpl:[0,9,10,49],simulation:0,sinc:[10,24,26,27,30,49],singlegroup:49,site_id:[15,26,28,39],site_temp:0,site_valid:26,siteglobusproxi:36,siteid_gen:39,siteid_ret:39,size:5,sleep:27,slop_op:27,slow:27,slow_op:27,slow_oper:27,small:15,smaller:15,socket:27,sole:27,solut:15,some:[8,10,16],someth:27,somewher:27,sourc:[0,2,5,8,9,10,11,12,13,25,26,35,36,39,47,49,50,51,52],source_nam:0,south:0,space:[0,15,16,32],spase:0,special:0,specif:[19,30],specifi:26,spend:27,spent:16,sprintf:11,sptr:0,sql:26,sqlite:30,squid:[22,30,38],src:[0,5],standard:[15,27,31],start:[0,9,15,20,27,30,39,47,49,50,52],start_dat:28,starter:11,startup:[24,30],stat:28,stat_kei:28,state:15,statist:16,statu:[16,26,28],status:28,status_chang:28,std:2,stderr:21,stdlog:21,stdout:[8,21],steal:34,steer:[0,11],steering_fil:0,still:15,stop:[9,24,27,30,47,51,52],storag:0,storage_loc:0,store:[15,24,30],str2datetim:26,str:[26,27,28,39],stream:8,streamfunc:5,streaming_callback:5,strftime:0,string:[0,9,10,11,12,15,20,25,26,28,39,50],structur:[10,20,27,30],stuff:5,style:27,subcategori:0,subclass:26,submiss:17,submit:[15,17,18,20,26,27,30,32,34],submit_dir:[26,28],submit_host:28,submit_tim:[26,28],submodul:39,subprocess:2,subtract:32,succe:15,success:[9,16],sum:26,summari:0,suppli:34,support:[10,12,14,27,30],sure:[15,27],surfac:47,suspend:[27,28,31],suspens:27,symbol:11,sync:15,syntax:[11,20,27],system:[0,11,14,22,31,49],tabl:15,table_nam:28,take:[15,26,27,30,32],taken:[15,30],talk:34,tar:22,task:[0,13,15,16,17,20],task_don:49,task_id:[9,20,26,28,33],task_index:28,task_log:28,task_log_id:28,task_log_offset:28,task_lookup:28,task_offset:28,task_rel:[28,30,32],task_rel_id:[28,33],task_rel_offset:28,task_resourc:13,task_resource_overusag:13,task_stat:28,task_stat_id:28,task_stat_offset:28,task_statu:28,task_temp:0,tasks_submit:28,tau:0,tdrss:0,telescop:0,tell:24,temporarili:15,temporary_storag:28,test:[0,18,27],testdaq:0,text:[25,28],than:[0,15,32,33],thei:[15,22,32,34],them:[15,30,34,49],thi:[0,2,9,15,16,18,20,21,24,25,26,27,28,30,32,33,34,50],thing:[10,27,33,34],those:[24,26],though:[20,27,30],thought:27,thousand:[27,34],thread:[25,27,35,49],threadpool:[49,50],threadpooldequ:49,threadpoolexecutor:27,three:20,through:[1,15,18,27,30,32],thu:27,time:[0,5,13,15,16,19,24,26,27,30,49,50],time_convert:10,timeout:[9,15],timestamp:28,tls:[22,38,47],to_fil:8,to_log:8,togeth:[15,22],token:18,tool:36,toolkit:[22,27],top:22,tornado:5,torqu:30,total:[16,28],tradit:27,trai:0,transact:49,transfer:15,translat:20,tray_temp:0,treat:[27,34],tree:11,trick:34,truli:27,tube:0,tupl:10,turn:[0,25],twist:27,two:[15,17,18],txt:35,type:[0,5,13,15,17],type_opt:0,unbias:0,uncheck:34,unclassifi:0,uncompress:10,under:[15,20],underli:12,unfinished_task:49,unicod:10,unicode_to_ascii:2,uniqu:[15,20],univers:0,unlik:47,unset:25,until:[15,24],updat:[15,30,52],update:36,update_index:28,update_proxi:36,updater:[22,38],upload:[1,34],upmu:0,url:[0,20,28,29],use:[25,50],used:10,useful:47,user_id:[26,28],user_offset:28,usernam:[26,28,34],using:[15,19,27],usr:39,usual:[26,27,32],utc:26,util:[10,13,27],utiliti:7,uwi:0,valid:[0,18,19,25,26,33,39],valid_categori:0,valid_nam:0,valid_paramet:0,valid_sensor_nam:0,valid_source_nam:0,valu:[0,10,11,12,13,15,18,25,27,28],var_convert:10,variabl:[0,30],variou:30,veri:[15,20,27,34],verifi:[15,30],version:[0,28,34],via:15,view:[16,17,18],visibl:27,vulcan:0,wai:[30,34,39],wait:[9,15,26,27,28,31,32,49],walk:10,walltim:28,walltime_err:28,walltime_err_n:28,want:[15,18,20],water:0,wattl:27,weak:47,web:[19,27],webcam:0,webnot:28,webnote_id:28,webnote_last:28,webserv:[14,47],website_url:28,webstat:28,webstat_id:28,webstat_last:28,welcom:20,well:[2,27],what:[20,24],whatev:27,when:[15,19,21,27,32,33,34],whenev:[15,27],where:[5,11,16,26,27,30],whether:33,which:[0,15,27,30,32,34],whole:32,why:34,wide:[8,36],wimp:0,wimps:0,wipacrepo:22,wipe:0,wisc:[5,17,18,22],wisconsin:0,within:[16,18,20,28,30],without:27,won:26,word:11,work:[18,27,49],worker:[27,52],world:27,worri:[25,27],would:[15,27],wrap:27,wrapper:[47,52],write:[27,35,49],written:35,x10:15,x509:34,yield:[27,35],you:[14,15,18,21,22,27,32,33,34],your:[15,18],zeromq:27},titles:["Dataclasses","Execution Functions","Execution Helpers","JSONRPC Calls","Functions","GridFTP","I3Exec","IceProd Core","Core Init","JSON-RPC Client","JSON Utilities","Meta-Language Parser","Serialization","Utilities","Dev Notes","Extras","Dataset Monitoring","User&#8217;s Guide","JSON-RPC Interface","Login","Dataset Submission","Task Monitoring","IceProd","IceProd Modules","Overview","Detailed Configuration","DB Methods","Asynchronous Programming","DB Config","Global Queueing","IceProd Server Details","Lifecycles","From Submission to Queue","Task Relationships","Website","File IO","Globus","Grid Queueing","IceProd Server","Server Init","Module","Database Module","Master Updater Module","Proxy Module","Queueing Module","Schedule Module","Website Module","Nginx","Condor Plugin","Pool","Schedule","Server","Squid","SSL/TLS Certificate Utilities"],titleterms:{"class":38,"function":[1,4],account:34,admin:22,advanc:20,algorithm:32,archive:28,asynchron:27,asyncio:27,authent:[18,19],background:27,backup:15,basic:20,brief:27,buffer:32,call:3,callback:27,certif:53,client:9,commun:[15,34],condor:48,config:28,configur:[0,25,30],core:[7,8,24],csrf:34,databas:[30,41],dataclass:0,dataset:[16,20,31,32],detail:[25,27,30],dev:14,disabl:14,document:22,environ:1,exception:15,execut:[1,2],expert:20,extra:15,factor:19,failur:15,file:35,from:32,futur:27,global:[15,29],globu:36,grid:37,gridftp:[5,27],guid:17,header:34,helper:2,how:14,human:34,i3exec:6,iceprod:[7,22,23,30,38],init:[8,39],installat:22,interact:34,interfac:18,job:31,join:15,json:[9,10,18,34],jsonrpc:3,kei:28,languag:11,lifecycl:31,login:[19,34],macro:20,mani:24,master:[15,42],meta:11,metadata:0,method:26,mode:24,modul:[23,38,40,41,42,43,44,45,46],monitor:[16,21],multipl:15,nginx:[34,47],note:[14,22,27],object:[0,1],openssl:30,other:30,overview:24,parser:11,password:14,plugin:[38,48],pool:[15,49],practic:27,program:27,protocol:29,proxi:[30,43],queue:[15,29,30,32,37,44],regular:38,relationship:33,role:15,rpc:[9,18,34],run:[1,14],schedul:[30,45,50],secur:[15,34],serial:12,server:[14,24,30,38,39,51],set:14,setup:1,singl:24,site:[15,34],some:27,squid:52,ssl:[14,53],submiss:[20,32,33],summari:27,synchron:15,tabl:28,task:[21,24,31,33,34],task_rel:33,tls:53,topic:17,tornado:27,two:19,type:20,updater:42,usage:27,user:[17,34],utiliti:[10,13,30,53],view:20,web:34,websit:[14,30,34,46],within:33}})