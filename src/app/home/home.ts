import { Component } from '@angular/core';
import {Header} from '../shared/components/header/header';
import {Preloader} from '../shared/components/preloader/preloader';
import {Introduction} from './components/introduction/introduction';
import {About} from './components/about/about';
import {Facts} from './components/facts/facts';
import {Services} from './components/services/services';
import {Movie} from './components/movie/movie';
import {Portfolio} from './components/portfolio/portfolio';
import {Projet} from './components/projet/projet';
import {Resume} from './components/resume/resume';
import {Testimonial} from './components/testimonial/testimonial';
import {Contact} from './components/contact/contact';
import {Footer} from '../shared/components/footer/footer';

@Component({
  selector: 'app-home',
  imports: [
    Header,
    Preloader,
    Introduction,
    About,
    Facts,
    Services,
    Movie,
    Portfolio,
    Projet,
    Resume,
    Testimonial,
    Contact,
    Footer
  ],
  templateUrl: './home.html'
})
export class Home {

}
