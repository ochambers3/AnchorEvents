import { Component, OnInit } from '@angular/core';
import { HomeComponent } from './features/home/home.component';
import { HousingLocationComponent } from './features/housing-location/housing-location.component';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './layout/header/header.component';
import { FooterComponent } from './layout/footer/footer.component';

@Component({
  selector: 'app-root',
  imports: [HomeComponent, RouterModule, HeaderComponent, FooterComponent],
  // <img class="brand-logo" src="/assets/logo.svg" alt="logo" aria-hidden="true" />
  template: `
    <main>
      <app-header></app-header>
      <section class="content">
        <router-outlet></router-outlet>
      </section>
      @if (showFooter) {
        <app-footer></app-footer>
      }
    </main>
  `,
  styleUrls: ['./app.component.css', './layout/header/header.component.css'],
  standalone: true,
})
export class AppComponent implements OnInit {
  showFooter = true;
  private lastScrollTop = 0;

  ngOnInit(): void {
      window.addEventListener('scroll', this.handleScroll, true);
  }

  handleScroll = (): void => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > this.lastScrollTop) {
      // Scrolling down
      this.showFooter = false;
    } else {
      // Scrolling up
      this.showFooter = true;
    }

    this.lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  };
  
  title = 'Anchor Events';
}
