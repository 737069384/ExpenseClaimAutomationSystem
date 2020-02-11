# Generated by Django 2.2.7 on 2020-02-11 10:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import workflow.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_auto_20200211_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('order', models.IntegerField(default=0, help_text='用于工单步骤接口时，step上状态的顺序(因为存在网状情况，所以需要人为设定顺序),值越小越靠前', verbose_name='状态顺序')),
                ('state_type', models.IntegerField(choices=[(0, '普通类型'), (1, '初始状态'), (2, '结束状态')], default=0, help_text='0.普通类型 1.初始状态(用于新建工单时,获取对应的字段必填及transition信息) 2.结束状态(此状态下的工单不得再处理，即没有对应的transition)', verbose_name='状态类型id')),
                ('participant_type', models.IntegerField(blank=True, choices=[(0, '无处理人'), (1, '个人'), (2, '多人'), (3, '部门'), (4, '角色'), (5, '脚本'), (6, '参与人')], default=1, help_text='0.无处理人,1.个人,2.多人,3.部门,4.角色,5.脚本,6.参与人', verbose_name='参与者类型id')),
                ('participant', models.CharField(blank=True, default='', help_text='可以为空(无处理人的情况，如结束状态)、username、多个username(以,隔开)、部门id、角色id、变量(creator,creator_tl)、        脚本记录的id等，包含子工作流的需要设置处理人为loonrobot', max_length=100, verbose_name='参与者')),
                ('distribute_type', models.IntegerField(choices=[(0, '主动接单'), (1, '直接处理'), (2, '随机分配'), (4, '全部处理')], default=0, help_text='0.主动接单(如果当前处理人实际为多人的时候，需要先接单才能处理) 1.直接处理(即使当前处理人实际为多人，也可以直接处理)        2.随机分配(如果实际为多人，则系统会随机分配给其中一个人) 3.全部处理(要求所有参与人都要处理一遍,才能进入下一步)', verbose_name='分配方式')),
                ('state_field_str', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='json格式字典存储,包括读写属性1：只读，2：必填，3：可选. 示例：{"created_at":1,"title":2, "sn":1},         内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,        workflow.workflow_name:工作流名称', verbose_name='表单字段')),
                ('creator', models.ForeignKey(help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.User')),
            ],
            options={
                'verbose_name': '工作流状态',
                'verbose_name_plural': '工作流状态',
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('description', models.CharField(max_length=50, verbose_name='描述')),
                ('flowchart', models.FileField(blank=True, help_text='工作流的流程图,为了方便别人', upload_to='flowchart', verbose_name='流程图')),
                ('limit_expression', models.CharField(blank=True, default='{}', help_text='限制周期({"period":24} 24小时), 限制次数({"count":1}在限制周期内只允许提交1次), 限制级别({"level":1} 针对(1单个用户 2全局)限制周期限制次数,        默认特定用户);允许特定人员提交({"allow_persons":"zhangsan,lisi"}只允许张三提交工单,{"allow_depts":"1,2"}只允许部门id为1和2的用户提交工单，        {"allow_roles":"1,2"}只允许角色id为1和2的用户提交工单)', max_length=1000, verbose_name='限制表达式')),
                ('display_form_str', models.CharField(blank=True, default='[]', help_text='默认"[]"，用于用户只有对应工单查看权限时显示哪些字段,field_key的list的json,如["days","sn"],        内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,        workflow.workflow_name:工作流名称', max_length=10000, verbose_name='展现表单字段')),
                ('creator', models.ForeignKey(help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.User')),
            ],
            options={
                'verbose_name': '工作流',
                'verbose_name_plural': '工作流',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('name', models.CharField(max_length=50, verbose_name='操作')),
                ('transition_type', models.IntegerField(choices=[(0, '常规流转'), (1, '定时器流转')], default=0, help_text='0.常规流转，1.定时器流转,需要设置定时器时间', verbose_name='流转类型')),
                ('timer', models.IntegerField(default=0, help_text='流转类型设置为定时器流转时生效,单位秒。处于源状态X秒后如果状态都没有过变化则自动流转到目标状态', verbose_name='定时器(单位秒)')),
                ('condition_expression', models.CharField(default='[]', help_text='流转条件表达式，根据表达式中的条件来确定流转的下个状态，格式为[{"expression":"{days} > 3 and {days}<10", "target_state_id":11}]         其中{}用于填充工单的字段key,运算时会换算成实际的值，当符合条件下个状态将变为target_state_id中的值,表达式只支持简单的运算或datetime/time运算.        loonflow会以首次匹配成功的条件为准，所以多个条件不要有冲突', max_length=1000, verbose_name='条件表达式')),
                ('attribute_type', models.IntegerField(choices=[(0, '同意'), (1, '拒绝'), (2, '其他')], default=0, help_text='属性类型，0.同意，1.拒绝，2.其他', verbose_name='属性类型')),
                ('creator', models.ForeignKey(help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.User')),
                ('destination_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_transitions', to='workflow.State', verbose_name='目的状态')),
                ('source_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_transitions', to='workflow.State', verbose_name='源状态')),
                ('workflow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.Workflow', verbose_name='工作流id')),
            ],
            options={
                'verbose_name': '工作流流转',
                'verbose_name_plural': '工作流流转',
            },
        ),
        migrations.AddField(
            model_name='state',
            name='sub_workflow',
            field=models.ForeignKey(blank=True, help_text='如果需要在此状态启用子工单,请填写对应的工作流id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_workflow_states', to='workflow.Workflow', verbose_name='子工作流'),
        ),
        migrations.AddField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workflow_states', to='workflow.Workflow', verbose_name='工作流'),
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('field_type', models.IntegerField(choices=[(0, '字符串'), (1, '整形'), (2, '浮点型'), (3, '布尔'), (4, '时间'), (5, '日期时间'), (6, '单选框'), (7, '多选框'), (8, '下拉列表'), (9, '多选下拉列表'), (10, '文本域'), (11, '附件')], help_text="(0, '字符串'), (1, '整形'), (2, '浮点型'), (3, '布尔'), (4, '时间'), (5, '日期时间'), (6, '单选框'), (7, '多选框'),\n                  (8, '下拉列表'), (9, '多选下拉列表'), (10, '文本域'),(11,'附件')", verbose_name='类型')),
                ('field_key', models.CharField(help_text='字段类型请尽量特殊，避免与系统中关键字冲突', max_length=50, verbose_name='字段标识')),
                ('field_name', models.CharField(max_length=50, verbose_name='字段名称')),
                ('order', models.IntegerField(default=0, help_text='工单基础字段在表单中排序为:流水号0,标题20,状态id40,状态名41,创建人80,创建时间100,更新时间120.前端展示工单信息的表单可以根据这个id顺序排列', verbose_name='排序')),
                ('default_value', models.CharField(blank=True, help_text='前端展示时，可以将此内容作为表单中的该字段的默认值', max_length=100, null=True, verbose_name='默认值')),
                ('description', models.CharField(blank=True, default='', help_text='字段的描述信息，对于非文本域字段可以将此内容作为placeholder', max_length=100, verbose_name='描述')),
                ('field_template', models.TextField(blank=True, default='', help_text='文本域类型字段前端显示时可以将此内容作为字段的placeholder', verbose_name='文本域模板')),
                ('boolean_field_display', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=workflow.models.CustomField.default_boolean_field_display, help_text='当为布尔类型时候，可以支持自定义显示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意数字也需要引号', verbose_name='布尔类型显示名')),
                ('field_choice', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{"1":"中国", "2":"美国"},注意数字也需要引号', verbose_name='radio、checkbox、select的选项')),
                ('creator', models.ForeignKey(help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.User')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Workflow', verbose_name='工作流')),
            ],
            options={
                'verbose_name': '工作流自定义字段',
                'verbose_name_plural': '工作流自定义字段',
            },
        ),
    ]
