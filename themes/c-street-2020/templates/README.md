## Tendenci Theme Update
In order to update the site to Bootstrap 4 compatibility, a significant number of base theme pages may need to be overridden to apply new styles. Django makes it easy to do this. In the case of files that had "-new" added to their name, the overriding template will be named according to the original name (which makes it easy for me to switch back and forth if I need to; eg. `top_menu/admin_top.html` vs `top_menu/admin_top-new.html`).


### Significant Changes
* Navbar classes seem to have changed a lot for Bootstrap 4.
* `.nav` is redundant with `.navbar-nav` when used inside `.navbar`.
* There's a `ul` in `header.html` outside the `<% nav >` tags, when the `navs` app spawns a `ul`. There should only be one, and it should be inside the app's templates (because a different app might use different tags).
* Why is there a `.t-main-navbar-nav` that doesn't get used for anything? It's next to `#t-main-navbar-nav-[num]` which is also unused. These names are confusing and non-expressive and should be limited. Anywhere I see something like that, I'm removing the `class` and changing the `id` to something straightforward like `#t-navbar-[num]`.
