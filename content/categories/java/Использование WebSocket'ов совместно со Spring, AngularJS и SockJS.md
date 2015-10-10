Title: Использование WebSocket'ов совместно со Spring, AgularJS и SocksJS
Tags: translate, java, spring, angular, socket
Date: 10-10-2015 14:11
Status: published
Slug: Using-WebSockets-with-Spring-AngularJS-and-SockJS

Некоторое время назад я написал стсатью о веб приложении использующем spring angularJS и WebSocket'ы. Тем не менее, это руководство использует только часть того что могут вебсокеты, поэтому в этом руководстве я буду объяснять как вы можете написать небольшой чат используя фреймворки Spring, AngularJS, Stromp.js и SockJS.

Внутри приложения будет описан использованный JavaConfig, даже web.xml (который я до сих пор храню с прежнего руководства) будет заменён на WebAppInitializer

Приложение которое будем писать, будет выглядить вот так:

![Внешний вид приложения]({filename}/images/app-chat-example.png "внешний вид приложения")

[TOC]

## Почему WebSocket'ы?

Однажды, кто-то решил написать приложение почтовой рассылки. Для начала он сделал клиент который проверял, наличие новых писем каждую минуту. Тем не менее, часто не было новых писем, а клиент всегда отправлял запрос, делая большую нагрузку на сервер. Эта техника была довольно популярна, и была названа *polling* (пер. с англ. "опросник"). Затем, через некоторое время, они использовали новую технику, когда клиент бы проверял если есть новые письма, и сервер бы отвечал как только новая почта стала доступна. Эта техника была немного лучше чем поллинг, но вы всё равно отправляли запрос, в результате чего использовался лишний трафик, мы назвали эту технику *long-polling*.

Когда вы начинаете думать, можете сделать только один вывод, это сервер должен отправить сообщение клиенту, когда новая почта станет доступна. Клиент не должен инициировать запрос, но сервер должен это делать. Это было невозможно долгое время, но как только были придуманы WebSocket'ы, это наконец стало возможным.

WebSocket'ы это протокол и JavaScript API, протокол очень низкоуровневый, двухуровневый (*full-duplex*), это означает, что сообщения могут быть отправлены в обе стороны соединения одновременно. Это даёт возможность для того что бы сервер отправлял данные клиенту, но не наоборот. *Polling* и *long-polling* стали больше не нужны, и жили они долго и счастливо...

Потому как WebSocket'ы предоставляют связь в друх направлениях, они часто используються для приложений реального времени. Если для примера, кто-то откроет ваше приложение и изменит в нём какие-либо данные, вы можете непосредственно обновить эти данные для всех пользователей, которые используют WebSocket'ы.

## Установка проекта

Вам будут необходимы несколько библиотек, основная это Spring Web MVC фреймворк для настройки нашего веб приложения и Spring messaging + WebSockets для WebSocket'ной части  приложения. Нам также необходима JSON сериализатор, например Jackson, потому что Stomp нуждается в JSON сериализации/десериализации, поэтому я также собираюсь добавить его в наше приложение.

**pom.xml**

    :::xml
    ...
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>4.1.1.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-websocket</artifactId>
        <version>4.1.1.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-messaging</artifactId>
        <version>4.1.1.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>javax.websocket</groupId>
        <artifactId>javax.websocket-api</artifactId>
        <version>1.0</version>
        <scope>provided</scope>
    </dependency>
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>3.1.0</version>
        <scope>provided</scope>
    </dependency>
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>jstl</artifactId>
        <version>1.2</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-core</artifactId>
        <version>2.3.3</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.3.3</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.jaxrs</groupId>
        <artifactId>jackson-jaxrs-json-provider</artifactId>
        <version>2.3.3</version>
    </dependency>
    ...

На front-end я добавлю нужные билиотеки, которые настрою при помощи Bower. Если вы им не пользуетесь, Вы всегда можете скачать эти библиотеки вручную.

    :::json
    {
      "name": "spring-ng-chat",
      "version": "0.0.1-SNAPSHOT",
      "dependencies": {
        "sockjs": "0.3.4",
        "stomp-websocket": "2.3.4",
        "angular": "1.3.8",
        "lodash": "2.4.1"
      }
    }

