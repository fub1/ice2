from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Modal(models.Model):
    """
    """
    import datetime
    index_weight = 1
    code = models.CharField("workflow code", max_length=6, blank=True, null=True)
    name = models.CharField(("workflow name"), max_length=40)
    description = models.TextField(("description"), blank=True,null=True)
    content_type = models.ForeignKey(ContentType, verbose_name=("content type"),limit_choices_to={"app_label__in":['basedata','organ']}, on_delete=models.CASCADE)
    app_name = models.CharField(("app name"), max_length=10, blank=True,null=True)
    model_name = models.CharField(("model name"), max_length=60,blank=True,null=True)
    # added by zhugl 2015-05-10
    begin = models.DateField(("begin date"), blank=True,null=True,default=datetime.date.today)
    end = models.DateField(("end date"), blank=True,null=True,default=datetime.date(9999,12,31))

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = ("workflow model")
        verbose_name_plural = ("workflow model")


class Node(models.Model):
    """
    submitter()
    upper()
    user()
    role()
    position()
    sql()
    etc:upper('zhangsan','lisi')
    """
    HANDLER_TYPE = (
        (1, ("designated user")),
        (2, ("designated position")),
        (3, ("designated role")),
        (4, ("submitter")),
    )
    index_weight = 2
    modal = models.ForeignKey(Modal,verbose_name=("workflow model"), on_delete = models.CASCADE)
    code = models.CharField(("node code"),max_length=4,blank=True,null=True)
    name = models.CharField(("node name"),max_length=80)
    tooltip = models.CharField(('tooltip words'),blank=True,null=True,max_length=120)

    start = models.BooleanField(("start node"),default=False)
    stop = models.BooleanField(("stop node"),default=False)
    can_terminate = models.BooleanField(("can terminate"),default=False)
    can_deny = models.BooleanField(("can deny"),default=True)
    can_edit = models.BooleanField(("can edit"),default=False)

    email_notice = models.BooleanField(("email notice"),default=True)
    short_message_notice = models.BooleanField(("short message notice"),default=False)
    approve_node = models.BooleanField(("approve node"),default=False)
    handler = models.TextField(("handler"),blank=True,null=True,help_text=u'自定义SQL语句，优先高于指定用户、岗位、角色')
    # added by zhugl 2015-05-10
    handler_type = models.IntegerField(("handler type"),choices=HANDLER_TYPE,default=1)
#    positions = models.ManyToManyField(Position,verbose_name=("designated position"),blank=True)
#    roles = models.ManyToManyField(Role,verbose_name=("designated role"),blank=True)
    users = models.ManyToManyField(User,verbose_name=("designated user"),blank=True)
#    departments = models.ManyToManyField(OrgUnit,verbose_name=("designated department"),blank=True)
#    next = models.ManyToManyField('self',blank=True,verbose_name=("next node"),symmetrical=False)
    # added by zhugl 2015-06-30
    next_user_handler = models.CharField(('next user handler'),blank=True,null=True,max_length=40)
    next_node_handler = models.CharField(('next node handler'),blank=True,null=True,max_length=40)
    status_field = models.CharField(('status field'),blank=True,null=True,max_length=40)
    status_value = models.CharField(('status value'),blank=True,null=True,max_length=40)
    action = models.CharField(('execute action'),blank=True,null=True,max_length=40)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.code:
            fmt = 'N%02d'
            self.code = fmt % (self.modal.node_set.count()+1)
        super(Node,self).save(force_insert,force_update,using,update_fields)

    def __unicode__(self):
        return "%s-%s" % (self.code, self.name)

    class Meta:
        verbose_name = ("workflow node")
        verbose_name_plural = ("workflow node")


class Instance(models.Model):
    """
    """
    STATUS = (
        (1, ("NEW")),
        (2, ("IN PROGRESS")),
        (3, ("DENY")),
        (4, ("TERMINATED")),
        (9, ("APPROVED")),
        (99, ("COMPLETED"))
    )
    index_weight = 3
    code = models.CharField(("code"),blank=True,null=True,max_length=10)
    modal = models.ForeignKey(Modal,verbose_name=("workflow model"), on_delete=None)
    object_id = models.PositiveIntegerField("object id")
    starter = models.ForeignKey(User,verbose_name=("start user"),related_name="starter", on_delete=None)
    start_time = models.DateTimeField(("start time"),auto_now_add=True)
    approved_time = models.DateTimeField(("approved time"),blank=True,null=True)
    status = models.IntegerField(("status"),default=1,choices=STATUS)
