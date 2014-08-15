/*!
 * Dataset submission tools
 */

var Submission = (function( $ ) {

    var data = {
        element : null,
        state : 'expert',
        passkey : null,
        submit_data : {}
    };
    
    function pluralize(value) {
        var ret = "" + value;
        if (ret in dataclasses['names'])
            return dataclasses['names'][ret];
        else
            return ret;
    }
    function singular(value) {
        var ret = "" + value;
        for (d in dataclasses['names']) {
            if (ret == dataclasses['names'][d])
                return d;
        }
        return ret;
    }
    function getDataclass(path,key) {
        console.log('getDataclass('+path+' , '+key+')')
        if (path === null || path == '')
            path = key;
        else if (key != null && key != '')
            path = path + '.' + key;
        var depths = path.split('.'), d = dataclasses['classes']['Job'],
            part = [], p = '', c = null;
        for (var i=0;i<depths.length;i++) {
            part = depths[i].split('_');
            if (part.length > 1) {
                p = part.slice(0,-1).join('_');
            } else
                p = part[0]
            if (p in d && $.type(d[p]) == 'array') {
                c = d[p][1];
                d = dataclasses['classes'][c]
            } else
                return null;
        }
        return c;
    }
    
    var private_methods = {
        clean_json : function(j) {
            var json = j;
            if (j === undefined)
                json = data.submit_data;
            if ($.type(json) === 'array') {
                for (var i=0;i<json.length;i++)
                    json[i] = private_methods.clean_json(json[i]);
            } else if ($.type(json) === 'object') {
                for (var i in json) {
                    if (i == '_type')
                        continue;
                    json[i] = private_methods.clean_json(json[i]);
                }
            }
            if (j === undefined)
                data.submit_data = json;
            else
                return json;
        },
        json_type_markup : function(j,t) {
            var json = j;
            if (j === null) {
                console.log('markup null');
                return j;
            }
            if (j === undefined && t === undefined) {
                console.log('markup undefined');
                json = data.submit_data;
                console.log(json);
                t = 'Job';
            }
            if ($.type(json) === 'array') {
                for (var i=0;i<json.length;i++) {
                    json[i] = private_methods.json_type_markup(json[i],t);
                }
            } else if ($.type(json) === 'object') {
                if (t in dataclasses['names']) {
                    var parent = dataclasses['classes'][t];
                    for (var i in json) {
                        if (i in parent && $.type(parent[i]) === 'array')
                            json[i] = private_methods.json_type_markup(json[i],parent[i][1]);
                    }
                    json['_type'] = t;
                }
            }
            if (j === undefined)
                data.submit_data = json;
            else
                return json;
        },
        submit : function(num_jobs, gridspec) {
            private_methods.clean_json();
            RPCclient('submit_dataset',{passkey:data.passkey,data:data.submit_data,njobs:num_jobs,gridspec:gridspec},callback=function(return_data){
                $('#error').html('success');
            });
        },
        build_basic : function( ) {
            private_methods.json_type_markup();
            var editing = (function(){
                var keys = {};
                var methods = {
                    is: function(key,path) {
                        if (!(path === undefined) && path != null && path != '')
                            key = path+'.'+key;
                        console.log('editing.is() key='+key);
                        if (key in keys)
                            return keys[key];
                        return keys[key] = false;
                    },
                    set: function(key,val,path) {
                        console.warn('editing.set('+key+' , '+val+' , '+path+')');
                        if (!(path === undefined) && path != null && path != '')
                            if (key != null && key != '')
                                key = path+'.'+key;
                            else
                                key = path;
                        console.log('editing.set() key='+key);
                        keys[key] = val;
                    },
                    clearall: function() {
                        keys = {};
                    }
                };
                return methods;
            })();
            var converters = {
                intToStr: function(value) {
                    if (value == null || value == undefined)
                        return ""
                    else
                        return "" + value;
                },
                strToInt: function(value) {
                    if (value.toLowerCase() == 'true')
                        return true;
                    else if (value.toLowerCase()  == 'false')
                        return false;
                    else if (value != '' && !isNaN(value)) {
                        if (value.indexOf('.') > -1)
                            return parseFloat(value);
                        else
                            return parseInt(value);
                    } else
                        return value;
                },
                keyToHtml: function(value) {
                    return "" + value.replace('_',' ');
                },
                singular: singular
            };
            var helpers = {
                editable: editing.is,
                equal: function(a,b){
                    var ret = (a == b);
                    console.warn('equal('+a+','+b+'):'+ret);
                    return ret;
                },
                isNull: function(input){
                    return input === null;
                },
                isArray: function(input){
                    return $.type(input) === 'array';
                },
                isBasicArray: function(input){
                    ret =  (input.length > 0 && $.type(input[0]) !== 'object');
                    console.log('isBasicArray '+ret)
                    return ret;
                },
                isObject: function(input){
                    return $.type(input) === 'object';
                },
                isNotPrivate: function(input){
                    return input.charAt(0) != '_';
                },
                isEnum: function(path,key){
                    var c = getDataclass(path);
                    if (c === null || !(c in dataclasses['classes'])) {
                        console.log('isEnum(): dataclass missing');
                        return false;
                    }
                    c = dataclasses['classes'][c];
                    if (!(key in c))
                        return false;
                    var ret= ($.type(c[key]) === 'array' && $.type(c[key][1] === 'array') && c[key][1].length > 0);
                    console.log('isEnum(): '+ret);
                    return ret;
                },
                getEnums: function(path,key){
                    var c = getDataclass(path);
                    if (c === null || !(c in dataclasses['classes']))
                        return [];
                    return dataclasses['classes'][c][key][1];
                },
                concat: function(a,b,c){
                    if (b === undefined)
                        return a;
                    else {
                        if (a != '')
                            a += '.';
                        if (c === undefined || c === null || c == '')
                            return a+b;
                        else
                            return a+c+'_'+b;
                    }
                },
                get_class: function(path,key){
                    var ret = getDataclass(path,key);
                    if (ret === null)
                        return key;
                    else
                        return ret;
                },
                isDataclass: function(path,key){
                    return !(getDataclass(path,key) === null);
                }
            };
            $.views.helpers(helpers);
            $.views.converters(converters);
            $.templates({
                AdvTmpl:"#AdvTmpl"
            });
            var id = '#basic_submit';
            $(id).off().empty();
            $.link.AdvTmpl(id,data.submit_data)
            .on('click','.editable span',function(){
                var parent = $(this).parent().parent().parent(),
                    key = $(this).parent().find('span.key').text().replace(' ','_'),
                    path = $(parent).children('span.path').text();
                if ($(this).hasClass('key') && $(this).parent().hasClass('key_editable'))
                    editing.set(key+"_key",true,path);
                else
                    editing.set(key,true,path);
                $.view(id, true, 'data').refresh();
                window.setTimeout(function(){
                    var input = $(id).find('.editing input').first();
                    if (input.length > 0) {
                        input.focus();
                        var strLength = input.val().length;
                        input[0].setSelectionRange(strLength,strLength);
                    } else {
                        input = $(id).find('.editing select').first();
                        if (input.length > 0) {
                            input.focus();
                        }
                        else
                            console.warn('no input for key:'+key);
                    }
                },100);
            })
            .on('blur','.editing',function(){
                var parent = $(this).parent().parent(), 
                    key = $(this).find('span.key').text().replace(' ','_'),
                    path = $(parent).children('span.path').text();
                if ((key === null || key == '') && path != null && path != '')  {
                    // this is a basic array
                    var val = converters.strToInt($(this).find('input').val()),
                        depths = path.split('.'), d = data.submit_data,
                        c = 0, part = [], p = '', i = 0;
                    for (;i<depths.length-1;i++) {
                        part = depths[i].split('_');
                        if (part.length > 1) {
                            p = part.slice(0,-1).join('_');
                            c = parseInt(part.slice(part.length-1)[0],10);
                            d = d[p][c];
                        } else
                            d = d[part[0]];
                    }
                    part = depths[i].split('_');
                    if (part.length > 1) {
                        p = part.slice(0,-1).join('_');
                        c = parseInt(part.slice(part.length-1)[0],10);
                        d[p][c] = val;
                    } else
                        d[part[0]] = val;
                } else if ($(this).find('select').length > 0) {
                    // this is an enum
                    var val = converters.strToInt($(this).find('select option:selected').text()),
                        depths = path.split('.'), d = data.submit_data,
                        c = 0, part = [], p = '', i = 0;
                    for (;i<depths.length;i++) {
                        part = depths[i].split('_');
                        if (part.length > 1) {
                            p = part.slice(0,-1).join('_');
                            c = parseInt(part.slice(part.length-1)[0],10);
                            d = d[p][c];
                        } else
                            d = d[part[0]];
                    }
                    d[key] = val;
                }
                // else, this is taken care of by jsviews
                editing.clearall();
                $.view(id, true, 'data').refresh();
            })
            .on('blur','.editing_key',function(){
                var parent = $(this).parent().parent(), 
                    key = $(this).find('span.key').text().replace(' ','_'),
                    path = $(parent).children('span.path').text(),
                    depths = path.split('.'), d = data.submit_data,
                    c = 0, part = [], p = '';
                if (!(path === undefined) && path != null && path != '') {
                    for (var i=0;i<depths.length;i++) {
                        part = depths[i].split('_');
                        if (part.length > 1) {
                            p = part.slice(0,-1).join('_');
                            c = parseInt(part.slice(part.length-1)[0],10);
                            d = d[p][c];
                        } else
                            d = d[part[0]];
                    }
                }
                var newkey = $(this).find('input').val();
                if (newkey != key) {
                    d[newkey] = d[key];
                    delete d[key];
                }
                editing.clearall();
                $.view(id, true, 'data').refresh();
            })
            .on('click','.add',function(){
                var parent = $(this).parent().parent(), key = $(this).find('span.key').text().replace(' ','_'),
                    path = $(parent).children('span.path').text(),
                    depths = path.split('.'), d = data.submit_data,
                    c = 0, part = [], p = '';
                if (!(path === undefined) && path != null && path != '') {
                    for (var i=0;i<depths.length;i++) {
                        part = depths[i].split('_');
                        if (part.length > 1) {
                            p = part.slice(0,-1).join('_');
                            c = parseInt(part.slice(part.length-1)[0],10);
                            d = d[p][c];
                        } else
                            d = d[part[0]];
                    }
                }
                console.log('add() path='+path+'   key='+key);
                console.log(d);
                var obj = private_methods.insert_dataclass(d,key);
                if ($(this).hasClass('null')) {
                    console.log('add() null');
                    console.log(d[key]);
                    d[key] = obj;
                    console.log(d[key]);
                    $.view(id, true, 'data').refresh();
                } else if ($(this).hasClass('array')) {
                    console.log('add() array')
                    if (d[key].length < 1) {
                        d[key].push(obj);
                        $.view(id, true, 'data').refresh();
                    } else
                        $.observable(d[key]).insert(obj);
                } else if ($(this).hasClass('object')) {
                    console.log('add() object')
                    d[key]['newkey'] = obj;
                    $.view(id, true, 'data').refresh();
                }
            });
            $('body').on('blur',function(){
                editing.clearall();
            });
        },
        new_dataclass : function( t ) {
            // return a new dataclass of type t
            if (!(t in dataclasses['names'])) {
                console.log(t+' not in dataclasses');
                return undefined;
            }
            console.log('making new dataclass: '+t);
            var target = dataclasses['classes'][t], ret = {'_type':t};
            for (var k in target) {
                if ($.type(target[k]) === 'array')
                    ret[k] = target[k][0];
                else
                    ret[k] = target[k];
            }
            console.log(ret);
            return ret;
        },
        insert_dataclass : function( parent, k ) {
            // return a new dataclass for the key in parent
            var target = {};
            if (parent === 'option') {
                console.log('making string')
                return '';
            } else if ($.type(parent) === 'string')
                target = dataclasses['classes'][parent];
            else if ('_type' in parent)
                target = dataclasses['classes'][parent['_type']];
            if (k in target && $.type(target[k]) === 'array') {
                var ret = target[k][1], t = $.type(ret);
                if (t === 'string' && ret in dataclasses['names']) {
                    return private_methods.new_dataclass(ret);
                } else if (t === 'object') {
                    console.log('making new dict');
                    return $.extend(true,{},ret);
                } else {
                    console.log('making new ret');
                    console.log(ret);
                    return ret;
                }
            }
            return undefined;
        }
    };
    
    var public_methods = {
        init : function(args) {
            if (args == undefined) {
                throw new Error('must supply args');
                return;
            }
            data.state = 'expert';
            data.passkey = args.passkey;
            data.element = $(args.element);
            data.submit_data = private_methods.new_dataclass('Job')
            private_methods.clean_json();
            
            var html = '<div><button id="basic_button">Basic View</button> <button id="expert_button">Expert View</button></div></div>';
            html += '<div id="basic_submit" style="display:none">basic</div>';
            html += '<div id="expert_submit"><textarea id="submit_box" style="width:90%;min-height:400px">'
            html += '</textarea></div>';
            html += '<div>Number of jobs: <input id="number_jobs" value="1" /> <select id="gridspec" style="margin-left:10px">';
            for (var g in args.gridspec) {
                html += '<option value="'+g+'">'+args.gridspec[g][1]+'</option>';
            }
            html += '</select></div>';
            html += '<button id="submit_action" style="padding:1em;margin:1em">Submit</button>';
            $(data.element).html(html);
            $('#submit_box').val(pprint_json(data.submit_data));
            
            $('#submit_action').on('click',function(){
                var njobs = ValueTypes.int.coerce($('#number_jobs').val());
                if ( njobs == null || njobs == undefined ) {
                    $('#error').text('Must specify integer number of jobs');
                    return;
                }
                private_methods.submit( njobs, $('#gridspec').val() );
            });
            var goto_basic = function(){
                if (data.state != 'basic') {
                    data.state = 'basic';
                    private_methods.build_basic();
                    $('#expert_submit').hide();
                    $('#basic_submit').show();
                }
            };
            var goto_expert = function(){
                if (data.state != 'expert') {
                    data.state = 'expert';
                    //private_methods.clean_json();
                    $('#expert_submit').find('textarea')
                    .on('blur',function(){data.submit_data = JSON.parse($(this).off().val());})
                    .val(pprint_json(data.submit_data));
                    $('#basic_submit').hide();
                    $('#expert_submit').show();
                }
            };
            $('#basic_button').on('click',goto_basic);
            $('#expert_button').on('click',goto_expert);
            
            // default to a view
            if (data.state == 'basic')
                goto_basic();
            else
                goto_expert();
        }
    };
    
    return function(m,args) {
        if (m == null || m == undefined) {
            throw new Error('must supply (method,arguments)');
        } else if (m in public_methods) {
            public_methods[m](args);
        } else {
            throw new Error('Cannot find method '+m);
        }
    };
})(jQuery);