Библиотеки которые я собираюсь использовать SockJS + Stomp.js для связи меджу WebSocket'ами, AngularJS буду использовать для настройки клиентской части приложения и Lo-Dash библиотека утилит (форк Underscore.js).

> Что такое *STOMP*? Как я говорил раньше, WebSocket протокол довольно низкоуровневый, однако есть неколько высоко-(выше-) уровневые протоколы, которые могут быть использованы поверх WebSocket'ов, например *MQTT* и *STOMP*. *STOMP* например добавляет дополнительные возможности к WebSocket'ам, такие как публикация и подписка на темы.

## Java конфигурация

Вместо конфигурации нашего протокола используя XML, я покажу вам как вы можете написать аналогичнее приложения без использования XML файлов. Первый класс который нам понадобиться который заменяет наш web.xml, для загрузки нашего веб приложения. В данном случае мы может определить application context, web application context и некоторые другие сервлет подобные конфигурации.

    :::java
    public class WebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

      @Override
      protected void customizeRegistration(ServletRegistration.Dynamic registration) {
        registration.setInitParameter("dispatchOptionsRequest", "true");
        registration.setAsyncSupported(true);
      }

      @Override
      protected Class< ?>[] getRootConfigClasses() {
        return new Class< ?>[] { AppConfig.class, WebSocketConfig.class };
      }

      @Override
      protected Class< ?>[] getServletConfigClasses() {
        return new Class< ?>[] { WebConfig.class };
      }

      @Override
      protected String[] getServletMappings() {
        return new String[] { "/" };
      }

      @Override
      protected Filter[] getServletFilters() {
        CharacterEncodingFilter characterEncodingFilter = new CharacterEncodingFilter();
        characterEncodingFilter.setEncoding(StandardCharsets.UTF_8.name());
        return new Filter[] { characterEncodingFilter };
      }
    }

Большая часть данного класса вполне понятно. Прежде всего мы должны `getRootConfigClasses()` и `getServletConfigClasses()` которые мы использовали для определения наших бинов. `getServletMappings()` и `getServletFilters()` связаны с конфигурацией сервлета. В данном случае я определяю приложение в context root и я добавляю фильтр для прогонки всего контента в кодировку UTF-8.

После последний метод здесь это `customizeRegistrion()`. Это может быть очень важно если вы запускаете приложение на Tomcat контейнере. Это объясняет что ассинхронная связь возможно, поэтому эти соединения не должны закрываться непосредственно.

Как вы могли заметить , вы будете получать три ошибки компиляции о классах которые на найдены. Я определю их сейчас, и начнём с `AppConfig`:

    :::java
    @Configuration
    @ComponentScan(basePackages = "be.g00glen00b", excludeFilters = {
        @ComponentScan.Filter(value = Controller.class, type = FilterType.ANNOTATION),
        @ComponentScan.Filter(value = Configuration.class, type = FilterType.ANNOTATION)
    })
    public class AppConfig {

    }

Довольно пустой и бесполезный, кторый говорит какой пакет сканировать, но исключает все конфигурационный и контроллер классы (конфигурационные каллсы которые загружаются нашим `WebAppInitializer` когда `Controller` классы связанные с нашим `WebConfig`). Так нам нужен будет лишь контроллер, этот класс не будет делать ничего особенного, но если вы используете специальные сервисы, тогда они станут Spring бинами, если их правильно аннотировать.