#    current_nodes = models.ManyToManyField(Node,verbose_name=("current node"),blank=True, on_delete=None)

    def __unicode__(self):
        return '%s' % self.code

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Instance,self).save(force_insert,force_update,using,update_fields)
        if not self.code:
            self.code = 'S%05d'%self.id
            self.save()

    class Meta:
        verbose_name = ("workflow instance")
        verbose_name_plural = ("workflow instance")


class History(models.Model):
    """
    workflow history
    """
    PROCESS_TYPE = (
        (0, ("SUBMIT")),
        (1, ("AGREE")),
        (3, ("DENY")),
        (4, ("TERMINATE")),
    )
    index_weight = 5
    inst = models.ForeignKey(Instance,verbose_name=("workflow instance"), on_delete=None)
    node = models.ForeignKey(Node,verbose_name=("workflow node"),blank=True,null=True, on_delete=None)
    user = models.ForeignKey(User,verbose_name=("submitter"), on_delete=None)
    pro_time = models.DateTimeField(("process time"),auto_now_add=True)
    pro_type = models.IntegerField(("process type"),choices=PROCESS_TYPE,default=0)
    memo = models.CharField(("memo"),max_length=40,blank=True,null=True)

    def get_node_desc(self):
        if self.node:
            return self.node.name
        else:
            return u'启动'

    def get_action_desc(self):
        action_mapping = {0:u'提交',1:u'同意',3:u'拒绝',4:u'终止',}
        # print action_mapping
        if self.pro_type:
            return action_mapping[self.pro_type]
        else:
            return u'提交'

    def get_memo_desc(self):
        if self.memo:
            return self.memo
        else:
            return ''

    class Meta:
        verbose_name = ("workflow history")
        verbose_name_plural = ("workflow history")
        ordering = ['inst','pro_time']


class TodoList(models.Model):
    """
    """
    index_weight = 4
    code = models.CharField(("code"),max_length=10,blank=True,null=True)
    inst = models.ForeignKey(Instance,verbose_name=("workflow instance"), on_delete=None)
    node = models.ForeignKey(Node,verbose_name=("current node"),blank=True,null=True, on_delete=None)
    app_name = models.CharField(("app name"),max_length=60,blank=True,null=True)
    model_name = models.CharField(("model name"),max_length=60,blank=True,null=True)
    user = models.ForeignKey(User,verbose_name=("handler"), on_delete=None)
    arrived_time = models.DateTimeField(("arrived time"),auto_now_add=True)
    is_read = models.BooleanField(("is read"),default=False)
    read_time = models.DateTimeField(("read time"),blank=True,null=True)
    status = models.BooleanField(("is done"),default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(TodoList,self).save(force_update,force_update,using,update_fields)
        if not self.code:
            self.code = 'TD%05d' % self.id
            self.save()

    def node_dsc(self):
        if self.node:
            return u'%s'%self.node.name
        else:
            return u'启动'

    def code_link(self):
        return format_html("<a href='/admin/{}/{}/{}'>{}</a>",
                           self.app_name,self.model_name,self.inst.object_id,self.code)
    code_link.allow_tags = True
    code_link.short_description = ("code")

    def href(self):
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        ct = ContentType.objects.get(app_label=self.app_name,model=self.model_name)
        obj = ct.get_object_for_this_type(id=self.inst.object_id)
        title = u"%s" % (obj)
        return format_html("<a href='/admin/{}/{}/{}'>{}</a>",
                           self.app_name,self.model_name,self.inst.object_id,title)
    def modal_dsc(self):
        return u'%s'%(self.inst.modal.name)
    modal_dsc.short_description = u'业务流程'

    def start_time(self):
        return self.inst.start_time.strftime('%Y-%m-%d %H:%M')

    href.allow_tags = True
    href.short_description = ("description")
    node_dsc.short_description = ('current node')

    def submitter(self):
        if self.inst.starter.last_name or self.inst.starter.first_name:
            return u"%s%s"%(self.inst.starter.last_name,self.inst.starter.first_name)
        return u"%s"%(self.inst.starter.username)
    submitter.short_description = ("submitter")

    class Meta:
        verbose_name = ("workflow todo")
        verbose_name_plural = ("workflow todo")
        ordering = ['user','-arrived_time']


def get_modal(app_label,model_name):
    """
    :param app_label:
    :param model_name:
    :return:
    """
    try:
        return Modal.objects.get(app_name=app_label,model_name=model_name)
    except Exception:
        return None


def get_instance(obj):
    """
    :param obj:
    :return:
    """
    if obj and obj._meta:
        modal = get_modal(obj._meta.app_label,obj._meta.model_name)
        if modal:
            try:
                return Instance.objects.get(modal=modal,object_id=obj.id)
            except Exception:
                return None
    else:
        return None