openerp.oepetstore = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.HomePage = instance.Widget.extend({
        template: "HomePage",
        start: function () {
            return $.when(
                new local.PetToysList(this).appendTo(this.$('.oe_petstore_homepage_left')),
                new local.MessageOfTheDay(this).appendTo(this.$('.oe_petstore_homepage_right'))
            );
        }
    });

    instance.web.client_actions.add('petstore.homepage', 'instance.oepetstore.HomePage');

    local.MessageOfTheDay = instance.Widget.extend({
        template: "MessageOfTheDay",
        start: function () {
            var self = this;
            return new instance.web.Model("oepetstore.message_of_the_day")
                .query(["message"])
                .order_by('-create_date', '-id')
                .first()
                .then(function (result) {
                    self.$(".oe_mywidget_message_of_the_day").text(result.message);
                });
        },
    });

    local.PetToysList = instance.Widget.extend({
        template: 'PetToysList',
        events: {
            'click .oe_petstore_pettoy': 'selected_item',
        },
        start: function () {
            var self = this;
            return new instance.web.Model('product.product')
                .query(['name', 'image'])
                .filter([['categ_id.name', '=', "Pet Toys"]])
                .limit(5)
                .all()
                .then(function (results) {
                    _(results).each(function (item) {
                        self.$el.append(QWeb.render('PetToy', {item: item}));
                    });
                });
        },
        selected_item: function (event) {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'product.product',
                res_id: $(event.currentTarget).data('id'),
                views: [[false, 'form']],
            });
        },
    });

    //local.HomePage = instance.Widget.extend({
    //    /**
    //     * Communcation with the Odoo Server, Contacting Models
    //     */
    //    start: function () {
    //        var self = this;
    //        var model = new instance.web.Model("oepetstore.message_of_the_day");
    //        model.call("my_method", {context: new instance.web.CompoundContext({'new_key': 'key_value'})}).then(function (result) {
    //            self.$el.append("<div>Hello " + result["hello"] + "</div>");
    //            // will show "Hello world" to the user
    //        });
    //        console.log(new TestClass().testMethod());
    //        // will print "hello world2"
    //    },
    //});

    var TestClass = instance.web.Class.extend({
        testMethod: function () {
            return "hello";
        },
    });

    TestClass.include({
        testMethod: function () {
            return this._super() + " world2";
        },
    });

    //local.HomePage = instance.Widget.extend({
    //    template: "HomePage",
    //    start: function () {
    //        this.colorInput = new local.ColorInputWidget(this);
    //        this.colorInput.on("change:color", this, this.color_changed);
    //        return this.colorInput.appendTo(this.$el);
    //    },
    //    color_changed: function () {
    //        this.$(".oe_color_div").css("background-color", this.colorInput.get("color"));
    //    },
    //});

    local.ColorInputWidget = instance.Widget.extend({
        template: "ColorInputWidget",
        events: {
            'change input': 'input_changed'
        },
        start: function () {
            this.input_changed();
            return this._super();
        },
        input_changed: function () {
            var color = [
                "#q",
                this.$(".oe_color_red").val(),
                this.$(".oe_color_green").val(),
                this.$(".oe_color_blue").val()
            ].join('');
            this.set("color", color);
            console.log(color);
        },
    });

    //local.HomePage = instance.Widget.extend({
    //    start: function () {
    //        var products = new local.ProductsWidget(
    //            this, ["cpu", "mouse", "keyboard", "graphic card", "screen"], "#00FF00");
    //        products.appendTo(this.$el);
    //    },
    //});

    local.ProductsWidget = instance.Widget.extend({
        template: "ProductsWidget",
        init: function (parent, products, color) {
            this._super(parent);
            this.products = products;
            this.color = color;
        },
    });

    //local.HomePage = instance.Widget.extend({
    //    className: 'oe_petstore_homepage',
    //    template: "HomePageTemplate",
    //    init: function (parent) {
    //        this._super(parent);
    //        this.name = "Shahrooz";
    //    },
    //    start: function() {
    //        //this.$el.append(QWeb.render("HomePageTemplate"));
    //        //this.$el.append(QWeb.render("HomePageTemplate", {name: "Shahrooz"}));
    //        console.log("pet store home page loaded");
    //        this.$el.append("<div>Hello dear Odoo user!</div>");
    //        var greeting = new local.GreetingsWidget(this);
    //        greeting.appendTo(this.$el);
    //        console.log(this.getChildren()[0].$el);
    //        // will print "div.oe_petstore_greetings" in the console
    //        //return greeting.appendTo(this.$el);
    //    },
    //});

    local.GreetingsWidget = instance.Widget.extend({
        init: function (parent, name) {
            this._super(parent);
            this.name = name;
        },
        className: 'oe_petstore_greetings',
        start: function () {
            console.log(this.getParent().$el);
            // will print "div.oe_petstore_homepage" in the console
            this.$el.append("<div>We are so happy to see you again in this menu!</div>");
        },
    });
};