Следующий класс это `WebConfig`:

    :::java
    @Configuration
    @EnableWebMvc
    @ComponentScan(basePackages = "be.g00glen00b.controller")
    public class WebConfig extends WebMvcConfigurerAdapter {

      @Bean
      public InternalResourceViewResolver getInternalResourceViewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return resolver;
      }

      @Override
      public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
      }

      @Bean
      public WebContentInterceptor webContentInterceptor() {
        WebContentInterceptor interceptor = new WebContentInterceptor();
        interceptor.setCacheSeconds(0);
        interceptor.setUseExpiresHeader(true);
        interceptor.setUseCacheControlHeader(true);
        interceptor.setUseCacheControlNoStore(true);

        return interceptor;
      }

      @Override
      public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/libs/**").addResourceLocations("/libs/");
        registry.addResourceHandler("/app/**").addResourceLocations("/app/");
        registry.addResourceHandler("/assets/**").addResourceLocations("/assets/");
      }

      @Override
      public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(webContentInterceptor());
      }
    }

Эта настоичный класс загружающий наш веб контекст. Он говорит нам какой статичный ресурс может быть обслужен (с `addResourceHandlers`. Он добавляет ~~нет кеш-перехватчик~~ (`webContentInterceptor()` и `addInterceptors()`) и также объяснит нам расположение нашиъ динамических ресурсов (JSP файлов) которые используются в `getInternalResourceViewResolver()` бином.

И наконец WebSocket конфиг:

    :::java
    @Configuration
    @EnableWebSocketMessageBroker
    @ComponentScan(basePackages = "be.g00glen00b.controller")
    public class WebSocketConfig extends AbstractWebSocketMessageBrokerConfigurer {

      @Override
      public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic");
        config.setApplicationDestinationPrefixes("/app");
      }

      @Override
      public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/chat").withSockJS();
      }
    }

Также как и `WebSocket` он сканирует компоненты в контроллер пакетах, потому  что мы определим наш WebSocket траффик в наши контроллеры. Тогда мы должны сконфигурировать сообщения брокер сообщений (где связь входит и выходит) используя `configMessegeBroker` и мы также должны сконфигурировать наши конечные точки `registerStompEndPoints`.

> WebSocket'ы не работают во всех броузерах. Много WebSocket библиотек (например SockJS и Socket.io) предоставляют запасной вариант использования *long-polling* и *polling*. Spring также предоставляет эти запасные варианты совместимые с SockJS. Именно поэтому выбрать SockJS как клиент - это хорошая идея.

## Объект обмена данными

Наше основное соединение будет проходить через WebSocket. Что бы общаться мы вышлем определенный полезную нагрузку и ответ, на специфический *Stomp.js* заголовок. Нам необходимо два класса для этого, `Message` и `OutputMessage`.

Предле всего, `Message` будет содержать сообщение чата и генерирует ID, например: 

    :::java
    public class Message {

      private String message;
      private int id;
      
      public Message() {
        
      }
      
      public Message(int id, String message) {
        this.id = id;
        this.message = message;
      }

      public String getMessage() {
        return message;
      }

      public void setMessage(String message) {
        this.message = message;
      }

      public int getId() {
        return id;
      }

      public void setId(int id) {
        this.id = id;
      }
    }

`OutputMessage` наследуется от  `Message`, но также добавляется метку (текущее время):

    :::java
    public class OutputMessage extends Message {

        private Date time;
        
        public OutputMessage(Message original, Date time) {
            super(original.getId(), original.getMessage());
            this.time = time;
        }
        
        public Date getTime() {
            return time;
        }
        
        public void setTime(Date time) {
            this.time = time;
        }
    }

## Spring Controller

Заключительной java частью приложения является контроллер который описывает два случая, первый для HTML/JSP страницы содержащей наше приложение, и остальной WebSocket трафик:

    :::java
    @Controller
    @RequestMapping("/")
    public class ChatController {

      @RequestMapping(method = RequestMethod.GET)
      public String viewApplication() {
        return "index";
      }
        
      @MessageMapping("/chat")
      @SendTo("/topic/message")
      public OutputMessage sendMessage(Message message) {
        return new OutputMessage(message, new Date());
      }
    }

Что здесь происходит достаточно просто, когда мы идём в context root, мы увидем этот `viewApplication()` отображается сюда же, поэтому этот **index.jsp** страница и использует эту **view**. Другой метод, `sendMessage()` предоставляет нам вещание сообщения в `/topic/message` когда сообщение введено в брокер сообщений `/app/chat` (не забудьте определить префикс `/app` в `WebSocketConfig`).

## View

Теперь наш внутренний java код написан, теперь оппишем JSP страницу. Эта страница будет содержавть 2 основных компонента: форму для добавления нового сообщения и список сообщений.

    :::hmtl
    <!DOCTYPE HTML>
    <html lang="en">
      <head>
        <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700" rel="stylesheet" type="text/css" />
        <link href="assets/style.css" rel="stylesheet" type="text/css" />
      </head>
      <body ng-app="chatApp">
        <div ng-controller="ChatCtrl" class="container">
          <form ng-submit="addMessage()" name="messageForm">
            <input type="text" placeholder="Compose a new message..." ng-model="message" />
            <div class="info">
              <span class="count" ng-bind="max - message.length" ng-class="{danger: message.length > max}">140</span>
              <button ng-disabled="message.length > max || message.length === 0">Send</button>
            </div>
          </form>
          <hr />
          <p ng-repeat="message in messages | orderBy:'time':true" class="message">
            <time>{{message.time | date:'HH:mm'}}</time>
            <span ng-class="{self: message.self}">{{message.message}}</span>
          </p>
        </div>
        
        <script src="libs/sockjs/sockjs.min.js" type="text/javascript"></script>
        <script src="libs/stomp-websocket/lib/stomp.min.js" type="text/javascript"></script>
        <script src="libs/angular/angular.min.js"></script>
        <script src="libs/lodash/dist/lodash.min.js"></script>
        <script src="app/app.js" type="text/javascript"></script>
        <script src="app/controllers.js" type="text/javascript"></script>
        <script src="app/services.js" type="text/javascript"></script>
      </body>
    </html>

Прежде всего мы добавим Open Sans шрифт и нашу таблицу стилей (которую опишем позже в этом руководстве). Затем мы описываем тело и загрузку AngularJS прложения которое мы назвали `appChat`. В этом приложении мы добавим один AngularJS контроллер, `ChatCtrl`. Не путайте этот с нашим Spring котроллером!

В первую очередь что мы должны сделать, это создать форму содержащую текстовое поле. Мы соединим это поле с моделью названной `message`. Когда форма будет отправлена, `addMessage()` функция в нашем контроллере будет вызвана, которую мы будем использовать для отправки сообщения при помощи WebSocket'ов.

Для того что бы форма была попышнее мы также добавим счетчик наподобие того который используеться в Twitter. В каждый момент времени сколько Вы ввели символов (**max**), и загораеться красным когда вы больше не можете отправить форму благодаря директиве `ng-disabled`. Сообщения отсортированы по их дате, последнее из низ показывается сверху списка.

В конце страницы мы подгружаем все библиотеки которые нам нужны, и JavaScript файлы нашео приложения.

## Загрузка AngularJS приложения

Наш первый JavaScript файл - app.js. Этот файл определяет все модули пакетов,в этом случае:

    :::javascript
    angular.module("chatApp", [
      "chatApp.controllers",
      "chatApp.services"
    ]);

    angular.module("chatApp.controllers", []);
    angular.module("chatApp.services", []);

## AngularJS контроллер

AngularJS контроллер достаточно простой, как он будет пересывать всё в отдельный сервис, мы опишем далее в этом руководстве. Контроллер содержит три модели свяанные с полями, это `message` которое будет содержать только что введенное сообщение в textbox, `messages` массив который содержит все отправленные сообщения и также `max` - максмум допустимых символов в сообщении, используемое как Twitter счётчик символов для твита.

    :::javascript
    angular.module("chatApp.controllers").controller("ChatCtrl", function($scope, ChatService) {
      $scope.messages = [];
      $scope.message = "";
      $scope.max = 140;

      $scope.addMessage = function() {
        ChatService.send($scope.message);
        $scope.message = "";
      };

      ChatService.receive().then(null, null, function(message) {
        $scope.messages.push(message);
      });
    });

Мы уже объяснили кто когда форма отправляется, `addMessage` ф-я вызывается, которая будет передаст сообщение дальше сервису, и которая очистит поле сбросив модель сообщения как пустую строку. Мы также вызываем сервис для получения сообщений. Эта часть сервиса будет возвращать отложенно, кадлый ра когда сообщения получены, обновит прогресс части директивы. Контроллер будет рагировать на это сообщение добавляя его в массив `messages`.

## AngularJS служба

Последняя часть нашего AngularJS клиентского приложения - это сервис. Сервис немного сложенее поскольку он будет содержать весь код обработки WebSocket трафика. Код этого сервиса: 

    :::javascript
    angular.module("chatApp.services").service("ChatService", function($q, $timeout) {
        
        var service = {}, listener = $q.defer(), socket = {
          client: null,
          stomp: null
        }, messageIds = [];
        
        service.RECONNECT_TIMEOUT = 30000;
        service.SOCKET_URL = "/spring-ng-chat/chat";
        service.CHAT_TOPIC = "/topic/message";
        service.CHAT_BROKER = "/app/chat";
        
        service.receive = function() {
          return listener.promise;
        };
        
        service.send = function(message) {
          var id = Math.floor(Math.random() * 1000000);
          socket.stomp.send(service.CHAT_BROKER, {
            priority: 9
          }, JSON.stringify({
            message: message,
            id: id
          }));
          messageIds.push(id);
        };
        
        var reconnect = function() {
          $timeout(function() {
            initialize();
          }, this.RECONNECT_TIMEOUT);
        };
        
        var getMessage = function(data) {
          var message = JSON.parse(data), out = {};
          out.message = message.message;
          out.time = new Date(message.time);
          if (_.contains(messageIds, message.id)) {
            out.self = true;
            messageIds = _.remove(messageIds, message.id);
          }
          return out;
        };
        
        var startListener = function() {
          socket.stomp.subscribe(service.CHAT_TOPIC, function(data) {
            listener.notify(getMessage(data.body));
          });
        };
        
        var initialize = function() {
          socket.client = new SockJS(service.SOCKET_URL);
          socket.stomp = Stomp.over(socket.client);
          socket.stomp.connect({}, startListener);
          socket.stomp.onclose = reconnect;
        };
        
        initialize();
        return service;
      });

Итак начнём снизу. В самом низу кода вы можете увидеть, что мы выполняем `initialize()` ф-ю для настройки сервиса. Это произойдет один раз, поскольку AngularJS сервисы синглтоны, это означает что кадждый раз один и тот же экземпляр будет возвращен.

Функция `initialize()` настроит SockJS WebSocket клиент и использует его для Stomp.js WebSocket клиента. Stomp.js является дополнением к WebSocket протоколу которое позволяет подписываться и публиковать темы и также позволяет JSON полезную нагрузку.

Когда клиент присоединился к WebSocket серверу, затем вызываеться `startListener()` ф-я, которая будет слушать `/topic/message` заголовок по которому будут получены все сообщения. Он затем отправит отложенные данные, которые будут использоваться контроллерами.

`startListener()` ф-я вызывает `getMessage()` функцию, которая переводит WebSocket данные (полезная нагрузка) в модель необходимую контроллеру. В этом случае парсинг JSON строки в объект, и он будет устанавливать время как `Date` объект.

Если поядковый номер (ID) сообщения был найден в `messageIds` массиву, то это означает что сообщение создано в этом клиенте, поэтому свойство **self** будет обозначено как **true**.

Затем она удалит этот ID сообщения из списка, потому что они доступны снова в пуле ID сообщений.

Когда соединение с WebSocket'ом сервера потеряно, это вызовет ф-ю `recconect()` будет пытаться возобновить совединение после 30 секунд.

В конце мы имеем две публичные функции нашего сервиса, `receive()` и `send()`. Начнём с `receive()` функции, так как она простейщая среди них. Единственное что эта функция делает, это возвращает отложено к отправке сообщения.

`send()` функция с другой стороны  отправляет сообщения как JSON объект (поле строка) и генерирует новый ID. Этот ID добавляеться к `messageIds` массиву, так что он может быть использован функцией `getMessage()` для проверки было ли добавлено сообщение данным клиентом, или другим.

## Стилизация

Это весь Java и JavaScript код который необходим, теперь закончим наше приложение добавив в него крутых стилей. Я использую следующий CSS код:

    :::css
    body, * {
      font-family: 'Open Sans', sans-serif;
      box-sizing: border-box;
    }

    .container {
      max-width: 1000px;
      margin: 0 auto;
      width: 80%;
    }

    input[type=text] {
      width: 100%;
      border: solid 1px #D4D4D1;
      transition: .7s;
      font-size: 1.1em;
      padding: 0.3em;
      margin: 0.2em 0;
    }

    input[type=text]:focus {
      -webkit-box-shadow: 0 0 5px 0 rgba(69, 155, 231, .75);
      -moz-box-shadow: 0 0 5px 0 rgba(69, 155, 231, .75);
      box-shadow: 0 0 5px 0 rgba(69, 155, 231, .75);
      border-color: #459be7;
      outline: none;
    }

    .info {
      float: right;
    }

    form:after {
      display: block;
      content: '';
      clear: both;
    }

    button {
      background: #459be7;
      color: #FFF;
      font-weight: 600;
      padding: .3em 1.9em;
      border: none;
      font-size: 1.2em;
      margin: 0;
      text-shadow: 0 0 5px rgba(0, 0, 0, .3);
      cursor: pointer;
      transition: .7s;
    }

    button:focus {
      outline: none;
    }

    button:hover {
      background: #1c82dd;
    }

    button:disabled {
      background-color: #90BFE8;
      cursor: not-allowed;
    }

    .count {
      font-weight: 300;
      font-size: 1.35em;
      color: #CCC;
      transition: .7s;
    }

    .count.danger {
      color: #a94442;
      font-weight: 600;
    }

    .message time {
      width: 80px;
      color: #999;
      display: block;
      float: left;
    }

    .message {
      margin: 0;
    }

    .message .self {
      font-weight: 600;
    }

    .message span {
      width: calc(100% - 80px);
      display: block;
      float: left;
      padding-left: 20px;
      border-left: solid 1px #F1F1F1;
      padding-bottom: .5em;
    }

    hr {
      display: block;
      height: 1px;
      border: 0;
      border-top: solid 1px #F1F1F1;
      margin: 1em 0;
      padding: 0;
    }

## Демонстрация

Перед тем как запустить наше приложение на веб сервере, сперва проверим некоторые вещи. Во-первых, убедимся, что вы настроили ваш context root на `/spring-ng-chat/`. Если вы этого не сделаеле, Ваш AngularJS сервис будет иметь проблемы с соединением к WebSocket серверу, так как он связан с `/spring-ng-chat/chat`. Если вы не хотите это, вы можете всегда изменить свойство `SOCKET_URL` в AngularJS сервисе.

Во-вторых, если вы запустите это приложение из встроенного в Eclipse Tomcat'а, вам прйдеться добавить ваши Maven зависимости в ваш deployment сборку. Вы можете сделать это в настройках проекта, выбрав *Deployment assembly* и добавив эти библиотеки.

![Окно Deployment assembly]({filename}/images/deployment-assembly.png "Окно Deployment assembly")

В конце концов убедитесь что контейнер который вы используете, поддерживает WebSocket Java API. Если это не так, то вам скорее всегда необходимо обновить ваш веб контейнер.

Если всё это готово, то можете начать запуск вашего приложения, которое выглядит вот так:

![Стартовый вид приложения]({filename}/images/initial-app.png "стартовый вид приложения")

Если вы начнёте набирать ваше сообщение, вы увидете что кнопка теперь активировалась, и счётчик запустился.

![Набранное сообщение, кнопка активировалась, и заработал счётчик")]({filename}/images/app-message.png "набранное сообщение, кнопка активировалась, и заработал счётчик")

Если вы будете набирать дальше, то увидите, что кнопка деактивировалась снова, и счётчик теперь показывается отрицательное значение в красном цвете:

![Слишком длинное сообщение, кнопка неактивна, счетчик отрицательный]({filename}/images/message-limit.png "слишком длинное сообщение, кнопка неактивна, счетчик отрицательный")

Как только Вы введёте сообщение и отправите его, Вы увидите что оно появится в списке сообщений, жирным шрифтом (потому как оно Вы его отправили). Вы также увидите, что поле ввода сообщения было очищено:

![Отправленное сообщение выделено жирным, строка ввода очищена]({filename}/images/message-sent.png "отправленное сообщение выделено жирным, строка ввода очищена")

Если вы откроете приложение в новом окне, вы сможете увидеть что оно пустое. Так как WebSocket'ы работают в режиме реального времени, поэтому только сообщения которые были доставлены в положенное время будут видны в списке сообщений, здесь нет истории сообщений.

Если Вы отправили сообщение в другом окне, вы должны будете увидеть это сообщение на обоих окнах. Но только на одном будет выделено жирным текстом, а на другом обычным.

![Вид чата в разных окнах приложения]({filename}/images/multiple-messages.png "вид чата в разных окнах приложения")

Как Вы можете видеть, WebSocket'ы работают должным образом и вы увидете сообщения появляются в режиме реального времени, потому что клиент отправляет сообщение на сервер, который отправляет это сообщение всем клиентам.

Такая сервер-клиентная модель возможно только благодаря WebSocket'ам.

[*source*](http://g00glen00b.be/spring-angular-sockjs/)